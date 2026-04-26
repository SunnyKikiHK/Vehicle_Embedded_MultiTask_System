import os
import uuid
from langchain_openai import ChatOpenAI
from langgraph.func import entrypoint, task 
from langgraph.checkpoint.memory import InMemorySaver 

from src.utils import get_llm
from src.schema.router_output import RouterOutput
from src.agent_schema.shared_slot_schema import SlotContext
from src.llm.reconstruction_router import ReconstructionRouter

ARK_API_BASE = os.getenv("ARK_API_BASE")
ARK_API_KEY = os.getenv("ARK_API_KEY")

@task 
def router(query: str, sender_id: str, conversation_history: list[SlotContext]) -> dict:
    structured_llm = get_llm(ARK_API_BASE, ARK_API_KEY, RouterOutput)
    router = ReconstructionRouter(structured_llm)
    result = router.route(query, sender_id, conversation_history)
    return {
        "reconstructed_query": result.reconstructed_query, 
        "target_agent": result.target_agent, 
        "confidence": result.confidence
    }

@task 
def arbitrator(query: str):
    return 

@entrypoint()
def workflow(query: str) -> str:
    arbitrator_result = arbitrator(query)

    # router_result = router(query, sender_id, conversation_history)



if __name__ == "__main__":
    pass