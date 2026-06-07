"""Agent class - for skill-based task execution.

Supports two execution modes:
- Simple mode (react_mode=False, default): single-pass LLM → tool → return
- ReAct mode (react_mode=True): LLM → tool → retry once on failure/invalid decision → return
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Awaitable, Callable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.constants import AGENT_MAX_STEPS, SKILLS_ROOT
from src.schema.agent_response_schema import AgentToolDecision

logger = logging.getLogger(__name__)


MCPExecutorFunc = Callable[[str, dict[str, Any]], Awaitable[Any]]


def _is_valid_decision(decision: AgentToolDecision) -> bool:
    """Check if the LLM decision has a non-empty tool name."""
    return bool(decision.tool_name and decision.tool_name.strip())


def _is_success_result(result: Any) -> bool:
    """
    Check if a tool result signals success.
    - dict with 'success': True  → success
    - dict with 'status': 'success' or 0  → success
    - Any other value (including error dicts) → not success
    """
    if isinstance(result, dict):
        if result.get("success") is True:
            return True
        status = result.get("status", result.get("code"))
        if status in ("success", 0, "0", True):
            return True
        return False
    if isinstance(result, bool) and result:
        return True
    return False


class Agent:
    """
    Two execution modes:

    Simple mode (react_mode=False):
        1. Load skill definition (SKILL.md) for LLM context
        2. LLM identifies intent + extracts slots
        3. Call MCP tool with resolved arguments
        4. Return immediately

    ReAct mode (react_mode=True):
        1. Load skill definition (SKILL.md) for LLM context
        2. LLM identifies intent + extracts slots
        3. Call MCP tool
        4. If tool_name is invalid OR result signals failure → retry once with error context
        5. Return
    """

    def __init__(self, agent_name: str):
        """
        Initialize Agent with its skill definition.

        Args:
            agent_name: The agent name (e.g., "Navigation Agent").
        """
        self.agent_name = agent_name
        self.skill = self._load_skill()

    def _load_skill(self) -> str:
        """Load skill definition from SKILL.md file."""
        skill_path = Path(SKILLS_ROOT) / self.agent_name / "SKILL.md"

        if not skill_path.exists():
            logger.warning("[Agent] Skill not found: %s", skill_path)
            return ""

        try:
            return skill_path.read_text(encoding="utf-8")
        except Exception as exc:
            logger.error("[Agent] Failed to load skill: %s", exc)
            return ""

    async def _call_llm(
        self,
        messages: list,
        llm: Any,
        reflection_context: str = "",
    ) -> AgentToolDecision:
        """Call the LLM with structured output, optionally with a reflection prompt."""
        if reflection_context:
            messages = list(messages) + [
                HumanMessage(content=reflection_context),
            ]
        result: AgentToolDecision = await llm.ainvoke(messages)
        return result

    async def _run_simple(
        self,
        query: str,
        llm: Any,
        mcp_executor: MCPExecutorFunc,
    ) -> tuple[AgentToolDecision, Any]:
        """
        Simple single-pass execution: LLM → one tool call → return.
        """
        messages = [
            SystemMessage(content=self.skill),
            HumanMessage(content=query),
        ]
        decision: AgentToolDecision = await self._call_llm(messages, llm)

        if not decision.tool_name:
            logger.info("[Agent] No tool to call in simple mode")
            return decision, None

        tool_result = await mcp_executor(decision.tool_name, decision.tool_args or {})
        return decision, tool_result

    async def _run_react(
        self,
        query: str,
        llm: Any,
        mcp_executor: MCPExecutorFunc,
        max_steps: int = AGENT_MAX_STEPS,
    ) -> tuple[AgentToolDecision, Any]:
        """
        Lightweight ReAct: one tool call, retry once only on failure or invalid decision.

        Loop logic:
        - Attempt tool call
        - If tool_name invalid OR tool_result not successful → retry once
        - Otherwise → return immediately
        """
        messages = [
            SystemMessage(content=self.skill),
            HumanMessage(content=query),
        ]

        decision: AgentToolDecision | None = None
        tool_result: Any = None
        success_result: bool = False

        for attempt in range(1, max_steps + 1):
            decision = await self._call_llm(messages, llm)

            if not _is_valid_decision(decision):
                logger.info(
                    "[Agent] ReAct attempt %d: invalid tool_name '%s' — retrying",
                    attempt,
                    decision.tool_name,
                )
                continue

            try:
                tool_result = await mcp_executor(
                    decision.tool_name, decision.tool_args or {}
                )
            except Exception as exc:
                logger.warning(
                    "[Agent] Tool '%s' raised exception: %s",
                    decision.tool_name,
                    exc,
                )
                tool_result = {"success": False, "error": str(exc)}

            success_result = _is_success_result(tool_result)
            if not success_result:
                logger.info(
                    "[Agent] ReAct attempt %d: tool '%s' returned non-success — "
                    "retrying with context",
                    attempt,
                    decision.tool_name,
                )
                messages.extend(
                    [
                        AIMessage(
                            content=(
                                f"[TOOL CALL] {decision.tool_name}("
                                f"{decision.tool_args or {}}) → {tool_result}"
                            )
                        ),
                        HumanMessage(
                            content=(
                                "The tool call above returned a failure or unexpected result. "
                                "Please reconsider your decision and output a new tool_name "
                                "and tool_args, or set tool_name to empty if no tool is "
                                "appropriate."
                            )
                        ),
                    ]
                )
                continue

            break

        if decision is None:
            raise RuntimeError(
                "[Agent] ReAct: LLM returned no decision after max attempts"
            )

        logger.info(
            "[Agent] ReAct: final tool_name='%s', success=%s",
            decision.tool_name,
            success_result,
        )
        return decision, tool_result

    async def run(
        self,
        query: str,
        llm: Any,
        mcp_executor: MCPExecutorFunc,
        react_mode: bool = False,
        max_steps: int = AGENT_MAX_STEPS,
    ) -> tuple[AgentToolDecision, Any]:
        """
        Execute the agent.

        Args:
            query: The reconstructed query from router.
            llm: LangChain LLM with structured output.
            mcp_executor: Function to execute MCP tools: (tool_name, slots) -> result.
            react_mode: If False (default), use single-pass: LLM → one tool → return.
                        If True, use lightweight ReAct: tool → retry once on failure/invalid → return.
            max_steps: Max attempts in ReAct mode (default 2 = 1 initial + 1 retry).
                       Ignored when react_mode=False.

        Returns:
            Tuple of (AgentToolDecision, tool_result or None).
        """
        if react_mode:
            return await self._run_react(query, llm, mcp_executor, max_steps)
        return await self._run_simple(query, llm, mcp_executor)


def get_agent(agent_name: str) -> Agent:
    """Factory to get an Agent instance."""
    return Agent(agent_name)
