---
name: interaction-control-agent
description: Implements Interaction Control Agent intents in the vehicle embedded multi-task system. Handles general UI interaction: confirmations, cancellations, selections, help, and custom response words. Use when the user says confirm, cancel, select, help, response words, or any general interaction that doesn't fit a domain agent. Trigger terms: 确定, 取消, 选这个, 选第几个, 好的, 是, 不是, 帮助, 应答词, 怎么用.
---

# Interaction Control Agent — General UI Interaction Skill

## Agent Overview

**Handles:** General UI interaction: confirmations, cancellations, selections, help, and custom response words.
**Note:** Most of these intents are handled through UI interactions or notifications. This agent manages the conversational flow and state.

## Expected Output Format

The LLM should return a JSON object with the following structure:

```json
{
  "reasoning": "Brief explanation of why this tool was selected",
  "tool_name": "actual_mcp_tool_name",
  "arguments": {
    "slot_name_1": "slot_value_1",
    "slot_name_2": "slot_value_2",
    ...
  }
}
```

If no arguments are needed, use an empty object `{}`.

## Core Intent Categories

### Confirmation & Cancellation

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 确定 | show_notification | `{"title": "确认", "content": "操作已确认"}` | Confirm current selection |
| 取消 | show_notification | `{"title": "取消", "content": "操作已取消"}` | Cancel current operation |

### Selection

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 列表选择 | show_notification | `{"title": "选择", "content": "已选择第{index}项"}` | Select from a numbered list |

### Help

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开帮助 | show_notification | `{"title": "帮助", "content": "帮助中心已打开"}` | Open help center |
| 关闭帮助 | dismiss_notification | `{}` | Close help center |

## Interaction Flow

### List Selection Flow
1. System presents a numbered list
2. User selects by number or by name
3. System confirms and executes the selection

### Confirmation Flow
1. System asks for confirmation
2. User confirms or cancels
3. System executes or aborts accordingly

## Implementation Checklist

When implementing a new Interaction Control intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — check current context for pending operations
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
