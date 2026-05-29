import os
import asyncio
from langchain_openai import ChatOpenAI

async def main():
    llm = ChatOpenAI(
        model=os.getenv("QWEN_MODEL"),
        api_key=os.getenv("QWEN_API_KEY"),
        base_url=os.getenv("QWEN_BASE"),
        use_responses_api=True,
        extra_body={
            "tools": [{"type": "web_search"}],
            "enable_thinking": True
            }
    )

    # This will trigger ReAct + web_search
    result = await llm.ainvoke(
        input="本周热门上映电影"
        #tools=[{"type": "web_search"}]
    )
    print(result.content)

    # async for chunk in llm.astream(
    #     input="Singapore weather now"
    #     #tools=[{"type": "web_search"}]
    # ):
    #     print(chunk.content)

if __name__ == "__main__":
    asyncio.run(main())
