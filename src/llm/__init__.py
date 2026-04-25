"""LLM integration for vehicle multi-task system."""

from src.llm.coreference import (
    CoreferenceOutput,
    CoreferenceResult,
    LLMCoreferenceResolver,
    TwoTierResolver,
)

__all__ = [
    "CoreferenceOutput",
    "CoreferenceResult",
    "LLMCoreferenceResolver",
    "TwoTierResolver",
]
