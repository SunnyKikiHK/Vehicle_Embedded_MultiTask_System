"""Query reconstruction using LangChain with structured output."""

from __future__ import annotations

import logging
from typing import Any

from src.schema.reconstructor_output import ReconstructorOutput
from src.utils import build_reconstructor_prompt

logger = logging.getLogger(__name__)


def _build_reconstruct_prompt(
    current_query: str,
    history_str: str | None,
    history_turns: int,
) -> str:
    """Assemble the full prompt from formatted history string."""
    formatted_history = history_str or "(无历史记录)"

    return build_reconstructor_prompt(
        conversation_history=formatted_history,
        current_query=current_query,
        history_turns=history_turns,
    )


async def reconstruct(
    structured_llm: Any,
    current_query: str,
    history_str: str | None = None,
    history_turns: int = 0,
) -> ReconstructorOutput:
    """
    Reconstruct the query into a complete, unambiguous form.

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ReconstructorOutput)`.
        current_query: The raw user query for the current turn.
        history_str: Pre-formatted conversation history string.
        history_turns: Number of history turns for display in prompt.

    Returns:
        ReconstructorOutput with reconstructed_query and reasoning.
    """
    prompt = _build_reconstruct_prompt(current_query, history_str, history_turns)

    try:
        output: ReconstructorOutput = await structured_llm.ainvoke(prompt)
        return output
    except Exception as exc:
        logger.warning("[Reconstructor] LLM call failed: %s", exc)
        return ReconstructorOutput(
            reconstructed_query=current_query,
            reasoning="LLM call failed; returning original query.",
        )


if __name__ == "__main__":
    import asyncio
    import logging
    import os
    import time
    from datetime import datetime
    from pathlib import Path

    from langchain_openai import ChatOpenAI

    # Setup logging
    log_dir = Path("src/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"reconstructor_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Reconstructor Self-Test Started")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    print("=" * 60)
    print("Reconstructor Self-Test")
    print(f"Log file: {log_file}")
    print("=" * 60)

    # --- Unit tests (no LLM required) ---
    print("\n[Unit Tests]")
    print("-" * 40)
    logger.info("[Unit Tests] Starting unit tests")

    # Test 1: Build prompt with simple query
    print("\n[Test 1] Build prompt with simple query")
    logger.info("[Test 1] Testing prompt building")
    prompt = _build_reconstruct_prompt("帮我导航到加油站", None, 0)
    assert "帮我导航到加油站" in prompt
    print("  PASS")
    logger.info("[Test 1] PASS")

    # Test 2: Build prompt with history
    print("\n[Test 2] Build prompt with history")
    logger.info("[Test 2] Testing prompt with history")
    history = "--- 轮次 1 ---\n用户: 打开空调\n系统: 好的，空调已打开"
    prompt = _build_reconstruct_prompt("关掉它", history, 1)
    assert "关掉它" in prompt and "打开空调" in prompt
    print("  PASS")
    logger.info("[Test 2] PASS")

    # Test 3: ReconstructorOutput schema
    print("\n[Test 3] ReconstructorOutput schema")
    logger.info("[Test 3] Testing ReconstructorOutput schema")
    from src.schema.reconstructor_output import ReconstructorOutput
    output = ReconstructorOutput(
        reconstructed_query="导航到加油站",
        reasoning="用户请求导航"
    )
    assert output.reconstructed_query == "导航到加油站"
    print("  PASS")
    logger.info("[Test 3] PASS")

    # --- LLM Integration Test ---
    print("\n[LLM Integration Test]")
    print("-" * 40)
    logger.info("[LLM Integration Test] Starting LLM tests")

    api_key = os.getenv("ARK_API_KEY")
    api_base = os.getenv("ARK_API_BASE")
    api_model = os.getenv("ARK_MODEL_MINI")

    if not api_key:
        print("  SKIP: ARK_API_KEY not set in .env or config.sh")
        logger.warning("ARK_API_KEY not set, skipping LLM tests")
    else:
        print("\n[Test LLM] Query reconstruction")
        logger.info("[Test LLM] Query reconstruction")

        # Time: LLM construction
        t0 = time.perf_counter()
        llm = ChatOpenAI(
            model=api_model,
            api_key=api_key,
            base_url=api_base,
            temperature=0.9,
            extra_body={
                "thinking": {"type": "disabled"}
            }
        ).with_structured_output(ReconstructorOutput)
        llm_construct_time = time.perf_counter() - t0
        print(f"  LLM construct time: {llm_construct_time:.3f}s")
        logger.info(f"  LLM construct time: {llm_construct_time:.3f}s")

        # Test with anaphora reference
        async def test_llm():
            t1 = time.perf_counter()

            # Test with anaphora reference
            history = "--- 轮次 1 ---\n用户: 打开空调\n系统: 好的，空调已打开"
            result = await reconstruct(llm, "关掉它", history, 1)
            llm_response_time = time.perf_counter() - t1
            return result, llm_response_time

        result, llm_resp_time = asyncio.run(test_llm())
        print(f"  LLM response time: {llm_resp_time:.3f}s")
        logger.info(f"  LLM response time: {llm_resp_time:.3f}s")
        print(f"  Original Query: 关掉它")
        print(f"  Reconstructed: {result.reconstructed_query}")
        print(f"  Reasoning: {result.reasoning}")
        logger.info(f"  Reconstructed: {result.reconstructed_query}, Reasoning: {result.reasoning}")
        assert len(result.reconstructed_query) > 0
        print("  PASS")
        logger.info("[Test LLM] PASS")

    print("\n" + "=" * 60)
    print("All Reconstructor tests passed!")
    print("=" * 60)
    logger.info("All Reconstructor tests passed!")
    logger.info("=" * 60)
