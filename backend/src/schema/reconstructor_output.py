from pydantic import BaseModel, Field


class ReconstructorOutput(BaseModel):
    """
    Structured output schema for the query reconstruction LLM call.
    """

    reconstructed_query: str = Field(
        description="The query rewritten into a complete, unambiguous form by resolving pronouns, "
        "ellipsis, and vague references using conversation history. "
        "If the original query is already complete and clear, return it unchanged."
    )
    reasoning: str = Field(
        default="",
        description="Brief explanation of the reconstruction decision (1-2 sentences).",
    )
