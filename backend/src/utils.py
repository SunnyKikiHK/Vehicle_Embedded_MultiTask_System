from multiprocessing import context
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

from src.prompts import (
    RECONSTRUCTOR_PROMPT, 
    ROUTER_PROMPT, 
    CLASSIFIER_PROMPT, 
    CHILL_CHAT_PROMPT
)
from src.skills.skill_loader import _SKILL_MANIFEST
from src.constants import (
    SERVER_USE, 
    AGENT_TO_SERVER, 
    DEFAULT_SERVER_URLS
)

def get_llm(
    model: str, 
    base_url: str, 
    api_key: str, 
    structured_output: BaseModel | None = None, 
    extra_body: dict = None,
    use_responses_api: bool = False,
    tools: list[dict] = None
):
    """Get a LangChain LLM instance."""
    if not model:
        raise ValueError(
            "model is None or empty — check that ARK_MODEL_MINI / ARK_MODEL_LITE "
            "environment variables are set and loaded."
        )
    llm = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        extra_body=extra_body,
        max_retries=3,
        timeout=10,
        use_responses_api=use_responses_api
    )
    if tools:
        llm = llm.bind_tools(tools)
    if structured_output:
        llm = llm.with_structured_output(structured_output)
    return llm


def build_reconstructor_prompt(
    conversation_history: str,
    current_query: str,
    history_turns: int = 3,
) -> str:
    """
    Build a query reconstruction prompt.

    Args:
        conversation_history: Formatted string of recent conversation turns.
        current_query: The raw user query to reconstruct.
        history_turns: Number of history turns included (for display).

    Returns:
        A fully formatted prompt string ready to be sent to the LLM.
    """
    return RECONSTRUCTOR_PROMPT.format(
        conversation_history=conversation_history,
        current_query=current_query,
        history_turns=history_turns,
    )


def build_routing_prompt(
    agent_definitions: str,
    agent_names: str,
    num_agents: int,
    current_query: str,
) -> str:
    """
    Build an agent routing prompt.

    Args:
        agent_definitions: Formatted string of all agent definitions (duty and keywords).
        agent_names: Comma-separated list of all agent names.
        num_agents: Total number of agents in the system.
        current_query: The reconstructed user query to route.

    Returns:
        A fully formatted prompt string ready to be sent to the LLM.
    """
    return ROUTER_PROMPT.format(
        agent_definitions=agent_definitions,
        agent_names=agent_names,
        num_agents=num_agents,
        current_query=current_query,
    )

def build_chat_prompt(query: str) -> str:
    """Build the chill chat prompt with query and history."""
    return CHILL_CHAT_PROMPT.format(
        query=query
    )

def format_history(contexts: list[dict] | None) -> str:
    """Format conversation history for the prompt."""
    if not contexts:
        return "(无历史记录)"

    lines = []
    for i, ctx in enumerate(reversed(contexts), start=1):
        lines.append(f"--- 轮次 {i} ---")
        lines.append(f"用户: {ctx['query']}")
        if ctx.get("intent"):
            lines.append(f"系统: 意图={ctx['intent']}")
        if ctx.get("slots"):
            lines.append(f"系统: 槽={ctx['slots']}")
        if ctx.get("response"):
            lines.append(f"系统: 响应={ctx['response']}")
        if ctx.get("metadata"):
            lines.append(f"系统: 元数据={ctx['metadata']}")
        lines.append("")

    return "\n".join(lines) if lines else "(无历史记录)"


def get_skill_agent_count() -> int:
    """Return the number of agents loaded from skill files."""
    return len(_SKILL_MANIFEST)


def build_classifier_prompt(
    query: str,
    conversation_history: str = "(无历史记录)",
) -> str:
    """
    Build a query classification prompt.

    Args:
        query: The user query to classify.
        conversation_history: Formatted string of recent conversation turns.

    Returns:
        A fully formatted prompt string ready to be sent to the LLM.
    """
    return CLASSIFIER_PROMPT.format(
        query=query,
        conversation_history=conversation_history,
    )

def get_enabled_servers() -> dict[str, str]:
    """
    Get the URLs of servers that should be connected based on SERVER_USE.
    
    Returns:
        Dict mapping server_name -> server_url for enabled servers only.
    """
    enabled_servers = {}
    for agent_name, is_enabled in SERVER_USE.items():
        if is_enabled:
            server_name = AGENT_TO_SERVER.get(agent_name)
            if server_name and server_name in DEFAULT_SERVER_URLS:
                enabled_servers[server_name] = DEFAULT_SERVER_URLS[server_name]
    return enabled_servers
