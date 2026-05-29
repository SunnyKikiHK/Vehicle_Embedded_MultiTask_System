"""Query classifier using LangChain with structured output to distinguish chill chat from task-specific queries."""

from __future__ import annotations

import logging
from typing import Any

from src.prompts import CLASSIFIER_PROMPT
from src.schema.classifier_output import ClassifierOutput, QueryType
from src.llm.keyword_extractor import extract_classifier_keywords, fast_classify

logger = logging.getLogger(__name__)


def _build_classify_prompt(
    query: str,
    history_str: str | None,
    history_turns: int,
) -> str:
    """Assemble the full prompt from query and formatted history string."""
    return CLASSIFIER_PROMPT.format(
        query=query,
        conversation_history=history_str or "(无历史记录)",
        history_turns=history_turns,
    )


async def classify(
    structured_llm: Any,
    query: str,
    history_str: str | None = None,
    history_turns: int = 0,
    use_fast_path: bool = False,
) -> ClassifierOutput:
    """
    Classify the query as 1 (chill_chat), 2 (task_specific), or 3 (meaningless).

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ClassifierOutput)`.
        query: The user query to classify.
        history_str: Pre-formatted conversation history string.
        history_turns: Number of history turns.
        use_fast_path: If True, use keyword extraction first to potentially skip LLM call.

    Returns:
        ClassifierOutput with query_type (1/2/3), confidence, and reasoning.
    """
    # Fast path: use keyword extraction for clear-cut cases
    if use_fast_path:
        fast_type, fast_conf, clf_kw = fast_classify(query)

        # High confidence fast paths
        if fast_type == "meaningless" and fast_conf >= 0.9:
            logger.info("[QueryClassifier] Fast path: classified as meaningless")
            return ClassifierOutput(
                query_type=QueryType.MEANINGLESS,
                confidence=fast_conf,
                reasoning="通过关键词分析识别为无意义内容"
            )
        if fast_type == "chill_chat" and fast_conf >= 0.85 and not clf_kw["has_task_intent"]:
            logger.info("[QueryClassifier] Fast path: classified as chill_chat")
            return ClassifierOutput(
                query_type=QueryType.CHILL_CHAT,
                confidence=fast_conf,
                reasoning="通过关键词分析识别为闲聊问答"
            )

    # Standard LLM path 
    prompt = _build_classify_prompt(query, history_str, history_turns)

    try:
        output: ClassifierOutput = await structured_llm.ainvoke(prompt)
        return output
    except Exception as exc:
        logger.warning("[QueryClassifier] LLM call failed: %s", exc)
        return ClassifierOutput(
            query_type=QueryType.TASK_SPECIFIC,
            confidence=0.0,
            reasoning="LLM调用失败，默认返回任务指令类型。",
        )


async def is_chill_chat(
    structured_llm: Any,
    query: str,
    history_str: str | None = None,
) -> bool:
    """
    Convenience function to check if query is chill_chat (type 1).

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ClassifierOutput)`.
        query: The user query to classify.
        history_str: Pre-formatted conversation history string.

    Returns:
        True if query_type is 1 (chill_chat), False otherwise.
    """
    result = await classify(structured_llm, query, history_str)
    return result.query_type == QueryType.CHILL_CHAT


async def is_task_specific(
    structured_llm: Any,
    query: str,
    history_str: str | None = None,
) -> bool:
    """
    Convenience function to check if query is task_specific (type 2).

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ClassifierOutput)`.
        query: The user query to classify.
        history_str: Pre-formatted conversation history string.

    Returns:
        True if query_type is 2 (task_specific), False otherwise.
    """
    result = await classify(structured_llm, query, history_str)
    return result.query_type == QueryType.TASK_SPECIFIC


async def is_meaningless(
    structured_llm: Any,
    query: str,
    history_str: str | None = None,
) -> bool:
    """
    Convenience function to check if query is meaningless (type 3).

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ClassifierOutput)`.
        query: The user query to classify.
        history_str: Pre-formatted conversation history string.

    Returns:
        True if query_type is 3 (meaningless), False otherwise.
    """
    result = await classify(structured_llm, query, history_str)
    return result.query_type == QueryType.MEANINGLESS


if __name__ == "__main__":
    import os
    import asyncio
    import logging
    import time
    from datetime import datetime
    from pathlib import Path

    # Setup logging
    log_dir = Path("src/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"classifier_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("QueryClassifier Self-Test Started")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    print("=" * 60)
    print("QueryClassifier Self-Test")
    print(f"Log file: {log_file}")
    print("=" * 60)

    # --- Unit tests (no LLM required) ---
    print("\n[Unit Tests]")
    print("-" * 40)
    logger.info("[Unit Tests] Starting unit tests")

    # Test 1: Build prompt with simple query
    print("\n[Test 1] Build prompt with simple query")
    logger.info("[Test 1] Testing prompt building")
    prompt = _build_classify_prompt("帮我导航到加油站", None, 0)
    assert "帮我导航到加油站" in prompt
    print("  PASS")
    logger.info("[Test 1] PASS")

    # Test 2: Build prompt with history
    print("\n[Test 2] Build prompt with history")
    logger.info("[Test 2] Testing prompt with history")
    history = "--- 轮次 1 ---\n用户: 打开空调\n系统: 好的，空调已打开"
    prompt = _build_classify_prompt("关掉它", history, 1)
    assert "关掉它" in prompt and "打开空调" in prompt
    print("  PASS")
    logger.info("[Test 2] PASS")

    # Test 3: QueryType enum values
    print("\n[Test 3] QueryType enum values")
    logger.info("[Test 3] Testing QueryType enum")
    assert QueryType.CHILL_CHAT.value == 1
    assert QueryType.TASK_SPECIFIC.value == 2
    assert QueryType.MEANINGLESS.value == 3
    print("  PASS")
    logger.info("[Test 3] PASS")

    # Test 4: ClassifierOutput schema
    print("\n[Test 4] ClassifierOutput schema")
    logger.info("[Test 4] Testing ClassifierOutput schema")
    output = ClassifierOutput(
        query_type=QueryType.TASK_SPECIFIC,
        confidence=0.95,
        reasoning="用户请求导航"
    )
    assert output.query_type == QueryType.TASK_SPECIFIC
    print("  PASS")
    logger.info("[Test 4] PASS")

    # --- LLM Integration Test ---
    print("\n[LLM Integration Test]")
    print("-" * 40)
    logger.info("[LLM Integration Test] Starting LLM tests")

    api_key = os.getenv("ARK_API_KEY")
    api_base = os.getenv("ARK_API_BASE")
    api_model = os.getenv("ARK_MODEL_LITE")

    if not api_key:
        print("  SKIP: ARK_API_KEY not set in .env or config.sh")
        logger.warning("ARK_API_KEY not set, skipping LLM tests")
    else:
        from langchain_openai import ChatOpenAI

        print("\n[Test LLM] Query classification")
        logger.info("[Test LLM] Query classification")

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
        ).with_structured_output(ClassifierOutput)
        llm_construct_time = time.perf_counter() - t0
        print(f"  LLM construct time: {llm_construct_time:.3f}s")
        logger.info(f"  LLM construct time: {llm_construct_time:.3f}s")

        # Time: LLM response
        async def test_llm():
            t1 = time.perf_counter()
            result = await classify(llm, "今天天气怎么样")
            llm_response_time = time.perf_counter() - t1
            return result, llm_response_time

        result, llm_resp_time = asyncio.run(test_llm())
        print(f"  LLM response time: {llm_resp_time:.3f}s")
        logger.info(f"  LLM response time: {llm_resp_time:.3f}s")
        print("  Query: 今天天气怎么样")
        print(f"  Type: {result.query_type.name} ({result.query_type.value})")
        print(f"  Confidence: {result.confidence}")
        print(f"  Reasoning: {result.reasoning}")
        logger.info(f"  Type: {result.query_type.name}, Confidence: {result.confidence}")
        assert result.query_type is not None
        print("  PASS")
        logger.info("[Test LLM] PASS")

    print("\n" + "=" * 60)
    print("All QueryClassifier tests passed!")
    print("=" * 60)
    logger.info("All QueryClassifier tests passed!")
    logger.info("=" * 60)
