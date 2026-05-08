"""Vehicle Voice Assistant Workflow - LangGraph-based multi-task processing."""

import os
import asyncio
from langgraph.func import entrypoint, task

from src.utils import get_llm
from src.agent.agent import Agent
from src.agent.executor import get_executor
from src.db.redis_client import RedisClient
from src.llm.classifier import QueryClassifier
from src.llm.answer_builder import quick_reconstruct
from src.llm.reconstruction_router import ReconstructionRouter
from src.schema.router_output import RouterOutput
from src.schema.classifier_output import ClassifierOutput, QueryType


ARK_API_BASE = os.getenv("ARK_API_BASE")
ARK_API_KEY = os.getenv("ARK_API_KEY")




@task
async def classifier(query: str) -> ClassifierOutput:
    """Classify the query as chill_chat (1), task_specific (2), or meaningless (3)."""

    structured_llm = get_llm(ARK_API_BASE, ARK_API_KEY, ClassifierOutput)
    classifier_instance = QueryClassifier(structured_llm)
    return await classifier_instance.classify(query)


@task
async def router(query: str, sender_id: str) -> RouterOutput:
    """Route the query to the appropriate agent (reconstruct + route)."""
    structured_llm = get_llm(ARK_API_BASE, ARK_API_KEY, RouterOutput)
    router_instance = ReconstructionRouter(structured_llm)
    return await router_instance.route(query, sender_id)


@task
async def run_agent(target_agent: str, query: str, user_id: str) -> dict:
    """
    Run the ReAct loop for the target agent.

    Flow:
    1. Agent loads skill definition (SKILL.md)
    2. LLM identifies intent + slots
    3. Call MCP tool with slots
    4. Return response
    """
    executor = get_executor()

    async def mcp_call(tool_name: str, slots: dict) -> dict:
        """Wrapper to call MCP tool through executor."""
        return await executor.call_tool(tool_name, slots, user_id)

    agent = Agent(target_agent)
    # result should be a dict with success, response, tool_result, etc...
    result = await agent.run(query, get_llm(ARK_API_BASE, ARK_API_KEY), mcp_call)

    return {
        "agent": target_agent,
        "success": result.success,
        "response": result.response,
        "tool_result": result.tool_result,
    }

@task
async def build_response(tool_name: str, tool_args: dict, tool_result: dict, query: str, server_name: str) -> str:
    """Quick helper to get the server description for the given server name."""
    return await quick_reconstruct(
        tool_name,
        tool_args,
        tool_result,
        query,
        server_name,
        )

@task
async def chill_chat(query: str) -> dict:
    """Handle chill chat queries (not yet implemented)."""
    return {
        "status": "not_implemented",
        "message": "Chill chat handling is not yet implemented.",
        "query": query
    }


@entrypoint()
async def workflow(query: str, sender_id: str = "user_001") -> dict:
    """
    Main workflow for processing user queries.

    Flow:
    1. Classifier → QueryType (chill_chat / task_specific / meaningless)
    2. If task_specific:
       a. Router → target_agent + reconstructed_query
       b. Agent (ReAct) → LLM identifies intent → calls MCP → returns response
    3. If chill_chat: handle with chill chat logic (TODO)
    4. If meaningless: return error message
    """
    # Step 1: Classify
    classifier_result = await classifier(query)

    if classifier_result.query_type == QueryType.MEANINGLESS:
        return {
            "status": "error",
            "message": "无法理解您的输入，请重新说一遍。",
            "confidence": classifier_result.confidence,
            "query_type": int(classifier_result.query_type),
            "reasoning": classifier_result.reasoning
        }

    elif classifier_result.query_type == QueryType.TASK_SPECIFIC:
        # Step 2: Route
        router_result = await router(query, sender_id)

        response = {
            # "status": "success",
            # "query_type": int(classifier_result.query_type),
            # "classification": classifier_result.reasoning,
            # "routing": {
            #     "reconstructed_query": router_result.reconstructed_query,
            #     "target_agent": router_result.target_agent,
            #     "confidence": router_result.confidence,
            # }
        }

        # Step 3: Execute on target agent
        if router_result.target_agent:
            agent_result = await run_agent(
                router_result.target_agent,
                router_result.reconstructed_query,
                sender_id
            )
            response["agent"] = agent_result
        else:
            response["agent"] = {
                "success": False,
                "response": "无法确定处理该请求的代理"
            }

        # Step 4: Create response 
        response["message"] = await build_response(
            agent_result["tool_result"]["tool_name"],
            agent_result["tool_result"]["tool_args"],
            agent_result["tool_result"]["tool_result"],
            router_result.reconstructed_query,
            router_result.target_agent,
        )

        return response

    elif classifier_result.query_type == QueryType.CHILL_CHAT:

        
        return {
            "status": "success",
            "query_type": int(classifier_result.query_type),
            "reasoning": classifier_result.reasoning,
            "chill_chat": await chill_chat(query)
        }

    return {
        "status": "error",
        "message": "未知错误，请重试。",
        "query_type": int(classifier_result.query_type)
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
            result = await workflow.ainvoke({"query": q})
            print(f"Result: {result}")

        # Cleanup
        await get_executor().cleanup()

    asyncio.run(main())
