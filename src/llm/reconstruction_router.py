"""Combined query reconstruction and agent routing using LangChain with structured output."""

from __future__ import annotations

import logging
from typing import Any

from src.schema.router_output import RouterOutput
from src.agent_schema.shared_slot_schema import SlotContext
from src.utils import (
    build_router_prompt,
    format_conversation_history,
    get_skill_agent_count,
)
from src.skills.skill_loader import (
    format_skill_descriptions, 
    get_agent_names_from_skills,
)

logger = logging.getLogger(__name__)

class ReconstructionRouter:
    """
    Combined query reconstruction and agent routing using a single LLM call.

    This class uses a llm model with structured output to:
    1. Reconstruct the raw query by resolving pronouns/ellipsis via conversation history
    2. Route the reconstructed query to the most appropriate agent

    Usage:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(RouterOutput)
        router = ReconstructionRouter(llm)

        result = router.route(
            current_query="关掉它",
            sender_id="user_001",
            conversation_history=[...],
        )
        print(result.reconstructed_query)  # "关掉空调"
        print(result.target_agent)          # "HVAC Agent"
    """

    MAX_HISTORY_TURNS: int = 3
    REDIS_KEY_PATTERN: str = "voice:last_service:{sender_id}"
    REDIS_TTL_SECONDS: int = 40

    def __init__(
        self,
        structured_llm: Any,
        redis_client: Any | None = None,
    ) -> None:
        """
        Args:
            structured_llm: A LangChain chat model bound with
                `.with_structured_output(RouterOutput)`.
            redis_client: Optional Redis client for loading conversation history.
        """
        self._llm = structured_llm
        self._redis = redis_client

    async def route(
        self,
        current_query: str,
        sender_id: str,
        conversation_history: list[SlotContext] | None = None,
    ) -> RouterOutput:
        """
        Reconstruct the query and route to the appropriate agent in a single call.

        Args:
            current_query: The raw user query for the current turn.
            sender_id: Unique user identifier (used for Redis history lookup).
            conversation_history: Explicit history list. If None, loaded from Redis.

        Returns:
            RouterOutput with reconstructed_query, target_agent, reasoning, confidence.
        """
        if conversation_history is None:
            conversation_history = self._load_history(sender_id)

        prompt = self._build_prompt(current_query, conversation_history)

        try:
            output: RouterOutput = await self._llm.ainvoke(prompt)
            return output
        except Exception as exc:
            logger.warning("[ReconstructionRouter] LLM call failed: %s", exc)
            return RouterOutput(
                reconstructed_query=current_query,
                target_agent="Info Query Agent",
                reasoning="LLM call failed; defaulting to Info Query Agent.",
                confidence=0.0,
            )

    def _build_prompt(
        self,
        current_query: str,
        conversation_history: list[SlotContext],
    ) -> str:
        """Assemble the full prompt from skill frontmatter and history."""
        agent_defs = format_skill_descriptions()
        agent_names = get_agent_names_from_skills()
        num_agents = get_skill_agent_count()
        history_str = format_conversation_history(
            conversation_history, self.MAX_HISTORY_TURNS
        )

        return build_router_prompt(
            agent_definitions=agent_defs,
            agent_names=agent_names,
            num_agents=num_agents,
            conversation_history=history_str,
            current_query=current_query,
            history_turns=self.MAX_HISTORY_TURNS,
        )

    def _load_history(self, sender_id: str) -> list[SlotContext]:
        """Load the last N turns of SlotContext from Redis."""
        if self._redis is None:
            return []

        history: list[SlotContext] = []
        key_prefix = self.REDIS_KEY_PATTERN.format(sender_id=sender_id)

        for i in range(self.MAX_HISTORY_TURNS):
            raw = self._redis.get(f"{key_prefix}:history:{i}")
            if raw:
                try:
                    history.insert(0, SlotContext.from_redis_value(raw))
                except Exception:
                    pass
        return history

if __name__ == "__main__":
    print("ReconstructionRouter self-test\n")

    class FakeRedis:
        def __init__(self) -> None:
            self._store: dict[str, str] = {}

        def get(self, key: str) -> str | None:
            return self._store.get(key)

        def set(self, key: str, value: str, ex: int | None = None) -> None:
            self._store[key] = value

    #  Mock LLM 
    class MockOutput:
        def __init__(
            self,
            reconstructed_query: str,
            target_agent: str,
            reasoning: str = "",
            confidence: float = 0.9,
        ) -> None:
            self.reconstructed_query = reconstructed_query
            self.target_agent = target_agent
            self.reasoning = reasoning
            self.confidence = confidence

        def dict(self) -> dict[str, Any]:
            return {
                "reconstructed_query": self.reconstructed_query,
                "target_agent": self.target_agent,
                "reasoning": self.reasoning,
                "confidence": self.confidence,
            }

    class MockLLM:

        def invoke(self, prompt: str) -> MockOutput:
            if "关掉它吧" in prompt:
                return MockOutput(
                    reconstructed_query="关掉空调",
                    target_agent="HVAC Agent",
                    reasoning="Query references HVAC context from history.",
                    confidence=0.95,
                )
            if "再高一点点" in prompt:
                return MockOutput(
                    reconstructed_query="把温度再调高一点",
                    target_agent="HVAC Agent",
                    reasoning="Relative temperature adjustment.",
                    confidence=0.9,
                )
            return MockOutput(
                reconstructed_query="播放歌曲",
                target_agent="Media Agent",
                reasoning="Simple media request.",
                confidence=0.8,
            )

    #  Tests 
    passed = 0
    failed = 0

    def check(label: str, condition: bool) -> None:
        global passed, failed
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {label}")
        if condition:
            passed += 1
        else:
            failed += 1

    fake_redis = FakeRedis()
    fake_redis.set(
        "voice:last_service:user_001:history:0",
        "HVAC Agent#调节温度#Temperature=22,Position=主驾#太热了，开点空调",
    )

    router = ReconstructionRouter(MockLLM(), redis_client=fake_redis)

    # Test 1: route with history
    result1 = router.route("关掉它吧", "user_001")
    print("[route with history]")
    check("reconstructed_query is non-empty", len(result1.reconstructed_query) > 0)
    check("target_agent is set", len(result1.target_agent) > 0)
    check("confidence in range", 0.0 <= result1.confidence <= 1.0)
    check("reasoning is non-empty", len(result1.reasoning) > 0)

    # Test 2: route with explicit history list
    explicit_history = [
        SlotContext.from_redis_value(
            "HVAC Agent#调节温度#Temperature=22,Position=主驾#太热了"
        )
    ]
    result2 = router.route("再高一点点", "user_001", conversation_history=explicit_history)
    print("\n[route with explicit history]")
    check("reconstructed_query is non-empty", len(result2.reconstructed_query) > 0)
    check("target_agent is HVAC Agent", result2.target_agent == "HVAC Agent")

    # Test 3: route without history (cold start)
    result3 = router.route("放首歌", "user_003", conversation_history=[])
    print("\n[route without history (cold start)]")
    check("still returns valid output", len(result3.reconstructed_query) > 0)
    check("defaults to Media Agent", result3.target_agent == "Media Agent")

    # Test 4: LLM failure falls back gracefully
    class FailingLLM:
        def invoke(self, prompt: str) -> MockOutput:
            raise RuntimeError("simulated LLM failure")

    router2 = ReconstructionRouter(FailingLLM(), redis_client=None)
    result4 = router2.route("随便什么都行", "user_999")
    print("\n[LLM failure fallback]")
    check("falls back to original query", result4.reconstructed_query == "随便什么都行")
    check("defaults to Info Query Agent", result4.target_agent == "Info Query Agent")
    check("confidence is 0.0", result4.confidence == 0.0)

    #  Summary 
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*40}")
    import sys

    sys.exit(0 if failed == 0 else 1)
