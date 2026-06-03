"""Router evaluation: task agent classification accuracy.

Loads test samples from router_samples.json and evaluates the LLM-based
agent router against ground-truth agent labels. Since deployment only has
navigation-agent active, this script temporarily enables all agents when
building the routing prompt to fairly evaluate routing across all 12 agents.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from openai import OpenAI
from tqdm import tqdm


from src.skills import skill_loader
from src.utils import build_routing_prompt
from src.constants import ROUTER_SAMPLE_PATH, LOG_DIR, EVAL_DIR, SERVER_USE


QWEN_API_KEY = os.environ.get("QWEN_API_KEY")
QWEN_BASE = os.environ.get("QWEN_BASE")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

SAMPLE_PATH = Path(ROUTER_SAMPLE_PATH)
LOG_DIR = Path(LOG_DIR)
LOG_FILE_PATH = LOG_DIR / "router_eval.log"
REPORT_DIR = Path(EVAL_DIR) / "reports"
REPORT_FILE_PATH = REPORT_DIR / "router_eval.json"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _enable_all_agents():
    """Enable all agents in SERVER_USE for evaluation prompt building.

    This is process-local only and has no effect after the script exits.
    """
    for key in SERVER_USE:
        SERVER_USE[key] = True
    skill_loader._SKILL_MANIFEST = skill_loader._build_manifest()


def _build_eval_routing_prompt(query: str) -> str:
    """Build routing prompt with all agents enabled (for evaluation)."""
    agent_defs = skill_loader.format_skill_descriptions()
    agent_names = skill_loader.get_agent_names_from_skills()
    num_agents = len(skill_loader._SKILL_MANIFEST)
    return build_routing_prompt(
        agent_definitions=agent_defs,
        agent_names=agent_names,
        num_agents=num_agents,
        current_query=query,
    )


@dataclass
class SingleResult:
    query: str
    expected: str
    predicted: str
    confidence: float
    reasoning: str
    latency_ms: float
    correct: bool
    description: str


@dataclass
class AgentMetrics:
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
    per_agent: dict[str, AgentMetrics]
    confusion_matrix: dict[str, dict[str, int]]
    error_cases: list[dict]

    @property
    def summary(self) -> str:
        agent_names = sorted(self.per_agent.keys())
        lines = [
            "=" * 60,
            f"  Router Evaluation Report  [{self.timestamp}]",
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
            "  Per-Agent Metrics",
            "  " + "-" * 57,
            f"  {'Agent':<28} {'Prec':>6} {'Recall':>6} {'F1':>6} {'Supp':>5} {'OK':>5} {'ERR':>5}",
            "  " + "-" * 57,
        ]
        for name in agent_names:
            m = self.per_agent[name]
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
    """Load router samples from JSON lines file."""
    samples = []
    if not path.exists():
        print(f"[RouterEval] Sample file not found: {path}")
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
    print(f"[RouterEval] Loaded {len(samples)} samples from {path}")
    return samples

def _compute_metrics(
    results: list[SingleResult],
) -> tuple[dict[str, AgentMetrics], dict[str, dict[str, int]]]:
    """Compute per-agent precision/recall/F1 and confusion matrix."""
    all_agents: set[str] = set()
    for r in results:
        all_agents.add(r.expected)
        all_agents.add(r.predicted)
    agent_names = sorted(all_agents)

    confusion: dict[str, dict[str, int]] = {
        e: {p: 0 for p in agent_names} for e in agent_names
    }
    class_correct: dict[str, int] = {a: 0 for a in agent_names}
    class_total: dict[str, int] = {a: 0 for a in agent_names}
    class_predicted: dict[str, int] = {a: 0 for a in agent_names}

    for r in results:
        exp, pred = r.expected, r.predicted
        confusion[exp][pred] += 1
        class_total[exp] += 1
        if r.correct:
            class_correct[exp] += 1
        class_predicted[pred] += 1

    metrics: dict[str, AgentMetrics] = {}
    for agent in agent_names:
        support = class_total.get(agent, 0)
        correct = class_correct.get(agent, 0)
        predicted = max(class_predicted.get(agent, 0), 1)

        precision = correct / predicted if predicted > 0 else 0.0
        recall = correct / support if support > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics[agent] = AgentMetrics(
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
    metrics: dict[str, AgentMetrics],
) -> tuple[float, float, float]:
    """Compute macro, micro, and weighted F1 scores."""
    all_agents = list(metrics.keys())
    if not all_agents:
        return 0.0, 0.0, 0.0

    # Macro F1: average of per-agent F1
    macro_f1 = sum(m.f1 for m in metrics.values()) / len(metrics)

    # Micro F1: global TP/FP/FN
    total_tp = sum(m.correct for m in metrics.values())
    total_fn = sum(m.incorrect for m in metrics.values())
    total_fp = sum(1 for r in results if not r.correct)
    micro_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0.0

    # Weighted F1: support-weighted average
    total_support = sum(m.support for m in metrics.values())
    weighted_f1 = sum(m.f1 * m.support for m in metrics.values()) / total_support if total_support > 0 else 0.0

    return macro_f1, micro_f1, weighted_f1

def parse_router_response(raw: str) -> tuple[str, float, str]:
    """Parse LLM router response into (target_agent, confidence, reasoning)."""
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
        agent = obj.get("target_agent", "")
        confidence = float(obj.get("confidence", 0.0))
        reasoning = str(obj.get("reasoning", ""))
        return agent, confidence, reasoning
    except (json.JSONDecodeError, (ValueError, TypeError)):
        pass

    # Fallback: regex extraction
    import re
    agent_m = re.search(r'"target_agent"\s*:\s*"([^"]+)"', text)
    conf_m = re.search(r'"confidence"\s*:\s*([0-9.]+)', text)
    reason_m = re.search(r'"reasoning"\s*:\s*"([^"]*)"', text)

    agent = agent_m.group(1) if agent_m else ""
    confidence = float(conf_m.group(1)) if conf_m else 0.0
    reasoning = reason_m.group(1) if reason_m else ""

    return agent, confidence, reasoning

def evaluate_router(
    samples: list[dict] | None = None,
    model_name: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    max_workers: int = 20,
) -> EvaluationReport:
    """
    Evaluate the agent router against test samples.

    Args:
        samples: List of sample dicts with `query`, `agent`, `description`.
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
    logging.info(f"[RouterEval] Starting evaluation (model={model_name})")

    if samples is None:
        samples = load_samples(SAMPLE_PATH)

    if not samples:
        print("[RouterEval] No samples to evaluate.")
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
            per_agent={},
            confusion_matrix={},
            error_cases=[],
        )

    # Enable all agents for prompt building (process-local only; no side effects after exit)
    _enable_all_agents()
    logging.info(f"[RouterEval] Enabled {len(skill_loader._SKILL_MANIFEST)} agents for evaluation prompt")

    # Pre-build prompts for all samples (all-agents context)
    prompts: dict[str, str] = {}
    for s in samples:
        prompts[s["query"]] = _build_eval_routing_prompt(s["query"])

    client = OpenAI(api_key=api_key, base_url=base_url, max_retries=5)

    results: list[SingleResult] = []
    import concurrent.futures

    def _eval_one(sample: dict) -> SingleResult:
        query = sample["query"]
        expected = sample["agent"]
        description = sample.get("description", "")

        t0 = time.perf_counter()
        try:
            prompt = prompts[query]
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                extra_body={"enable_thinking": False},
                timeout=60,
            )
            raw_output = response.choices[0].message.content
            predicted, confidence, reasoning = parse_router_response(raw_output)
        except Exception as exc:
            logging.warning(f"[RouterEval] LLM call failed for {query!r}: {exc}")
            predicted = ""
            confidence = 0.0
            reasoning = f"Error: {exc}"

        latency_ms = (time.perf_counter() - t0) * 1000

        # Normalize comparison (case-insensitive)
        correct = (predicted.strip().lower() == expected.strip().lower())

        return SingleResult(
            query=query,
            expected=expected,
            predicted=predicted,
            confidence=confidence,
            reasoning=reasoning,
            latency_ms=latency_ms,
            correct=correct,
            description=description,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_eval_one, s): s for s in samples}
        for future in tqdm(concurrent.futures.as_completed(futures),
                          total=len(futures),
                          desc="[RouterEval] Evaluating"):
            results.append(future.result())

    # Sort by original sample order
    sample_map = {s["query"]: i for i, s in enumerate(samples)}
    results.sort(key=lambda r: sample_map.get(r.query, 0))

    # Compute metrics
    per_agent, confusion = _compute_metrics(results)
    macro_f1, micro_f1, weighted_f1 = _compute_f1_scores(results, per_agent)

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
            "reasoning": r.reasoning,
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
        per_agent=per_agent,
        confusion_matrix=confusion,
        error_cases=error_cases,
    )

def main():
    log_file = LOG_DIR / f"router_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    samples = load_samples(SAMPLE_PATH)
    if not samples:
        print("[RouterEval] No samples loaded, exiting.")
        return

    report = evaluate_router(
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
        "per_agent": {k: asdict(v) for k, v in report.per_agent.items()},
        "confusion_matrix": report.confusion_matrix,
        "error_cases": report.error_cases,
    }
    with REPORT_FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    print(f"\n[RouterEval] JSON report saved to: {str(REPORT_FILE_PATH)}")
    print(f"[RouterEval] Log file: {str(LOG_FILE_PATH)}")


if __name__ == "__main__":
    main()
