"""Two-tier coreference resolver using LangChain for LLM-backed resolution."""

from __future__ import annotations

import logging
import re
import sys

from typing import Any
from pydantic import BaseModel, Field
from dataclasses import dataclass, field


from src.schema.shared_slot_schema import SlotContext, CoreferenceResolver

from src.prompts import (
    build_coreference_prompt,
    format_conversation_history,
    format_slot_definitions,
)

logger = logging.getLogger(__name__)


class CoreferenceOutput(BaseModel):
    """Structured output schema for LLM coreference resolution."""

    resolved_slots: dict[str, Any] = Field(
        default_factory=dict,
        description="Resolved slot key-value pairs from conversation context",
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of how each slot was resolved",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0",
    )

# Result dataclass
class CoreferenceResult:
    """Result of a coreference resolution attempt."""

    def __init__(
        self,
        resolved_slots: dict[str, Any] | None = None,
        reasoning: str = "",
        confidence: float = 1.0,
        source: str = "rule",
        raw: dict[str, Any] | None = None,
    ) -> None:
        self.resolved_slots = resolved_slots or {}
        self.reasoning = reasoning
        self.confidence = confidence
        self.source = source  # "rule" | "llm"
        self.raw = raw or {}

    def merged_with_current(self, current_slots: dict[str, Any]) -> dict[str, Any]:
        """
        Merge resolved slots (takes slots resolved from conversation context (Tier-1 rules or Tier-2 LLM))
        into current slots, filling in only missing keys.

        For example:

        Suppose the NLU pipeline extracts {"Ratio": "高一点"} from "再高一点". The context from the previous turn has {"Position": "主驾"}. After merging:
        result = {"Ratio": "高一点"}
        # self.resolved_slots = {"Position": "主驾"}
        # "Ratio" is already in result → skip
        # "Position" is not in result → add
        return {"Ratio": "高一点", "Position": "主驾"}
        """
        result = dict(current_slots)
        for key, value in self.resolved_slots.items():
            if key not in result:
                result[key] = value
        return result



# Tier-2: LLM Resolver
class LLMCoreferenceResolver:
    """
    Tier-2 of the two-tier coreference system.

    Wraps a chat model with structured output and uses it as a
    fallback when the rule-based resolver (Tier-1) cannot handle a query.

    Usage:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(CoreferenceOutput)
        resolver = LLMCoreferenceResolver(llm, schema)
        result = resolver.resolve("再高一点", history, current_slots)
    """

    def __init__(
        self,
        structured_llm: Any,
        slot_schema: Any,
        max_history_turns: int = 3,
    ) -> None:
        """
        Args:
            structured_llm: A llm model bound with .with_structured_output(CoreferenceOutput).
            slot_schema: A SharedSlotSchema instance for formatting slot definitions in the prompt.
            max_history_turns: Maximum conversation turns to include in the prompt. Default 3.
        """
        self._llm = structured_llm
        self._schema = slot_schema
        self._max_history = max_history_turns

    def resolve(
        self,
        current_query: str,
        conversation_history: list,
        current_slots: dict[str, Any],
    ) -> CoreferenceResult:
        """
        Resolve ambiguous references using the LLM.

        Args:
            current_query: Raw user query for the current turn.
            conversation_history: List of SlotContext objects from prior turns (most recent last).
            current_slots: Slots already extracted from the current query.

        Returns:
            CoreferenceResult with resolved slots, or an empty result on failure.
        """
        slot_def_str = format_slot_definitions(self._schema)
        history_str = format_conversation_history(conversation_history, self._max_history)

        prompt = build_coreference_prompt(
            slot_definitions=slot_def_str,
            conversation_history=history_str,
            current_query=current_query,
            history_turns=self._max_history,
        )

        try:
            output: CoreferenceOutput = self._llm.invoke(prompt)
            return CoreferenceResult(
                resolved_slots=output.resolved_slots,
                reasoning=output.reasoning,
                confidence=output.confidence,
                source="llm",
                raw=output.dict(),
            )
        except Exception as exc:
            logger.warning("[LLM Coreference] LLM call failed: %s", exc)
            return CoreferenceResult(source="llm", confidence=0.0)



# Two-Tier Resolver 
class TwoTierResolver:
    """
    Two-tier coreference resolver: rule-based (Tier-1) + LLM (Tier-2).

    Resolution flow:
        1. Tier-1 (CoreferenceResolver.resolve): fast dict lookup for known pronouns.
           Sub-millisecond, works offline. Handles: 它, 那个, 继续, 调高, 调低.
        2. Tier-2 (LLMCoreferenceResolver): LLM-powered for arbitrary references.
           Called only when Tier-1 returns None.
    """

    KNOWN_PRONOUNS = re.compile(
        r"\b(它|那个|继续|调高|调低|那|这个)\b"
    )

    def __init__(
        self,
        redis_client: Any,
        structured_llm: Any,
        slot_schema: Any,
    ) -> None:
        self._redis = redis_client
        self._tier1 = CoreferenceResolver(redis_client=redis_client)
        self._tier2 = LLMCoreferenceResolver(structured_llm, slot_schema)

    def resolve(
        self,
        sender_id: str,
        current_query: str,
        current_slots: dict[str, Any],
    ) -> CoreferenceResult:
        """
        Resolve coreferences in the current query.

        Args:
            sender_id: Unique user identifier (Redis key suffix).
            current_query: Raw user query.
            current_slots: Slots extracted from the current query.

        Returns:
            CoreferenceResult. resolved_slots contains extra slots from context.
        """
        pronoun = self._KNOWN_PRONOUNS.search(current_query)

        # Tier-1: rule-based
        tier1_result = self._tier1.resolve(
            pronoun=pronoun.group(0) if pronoun else None,
            sender_id=sender_id,
            current_slots=current_slots,
        )
        if tier1_result is not None:
            return CoreferenceResult(
                resolved_slots=tier1_result,
                reasoning="Rule-based resolution",
                confidence=1.0,
                source="rule",
            )

        # Tier-2: LLM fallback
        history = self._load_history(sender_id)
        return self._tier2.resolve(current_query, history, current_slots)

    def resolve_and_merge(
        self,
        sender_id: str,
        current_query: str,
        current_slots: dict[str, Any], # ???
    ) -> dict[str, Any]:
        """Convenience: resolve and merge resolved slots into current_slots."""
        result = self.resolve(sender_id, current_query, current_slots)
        return result.merged_with_current(current_slots)

    def _load_history(self, sender_id: str) -> list:
        history: list = []
        key_prefix = f"voice:last_service:{sender_id}"

        for i in range(3):
            raw = self._redis.get(f"{key_prefix}:history:{i}")
            if raw:
                try:
                    history.insert(0, SlotContext.from_redis_value(raw))
                except Exception:
                    pass
        return history


if __name__ == "__main__":
    print("coreference.py self-test")

    # Fake Redis so we never hit a real server.
    class FakeRedis:
        def __init__(self) -> None:
            self._store: dict[str, str] = {}

        def get(self, key: str) -> str | None:
            return self._store.get(key)

        def set(self, key: str, value: str, ex: int | None = None) -> None:
            self._store[key] = value

    fake_redis = FakeRedis()
    fake_redis.set(
        "voice:last_service:user_001:history:0",
        "HVAC Agent#调节温度#Temperature=22,Position=主驾#太热了，开点空调",
    )

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

    #  CoreferenceResult.merged_with_current 
    print("[CoreferenceResult.merged_with_current]")
    result = CoreferenceResult(resolved_slots={"Position": "主驾", "Temperature": "20"})
    merged = result.merged_with_current({"Ratio": "高一点"})
    check("Current slots preserved", "Ratio" in merged)
    check("Resolved slots fill gaps", "Position" in merged)
    check("Resolved slots fill gaps (2)", "Temperature" in merged)
    check("Resolved does not override current", merged.get("Ratio") == "高一点")
    check("Resolved fills missing key", merged.get("Position") == "主驾")

    #  Tier-1 with fake Redis 
    print("\n[Tier-1: CoreferenceResolver with fake Redis]")
    from src.schema.shared_slot_schema import CoreferenceResolver as Tier1Resolver

    tier1 = Tier1Resolver(redis_client=fake_redis)
    tier1_out = tier1.resolve(pronoun="它", sender_id="user_001", current_slots={})
    check("Tier-1 resolves pronoun to slot", tier1_out is not None and "Position" in tier1_out)
    check("Tier-1 returns None for unknown pronoun", tier1.resolve("未知词", "user_001", {}) is None)
    check("Tier-1 returns None when redis is None", Tier1Resolver(redis_client=None).resolve("它", "user_001", {}) is None)

    #  Tier-2 with mock LLM 
    print("\n[Tier-2: LLMCoreferenceResolver with mock LLM]")

    @dataclass
    class MockOutput:
        resolved_slots: dict[str, Any] = field(default_factory=dict)
        reasoning: str = "Mock reasoning"
        confidence: float = 0.9

        def dict(self) -> dict[str, Any]:
            return {
                "resolved_slots": self.resolved_slots,
                "reasoning": self.reasoning,
                "confidence": self.confidence,
            }

    class MockLLM:
        def invoke(self, prompt: str) -> MockOutput:
            # Pretend the LLM resolved a Temperature slot from context.
            return MockOutput(
                resolved_slots={"Temperature": "24"},
                reasoning="Inferred from previous HVAC turn",
                confidence=0.95,
            )

    from src.schema.shared_slot_schema import SharedSlotSchema

    schema = SharedSlotSchema()
    tier2 = LLMCoreferenceResolver(MockLLM(), schema, max_history_turns=3)
    history = [
        SlotContext.from_redis_value(
            "HVAC Agent#调节温度#Temperature=22,Position=主驾#太热了"
        )
    ]
    tier2_out = tier2.resolve("再高一点", history, {"Ratio": "高一点"})
    check("Tier-2 returns source=llm", tier2_out.source == "llm")
    check("Tier-2 resolved slots present", "Temperature" in tier2_out.resolved_slots)
    check("Tier-2 resolved to correct value", tier2_out.resolved_slots.get("Temperature") == "24")
    check("Tier-2 confidence in valid range", 0.0 <= tier2_out.confidence <= 1.0)
    check("Tier-2 raw dict populated", len(tier2_out.raw) > 0)

    #  TwoTierResolver end-to-end 
    print("\n[TwoTierResolver: end-to-end]")

    @dataclass
    class MockOutput2:
        resolved_slots: dict[str, Any] = field(default_factory=dict)
        reasoning: str = ""
        confidence: float = 0.8

        def dict(self) -> dict[str, Any]:
            return {
                "resolved_slots": self.resolved_slots,
                "reasoning": self.reasoning,
                "confidence": self.confidence,
            }

    class MockLLM2:
        def invoke(self, prompt: str) -> MockOutput2:
            return MockOutput2(resolved_slots={"Temperature": "26"})

    fake_redis2 = FakeRedis()
    fake_redis2.set(
        "voice:last_service:user_002:history:0",
        "HVAC Agent#调节温度#Temperature=22,Position=副驾#主驾太热了",
    )

    resolver = TwoTierResolver(
        redis_client=fake_redis2,
        structured_llm=MockLLM2(),
        slot_schema=schema,
    )

    # Case 1: Tier-1 fires on known pronoun
    r1 = resolver.resolve("user_002", "它", {"Ratio": "高一点"})
    check("TwoTier: pronoun triggers Tier-1", r1.source == "rule")
    check("TwoTier: Tier-1 resolves Position", r1.resolved_slots.get("Position") == "副驾")

    # Case 2: Tier-2 fires when no known pronoun
    r2 = resolver.resolve("user_002", "调高一点", {"Ratio": "高一点"})
    check("TwoTier: no pronoun triggers Tier-2", r2.source == "llm")
    check("TwoTier: Tier-2 resolved Temperature", r2.resolved_slots.get("Temperature") == "26")

    # Case 3: resolve_and_merge convenience
    merged = resolver.resolve_and_merge("user_002", "它", {"Ratio": "高一点"})
    check("resolve_and_merge: preserves current slots", "Ratio" in merged)
    check("resolve_and_merge: fills from context", "Position" in merged)

    #  Summary 
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*40}")
    sys.exit(0 if failed == 0 else 1)
