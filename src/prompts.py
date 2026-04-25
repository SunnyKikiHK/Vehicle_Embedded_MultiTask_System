from __future__ import annotations

# Coreference Resolution Prompt
COREFERENCE_PROMPT = """你是一个车载多任务系统的指代消解助手。你的任务是根据对话历史，将当前查询中的指代词/模糊引用解析为具体的槽位值。

## 可用的槽位类型（及其有效值）

以下是系统中所有可能的槽位类型及其有效值。如果某个槽位没有枚举限制，则接受任意合理的字符串值。

{slot_definitions}

## 对话历史（最近 {history_turns} 轮）

{conversation_history}

## 当前查询

{current_query}

## 输出格式

请以JSON格式输出，包含以下字段：
{{
    "resolved_slots": {{
        // 解析出的槽位名: 值
    }},
    "reasoning": "解析逻辑的简要说明（1-2句话）",
    "confidence": 0.0-1.0之间的置信度评分
}}

## 注意事项

1. 如果当前查询中没有指代词或模糊引用需要解析，resolved_slots 应为空对象 {{}}
2. 优先使用对话历史中的信息来解析指代
3. 如果无法确定指代对象，confidence 设置为较低值（如 0.3）
4. 槽位值应使用中文原文（如 "主驾"、"后排"），不要翻译
5. 只输出JSON，不要包含任何其他文字
"""


def build_coreference_prompt(
    slot_definitions: str,
    conversation_history: str,
    current_query: str,
    history_turns: int = 3,
) -> str:
    """
    Build a coreference resolution prompt with formatted context.

    Args:
        slot_definitions: Formatted string of all slot types and their valid values.
        conversation_history: The last N turns of conversation history.
        current_query: The current user query to resolve.
        history_turns: Number of history turns included (for display).

    Returns:
        A fully formatted prompt string ready to be sent to the LLM.
    """
    return COREFERENCE_PROMPT.format(
        slot_definitions=slot_definitions,
        conversation_history=conversation_history,
        current_query=current_query,
        history_turns=history_turns,
    )


def format_slot_definitions(schema) -> str:
    """
    Format slot definitions from a SharedSlotSchema instance into a readable string.

    Args:
        schema: A SharedSlotSchema instance.

    Returns:
        A multi-line string listing each slot type with its description and enum values.
    """
    lines = []
    for slot_type, defn in schema.slot_definitions.items():
        lines.append(f"- {slot_type}: {defn.get('description', 'N/A')}")
        enum = defn.get("enum")
        examples = defn.get("examples")
        if enum:
            lines.append(f"  有效值: {', '.join(enum)}")
        elif examples:
            lines.append(f"  示例: {', '.join(str(e) for e in examples)}")
        agents = defn.get("agents", [])
        if agents:
            lines.append(f"  所属代理: {', '.join(agents)}")
        lines.append("")
    return "\n".join(lines)


def format_conversation_history(contexts: list, max_turns: int = 3) -> str:
    """
    Format a list of SlotContext objects into a readable conversation history string.

    Args:
        contexts: List of SlotContext objects, most recent last.
        max_turns: Maximum number of turns to include.

    Returns:
        A formatted history string for the prompt.
    """
    if not contexts:
        return "(无历史记录)"

    turns = contexts[-max_turns:]
    lines = []
    for i, ctx in enumerate(turns, start=len(contexts) - len(turns) + 1):
        lines.append(f"--- 轮次 {i} ---")
        lines.append(f"代理: {ctx.agent}")
        lines.append(f"意图: {ctx.intent}")
        if ctx.raw_query:
            lines.append(f"用户原话: {ctx.raw_query}")
        if ctx.slots:
            slot_strs = [f"  {k}={v.resolved_value}" for k, v in ctx.slots.items()]
            lines.append("提取的槽位:\n" + "\n".join(slot_strs))
        else:
            lines.append("提取的槽位: (无)")
        lines.append("")
    return "\n".join(lines)
