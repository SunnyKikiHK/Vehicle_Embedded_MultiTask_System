from pydantic import BaseModel, Field


class RouterOutput(BaseModel):
    """
    Structured output schema for the agent routing LLM call.
    """

    target_agent: str = Field(
        description="The single most appropriate agent name for the query, "
        "chosen from the available agent list. Must follow format: <agent_type>-agent, "
        "e.g., ambient-light-agent, hvac-agent, navigation-agent."
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
