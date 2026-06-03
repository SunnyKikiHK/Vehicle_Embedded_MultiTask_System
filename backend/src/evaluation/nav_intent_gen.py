import os
import json
import time
import random
import concurrent.futures
from tqdm import tqdm
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from src.constants import NAV_INTENT_SAMPLE_PATH
from src.prompts import NAV_INTENT_SAMPLES_PROMPT


# Configuration
_MAX_CONCURRENT_WORKERS = 20
_PER_SAMPLE_GENERATION = 100
_PER_SAMPLE_RESPONSE = 20

DEFAULT_MODEL_NAME = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

NAV_INTENT_PATH = Path(NAV_INTENT_SAMPLE_PATH)
NAV_INTENT_PATH.parent.mkdir(parents=True, exist_ok=True)

client = OpenAI(
    api_key=os.environ['QWEN_API_KEY'],
    base_url=os.environ['QWEN_BASE']
)


class NavIntentSample(BaseModel):
    query: str
    intent: str
    description: str


def call_llm_4_nav_intent_samples(num_queries: int = _PER_SAMPLE_RESPONSE, model_name: str = DEFAULT_MODEL_NAME, max_retry=5) -> list[NavIntentSample]:
    """
    Sends a request to the LLM to generate nav intent samples.
    """
    existing_samples = []
    attempt = 0
    while len(existing_samples) < _PER_SAMPLE_GENERATION and attempt < max_retry:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": NAV_INTENT_SAMPLES_PROMPT.format(num_queries=num_queries, existing_samples=existing_samples)}
                ],
                top_p=0.9,
                temperature=0.9,
                extra_body={
                    "enable_thinking": False,
                    "repetition_penalty": 1.1,  
                    "seed": random.randint(0, 999999)  
                    },
                timeout=60,
            )

            if response.choices and len(response.choices) > 0:
                newest_samples = extract_nav_intent_samples(response.choices[0].message.content)
                if newest_samples:
                    existing_samples.extend(newest_samples)
                    attempt = 0
                else:
                    attempt += 1
                    continue
        except Exception as e:
            if attempt < max_retry-1:
                time.sleep(1)
                attempt += 1
            else:
                print(f"Error: {str(e)}")
                return []
    return existing_samples


def extract_nav_intent_samples(raw_response: str) -> list[NavIntentSample]:
    text = raw_response.strip()
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
        return []

    validated = []
    for item in raw_list:
        try:
            validated.append(NavIntentSample.model_validate(item))
        except ValidationError:
            continue
    return validated


def request_nav_intent_samples(nums: int = 1000):
    """
    Processes a list of documents using multi-threading to generate nav_intent samples.
    """
    total_samples = []

    total_calls = (nums + _PER_SAMPLE_GENERATION - 1) // _PER_SAMPLE_GENERATION
    print(f"Starting to generate {nums} of nav intent samples in {total_calls} calls...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_WORKERS) as executor:
        futures = [
            executor.submit(call_llm_4_nav_intent_samples, _PER_SAMPLE_RESPONSE) for _ in range(total_calls)
        ]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Generating nav intent samples ..."):
            samples_list = future.result()
            total_samples.extend(samples_list)

    return total_samples[:nums]


def write_txt(samples: list[NavIntentSample], mode='a'):
    if mode == "w" and NAV_INTENT_PATH.exists():
        NAV_INTENT_PATH.unlink()
    with NAV_INTENT_PATH.open(mode, encoding="utf-8") as f:
        for sample in samples:
            f.write(sample.model_dump_json() + "\n")


if __name__ == "__main__":
    total_samples = request_nav_intent_samples()
    write_txt(total_samples)
    print(f"Finish generating nav intent samples and write to {str(NAV_INTENT_PATH)}.")
