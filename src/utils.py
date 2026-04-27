from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from src.prompts import ROUTER_PROMPT
from src.db.redis_client import RedisClient
from src.agent_schema.shared_slot_schema import SlotContext

from src.skills.skill_loader import (  
    format_skill_descriptions, # re-exported for reconstruction_router.py
    get_agent_names_from_skills,
    get_skill_manifest
)


def get_llm(base_url: str, api_key: str, structured_output: BaseModel) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
    ).with_structured_output(structured_output)


def load_history(sender_id: str, redis_client: RedisClient=None, max_history_turn=3) -> list[SlotContext]:
    """Load the last N turns of SlotContext from Redis."""
    if redis_client is None:
        return []
    key_prefix = "voice:last_service:{sender_id}"
    history: list[SlotContext] = []
    for i in range(max_history_turn):
        raw = redis_client.get(f"{key_prefix}:history:{i}")
        if raw:
            history.insert(0, SlotContext.from_redis_value(raw))


def build_router_prompt(
    agent_definitions: str,
    agent_names: str,
    num_agents: int,
    conversation_history: str,
    current_query: str,
    history_turns: int = 3,
) -> str:
    """
    Build a combined routing + query-reconstruction prompt.

    Args:
        agent_definitions: Formatted string of all agent definitions (duty and keywords).
        agent_names: Comma-separated list of all agent names.
        num_agents: Total number of agents in the system.
        conversation_history: Formatted string of recent conversation turns.
        current_query: The raw user query to analyze.
        history_turns: Number of history turns included (for display).

    Returns:
        A fully formatted prompt string ready to be sent to the LLM.
    """
    return ROUTER_PROMPT.format(
        agent_definitions=agent_definitions,
        agent_names=agent_names,
        num_agents=num_agents,
        conversation_history=conversation_history,
        current_query=current_query,
        history_turns=history_turns,
    )


def format_slot_definitions(schema) -> str:
    """
    Format slot definitions from a SharedSlotSchema instance into a readable string.

    Args:
        schema: A SharedSlotSchema instance.

    Returns:
        A multi-line string listing each slot type with its description and enum values.
    """
    lines = []
    for slot_type, defn in schema.slot_definitions.items():
        lines.append(f"- {slot_type}: {defn.get('description', 'N/A')}")
        enum = defn.get("enum")
        examples = defn.get("examples")
        if enum:
            lines.append(f"  有效值: {', '.join(enum)}")
        elif examples:
            lines.append(f"  示例: {', '.join(str(e) for e in examples)}")
        agents = defn.get("agents", [])
        if agents:
            lines.append(f"  所属代理: {', '.join(agents)}")
        lines.append("")
    return "\n".join(lines)


def format_conversation_history(contexts: list, max_turns: int = 3) -> str:
    """
    Format a list of SlotContext objects into a readable conversation history string.

    Args:
        contexts: List of SlotContext objects, most recent last.
        max_turns: Maximum number of turns to include.

    Returns:
        A formatted history string for the prompt.
    """
    if not contexts:
        return "(无历史记录)"

    turns = contexts[-max_turns:]
    lines = []
    for i, ctx in enumerate(turns, start=len(contexts) - len(turns) + 1):
        lines.append(f"--- 轮次 {i} ---")
        lines.append(f"代理: {ctx.agent}")
        lines.append(f"意图: {ctx.intent}")
        if ctx.raw_query:
            lines.append(f"用户原话: {ctx.raw_query}")
        if ctx.slots:
            slot_strs = [f"  {k}={v.resolved_value}" for k, v in ctx.slots.items()]
            lines.append("提取的槽位:\n" + "\n".join(slot_strs))
        else:
            lines.append("提取的槽位: (无)")
        lines.append("")
    return "\n".join(lines)


def get_skill_agent_count() -> int:
    """Return the number of agents loaded from skill files."""
    return len(get_skill_manifest())
