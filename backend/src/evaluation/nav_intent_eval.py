"""Navigation intent evaluation: intent recognition F1 score.

Loads test samples from nav_intent_samples.json and evaluates the LLM-based
navigation intent classifier against ground-truth intent labels. Produces overall
accuracy, per-intent precision/recall/F1, and error case lists.
"""

import os
import json
import time
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from openai import OpenAI
from tqdm import tqdm
from src.constants import NAV_INTENT_SAMPLE_PATH, LOG_DIR, EVAL_DIR

QWEN_API_KEY = os.environ.get("QWEN_API_KEY")
QWEN_BASE = os.environ.get("QWEN_BASE")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

SAMPLE_PATH = Path(NAV_INTENT_SAMPLE_PATH)
LOG_DIR = Path(LOG_DIR)
LOG_FILE_PATH = LOG_DIR / "nav_intent_eval.log"
REPORT_DIR = Path(EVAL_DIR) / "reports"
REPORT_FILE_PATH = REPORT_DIR / "nav_intent_eval.json"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


NAV_INTENT_SKILL_PATH = Path(__file__).parent.parent / "skills" / "navigation-agent" / "SKILL.md"


def _load_skill_prompt() -> str:
    """Load the navigation-agent SKILL.md and format it as a prompt template.

    Uses the deployment SKILL.md so the evaluator mirrors what the real agent uses.
    """
    if not NAV_INTENT_SKILL_PATH.exists():
        raise FileNotFoundError(f"SKILL.md not found at {NAV_INTENT_SKILL_PATH}")

    return NAV_INTENT_SKILL_PATH.read_text(encoding="utf-8")


NAV_INTENT_PROMPT_TEMPLATE = _load_skill_prompt()
@dataclass
class SingleResult:
    query: str
    expected: str
    predicted: str
    confidence: float
    latency_ms: float
    correct: bool
    description: str


@dataclass
class IntentMetrics:
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    support: int = 0
    correct: int = 0
    incorrect: int = 0


@dataclass
class EvaluationReport:
    timestamp: str
    model: str
    total_cases: int
    correct: int
    accuracy: float
    macro_f1: float
    micro_f1: float
    weighted_f1: float
    avg_latency_ms: float
    per_intent: dict[str, IntentMetrics]
    confusion_matrix: dict[str, dict[str, int]]
    error_cases: list[dict]

    @property
    def summary(self) -> str:
        intent_names = sorted(self.per_intent.keys())
        lines = [
            "=" * 60,
            f"  Navigation Intent Evaluation Report  [{self.timestamp}]",
            "=" * 60,
            f"  Model          : {self.model}",
            f"  Total Cases    : {self.total_cases}",
            f"  Correct        : {self.correct}",
            f"  Accuracy       : {self.accuracy:.1%}",
            f"  Macro F1       : {self.macro_f1:.4f}",
            f"  Micro F1       : {self.micro_f1:.4f}",
            f"  Weighted F1    : {self.weighted_f1:.4f}",
            f"  Avg Latency    : {self.avg_latency_ms:.1f} ms",
            "=" * 60,
            "  Per-Intent Metrics",
            "  " + "-" * 57,
            f"  {'Intent':<28} {'Prec':>6} {'Recall':>6} {'F1':>6} {'Supp':>5} {'OK':>5} {'ERR':>5}",
            "  " + "-" * 57,
        ]
        for name in intent_names:
            m = self.per_intent[name]
            lines.append(
                f"  {name:<28} {m.precision:>6.1%} {m.recall:>6.1%} "
                f"{m.f1:>6.1%} {m.support:>5d} {m.correct:>5d} {m.incorrect:>5d}"
            )
        lines.append("=" * 60)
        if self.error_cases:
            lines.append(f"  Error Cases ({len(self.error_cases)} total, showing top 10)")
            lines.append("  " + "-" * 57)
            for e in self.error_cases[:10]:
                lines.append(f"  [E] query={e['query'][:40]!r}")
                lines.append(f"      expected={e['expected']}, predicted={e['predicted']}")
        lines.append("=" * 60)
        return "\n".join(lines)

def load_samples(path: Path) -> list[dict]:
    """Load nav-intent samples from JSON lines file."""
    samples = []
    if not path.exists():
        print(f"[NavIntentEval] Sample file not found: {path}")
        return samples
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                samples.append(obj)
            except json.JSONDecodeError:
                continue
    print(f"[NavIntentEval] Loaded {len(samples)} samples from {path}")
    return samples

def _compute_metrics(
    results: list[SingleResult],
) -> tuple[dict[str, IntentMetrics], dict[str, dict[str, int]]]:
    """Compute per-intent precision/recall/F1 and confusion matrix."""
    all_intents: set[str] = set()
    for r in results:
        all_intents.add(r.expected)
        all_intents.add(r.predicted)
    intent_names = sorted(all_intents)

    confusion: dict[str, dict[str, int]] = {
        e: {p: 0 for p in intent_names} for e in intent_names
    }
    class_correct: dict[str, int] = {i: 0 for i in intent_names}
    class_total: dict[str, int] = {i: 0 for i in intent_names}
    class_predicted: dict[str, int] = {i: 0 for i in intent_names}

    for r in results:
        exp, pred = r.expected, r.predicted
        confusion[exp][pred] += 1
        class_total[exp] += 1
        if r.correct:
            class_correct[exp] += 1
        class_predicted[pred] += 1

    metrics: dict[str, IntentMetrics] = {}
    for intent in intent_names:
        support = class_total.get(intent, 0)
        correct = class_correct.get(intent, 0)
        predicted = max(class_predicted.get(intent, 0), 1)

        precision = correct / predicted if predicted > 0 else 0.0
        recall = correct / support if support > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics[intent] = IntentMetrics(
            precision=precision,
            recall=recall,
            f1=f1,
            support=support,
            correct=correct,
            incorrect=support - correct,
        )

    return metrics, confusion


def _compute_f1_scores(
    results: list[SingleResult],
    metrics: dict[str, IntentMetrics],
) -> tuple[float, float, float]:
    """Compute macro, micro, and weighted F1 scores."""
    all_intents = list(metrics.keys())
    if not all_intents:
        return 0.0, 0.0, 0.0

    # Macro F1: average of per-intent F1
    macro_f1 = sum(m.f1 for m in metrics.values()) / len(metrics)

    # Micro F1: global TP/FP/FN
    total_tp = sum(m.correct for m in metrics.values())
    total_fn = sum(m.incorrect for m in metrics.values())
    total_fp = 0
    for r in results:
        if not r.correct:
            total_fp += 1
    micro_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0.0

    # Weighted F1: support-weighted average of per-intent F1
    total_support = sum(m.support for m in metrics.values())
    weighted_f1 = sum(m.f1 * m.support for m in metrics.values()) / total_support if total_support > 0 else 0.0

    return macro_f1, micro_f1, weighted_f1


def parse_nav_intent_response(raw: str) -> str:
    """Parse LLM response to extract predicted intent (tool_name)."""
    text = raw.strip()

    # Strip markdown code fences
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        obj = json.loads(text)
        tool_name = obj.get("tool_name", "")
        if tool_name:
            return tool_name
    except json.JSONDecodeError:
        pass

    # Fallback: try to extract tool_name via regex
    import re
    m = re.search(r'"tool_name"\s*:\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    return ""

def evaluate_nav_intent(
    samples: list[dict] | None = None,
    model_name: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    max_workers: int = 20,
) -> EvaluationReport:
    """
    Evaluate the navigation intent classifier against test samples.

    Args:
        samples: List of sample dicts with `query`, `intent`, `description`.
                 If None, loads from SAMPLE_PATH.
        model_name: LLM model name (defaults to QWEN_MODEL).
        api_key: API key (defaults to QWEN_API_KEY).
        base_url: API base URL (defaults to QWEN_BASE).
        max_workers: Max concurrent LLM calls.

    Returns:
        EvaluationReport with metrics and results.
    """
    if api_key is None:
        api_key = QWEN_API_KEY
    if base_url is None:
        base_url = QWEN_BASE
    if model_name is None:
        model_name = QWEN_MODEL

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[NavIntentEval] Starting evaluation (model={model_name})")

    skill_content = NAV_INTENT_SKILL_PATH.read_text(encoding="utf-8")

    if samples is None:
        samples = load_samples(SAMPLE_PATH)

    if not samples:
        print("[NavIntentEval] No samples to evaluate.")
        return EvaluationReport(
            timestamp=timestamp,
            model=model_name,
            total_cases=0,
            correct=0,
            accuracy=0.0,
            macro_f1=0.0,
            micro_f1=0.0,
            weighted_f1=0.0,
            avg_latency_ms=0.0,
            per_intent={},
            confusion_matrix={},
            error_cases=[],
        )

    client = OpenAI(api_key=api_key, base_url=base_url, max_retries=5)

    results: list[SingleResult] = []

    import concurrent.futures

    def _eval_one(sample: dict, skill_content: str) -> SingleResult:
        query = sample["query"]
        expected = sample["intent"]
        description = sample.get("description", "")

        t0 = time.perf_counter()
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": NAV_INTENT_PROMPT_TEMPLATE},{"role": "user", "content": query}],
                extra_body={"enable_thinking": False},
                timeout=60,
            )
            raw_output = response.choices[0].message.content
            predicted = parse_nav_intent_response(raw_output)
            confidence = 1.0
        except Exception as exc:
            logging.warning(f"[NavIntentEval] LLM call failed for {query!r}: {exc}")
            predicted = ""
            confidence = 0.0

        latency_ms = (time.perf_counter() - t0) * 1000

        # Normalize comparison
        correct = (predicted.strip().lower() == expected.strip().lower())

        return SingleResult(
            query=query,
            expected=expected,
            predicted=predicted,
            confidence=confidence,
            latency_ms=latency_ms,
            correct=correct,
            description=description,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_eval_one, s, skill_content): s for s in samples}
        for future in tqdm(concurrent.futures.as_completed(futures),
                           total=len(futures),
                           desc="[NavIntentEval] Evaluating"):
            results.append(future.result())

    # Sort by original sample order
    sample_map = {s["query"]: i for i, s in enumerate(samples)}
    results.sort(key=lambda r: sample_map.get(r.query, 0))

    # Compute metrics
    per_intent, confusion = _compute_metrics(results)
    macro_f1, micro_f1, weighted_f1 = _compute_f1_scores(results, per_intent)

    total = len(results)
    correct = sum(1 for r in results if r.correct)
    accuracy = correct / total if total > 0 else 0.0
    avg_latency = sum(r.latency_ms for r in results) / total if total > 0 else 0.0

    error_cases = [
        {
            "query": r.query,
            "expected": r.expected,
            "predicted": r.predicted,
            "confidence": r.confidence,
            "description": r.description,
        }
        for r in results if not r.correct
    ]

    return EvaluationReport(
        timestamp=timestamp,
        model=model_name,
        total_cases=total,
        correct=correct,
        accuracy=accuracy,
        macro_f1=macro_f1,
        micro_f1=micro_f1,
        weighted_f1=weighted_f1,
        avg_latency_ms=avg_latency,
        per_intent=per_intent,
        confusion_matrix=confusion,
        error_cases=error_cases,
    )

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    samples = load_samples(Path(NAV_INTENT_SAMPLE_PATH))
    if not samples:
        print("[NavIntentEval] No samples loaded, exiting.")
        return

    report = evaluate_nav_intent(
        samples=samples
    )

    print("\n" + report.summary)

    report_dict = {
        "timestamp": report.timestamp,
        "model": report.model,
        "total_cases": report.total_cases,
        "correct": report.correct,
        "accuracy": round(report.accuracy, 4),
        "macro_f1": round(report.macro_f1, 4),
        "micro_f1": round(report.micro_f1, 4),
        "weighted_f1": round(report.weighted_f1, 4),
        "avg_latency_ms": round(report.avg_latency_ms, 2),
        "per_intent": {k: asdict(v) for k, v in report.per_intent.items()},
        "confusion_matrix": report.confusion_matrix,
        "error_cases": report.error_cases,
    }
    with REPORT_FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    print(f"\n[NavIntentEval] JSON report saved to: {str(REPORT_FILE_PATH)}")
    print(f"[NavIntentEval] Log file: {str(LOG_FILE_PATH)}")


if __name__ == "__main__":
    main()
