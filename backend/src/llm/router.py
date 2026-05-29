"""Agent routing using LangChain with structured output."""

from __future__ import annotations

import logging
from typing import Any

from src.schema.router_output import RouterOutput
from src.utils import (
    build_routing_prompt,
    get_skill_agent_count,
)
from src.skills.skill_loader import (
    format_skill_descriptions,
    get_agent_names_from_skills,
)
from src.llm.keyword_extractor import fast_route

logger = logging.getLogger(__name__)


def _build_routing_prompt(
    reconstructed_query: str,
) -> str:
    """Assemble the full prompt from skill frontmatter."""
    agent_defs = format_skill_descriptions()
    agent_names = get_agent_names_from_skills()
    num_agents = get_skill_agent_count()

    return build_routing_prompt(
        agent_definitions=agent_defs,
        agent_names=agent_names,
        num_agents=num_agents,
        current_query=reconstructed_query,
    )


async def route(
    structured_llm: Any,
    reconstructed_query: str,
    use_fast_path: bool = False,
) -> RouterOutput:
    """
    Route the query to the appropriate agent.

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(RouterOutput)`.
        reconstructed_query: The reconstructed user query (complete and unambiguous).
        use_fast_path: If True, use keyword extraction first to potentially skip LLM call.

    Returns:
        RouterOutput with target_agent, reasoning, confidence.
    """
    # Fast path: use keyword extraction for clear-cut cases
    if use_fast_path:
        agent, confidence = fast_route(reconstructed_query)
        if agent and confidence >= 0.8:
            logger.info(f"[Router] Fast path: routed to {agent} (confidence={confidence:.2f})")
            return RouterOutput(
                target_agent=agent,
                reasoning="通过关键词分析快速路由",
                confidence=confidence,
            )

    # Standard LLM path
    prompt = _build_routing_prompt(reconstructed_query)

    try:
        output: RouterOutput = await structured_llm.ainvoke(prompt)
        return output
    except Exception as exc:
        logger.warning("[Router] LLM call failed: %s", exc)
        return RouterOutput(
            target_agent="navigation-agent",
            reasoning="LLM call failed; defaulting to navigation-agent.",
            confidence=0.0,
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
    log_file = log_dir / f"router_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("Router Self-Test Started")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    print("=" * 60)
    print("Router Self-Test")
    print(f"Log file: {log_file}")
    print("=" * 60)

    # --- Unit tests (no LLM required) ---
    print("\n[Unit Tests]")
    print("-" * 40)
    logger.info("[Unit Tests] Starting unit tests")

    # Test 1: Build prompt with simple query
    print("\n[Test 1] Build prompt with simple query")
    logger.info("[Test 1] Testing prompt building")
    prompt = _build_routing_prompt("帮我导航到加油站")
    assert "帮我导航到加油站" in prompt
    print("  PASS")
    logger.info("[Test 1] PASS")

    # Test 2: RouterOutput schema
    print("\n[Test 2] RouterOutput schema")
    logger.info("[Test 2] Testing RouterOutput schema")
    from src.schema.router_output import RouterOutput
    output = RouterOutput(
        target_agent="navigation-agent",
        reasoning="用户请求导航",
        confidence=0.98
    )
    assert output.target_agent == "navigation-agent"
    print("  PASS")
    logger.info("[Test 2] PASS")

    # Test 3: Get enabled skills
    print("\n[Test 3] Get enabled skills")
    logger.info("[Test 3] Testing skill loading")
    from src.skills.skill_loader import format_skill_descriptions, get_agent_names_from_skills
    desc = format_skill_descriptions()
    names = get_agent_names_from_skills()
    print(f"  Enabled agents: {names}")
    logger.info(f"  Enabled agents: {names}")
    assert len(desc) > 0
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
        print("\n[Test LLM] Agent routing")
        logger.info("[Test LLM] Agent routing")

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
        ).with_structured_output(RouterOutput)
        llm_construct_time = time.perf_counter() - t0
        print(f"  LLM construct time: {llm_construct_time:.3f}s")
        logger.info(f"  LLM construct time: {llm_construct_time:.3f}s")

        # Time: LLM response
        async def test_llm():
            t1 = time.perf_counter()
            result = await route(llm, "导航到加油站")
            llm_response_time = time.perf_counter() - t1
            return result, llm_response_time

        result, llm_resp_time = asyncio.run(test_llm())
        print(f"  LLM response time: {llm_resp_time:.3f}s")
        logger.info(f"  LLM response time: {llm_resp_time:.3f}s")
        print("  Query: 导航到加油站")
        print(f"  Target Agent: {result.target_agent}")
        print(f"  Confidence: {result.confidence}")
        logger.info(f"  Target: {result.target_agent}, Confidence: {result.confidence}")
        assert len(result.target_agent) > 0
        print("  PASS")
        logger.info("[Test LLM] PASS")

    print("\n" + "=" * 60)
    print("All Router tests passed!")
    print("=" * 60)
    logger.info("All Router tests passed!")
    logger.info("=" * 60)
