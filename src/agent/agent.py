"""Agent class - for skill-based task execution.

The agent uses a sequencial workflow:
1. Receive query from router
2. LLM identifies intent + extracts slots → returns function call
3. Call MCP tool with slots
4. Respond to user and exit loop
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Awaitable

from src.prompts import AGENT_PROMPT
from src.skills.skill_loader import _KNOWN
from src.schema.agent_response_schema import AgentResponse, ActionType

logger = logging.getLogger(__name__)


@dataclass
class IntentCall:
    """Represents an intent call from the LLM: function name + arguments."""
    intent_key: str
    slots: dict[str, Any]


# Type alias for MCP executor function
MCPExecutorFunc = Callable[[str, dict[str, Any]], Awaitable[Any]]


class Agent:
    """
    Flow:
    1. Load skill definition (SKILL.md) to provide context to LLM
    2. LLM identifies intent + extracts slots
    3. Call MCP tool with the slots
    4. Return response and exit

    Usage:
        agent = Agent("Navigation Agent")

        async def mcp_call(tool_name: str, slots: dict) -> dict:
            return await executor.call_tool("Navigation Agent", tool_name, slots, "user_001")

        result = await agent.run(
            query="帮我导航到最近的加油站",
            llm=structured_llm,
            mcp_executor=mcp_call
        )
    """

    def __init__(self, agent_name: str):
        """
        Initialize Agent with its skill definition.

        Args:
            agent_name: The agent name (e.g., "Navigation Agent").
        """
        self.agent_name = agent_name
        self.skill_slug = self._agent_name_to_slug(agent_name)
        self.skill_dir = self._find_skill_dir()
        self.skill_md_path = self.skill_dir / "SKILL.md" if self.skill_dir else None
        self.skill = ""
        self._load_skill()

    def _agent_name_to_slug(self, agent_name: str) -> str:
        """Convert agent name to skill slug."""
        for slug, name in _KNOWN.items():
            if name == agent_name:
                return slug
        base = agent_name.replace(" Agent", "").strip()
        parts = base.split()
        return "-".join(p.lower() for p in parts) + "-agent"

    def _find_skill_dir(self) -> Path | None:
        """Find the skill directory for this agent."""
        skills_root = Path(__file__).parent.parent / "skills"
        if not skills_root.exists():
            return None
        for item in skills_root.iterdir():
            if item.is_dir() and item.name == self.skill_slug:
                return item
        return None

    def _load_skill(self) -> None:
        """Load intent definitions from SKILL.md."""
        if not self.skill_md_path or not self.skill_md_path.exists():
            logger.warning("[Agent] Skill not found: %s", self.skill_md_path)
            return

        try:
            self.skill = self.skill_md_path.read_text(encoding="utf-8")
        except Exception as exc:
            logger.error("[Agent] Failed to load skill: %s", exc)

    async def call_llm(self, query: str, llm: Any) -> AgentResponse:
        """Call the LLM to get intent and slots."""
        prompt = AGENT_PROMPT.format(
            skill=self.skill,
            query=query,
            agent_name=self.agent_name
        )
        
        # Use the LLM with structured output
        result = await llm.ainvoke(prompt)
        return result

    async def run(
        self,
        query: str,
        llm: Any,
        mcp_executor: MCPExecutorFunc,
    ) -> AgentResponse:
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
        # Step 1: LLM returns an structured output of AgentResponse
        response: AgentResponse = await self.call_llm(query, llm)

        # Step 2: Call MCP tool
        tool_result = await mcp_executor(response.tool_name, response.tool_args or {})

        # Step 3: Return the tool result
        return AgentResponse(
            success=True,
            response=str(tool_result),
            tool_name=response.tool_name,
            tool_args=response.tool_args,
            action_type=ActionType.MCP_CALL,
        )


def get_agent(agent_name: str) -> Agent:
    """Factory to get an Agent instance."""
    return Agent(agent_name)