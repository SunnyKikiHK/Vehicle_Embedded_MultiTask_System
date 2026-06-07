"""Vehicle Voice Assistant Workflow - LangGraph-based multi-task processing."""

import os
import asyncio
import logging
import time
from langgraph.func import entrypoint, task
from typing import TypedDict

from src.utils import get_llm, format_history
from src.agent.agent import Agent
from src.agent.executor import get_executor
from src.llm.chat import chill_chat, chill_chat_stream
from src.llm.classifier import classify
from src.llm.answer_builder import quick_reconstruct, quick_reconstruct_stream
from src.llm.reconstructor import reconstruct
from src.llm.router import route
from src.schema.router_output import RouterOutput
from src.schema.reconstructor_output import ReconstructorOutput
from src.schema.agent_response_schema import AgentToolDecision
from src.schema.classifier_output import ClassifierOutput, QueryType
from src.schema.response_output import ResponseOutput

ARK_API_BASE = os.getenv("ARK_API_BASE")
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_MODEL_MINI = os.getenv("ARK_MODEL_MINI")
ARK_MODEL_LITE = os.getenv("ARK_MODEL_LITE")

QWEN_MODEL = os.getenv("QWEN_MODEL")
QWEN_BASE = os.getenv("QWEN_BASE")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

extra_body_doubao = {
    "thinking": {
        "type": "disabled"
    }
}

responsive_tools_qwen = [
    {"type": "web_search"}
    # {"type": "web_extractor"}
]

extra_body_qwen = {
    "tools": responsive_tools_qwen,
    "enable_thinking": True
}


logger = logging.getLogger(__name__)

class WorkflowInputSchema(TypedDict):
    query: str
    user_id: str
    last_n_history: list[dict] | None
    history_turns: int
    stream_mode: bool
    metadata: dict | None
    react_mode: bool

@task
async def format_history_task(history: list[dict] | None) -> str:
    """Format conversation history as a string for use in prompts."""
    return format_history(history)

@task
async def classifier(query: str, history_str: str, history_turns: int) -> dict:
    """Classify the query as chill_chat (1), task_specific (2), or meaningless (3)."""
    structured_llm = get_llm(ARK_MODEL_MINI, ARK_API_BASE, ARK_API_KEY, ClassifierOutput, extra_body=extra_body_doubao)
    result = await classify(structured_llm, query, history_str, history_turns, use_fast_path=True)
    return {
        "query_type": result.query_type,
        "confidence": result.confidence,
        "reasoning": result.reasoning
    }


@task
async def reconstructor(query: str, history_str: str, history_turns: int) -> dict:
    """Reconstruct the query into a complete, unambiguous form."""
    structured_llm = get_llm(ARK_MODEL_MINI, ARK_API_BASE, ARK_API_KEY, ReconstructorOutput, extra_body=extra_body_doubao)
    result = await reconstruct(structured_llm, query, history_str, history_turns)
    return {
        "reconstructed_query": result.reconstructed_query,
        "reasoning": result.reasoning
    }


@task
async def router(reconstructed_query: str) -> dict:
    """Route the reconstructed query to the appropriate agent."""
    structured_llm = get_llm(ARK_MODEL_MINI, ARK_API_BASE, ARK_API_KEY, RouterOutput, extra_body=extra_body_doubao)
    result = await route(structured_llm, reconstructed_query, use_fast_path=True)
    return {
        "target_agent": result.target_agent,
        "confidence": result.confidence,
        "reasoning": result.reasoning
    }


@task
async def run_agent(
    target_agent: str,
    query: str,
    user_id: str,
    metadata: dict | None = None,
    react_mode: bool = False,
) -> dict:
    """
    Execute the agent with optional ReAct loop.

    Simple mode (react_mode=False):
        1. Agent loads skill definition (SKILL.md)
        2. LLM identifies intent + slots
        3. Call MCP tool with slots
        4. Return response

    ReAct mode (react_mode=True):
        1. Agent loads skill definition (SKILL.md)
        2. LLM reasons, picks a tool, and provides args
        3. Call MCP tool, feed result back into LLM context
        4. Repeat until LLM returns no tool_name or max_steps reached
        5. Return all tool results
    """
    executor = get_executor()

    async def mcp_call(tool_name: str, slots: dict) -> dict:
        """Wrapper to call MCP tool through executor."""
        return await executor.call_tool(tool_name, slots, user_id, metadata=metadata)

    agent = Agent(target_agent)
    tool_decision, tool_result_raw = await agent.run(
        query,
        get_llm(ARK_MODEL_LITE, ARK_API_BASE, ARK_API_KEY, AgentToolDecision, extra_body=extra_body_doubao),
        mcp_call,
        react_mode=react_mode,
    )

    if react_mode and isinstance(tool_result_raw, list):
        results = tool_result_raw
    else:
        results = [(tool_decision.tool_name, tool_result_raw)]

    first_result = results[0] if results else (None, None)

    return {
        "agent": target_agent,
        "react_mode": react_mode,
        "all_tool_results": results,
        "tool_result": first_result[1],
        "tool_name": first_result[0],
        "tool_args": tool_decision.tool_args,
    }


@task
async def build_response(tool_name: str, tool_args: dict, tool_result: dict, query: str) -> str:
    """Quick helper to get the server description for the given server name."""
    structured_llm = get_llm(ARK_MODEL_MINI, ARK_API_BASE, ARK_API_KEY, ResponseOutput, extra_body=extra_body_doubao)
    return await quick_reconstruct(
        tool_name,
        tool_args,
        tool_result,
        query,
        structured_llm,
    )


@task
async def build_response_stream(tool_name: str, tool_args: dict, tool_result: dict, query: str) -> str:
    """Build response with streaming support."""        
    llm = get_llm(ARK_MODEL_MINI, ARK_API_BASE, ARK_API_KEY, extra_body=extra_body_doubao)
    return await quick_reconstruct_stream(
        tool_name,
        tool_args,
        tool_result,
        query,
        llm,
    )


@task
async def chat(query: str) -> dict:
    """Handle chill chat queries (not yet implemented)."""
    return await chill_chat(query, get_llm(QWEN_MODEL, QWEN_BASE, QWEN_API_KEY, extra_body=extra_body_qwen, use_responses_api=True))

@task 
async def chat_stream(query: str) -> dict:
    return await chill_chat_stream(query, get_llm(QWEN_MODEL, QWEN_BASE, QWEN_API_KEY, extra_body=extra_body_qwen, use_responses_api=True))

@entrypoint()
async def workflow(
    input: WorkflowInputSchema
    ) -> dict:
    """
    Main workflow for processing user queries.

    Optimization: Uses keyword extraction for fast-path classification and routing
    to reduce LLM latency. Parallel execution where possible.

    Flow:
    1. Format history
    2. Fast classification check -> If meaningless, return early
    3. If task_specific:
       a. Reconstructor -> reconstructed_query
       b. Fast route check -> If confident, use fast route
       c. If not confident, LLM route
       d. Agent -> LLM identifies intent -> calls MCP -> returns response
    4. If chill_chat: handle with chill chat logic (TODO)
    """
    query = input["query"]
    user_id = input["user_id"]
    last_n_history = input["last_n_history"]
    history_turns = input["history_turns"]
    stream_mode = input.get("stream_mode", False)
    metadata = input.get("metadata", {})
    react_mode = input.get("react_mode", False)

    workflow_start = time.perf_counter()
    logger.info(f"[Workflow] Starting workflow for query: {query}, stream_mode: {stream_mode}")

    # Step 1: Format history
    t0 = time.perf_counter()
    history_str = await format_history_task(last_n_history)
    t1 = time.perf_counter()
    logger.info(f"[Timing] format_history_task: {(t1-t0)*1000:.2f}ms")

    # Step 2: Run classifier and reconstructor in parallel
    t0 = time.perf_counter()
    classifier_task = classifier(query, history_str=history_str, history_turns=history_turns)
    reconstructor_task = reconstructor(query, history_str=history_str, history_turns=history_turns)
    classifier_result, reconstructor_result = await asyncio.gather(classifier_task, reconstructor_task)
    t1 = time.perf_counter()

    logger.info(f"[Timing] classifier + reconstructor (parallel): {(t1-t0)*1000:.2f}ms")
    logger.info(f"[Workflow] Classifier result: {classifier_result}")
    logger.info(f"[Workflow] Reconstructor result: {reconstructor_result}")

    if classifier_result["query_type"] == QueryType.MEANINGLESS:
        workflow_end = time.perf_counter()
        logger.info(f"[Timing] Total workflow: {(workflow_end-workflow_start)*1000:.2f}ms")
        return {
            "status": "error",
            "response": "无法理解您的输入，请重新说一遍。",
            "classification": classifier_result,
            "reconstruction": reconstructor_result
        }

    elif classifier_result["query_type"] == QueryType.TASK_SPECIFIC:
        # Step 3a: Fast route check using extracted keywords
        reconstructed_query = reconstructor_result["reconstructed_query"]

        t0 = time.perf_counter()
        router_result = await router(reconstructed_query)
        t1 = time.perf_counter()
        logger.info(f"[Timing] router: {(t1-t0)*1000:.2f}ms")
        logger.info(f"[Workflow] Router result: {router_result}")

        result = {
            "classification": classifier_result,
            "reconstruction": reconstructor_result,
            "routing": router_result
        }

        # Step 3b: Execute on target agent
        if router_result["target_agent"] and router_result["confidence"] >= 0.6:
            t0 = time.perf_counter()
            metadata = input.get("metadata", {})
            agent_result = await run_agent(
                router_result["target_agent"],
                reconstructor_result["reconstructed_query"],
                user_id,
                metadata=metadata,
                react_mode=react_mode,
            )
            t1 = time.perf_counter()
            logger.info(f"[Timing] run_agent: {(t1-t0)*1000:.2f}ms")
            result["agent"] = agent_result
        elif router_result["confidence"] < 0.6:
            result["agent"] = {
                "status": "fail",
                "message": "请重新说一遍，因为您的要求可能不够清晰。"
            }
            result["response"] = "请重新说一遍，因为您的要求可能不够清晰。"
            return result
        else:
            result["agent"] = {
                "status": "fail",
                "message": "无法确定处理该请求的代理"
            }
            result["response"] = "无法确定处理该请求的代理"
            return result
        logger.info(f"[Workflow] Agent result: {result['agent']}")

        # Step 4: Create response
        t0 = time.perf_counter()
        if stream_mode:
            # Use streaming version for true token streaming
            result["response"] = await build_response_stream(
                agent_result["tool_name"],
                agent_result["tool_args"],
                agent_result["tool_result"],
                reconstructor_result["reconstructed_query"],
            )
        else:
            result["response"] = await build_response(
                agent_result["tool_name"],
                agent_result["tool_args"],
                agent_result["tool_result"],
                reconstructor_result["reconstructed_query"],
            )
        t1 = time.perf_counter()
        logger.info(f"[Timing] build_response: {(t1-t0)*1000:.2f}ms")
        logger.info(f"[Workflow] Result: {result}")

        workflow_end = time.perf_counter()
        logger.info(f"[Timing] Total workflow: {(workflow_end-workflow_start)*1000:.2f}ms")
        return result

    elif classifier_result["query_type"] == QueryType.CHILL_CHAT:
        t0 = time.perf_counter()
        if stream_mode:
            chill_chat_result = await chat_stream(
                reconstructor_result["reconstructed_query"]
                )
        else:
            chill_chat_result = await chat(
                reconstructor_result["reconstructed_query"]
                )
        t1 = time.perf_counter()
        logger.info(f"[Timing] chill_chat: {(t1-t0)*1000:.2f}ms")

        workflow_end = time.perf_counter()
        logger.info(f"[Timing] Total workflow: {(workflow_end-workflow_start)*1000:.2f}ms")
        return {
            "status": "success",
            "classification": classifier_result,
            "reconstruction": reconstructor_result,
            "chill_chat": chill_chat_result,
            "response": chill_chat_result["response"]
        }

    workflow_end = time.perf_counter()
    logger.info(f"[Timing] Total workflow: {(workflow_end-workflow_start)*1000:.2f}ms")
    return {
        "status": "error",
        "response": "未知错误，请重试。",
        "classification": classifier_result
    }


if __name__ == "__main__":
    async def main():
        test_queries = [
            "帮我导航到最近的加油站",
            "把空调调到24度",
            "asdfghjkl123"
        ]

        for q in test_queries:
            print(f"\n{'='*50}")
            print(f"Query: {q}")
            result = await workflow.ainvoke({"query": q, "user_id": "test-user", "last_n_history": None, "history_turns": 0})
            print(f"Result: {result}")

        # Cleanup
        await get_executor().cleanup()

    asyncio.run(main())
