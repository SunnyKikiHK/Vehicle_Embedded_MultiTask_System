from pydantic import BaseModel, Field

class RouterOutput(BaseModel):
    """
    Structured output schema for the combined routing + reconstruction LLM call.
    """

    reconstructed_query: str = Field(
        description="The query rewritten into a complete, unambiguous form by resolving pronouns, "
        "ellipsis, and vague references using conversation history. "
        "If the original query is already complete and clear, return it unchanged."
    )
    target_agent: str = Field(
        description="The single most appropriate agent name for the reconstructed query, "
        "chosen from the available agent list."
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of the routing decision (1-2 sentences).",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0.",
    )