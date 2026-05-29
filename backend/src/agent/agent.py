"""Agent class - for skill-based task execution.

The agent uses a sequencial workflow:
1. Receive query from router
2. LLM identifies intent + extracts slots → returns function call
3. Call MCP tool with slots
4. Respond to user and exit loop
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Awaitable
from langchain_core.messages import SystemMessage, HumanMessage

from src.constants import SKILLS_ROOT
from src.schema.agent_response_schema import AgentToolDecision

logger = logging.getLogger(__name__)


# Type alias for MCP executor function
MCPExecutorFunc = Callable[[str, dict[str, Any]], Awaitable[Any]]


class Agent:
    """
    Flow:
    1. Load skill definition (SKILL.md) to provide context to LLM
    2. LLM identifies intent + extracts slots
    3. Call MCP tool with the slots
    4. Return response and exit
    """

    def __init__(self, agent_name: str):
        """
        Initialize Agent with its skill definition.

        Args:
            agent_name: The agent name (e.g., "Navigation Agent").
        """
        self.agent_name = agent_name
        self.skill = self._load_skill()

    # def _get_skill_slug(self, agent_name: str) -> str:
    #     """Convert agent name to skill slug."""
    #     for slug, name in _KNOWN.items():
    #         if name == agent_name:
    #             return slug
    #     base = agent_name.replace(" Agent", "").strip()
    #     parts = base.split()
    #     return "-".join(p.lower() for p in parts) + "-agent"

    def _load_skill(self) -> str:
        """Load skill definition from SKILL.md file."""
        #skill_slug = self._get_skill_slug(self.agent_name)
        skill_path = Path(SKILLS_ROOT) / self.agent_name / "SKILL.md"

        if not skill_path.exists():
            logger.warning("[Agent] Skill not found: %s", skill_path)
            return ""

        try:
            return skill_path.read_text(encoding="utf-8")
        except Exception as exc:
            logger.error("[Agent] Failed to load skill: %s", exc)
            return ""

    async def call_llm(self, query: str, llm: Any) -> AgentToolDecision:
        """Call the LLM to get intent and slots."""

        messages = [
            SystemMessage(content=self.skill),
            HumanMessage(content=query)
        ]
        
        # Use the LLM with structured output
        result: AgentToolDecision = await llm.ainvoke(messages)
        return result

    async def run(
        self,
        query: str,
        llm: Any,
        mcp_executor: MCPExecutorFunc,
    ) -> [AgentToolDecision, dict]:
        """
        Steps:
        1. Build prompt with skill context
        2. LLM returns intent + slots
        3. Call MCP tool
        4. LLM gets the tool result 
        5. LLM returns a friendly response to the user based on the tool result

        Args:
            query: The reconstructed query from router.
            llm: LangChain LLM with structured output.
            mcp_executor: Function to execute MCP tools: (tool_name, slots) -> result

        Returns:
            ExecutionResult with success status and response text.
        """
        # Step 1: LLM returns an structured output of AgentToolDecision
        response: AgentToolDecision = await self.call_llm(query, llm)

        # Step 2: Call MCP tool
        tool_result = await mcp_executor(response.tool_name, response.tool_args or {})

        # Step 3: Return the tool result
        return response, tool_result


def get_agent(agent_name: str) -> Agent:
    """Factory to get an Agent instance."""
    return Agent(agent_name)