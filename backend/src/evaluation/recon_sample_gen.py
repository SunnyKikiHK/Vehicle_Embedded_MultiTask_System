"""Reconstructor sample generator: generate multi-turn context completion test samples.

Uses the LLM to generate diverse test cases covering 6 anaphora types:
pronoun, ellipsis, vague_reference, adjustment, continue, context_extension.
Output is written as JSON lines to RECONSTRUCTOR_SAMPLE_PATH.
"""

import os
import json
import time
import random
import concurrent.futures
from pathlib import Path
from tqdm import tqdm
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from src.constants import RECONSTRUCTOR_SAMPLE_PATH
from src.prompts import RECONSTRUCTOR_SAMPLES_PROMPT


_MAX_CONCURRENT_WORKERS = 20
_PER_SAMPLE_GENERATION = 100
_PER_SAMPLE_RESPONSE = 10

QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

RECONSTRUCTOR_SAMPLE_PATH = Path(RECONSTRUCTOR_SAMPLE_PATH)
RECONSTRUCTOR_SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _build_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["QWEN_API_KEY"],
        base_url=os.environ["QWEN_BASE"],
    )


def _load_existing() -> list[dict]:
    if not RECONSTRUCTOR_SAMPLE_PATH.exists():
        return []
    samples = []
    with RECONSTRUCTOR_SAMPLE_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return samples


class ReconstructorSample(BaseModel):
    turn: int
    query: str
    history: list[dict]
    expected_reconstructed: str
    description: str


def _call_llm(
    num_queries: int,
    model_name: str,
    existing_samples: list[dict],
    max_retry: int = 5,
) -> list[ReconstructorSample]:
    accumulated: list[ReconstructorSample] = []
    attempt = 0

    while len(accumulated) < _PER_SAMPLE_GENERATION and attempt < max_retry:
        try:
            client = _build_client()
            # Serialize existing samples as JSON text for the prompt
            existing_text = json.dumps(existing_samples, ensure_ascii=False)
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": RECONSTRUCTOR_SAMPLES_PROMPT.format(
                            num_queries=num_queries,
                            existing_samples=existing_text,
                        ),
                    }
                ],
                top_p=0.9,
                temperature=0.9,
                extra_body={
                    "enable_thinking": False,
                    "repetition_penalty": 1.1,
                    "seed": random.randint(0, 999999),
                },
                timeout=60,
            )

            if not response.choices:
                attempt += 1
                continue

            parsed = _parse_response(response.choices[0].message.content)
            if parsed:
                # Add to existing list so LLM avoids duplicates in next call
                existing_samples.extend(s.model_dump() for s in parsed)
                accumulated.extend(parsed)
                attempt = 0
            else:
                attempt += 1

        except Exception as exc:
            if attempt < max_retry - 1:
                time.sleep(1)
                attempt += 1
            else:
                print(f"[ReconstructorGen] Error: {exc}")
                return accumulated

    return accumulated


def _parse_response(raw: str) -> list[ReconstructorSample]:
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        raw_list = json.loads(text)
    except json.JSONDecodeError:
        print(f"[ReconstructorGen] JSON decode failed. Raw: {raw[:100]}")
        return []

    if not isinstance(raw_list, list):
        print(f"[ReconstructorGen] Expected list, got {type(raw_list).__name__}")
        return []

    validated = []
    for item in raw_list:
        try:
            validated.append(ReconstructorSample.model_validate(item))
        except ValidationError:
            continue
    return validated


def request_reconstructor_samples(nums: int = 1000) -> list[ReconstructorSample]:
    """Generate N reconstructor samples using concurrent LLM calls."""
    existing_samples = _load_existing()
    total_calls = (nums + _PER_SAMPLE_GENERATION - 1) // _PER_SAMPLE_GENERATION
    print(
        f"[ReconstructorGen] Generating {nums} samples in {total_calls} calls "
        f"(existing: {len(existing_samples)}) ..."
    )

    total: list[ReconstructorSample] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_WORKERS) as executor:
        futures = {
            executor.submit(
                _call_llm,
                _PER_SAMPLE_RESPONSE,
                QWEN_MODEL,
                existing_samples,
            ): i
            for i in range(total_calls)
        }

        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="[ReconstructorGen] Generating samples ...",
        ):
            batch = future.result()
            total.extend(batch)

    # Deduplicate by (query, history) key
    seen: set[str] = set()
    unique: list[ReconstructorSample] = []
    for s in total:
        key = s.query + "|" + json.dumps(s.history, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append(s)

    return unique[:nums]


def write_txt(samples: list[ReconstructorSample], mode: str = "a") -> None:
    if mode == "w" and RECONSTRUCTOR_SAMPLE_PATH.exists():
        RECONSTRUCTOR_SAMPLE_PATH.unlink()
    with RECONSTRUCTOR_SAMPLE_PATH.open(mode, encoding="utf-8") as f:
        for sample in samples:
            f.write(sample.model_dump_json() + "\n")


def main():
    print(f"[ReconstructorGen] Output: {RECONSTRUCTOR_SAMPLE_PATH}")
    total_samples = request_reconstructor_samples()
    write_txt(total_samples, mode="a")
    print(
        f"[ReconstructorGen] Done. Wrote {len(total_samples)} samples to "
        f"{RECONSTRUCTOR_SAMPLE_PATH}."
    )


if __name__ == "__main__":
    main()
