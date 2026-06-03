import os
import json
import time
import random
import concurrent.futures
from tqdm import tqdm
from pathlib import Path
from openai import OpenAI
from pydantic import BaseModel, ValidationError

from src.constants import ROUTER_SAMPLE_PATH
from src.prompts import ROUTER_SAMPLES_PROMPT 


# Configuration 
_MAX_CONCURRENT_WORKERS = 20
_PER_SAMPLE_GENERATION = 100 # each llm generate 100 samples
_PER_SAMPLE_RESPONSE = 20 # generate 20 samples per call, but total 100 samples.

DEFAULT_MODEL_NAME = os.environ.get("QWEN_MODEL", "qwen3.5-flash")

ROUTER_SAMPLE_PATH = Path(ROUTER_SAMPLE_PATH)
ROUTER_SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

client = OpenAI(
    api_key=os.environ['QWEN_API_KEY'],
    base_url=os.environ['QWEN_BASE'],
    max_retries=5
)

class RouterSample(BaseModel):
    query: str  
    agent: str
    description: str

def call_llm_4_router_samples(num_queries: int = _PER_SAMPLE_RESPONSE, model_name: str = DEFAULT_MODEL_NAME, max_retry=5) -> list[RouterSample]:
    """
    Sends a request to the LLM to generate router samples.
    """
    existing_samples = []
    attempt = 0
    while len(existing_samples) < _PER_SAMPLE_GENERATION and attempt < max_retry:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": ROUTER_SAMPLES_PROMPT.format(num_queries=num_queries, existing_samples=existing_samples)}
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
                newest_samples = extract_router_samples(response.choices[0].message.content)
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


def extract_router_samples(raw_response: str) -> list[RouterSample]:
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
            validated.append(RouterSample.model_validate(item))
        except ValidationError:
            continue
    return validated

def request_router_samples(nums: int = 1000):
    """
    Processes a list of documents using multi-threading to generate router samples.
    """
    total_samples = []

    total_calls = (nums + _PER_SAMPLE_GENERATION - 1) // _PER_SAMPLE_GENERATION
    print(f"Starting to generate {nums} of samples in {total_calls} calls...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_WORKERS) as executor:
        # Submit tasks and map them to their unique IDs
        futures = [
            executor.submit(call_llm_4_router_samples, _PER_SAMPLE_RESPONSE) for _ in range(total_calls)
        ]

        # Process results as they complete
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Generating samples ..."):   
            samples_list = future.result()
            total_samples.extend(samples_list)

    return total_samples[:nums]

def write_txt(samples: list[RouterSample], mode='a'):
    if mode == "w" and ROUTER_SAMPLE_PATH.exists():
        ROUTER_SAMPLE_PATH.unlink()
    with ROUTER_SAMPLE_PATH.open(mode, encoding="utf-8") as f:
        for sample in samples:
            f.write(sample.model_dump_json() + "\n")
if __name__ == "__main__":
    total_samples = request_router_samples()
    write_txt(total_samples)
    print(f"Finish generating samples and write to {str(ROUTER_SAMPLE_PATH)}.")
