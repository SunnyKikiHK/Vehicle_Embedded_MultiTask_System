"""Response reconstruction module - generates user-friendly responses from MCP tool results.

This module provides functionality to convert raw MCP tool execution results
into natural, conversational responses for the user. It uses an LLM to generate
human-readable outputs based on:
1. The original user query
2. The MCP server that was called
3. The tool that was executed
4. The raw tool result
"""

from __future__ import annotations

import logging
import os
from typing import Any

from langgraph.config import get_stream_writer

from src.prompts import ANSWER_PROMPT
from src.constants import TOOL_RESPONSE_TEMPLATES, TOOL_VARIABLE_MAPPING
from src.mcp.mapping import get_server_for_tool, get_server_description
from src.schema.response_output import ResponseOutput

logger = logging.getLogger(__name__)


def _try_template(tool_name: str, tool_result: dict[str, Any]) -> str | None:
    """
    Try to generate response from predefined templates.

    Args:
        tool_name: The name of the tool that was executed.
        tool_result: The result returned by the tool.

    Returns:
        A template-based response if matched, None otherwise.
    """
    template = TOOL_RESPONSE_TEMPLATES.get(tool_name)
    if not template:
        return None

    variable_names = TOOL_VARIABLE_MAPPING.get(tool_name, [])

    if not variable_names:
        return template

    try:
        # Extract variables from tool_result using the mapping
        format_kwargs = {}
        for var_name in variable_names:
            if var_name in tool_result:
                format_kwargs[var_name] = tool_result[var_name]
            else:
                return None

        return template.format(**format_kwargs)
    except (KeyError, TypeError):
        # Formatting failed, fallback to LLM
        return None


def _format_tool_result(result: Any) -> str:
    """Format tool result for the prompt."""
    if result is None:
        return "（无返回结果）"
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        return _format_dict(result)
    if isinstance(result, (list, tuple)):
        return "\n".join(f"- {item}" for item in result)
    return str(result)


def _format_dict(d: dict[str, Any]) -> str:
    """Format a dictionary for the prompt."""
    if not d:
        return "（无参数）"
    return "\n".join(f"- {k}: {v}" for k, v in d.items())


def _generate_fallback_response(tool_name: str, tool_result: dict[str, Any]) -> str:
    """
    Generate a simple fallback response when LLM fails.

    Args:
        tool_name: The name of the tool that was executed.
        tool_result: The result returned by the tool.

    Returns:
        A simple response string.
    """
    server_name = get_server_for_tool(tool_name)

    if server_name == "nav_server":
        if tool_name in ("go_poi", "go_home", "go_company"):
            return "好的，已为您设置好导航"
        return "好的，导航操作已完成"

    if server_name == "ac_server":
        return "好的，空调设置已完成"

    if server_name == "media_server":
        if tool_name == "play_media":
            return "好的，正在为您播放"
        if tool_name == "pause_media":
            return "好的，已暂停播放"
        return "好的，媒体操作已完成"

    if server_name == "map_server":
        return "好的，地图已更新"

    if server_name == "phone_server":
        return "好的，电话操作已完成"

    return "好的，已为您完成操作"


async def _reconstruct_with_llm(
    structured_llm: Any,
    query: str,
    server_description: str,
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: dict[str, Any],
) -> str:
    """
    Use LLM to generate a response from the tool result.

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ResponseOutput)`.
        query: The original user query.
        server_description: The description of the server.
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.

    Returns:
        An LLM-generated natural language response.
    """
    tool_result_str = _format_tool_result(tool_result)
    tool_args_str = _format_dict(tool_args)

    prompt = ANSWER_PROMPT.format(
        query=query,
        server_description=server_description,
        tool_name=tool_name,
        tool_args=tool_args_str,
        tool_result=tool_result_str
    )

    try:
        response: ResponseOutput = await structured_llm.ainvoke(prompt)
        return response.response
    except Exception as exc:
        logger.warning("[ResponseBuilder] LLM call failed: %s, using fallback response", exc)
        return _generate_fallback_response(tool_name, tool_result)


async def reconstruct(
    structured_llm: Any,
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: dict[str, Any],
    query: str = "",
    server_description: str = "",
) -> str:
    """
    Generate a friendly response based on the tool execution result.

    Args:
        structured_llm: A LangChain chat model bound with
            `.with_structured_output(ResponseOutput)`.
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.
        query: The original user query.
        server_description: The description of the server.

    Returns:
        A natural language response string for the user.
    """
    template_response = _try_template(tool_name, tool_result)
    if template_response:
        return template_response

    return await _reconstruct_with_llm(
        structured_llm,
        query,
        server_description,
        tool_name,
        tool_args,
        tool_result
    )


async def quick_reconstruct(
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: Any,
    query: str = "",
    llm: Any | None = None,
) -> str:
    """
    Quick helper to reconstruct a response.

    Args:
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.
        query: The original user query.
        llm: Optional LLM for complex reconstruction.

    Returns:
        A friendly response string.
    """
    server_description = get_server_description(get_server_for_tool(tool_name))

    # Try template first
    template = TOOL_RESPONSE_TEMPLATES.get(tool_name)
    if template:
        # Check if template has any placeholders
        has_placeholders = "{" in template and "}" in template
        if not has_placeholders:
            return template
        if isinstance(tool_result, dict):
            try:
                return template.format(**tool_result)
            except (KeyError, TypeError):
                pass

    # Return simple acknowledgment if no LLM provided
    if llm is None:
        return _generate_fallback_response(tool_name, tool_result)

    return await reconstruct(
        llm,
        tool_name,
        tool_args,
        tool_result,
        query,
        server_description,
    )


async def reconstruct_stream(
    llm: Any,
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: Any,
    query: str = "",
    server_description: str = "",
) -> str:
    """
    Generate a friendly response with streaming support.

    Args:
        llm: LangChain chat model (NOT bound with structured output for streaming)
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.
        query: The original user query.
        server_description: The description of the server.

    Returns:
        The complete response string.
    """
    writer = get_stream_writer()
    if tool_result is None:
        writer("不好意思，服务器出错了，请稍后再试")
        return "不好意思，服务器出错了，请稍后再试"

    # Try template first
    template_response = _try_template(tool_name, tool_result)
    if template_response:
        writer(template_response)
        return template_response

    # Build prompt
    tool_result_str = _format_tool_result(tool_result)
    tool_args_str = _format_dict(tool_args)
    prompt = ANSWER_PROMPT.format(
        query=query,
        server_description=server_description,
        tool_name=tool_name,
        tool_args=tool_args_str,
        tool_result=tool_result_str
    )

    # Stream tokens from LLM
    accumulated = ""
    try:
        async for chunk in llm.astream(prompt):
            if chunk.content:
                content = chunk.content
                accumulated += content
                writer(content)
        return accumulated
    except Exception as e:
        logger.warning("[ResponseBuilder] Streaming LLM call failed: %s, using fallback response", e)
        return _generate_fallback_response(tool_name, tool_result)


async def quick_reconstruct_stream(
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: Any,
    query: str = "",
    llm: Any | None = None,
) -> str:
    """
    Quick helper to reconstruct a response with streaming.

    Args:
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.
        query: The original user query.
        llm: LangChain chat model (NOT bound with structured output).

    Returns:
        A friendly response string.
    """
    if tool_result is None:
        return "不好意思，服务器出错了，请稍后再试"

    if llm is None:
        response = _generate_fallback_response(tool_name, tool_result)
        writer = get_stream_writer()
        writer(response)
        return response

    server_description = get_server_description(get_server_for_tool(tool_name))
    return await reconstruct_stream(
        llm,
        tool_name,
        tool_args,
        tool_result,
        query,
        server_description,
    )


if __name__ == "__main__":
    import asyncio
    import logging
    import time
    from datetime import datetime
    from pathlib import Path

    # Setup logging
    log_dir = Path("src/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"answer_builder_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    logger.info("ResponseBuilder Self-Test Started")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)

    print("=" * 60)
    print("ResponseBuilder Self-Test")
    print(f"Log file: {log_file}")
    print("=" * 60)

    # --- Unit tests (no LLM required) ---
    print("\n[Unit Tests]")
    print("-" * 40)
    logger.info("[Unit Tests] Starting unit tests")

    # Test 1: Template without placeholders
    print("\n[Test 1] Template without placeholders")
    logger.info("[Test 1] Testing template without placeholders")
    result = _try_template("ac_on", {})
    logger.info(f"  Result: {result}")
    assert result == "好的，空调已打开", f"Expected '好的，空调已打开', got {result}"
    print("  PASS")
    logger.info("[Test 1] PASS")

    # Test 2: Template with placeholders (all variables present)
    print("\n[Test 2] Template with placeholders (complete)")
    logger.info("[Test 2] Testing template with placeholders")
    result = _try_template("go_poi", {"destination": "加油站", "address": "北京市朝阳区"})
    logger.info(f"  Result: {result}")
    assert result == "好的，正在为您导航到 加油站，地址是 北京市朝阳区"
    print("  PASS")
    logger.info("[Test 2] PASS")

    # Test 3: Fallback response for nav_server
    print("\n[Test 3] Fallback response - nav_server")
    logger.info("[Test 3] Testing fallback response")
    result = _generate_fallback_response("go_poi", {})
    logger.info(f"  Result: {result}")
    assert result == "好的，已为您设置好导航"
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
        from langchain_openai import ChatOpenAI

        print("\n[Test LLM] LLM-based response reconstruction")
        logger.info("[Test LLM] LLM-based response reconstruction")

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
        ).with_structured_output(ResponseOutput)
        llm_construct_time = time.perf_counter() - t0
        print(f"  LLM construct time: {llm_construct_time:.3f}s")
        logger.info(f"  LLM construct time: {llm_construct_time:.3f}s")

        # Time: LLM response
        async def test_llm():
            t1 = time.perf_counter()
            result = await reconstruct(
                llm,
                tool_name="go_poi",
                tool_args={"destination": "加油站", "address": "北京市朝阳区"},
                tool_result={"destination": "加油站"},
                query="帮我导航到加油站",
            )
            llm_response_time = time.perf_counter() - t1
            return result, llm_response_time

        response, llm_resp_time = asyncio.run(test_llm())
        print(f"  LLM response time: {llm_resp_time:.3f}s")
        logger.info(f"  LLM response time: {llm_resp_time:.3f}s")
        print(f"  Response: {response}")
        logger.info(f"  Response: {response}")
        assert len(response) > 0, "LLM response should not be empty"
        print("  PASS")
        logger.info("[Test LLM] PASS")

    print("\n" + "=" * 60)
    print("All ResponseBuilder tests passed!")
    print("=" * 60)
    logger.info("All ResponseBuilder tests passed!")
    logger.info("=" * 60)
