import logging
from langchain_openai import ChatOpenAI
from langgraph.config import get_stream_writer

from src.utils import build_chat_prompt

logger = logging.getLogger(__name__)

async def chill_chat(query: str, llm: ChatOpenAI):
    try:
        response = await llm.ainvoke(build_chat_prompt(query))
        if isinstance(response.content, list) and len(response.content) > 0:
            content = response.content[0].get("text", "")
        elif isinstance(response.content, str) and response.content:
            content = response.content
        else:
            content = ""
        return {
            "status": "success",
            "response": content
        }
    except Exception as e:
        logger.warning(f"[Chill Chat] Error in chill_chat: {e}")
        return {
            "status": "error",
            "response": "服务器错误，请稍后重试。"
        }

async def chill_chat_stream(query: str, llm: ChatOpenAI):
    writer = get_stream_writer()
    accumulated = ""
    try:
        async for chunk in llm.astream(
            build_chat_prompt(query)
        ):
            if isinstance(chunk.content, list) and len(chunk.content) > 0:
                content = chunk.content[0].get("text", "")
                writer(content)
                accumulated += content
            elif isinstance(chunk.content, str) and chunk.content:
                writer(chunk.content)
                accumulated += chunk.content
        return {
            "status": "success",
            "response": accumulated
        }
    except Exception as e:
        logger.warning("[Chill Chat] Streaming LLM call failed: %s", e)
        return {
            "status": "error",
            "response": "服务器错误，请稍后重试。"
        }