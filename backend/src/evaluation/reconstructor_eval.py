"""Reconstructor evaluation: multi-turn context completion accuracy.

Loads test samples from reconstructor_samples.json and evaluates the LLM-based
reconstructor against ground-truth reconstructed queries.

Evaluation strategy (exact-match fast-path + LLM-as-Judge):
  - norm(expected) == norm(predicted)  → fast pass: mark "correct" (1 LLM call)
  - otherwise                           → LLM-as-Judge for semantic decision (2 LLM calls)

Metrics:
  - 多轮上下文补全率 = ("correct" verdicts) / total
  - Per-result breakdown: correct / incorrect / over_complete / under_complete
  - Per-anaphora-type breakdown: pronoun / ellipsis / vague_reference / ...
  - Intent preservation rate, entity match rate (from judge)
  - Keyword F1 (kept as fast-path signal, not final verdict)
"""

import os
import json
import time
import logging
import re
import concurrent.futures
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from tqdm import tqdm

from src.constants import RECONSTRUCTOR_SAMPLE_PATH, LOG_DIR, EVAL_DIR
from src.prompts import RECONSTRUCTOR_JUDGE_PROMPT
from src.utils import build_reconstructor_prompt, format_history

QWEN_API_KEY = os.environ.get("QWEN_API_KEY")
QWEN_BASE = os.environ.get("QWEN_BASE")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

SAMPLE_PATH = Path(RECONSTRUCTOR_SAMPLE_PATH)
LOG_DIR = Path(LOG_DIR)
EVAL_DIR = Path(EVAL_DIR)
LOG_FILE_PATH = LOG_DIR / "reconstructor_eval.log"
REPORT_DIR = EVAL_DIR / "reports"
REPORT_FILE_PATH = REPORT_DIR / "reconstructor_eval.json"
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Fast-path: only skip judge on exact string match
_JUDGE_TIMEOUT = 30     # seconds for judge LLM call


#  helpers 

def _normalize(s: str) -> str:
    """Strip punctuation and whitespace for comparison."""
    s = re.sub(r"[^\w\u4e00-\u9fff]", " ", s) # anything that is NOT English/number/underscore/Chinese
    return " ".join(s.split()).lower()


def _keyword_f1(expected: str, predicted: str) -> float:
    """Token-level F1 between two strings (Chinese-aware tokenisation)."""
    exp_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", _normalize(expected)))
    pred_tokens = set(re.findall(r"[\w\u4e00-\u9fff]+", _normalize(predicted)))
    if not exp_tokens:
        return 0.0
    overlap = len(exp_tokens & pred_tokens)
    precision = overlap / len(pred_tokens) if pred_tokens else 0.0
    recall = overlap / len(exp_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _anaphora_type(description: str) -> str:
    """Infer anaphora type from the description field."""
    d = description.lower()
    for t, label in [
        (("pronoun", "代词", "指代"), "pronoun"),
        (("ellipsis", "省略"), "ellipsis"),
        (("vague", "模糊"), "vague_reference"),
        (("adjustment", "调节", "调高", "调低"), "adjustment"),
        (("continue", "继续", "重复"), "continue"),
        (("extension", "扩展", "context"), "context_extension"),
    ]:
        if any(keyword in d for keyword in t):
            return label
    return "unknown"


#  response parsing 

def _parse_reconstructor_response(raw: str) -> tuple[str, str]:
    """Parse LLM reconstructor response. Returns (reconstructed_query, reasoning)."""
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        obj = json.loads(text)
        return obj.get("reconstructed_query", ""), obj.get("reasoning", "")
    except json.JSONDecodeError:
        pass

    # Fallback: regex extraction
    m = re.search(r'"reconstructed_query"\s*:\s*"([^"]*)"', text)
    if m:
        return m.group(1), ""
    m = re.search(r"→\s*(.+?)(?:\n|$)", text)
    if m:
        return m.group(1).strip(), ""

    logging.warning(f"[ReconstructorEval] Could not parse response: {text[:80]!r}")
    return "", ""


def _parse_judge_response(raw: str) -> dict | None:
    """Parse LLM judge response. Returns dict or None on failure."""
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        obj = json.loads(text)
        result = obj.get("result", "")
        valid_results = {"correct", "incorrect", "over_complete", "under_complete"}
        if result not in valid_results:
            logging.warning(f"[ReconstructorEval] Unknown judge result: {result!r}")
            return None
        return {
            "result": result,
            "reasoning": str(obj.get("reasoning", "")),
            "key_entity_match": bool(obj.get("key_entity_match", False)),
            "intent_preserved": bool(obj.get("intent_preserved", False)),
        }
    except json.JSONDecodeError:
        logging.warning(f"[ReconstructorEval] Judge JSON decode failed: {raw[:80]!r}")
        return None


#  sample loading 

def load_samples(path: Path) -> list[dict]:
    samples = []
    if not path.exists():
        print(f"[ReconstructorEval] Sample file not found: {path}")
        return samples
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    print(f"[ReconstructorEval] Loaded {len(samples)} samples from {path}")
    return samples


#  single-sample evaluation 

def _eval_one(
    client: OpenAI,
    model_name: str,
    sample: dict,
) -> dict:
    """
    Evaluate one reconstructor sample using fast-path + LLM-as-Judge.

    Returns a result dict with:
      query, history, expected, predicted, reasoning,
      anaphora_type, description, kw_f1,
      judge_result, judge_reasoning, key_entity_match, intent_preserved,
      evaluation_mode ("fast_correct" | "judge"),
      latency_ms, reconstruction_latency_ms, judge_latency_ms
    """
    query = sample["query"]
    history = sample.get("history", [])
    expected = sample.get("expected_reconstructed", "")
    description = sample.get("description", "")
    anaphora = _anaphora_type(description)

    history_str = format_history(history[::-1])
    num_turns = len(history) if history else 0

    prompt = build_reconstructor_prompt(
        conversation_history=history_str,
        current_query=query,
        history_turns=num_turns,
    )

    #  Step 1: call reconstructor 
    t0 = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"enable_thinking": False},
            timeout=60,
        )
        raw_output = response.choices[0].message.content
        predicted, reasoning = _parse_reconstructor_response(raw_output)
    except Exception as exc:
        logging.warning(f"[ReconstructorEval] LLM call failed for {query!r}: {exc}")
        predicted, reasoning = "", ""
    reconstruction_latency_ms = (time.perf_counter() - t0) * 1000

    kw_f1 = _keyword_f1(expected, predicted)

    # ── Step 2: decide evaluation strategy ────────────────────────────────────
    # kw_f1 is kept as a diagnostic signal; evaluation always uses the LLM judge
    # unless expected and predicted are exactly equal after normalisation.
    evaluation_mode = None
    judge_result = None
    judge_reasoning = ""
    key_entity_match = False
    intent_preserved = False
    judge_latency_ms = 0.0

    norm_exp = _normalize(expected)
    norm_pred = _normalize(predicted)
    exact_match = norm_exp == norm_pred

    if exact_match:
        # Perfect match — skip judge, mark correct immediately
        evaluation_mode = "fast_correct"
        judge_result = "correct"
        judge_reasoning = "(fast path: exact match)"
        key_entity_match = True
        intent_preserved = True
    else:
        # ── Step 3: LLM-as-Judge ───────────────────────────────────────────────
        evaluation_mode = "judge"
        judge_prompt = RECONSTRUCTOR_JUDGE_PROMPT.format(
            query=query,
            history_str=history_str,
            expected=expected,
            predicted=predicted,
        )

        t_judge = time.perf_counter()
        try:
            judge_response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": judge_prompt}],
                extra_body={"enable_thinking": False},
                timeout=_JUDGE_TIMEOUT
            )
            raw_judge = judge_response.choices[0].message.content
            parsed = _parse_judge_response(raw_judge)
            if parsed:
                judge_result = parsed["result"]
                judge_reasoning = parsed["reasoning"]
                key_entity_match = parsed["key_entity_match"]
                intent_preserved = parsed["intent_preserved"]
            else:
                # Judge failed — mark as incorrect rather than guessing
                judge_result = "incorrect"
                judge_reasoning = "(judge parse failed)"
                key_entity_match = False
                intent_preserved = False
        except Exception as exc:
            logging.warning(f"[ReconstructorEval] Judge call failed for {query!r}: {exc}")
            judge_result = "incorrect"
            judge_reasoning = f"(judge error: {exc})"
            key_entity_match = False
            intent_preserved = False
        judge_latency_ms = (time.perf_counter() - t_judge) * 1000

    latency_ms = reconstruction_latency_ms + judge_latency_ms

    return {
        "query": query,
        "history": history,
        "expected": expected,
        "predicted": predicted,
        "reasoning": reasoning,
        "anaphora_type": anaphora,
        "description": description,
        "kw_f1": kw_f1,
        "judge_result": judge_result,
        "judge_reasoning": judge_reasoning,
        "key_entity_match": key_entity_match,
        "intent_preserved": intent_preserved,
        "evaluation_mode": evaluation_mode,
        "reconstruction_latency_ms": reconstruction_latency_ms,
        "judge_latency_ms": judge_latency_ms,
        "latency_ms": latency_ms,
    }


#  metrics computation 

def _compute_metrics(results: list[dict]) -> dict:
    """Aggregate per-sample results into summary metrics."""
    total = len(results)
    if total == 0:
        return _empty_metrics()

    valid_results = {"correct", "incorrect", "over_complete", "under_complete"}

    # Count by judge result
    result_counts = {r: 0 for r in valid_results}
    for r in results:
        result_counts[r["judge_result"]] += 1

    # 多轮上下文补全率 = correct / total
    context_completion_rate = result_counts["correct"] / total
    entity_match_rate = sum(1 for r in results if r["key_entity_match"]) / total
    intent_preservation_rate = sum(1 for r in results if r["intent_preserved"]) / total

    # Per evaluation mode
    mode_counts = {}
    for r in results:
        mode_counts[r["evaluation_mode"]] = mode_counts.get(r["evaluation_mode"], 0) + 1

    # Per anaphora type
    type_names = [
        "pronoun", "ellipsis", "vague_reference", "adjustment",
        "continue", "context_extension", "unknown",
    ]
    per_type = {}
    for t in type_names:
        subset = [r for r in results if r["anaphora_type"] == t]
        n = len(subset)
        if n == 0:
            per_type[t] = {
                "count": 0,
                "completion_rate": 0.0,
                "entity_match_rate": 0.0,
                "intent_preservation_rate": 0.0,
                "avg_kw_f1": 0.0,
                "result_counts": {r: 0 for r in valid_results},
            }
            continue

        t_correct = sum(1 for r in subset if r["judge_result"] == "correct")
        t_entity = sum(1 for r in subset if r["key_entity_match"])
        t_intent = sum(1 for r in subset if r["intent_preserved"])
        t_counts = {res: sum(1 for r in subset if r["judge_result"] == res) for res in valid_results}
        per_type[t] = {
            "count": n,
            "completion_rate": t_correct / n,
            "entity_match_rate": t_entity / n,
            "intent_preservation_rate": t_intent / n,
            "avg_kw_f1": sum(r["kw_f1"] for r in subset) / n,
            "result_counts": t_counts,
        }

    error_cases = [
        {
            "query": r["query"],
            "expected": r["expected"],
            "predicted": r["predicted"],
            "judge_result": r["judge_result"],
            "judge_reasoning": r["judge_reasoning"],
            "kw_f1": round(r["kw_f1"], 4),
            "anaphora_type": r["anaphora_type"],
            "description": r["description"],
        }
        for r in results if r["judge_result"] != "correct"
    ]

    avg_reconstruction_latency = sum(r["reconstruction_latency_ms"] for r in results) / total
    avg_judge_latency = sum(r["judge_latency_ms"] for r in results) / total
    avg_total_latency = sum(r["latency_ms"] for r in results) / total

    return {
        "total_cases": total,
        # 多轮上下文补全率
        "context_completion_rate": context_completion_rate,
        # Supporting metrics
        "entity_match_rate": entity_match_rate,
        "intent_preservation_rate": intent_preservation_rate,
        "avg_keyword_f1": sum(r["kw_f1"] for r in results) / total,
        # Judge result distribution
        "result_counts": result_counts,
        # Evaluation mode distribution
        "evaluation_mode_counts": mode_counts,
        # Latency
        "avg_reconstruction_latency_ms": avg_reconstruction_latency,
        "avg_judge_latency_ms": avg_judge_latency,
        "avg_total_latency_ms": avg_total_latency,
        # Breakdown
        "per_anaphora_type": per_type,
        "error_cases": error_cases,
    }


def _empty_metrics() -> dict:
    return {
        "total_cases": 0,
        "context_completion_rate": 0.0,
        "entity_match_rate": 0.0,
        "intent_preservation_rate": 0.0,
        "avg_keyword_f1": 0.0,
        "result_counts": {"correct": 0, "incorrect": 0, "over_complete": 0, "under_complete": 0},
        "evaluation_mode_counts": {},
        "avg_reconstruction_latency_ms": 0.0,
        "avg_judge_latency_ms": 0.0,
        "avg_total_latency_ms": 0.0,
        "per_anaphora_type": {},
        "error_cases": [],
    }


def _format_summary(report: dict) -> str:
    ts = report["timestamp"]
    model = report["model"]
    total = report["total_cases"]
    ccr = report["context_completion_rate"]   # 多轮上下文补全率
    emr = report["entity_match_rate"]
    ipr = report["intent_preservation_rate"]
    kw_f1 = report["avg_keyword_f1"]
    recon_lat = report["avg_reconstruction_latency_ms"]
    judge_lat = report["avg_judge_latency_ms"]
    total_lat = report["avg_total_latency_ms"]
    rc = report["result_counts"]
    em = report["evaluation_mode_counts"]
    errors = report["error_cases"]

    lines = [
        "=" * 60,
        f"  Reconstructor Evaluation Report  [{ts}]",
        "=" * 60,
        f"  Model                    : {model}",
        f"  Total Cases              : {total}",
        "  " + "-" * 56,
        f"  多轮上下文补全率           : {ccr:.1%}",
        f"  Entity Match Rate        : {emr:.1%}",
        f"  Intent Preservation Rate : {ipr:.1%}",
        f"  Avg Keyword F1           : {kw_f1:.1%}",
        "  " + "-" * 56,
        "  Judge Result Distribution",
        f"    correct       : {rc['correct']:>5}  ({rc['correct']/total:.1%})",
        f"    incorrect     : {rc['incorrect']:>5}  ({rc['incorrect']/total:.1%})",
        f"    over_complete : {rc['over_complete']:>5}  ({rc['over_complete']/total:.1%})",
        f"    under_complete: {rc['under_complete']:>5}  ({rc['under_complete']/total:.1%})",
        "  " + "-" * 56,
        "  Evaluation Mode (fast path vs judge)",
        f"    fast_correct  : {em.get('fast_correct', 0):>5}",
        f"    judge         : {em.get('judge', 0):>5}",
        "  " + "-" * 56,
        f"  Avg Recon Latency : {recon_lat:>7.1f} ms",
        f"  Avg Judge Latency : {judge_lat:>7.1f} ms",
        f"  Avg Total Latency : {total_lat:>7.1f} ms",
        "=" * 60,
        "  Per-Anaphora-Type Metrics",
        "  " + "-" * 56,
        f"  {'Type':<22} {'Cnt':>4} {'CCR%':>6} {'EMR%':>6} {'IPR%':>6} {'AvgF1':>6}",
        "  " + "-" * 56,
    ]

    for t, m in report["per_anaphora_type"].items():
        lines.append(
            f"  {t:<22} {m['count']:>4} {m['completion_rate']:>6.1%} "
            f"{m['entity_match_rate']:>6.1%} {m['intent_preservation_rate']:>6.1%} "
            f"{m['avg_kw_f1']:>6.1%}"
        )
    lines.append("  " + "-" * 56)

    if errors:
        lines.append(f"  Non-Correct Cases ({len(errors)} total — first 10)")
        lines.append("  " + "-" * 56)
        for e in errors[:10]:
            lines.append(f"  [{e['judge_result']:>14}] {e['query'][:35]!r}")
            lines.append(f"      expected: {e['expected'][:35]!r}")
            lines.append(f"      predicted: {e['predicted'][:35]!r}")
            lines.append(f"      f1={e['kw_f1']:.2f}  type={e['anaphora_type']}")
        lines.append("  " + "-" * 56)

    lines.append("=" * 60)
    return "\n".join(lines)


#  main evaluation function 

def evaluate_reconstructor(
    samples: list[dict] | None = None,
    model_name: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    max_workers: int = 20,
) -> dict:
    """
    Evaluate the reconstructor on multi-turn context completion.

    Args:
        samples:     List of sample dicts with query, history, expected_reconstructed.
                     If None, loads from SAMPLE_PATH.
        model_name:  LLM model name (defaults to QWEN_MODEL).
        api_key:     API key (defaults to QWEN_API_KEY).
        base_url:    API base URL (defaults to QWEN_BASE).
        max_workers: Max concurrent LLM calls.

    Returns:
        Evaluation report dict ready to be serialised to JSON.
    """
    if api_key is None:
        api_key = QWEN_API_KEY
    if base_url is None:
        base_url = QWEN_BASE
    if model_name is None:
        model_name = QWEN_MODEL

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[ReconstructorEval] Starting (model={model_name})")

    if samples is None:
        samples = load_samples(SAMPLE_PATH)

    if not samples:
        logging.warning("[ReconstructorEval] No samples to evaluate.")
        return {"timestamp": timestamp, "model": model_name, **_empty_metrics()}

    client = OpenAI(api_key=api_key, base_url=base_url, max_retries=5)
    results: list[dict] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_eval_one, client, model_name, s): s for s in samples
        }
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="[ReconstructorEval] Evaluating",
        ):
            results.append(future.result())

    # Restore original order
    sample_map = {s["query"]: i for i, s in enumerate(samples)}
    results.sort(key=lambda r: sample_map.get(r["query"], 0))

    metrics = _compute_metrics(results)

    report = {"timestamp": timestamp, "model": model_name, **metrics}

    logging.info(
        f"[ReconstructorEval] Done. CCR={metrics['context_completion_rate']:.1%}  "
        f"EMR={metrics['entity_match_rate']:.1%}  IPR={metrics['intent_preservation_rate']:.1%}"
    )

    return report


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    samples = load_samples(SAMPLE_PATH)
    if not samples:
        print("[ReconstructorEval] No samples loaded, exiting.")
        return

    report = evaluate_reconstructor(samples=samples)
    print("\n" + _format_summary(report))

    # Round floats for JSON serialisability
    def _round(obj):
        if isinstance(obj, dict):
            return {k: _round(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_round(v) for v in obj]
        if isinstance(obj, float):
            return round(obj, 4)
        return obj

    report = _round(report)

    with REPORT_FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n[ReconstructorEval] JSON report saved to: {REPORT_FILE_PATH}")
    print(f"[ReconstructorEval] Log file: {LOG_FILE_PATH}")


if __name__ == "__main__":
    main()
