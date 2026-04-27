---
name: interaction-control-agent
description: Implements Interaction Control Agent intents in the vehicle embedded multi-task system. Handles general UI interaction: confirmations, cancellations, selections, help, and custom response words. Use when the user says confirm, cancel, select, help, response words, or any general interaction that doesn't fit a domain agent. Trigger terms: 确定, 取消, 选这个, 选第几个, 好的, 是, 不是, 帮助, 应答词, 怎么用.
---

# Interaction Control Agent — General UI Interaction Skill

## Agent Overview

**Handles:** General UI interaction: confirmations, cancellations, selections, help, and custom response words.
**Total intents: 10**
**No shared slot types required.**

## Core Intent Categories

### Confirmation & Cancellation

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 确定 | Confirm | — | Confirm current selection |
| 取消 | Cancel | — | Cancel current operation |

### Selection

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 列表选择 | List_Select | Index | Select from a numbered list |

### Simultaneous Actions

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 同时打开 | Open_Two_Both | — | Open two items simultaneously |
| 同时关闭 | Close_Two_Both | — | Close two items simultaneously |

### Help

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开帮助 | Open_Help | — | Open help center |
| 关闭帮助 | Close_Help | — | Close help center |

### Custom Response Words

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 询问修改应答词 | Ask_Answer_Words | — | Ask about custom response words |
| 修改为指定应答词 | Get_Answer | Response | Set a custom response phrase |
| 删除应答词 | Delete_Answer_Words | — | Delete custom response word |

## Slot Resolution Rules

- **Index**: For `List_Select`, the position number (1-based) of the item in the presented list. Default to 1.
- **Response**: Custom phrase the user wants to use as an affirmative response.
- When **user says a number** during a list presentation, treat as `List_Select`.
- When **user says "好的" / "是的"** after a confirmation prompt, treat as `Confirm`.

## Interaction Flow

### List Selection Flow
1. System presents a numbered list (e.g., "找到3个结果，请选择：1. 晴天 2. 七里香 3. 稻香")
2. User selects by number (`List_Select`) or by name
3. System confirms and executes the selection

### Confirmation Flow
1. System asks for confirmation ("确定要关闭空调吗？")
2. User confirms (`Confirm`) or cancels (`Cancel`)
3. System executes or aborts accordingly

### Custom Response Words Flow
1. User asks about or sets a custom response word
2. System validates (not a common phrase, not offensive)
3. System confirms and saves the custom word

## Implementation Checklist

When implementing a new Interaction Control intent:

1. **Match the intent key** (e.g., `Confirm`) to the skill function.
2. **Check current context** — what operation is pending confirmation or selection?
3. **Execute the interaction** based on current context.
4. **Confirm** with a natural response (e.g., "好的，已确认" or "已取消").
5. **Save SlotContext** to Redis with `agent=Interaction Control Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
确认: "好的，已确认。"
取消: "已取消。"
选择: "已选择第{index}项：{item}。"
帮助开: "帮助中心已打开，您可以使用语音助手查询各种功能的使用方法。"
应答词设置: "应答词已设置为{response}。您现在可以说'{response}'来确认操作。"
应答词删除: "应答词已删除。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
