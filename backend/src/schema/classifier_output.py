from pydantic import BaseModel, Field
from enum import IntEnum


class QueryType(IntEnum):
    """Query type enumeration with integer values."""
    CHILL_CHAT = 1       # 闲聊问答
    TASK_SPECIFIC = 2    # 任务指令
    MEANINGLESS = 3     # 无意义内容


class ClassifierOutput(BaseModel):
    """
    Structured output schema for the query classifier.
    """

    query_type: QueryType = Field(
        description="分类类型：1=闲聊问答，2=任务指令，3=无意义内容"
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="置信度评分，范围0.0-1.0",
    )
    reasoning: str = Field(
        default="",
        description="分类判断的简要说明（1-2句话）",
    )
