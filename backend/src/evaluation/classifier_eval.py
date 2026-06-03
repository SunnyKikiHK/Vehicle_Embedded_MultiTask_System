"""Classifier evaluation: query classification accuracy.

Loads test samples from classifier_samples.json and evaluates the LLM-based
query classifier against ground-truth labels. Produces overall accuracy,
per-class metrics, and error case lists.
"""

import os
import sys
import json
import time
import logging
import concurrent.futures
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from openai import OpenAI
from tqdm import tqdm

from src.prompts import CLASSIFIER_PROMPT
from src.constants import CLASSIFIER_SAMPLE_PATH, LOG_DIR, EVAL_DIR
from src.schema.classifier_output import ClassifierOutput, QueryType

QWEN_API_KEY = os.environ.get("QWEN_API_KEY")
QWEN_BASE = os.environ.get("QWEN_BASE")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

SAMPLE_PATH = Path(CLASSIFIER_SAMPLE_PATH)
LOG_DIR = Path(LOG_DIR)
LOG_FILE_PATH = LOG_DIR / "classifier_eval.log"
REPORT_DIR = Path(EVAL_DIR) / "reports"
REPORT_FILE_PATH = REPORT_DIR / "classifier_eval.json"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)



@dataclass
class SingleResult:
    query: str
    expected: QueryType
    predicted: QueryType
    confidence: float
    latency_ms: float
    correct: bool
    description: str


@dataclass
class ClassMetrics:
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
    avg_latency_ms: float
    per_class: dict[str, ClassMetrics]
    confusion_matrix: dict[str, dict[str, int]]
    error_cases: list[dict]

    @property
    def summary(self) -> str:
        type_names = [t.name for t in QueryType]
        lines = [
            "=" * 60,
            f"  Classifier Evaluation Report  [{self.timestamp}]",
            "=" * 60,
            f"  Model          : {self.model}",
            f"  Total Cases    : {self.total_cases}",
            f"  Correct        : {self.correct}",
            f"  Accuracy       : {self.accuracy:.1%}",
            f"  Avg Latency    : {self.avg_latency_ms:.1f} ms",
            "=" * 60,
            "  Per-Class Metrics",
            "  " + "-" * 57,
            f"  {'Class':<18} {'Prec':>6} {'Recall':>6} {'F1':>6} {'Supp':>5} {'OK':>5} {'ERR':>5}",
            "  " + "-" * 57,
        ]
        for name, m in self.per_class.items():
            lines.append(
                f"  {name:<18} {m.precision:>6.1%} {m.recall:>6.1%} "
                f"{m.f1:>6.1%} {m.support:>5d} {m.correct:>5d} {m.incorrect:>5d}"
            )
        lines.append("  " + "-" * 57)
        lines.append("  Confusion Matrix (rows=expected, cols=predicted)")
        lines.append("  " + "-" * 57)
        header = f"  {'':>20}" + "".join(f" {t[:7]:>8}" for t in type_names)
        lines.append(header)
        for r in type_names:
            row = f"  {r:<20}" + "".join(
                f" {self.confusion_matrix[r].get(c, 0):>8d}" for c in type_names
            )
            lines.append(row)
        lines.append("=" * 60)
        if self.error_cases:
            lines.append(f"  Error Cases ({len(self.error_cases)} total)")
            lines.append("  " + "-" * 57)
            for e in self.error_cases[:10]:
                lines.append(f"  [E] query={e['query'][:40]!r}")
                lines.append(f"      expected={e['expected']}, predicted={e['predicted']}")
        lines.append("=" * 60)
        return "\n".join(lines)

def _map_expected(raw: int | str) -> QueryType:
    """Map raw integer (1/2/3) or string label to QueryType."""
    if isinstance(raw, int) or (isinstance(raw, str) and raw.isdigit()):
        val = int(raw)
        if val == 1:
            return QueryType.CHILL_CHAT
        elif val == 2:
            return QueryType.TASK_SPECIFIC
        else:
            return QueryType.MEANINGLESS
    name = str(raw).upper()
    if "CHILL" in name or "闲聊" in name:
        return QueryType.CHILL_CHAT
    if "TASK" in name or "任务" in name:
        return QueryType.TASK_SPECIFIC
    return QueryType.MEANINGLESS


def load_samples(path: Path) -> list[dict]:
    """Load classifier samples from JSON lines file."""
    samples = []
    if not path.exists():
        print(f"[ClassifierEval] Sample file not found: {path}")
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
    print(f"[ClassifierEval] Loaded {len(samples)} samples from {path}")
    return samples


def _compute_metrics(results: list[SingleResult]) -> tuple[dict[str, ClassMetrics], dict[str, dict[str, int]]]:
    """Compute per-class precision/recall/F1 and confusion matrix."""
    type_names = [t.name for t in QueryType]

    confusion: dict[str, dict[str, int]] = {
        r: {c: 0 for c in type_names} for r in type_names
    }
    class_correct: dict[str, int] = {t: 0 for t in type_names}
    class_total: dict[str, int] = {t: 0 for t in type_names}
    class_predicted: dict[str, int] = {t: 0 for t in type_names}

    for r in results:
        exp_name = r.expected.name
        pred_name = r.predicted.name
        confusion[exp_name][pred_name] += 1
        class_total[exp_name] += 1
        if r.correct:
            class_correct[exp_name] += 1
        class_predicted[pred_name] += 1

    metrics: dict[str, ClassMetrics] = {}
    for t_name in type_names:
        support = class_total.get(t_name, 0)
        correct = class_correct.get(t_name, 0)
        predicted = max(class_predicted.get(t_name, 0), 1)

        precision = correct / predicted if predicted > 0 else 0.0
        recall = correct / support if support > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics[t_name] = ClassMetrics(
            precision=precision,
            recall=recall,
            f1=f1,
            support=support,
            correct=correct,
            incorrect=support - correct,
        )

    return metrics, confusion

def _eval_one(client: OpenAI, model_name: str, sample: dict) -> SingleResult:
    query = sample["query"]
    raw_expected = sample.get("expected", 2)
    expected = _map_expected(raw_expected)
    description = sample.get("description", "")

    t0 = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": CLASSIFIER_PROMPT.format(
                    query=query,
                    history_turns=0,
                    conversation_history="(无历史记录)",
                )}
            ],
            extra_body={"enable_thinking": False},
            timeout=60
        )
        raw_output = response.choices[0].message.content
        output: ClassifierOutput = parse_classifier_response(raw_output)
        predicted = output.query_type
        confidence = output.confidence
    except Exception as exc:
        logging.warning(f"[ClassifierEval] LLM call failed for {query!r}: {exc}")
        predicted = QueryType.TASK_SPECIFIC
        confidence = 0.0

    latency_ms = (time.perf_counter() - t0) * 1000

    return SingleResult(
        query=query,
        expected=expected,
        predicted=predicted,
        confidence=confidence,
        latency_ms=latency_ms,
        correct=(predicted == expected),
        description=description,
    )

def evaluate_classifier(
    samples: list[dict] | None = None,
    model_name: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    max_workers: int = 20,
) -> EvaluationReport:
    """
    Evaluate the query classifier against test samples.

    Args:
        samples: List of sample dicts with `query`, `expected`, `description`.
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
    logging.info(f"[ClassifierEval] Starting evaluation (model={model_name})")

    if samples is None:
        samples = load_samples(SAMPLE_PATH)

    if not samples:
        print("[ClassifierEval] No samples to evaluate.")
        return EvaluationReport(
            timestamp=timestamp,
            model=model_name,
            total_cases=0,
            correct=0,
            accuracy=0.0,
            avg_latency_ms=0.0,
            per_class={},
            confusion_matrix={},
            error_cases=[],
        )

    client = OpenAI(api_key=api_key, base_url=base_url, max_retries=5)

    results: list[SingleResult] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_eval_one, client, model_name, s): s for s in samples}
        for future in tqdm(concurrent.futures.as_completed(futures),
                           total=len(futures),
                           desc="[ClassifierEval] Evaluating"):
            results.append(future.result())

    # Sort results by original sample order
    sample_map = {s["query"]: i for i, s in enumerate(samples)}
    results.sort(key=lambda r: sample_map.get(r.query, 0))

    # Compute metrics
    per_class, confusion = _compute_metrics(results)

    total = len(results)
    correct = sum(1 for r in results if r.correct)
    accuracy = correct / total if total > 0 else 0.0
    avg_latency = sum(r.latency_ms for r in results) / total if total > 0 else 0.0

    error_cases = [
        {
            "query": r.query,
            "expected": r.expected.name,
            "predicted": r.predicted.name,
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
        avg_latency_ms=avg_latency,
        per_class=per_class,
        confusion_matrix=confusion,
        error_cases=error_cases,
    )


def parse_classifier_response(raw: str) -> ClassifierOutput:
    """Parse LLM classifier response into ClassifierOutput."""
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
    except json.JSONDecodeError:
        return ClassifierOutput(
            query_type=QueryType.TASK_SPECIFIC,
            confidence=0.0,
            reasoning="JSON parse failed",
        )

    # Map numeric or string query_type
    qt = obj.get("query_type") or obj.get("type") or obj.get("label") or obj.get("category")
    if isinstance(qt, int):
        qt = _map_expected(qt)

    try:
        return ClassifierOutput(
            query_type=_map_expected(qt),
            confidence=float(obj.get("confidence", 0.0)),
            reasoning=str(obj.get("reasoning", "")),
        )
    except (ValueError, TypeError):
        return ClassifierOutput(
            query_type=QueryType.TASK_SPECIFIC,
            confidence=0.0,
            reasoning=f"Unknown query_type: {qt}",
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

    # Load samples
    samples = load_samples(Path(CLASSIFIER_SAMPLE_PATH))
    if not samples:
        print("[ClassifierEval] No samples loaded, exiting.")
        return

    report = evaluate_classifier(
        samples=samples
    )

    print("\n" + report.summary)

    report_dict = {
        "timestamp": report.timestamp,
        "model": report.model,
        "total_cases": report.total_cases,
        "correct": report.correct,
        "accuracy": round(report.accuracy, 4),
        "avg_latency_ms": round(report.avg_latency_ms, 2),
        "per_class": {k: asdict(v) for k, v in report.per_class.items()},
        "confusion_matrix": report.confusion_matrix,
        "error_cases": report.error_cases,
    }
    with REPORT_FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    print(f"\n[ClassifierEval] JSON report saved to: {str(REPORT_FILE_PATH)}")
    print(f"[ClassifierEval] Log file: {str(LOG_FILE_PATH)}")


if __name__ == "__main__":
    main()
