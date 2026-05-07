from pydantic import BaseModel, Field 

class AgentResponse(BaseModel):
    reasoning: str = Field(..., description="The reasoning of calling the tool")
    tool_name: str = Field(default="", description="The name of the tool to execute")
    tool_args: dict = Field(default={}, description="The arguments to pass to the tool")
