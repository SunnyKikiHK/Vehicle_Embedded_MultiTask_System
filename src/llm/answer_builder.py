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
from typing import Any

from src.prompts import ANSWER_PROMPT 
from src.constants import TOOL_RESPONSE_TEMPLATES
from src.mcp.mapping import get_server_for_tool, get_server_description

logger = logging.getLogger(__name__)


class ResponseBuilder:
    """
    Reconstructs user-friendly responses from MCP tool execution results.

    This class uses an LLM to generate natural language responses based on:
    - The original user query
    - Which server/tool was executed
    - The raw tool result

    Usage:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-mini")
        reconstructor = ResponseBuilder(llm)

        context = ReconstructionContext(
            query="帮我导航到加油站",
            server_description="导航服务器 - 处理路线规划、POI搜索、交通信息",
            tool_name="go_poi",
            tool_args={"poi": "加油站", "city": "北京"},
            tool_result={"status": "success", "destination": "中石化加油站", "address": "朝阳区XX路"}
        )

        response = await reconstructor.reconstruct(context)
        print(response)  # "好的，正在为您导航到中石化加油站，地址是朝阳区XX路"
    """

    def __init__(self, llm: Any) -> None:
        """
        Initialize the reconstructor with an LLM.

        Args:
            llm: A LangChain chat model (with or without structured output).
        """
        self._llm = llm

    async def reconstruct(
        self, 
        tool_name: str, 
        tool_args: dict[str, Any],
        tool_result: dict[str, Any],
        query: str = "",
        server_description: str = "",
        ) -> str:
        """
        Generate a friendly response based on the tool execution result.

        Args:
            context: The reconstruction context containing query and tool info.

        Returns:
            A natural language response string for the user.
        """
        # Try template first for simple cases
        template_response = self._try_template(tool_name, tool_result)
        if template_response:
            return template_response

        # Use LLM for complex cases
        return await self._reconstruct_with_llm(
            query, 
            server_description, 
            tool_name, 
            tool_args,
            tool_result
            )

    def _try_template(self, tool_name: str, tool_result: dict[str, Any]) -> str | None:
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

        # Check if template has any placeholders
        has_placeholders = "{" in template and "}" in template

        if not has_placeholders:
            # Template without placeholders - return it directly
            return template

        try:
            result = tool_result
            if isinstance(result, dict):
                return template.format(**result)
            return None
        except (KeyError, TypeError):
            # Try safe format - replace only keys that exist in result
            if isinstance(tool_result, dict):
                safe_result = template
                for k, v in tool_result.items():
                    safe_result = safe_result.replace(f"{{{k}}}", str(v))
                # If no replacement happened, return None
                if safe_result == template:
                    return None
                return safe_result
            return None

    async def _reconstruct_with_llm(
            self, 
            query: str, 
            server_description: str, 
            tool_name: str, 
            tool_args: dict[str, Any], 
            tool_result: dict[str, Any]
        ) -> str:
        """
        Use LLM to generate a response from the tool result.

        Args:
            context: The reconstruction context.

        Returns:
            An LLM-generated natural language response.
        """
        tool_result_str = self._format_tool_result(tool_result)
        tool_args_str = self._format_dict(tool_args)

        prompt = ANSWER_PROMPT.format(
            query=query,
            server_description=server_description,
            tool_name=tool_name,
            tool_args=tool_args_str,
            tool_result=tool_result_str
        )

        try:
            if self._llm is None:
                raise AttributeError("LLM is None")
            response = await self._llm.ainvoke(prompt)
            # Handle both string and structured responses
            if hasattr(response, "content"):
                return response.content.strip()
            return str(response).strip()
        except Exception as exc:
            logger.warning("[ResponseBuilder] LLM call failed: %s", exc)
            return self._generate_fallback_response()

    def _format_tool_result(self, result: Any) -> str:
        """Format tool result for the prompt."""
        if result is None:
            return "（无返回结果）"
        if isinstance(result, str):
            return result
        if isinstance(result, dict):
            return self._format_dict(result)
        if isinstance(result, (list, tuple)):
            return "\n".join(f"- {item}" for item in result)
        return str(result)

    def _format_dict(self, d: dict[str, Any]) -> str:
        """Format a dictionary for the prompt."""
        if not d:
            return "（无参数）"
        return "\n".join(f"- {k}: {v}" for k, v in d.items())

    def _generate_fallback_response(self, tool_name: str, tool_result: dict[str, Any]) -> str:
        """
        Generate a simple fallback response when LLM fails.

        Args:
            context: The reconstruction context.

        Returns:
            A simple response string.
        """
        server_name = get_server_for_tool(tool_name)

        # Simple acknowledgment based on tool type
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


async def quick_reconstruct(
    tool_name: str,
    tool_args: dict[str, Any],
    tool_result: Any,
    query: str = "",
    server_description: str = "",
    llm: Any | None = None,
) -> str:
    """
    Quick helper to reconstruct a response without creating a class instance.

    Args:
        tool_name: The name of the tool that was executed.
        tool_args: The arguments passed to the tool.
        tool_result: The result returned by the tool.
        query: The original user query.
        server_description: The server description.
        llm: Optional LLM for complex reconstruction.

    Returns:
        A friendly response string.
    """
    server_name = get_server_for_tool(tool_name)
    server_description = get_server_description(server_name)


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
        reconstructor = ResponseBuilder(None)
        return reconstructor._generate_fallback_response(tool_name, tool_result)

    reconstructor = ResponseBuilder(llm)
    return await reconstructor.reconstruct(
        tool_name,
        tool_args,
        tool_result,
        query,
        server_description,
    )


if __name__ == "__main__":
    print("ResponseBuilder self-test\n")

    # Mock LLM for testing
    class MockLLM:
        async def ainvoke(self, prompt: str) -> str:
            # Simple mock response based on tool name
            if "go_poi" in prompt or "导航" in prompt:
                if "destination" in prompt:
                    return "好的，正在为您导航到目的地"
                return "好的，已为您设置好导航"
            if "空调" in prompt or "temperature" in prompt.lower():
                return "好的，空调温度已调整"
            if "播放" in prompt or "play" in prompt.lower():
                return "好的，正在为您播放"
            return "好的，操作已完成"

    # Mock context
    class MockContext:
        def __init__(self, tool_name: str, tool_args: dict, tool_result: Any):
            self.query = "测试查询"
            self.server_description = "Test Server"
            self.tool_name = tool_name
            self.tool_args = tool_args
            self.tool_result = tool_result

    passed = 0
    failed = 0

    def check(label: str, condition: bool) -> None:
        global passed, failed
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {label}")
        if condition:
            passed += 1
        else:
            failed += 1

    import asyncio

    async def run_tests():
        mock_llm = MockLLM()
        reconstructor = ResponseBuilder(mock_llm)

        # Test 1: Navigation with result
        print("[Test 1: Navigation with result]")
        ctx1 = MockContext(
            tool_name="go_poi",
            tool_args={"poi": "加油站"},
            tool_result={"status": "success", "destination": "中石化加油站"}
        )
        result1 = await reconstructor.reconstruct(ctx1)
        check("response is non-empty", len(result1) > 0)
        check("response contains confirmation", "好" in result1 or "已" in result1)

        # Test 2: Template matching
        print("\n[Test 2: Template matching]")
        ctx2 = MockContext(
            tool_name="open_nav",
            tool_args={},
            tool_result="导航已打开"
        )
        result2 = await reconstructor.reconstruct(ctx2)
        check("response matches template", "导航已打开" in result2)

        # Test 3: Fallback response
        print("\n[Test 3: Fallback response (no LLM)]")
        reconstructor_no_llm = ResponseBuilder(None)
        ctx3 = MockContext(
            tool_name="unknown_tool",
            tool_args={},
            tool_result={"status": "ok"}
        )
        result3 = reconstructor_no_llm._generate_fallback_response(ctx3)
        check("fallback is non-empty", len(result3) > 0)

        # Test 4: quick_reconstruct
        print("\n[Test 4: quick_reconstruct]")
        result4 = await quick_reconstruct(
            tool_name="nav_zoom_in",
            tool_args={},
            tool_result="地图已放大",
            query="放大地图",
        )
        check("quick_reconstruct returns template", "地图已放大" in result4)

        # Test 5: quick_reconstruct with LLM
        print("\n[Test 5: quick_reconstruct with LLM]")
        result5 = await quick_reconstruct(
            tool_name="custom_tool",
            tool_args={"value": 10},
            tool_result={"result": "success"},
            query="执行自定义操作",
            llm=mock_llm,
        )
        check("quick_reconstruct with LLM is non-empty", len(result5) > 0)

        # Summary
        print(f"\n{'=' * 40}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'=' * 40}")

    asyncio.run(run_tests())
