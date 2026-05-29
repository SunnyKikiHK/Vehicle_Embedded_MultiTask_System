from pydantic import BaseModel, Field

class ResponseOutput(BaseModel):
    """
    Structured output schema for the answer builder LLM call.
    """

    response: str = Field(
        ..., description="The response based on the query and tool result, should be a natural, friendly response"
    )