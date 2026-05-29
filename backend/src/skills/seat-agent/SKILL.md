---
name: seat-agent
description: Implements Seat Agent intents in the vehicle embedded multi-task system. Handles all seat adjustments including position, heating, cooling, massage, and ventilation. Also controls steering wheel heating, rearview mirrors, and seat memory profiles. Use when the user mentions seat, adjust seat, seat heating, seat ventilation, seat massage, steering wheel, mirror, or seat position. Trigger terms: 座椅, 座位, 主驾, 副驾, 后排, 座椅加热, 座椅通风, 座椅按摩, 方向盘加热, 后视镜, 折叠, 展开.
---

# Seat Agent — Seat & Comfort Adjustment Skill

## Agent Overview

**Handles:** All seat adjustments including position, heating, cooling, massage, and ventilation. Also covers steering wheel heating and rearview mirror control.
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

### Seat Position Adjustment

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 座椅前后调整 | adjust_seat | `{"direction": "forward/backward", "position": "<Position>"}` | Adjust seat forward/backward |
| 座椅水平调整 | adjust_seat | `{"direction": "up/down", "position": "<Position>"}` | Adjust seat vertical height |

### Seat Heating

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开座椅加热 | seat_heating | `{"switch": "on", "position": "<Position>"}` | Turn on seat heating |
| 关闭座椅加热 | seat_heating | `{"switch": "off", "position": "<Position>"}` | Turn off seat heating |
| 调低座椅温度 | seat_heating | `{"level": <Number>, "direction": "down", "position": "<Position>"}` | Decrease seat heat level |
| 调高座椅温度 | seat_heating | `{"level": <Number>, "direction": "up", "position": "<Position>"}` | Increase seat heat level |
| 设置座椅温度 | seat_heating | `{"level": <Number>, "position": "<Position>"}` | Set seat temperature (1-3) |

### Seat Ventilation

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开座椅通风 | seat_ventilation | `{"switch": "on", "position": "<Position>"}` | Turn on seat ventilation |
| 关闭座椅通风 | seat_ventilation | `{"switch": "off", "position": "<Position>"}` | Turn off seat ventilation |
| 调低座椅通风 | seat_ventilation | `{"level": <Number>, "direction": "down", "position": "<Position>"}` | Decrease ventilation level |
| 调大座椅通风 | seat_ventilation | `{"level": <Number>, "direction": "up", "position": "<Position>"}` | Increase ventilation level |
| 设置座椅通风 | seat_ventilation | `{"level": <Number>, "position": "<Position>"}` | Set ventilation level (1-3) |

### Seat Massage

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开座椅按摩 | seat_massage | `{"switch": "on", "position": "<Position>"}` | Turn on seat massage |
| 关闭座椅按摩 | seat_massage | `{"switch": "off", "position": "<Position>"}` | Turn off seat massage |
| 调低座椅按摩 | seat_massage | `{"level": <Number>, "direction": "down", "position": "<Position>"}` | Decrease massage intensity |
| 调大座椅按摩 | seat_massage | `{"level": <Number>, "direction": "up", "position": "<Position>"}` | Increase massage intensity |
| 设置座椅按摩 | seat_massage | `{"level": <Number>, "position": "<Position>"}` | Set massage mode/intensity |

### Rearview Mirrors

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 展开后视镜 | adjust_seat | `{"target": "mirror", "action": "unfold"}` | Unfold side mirrors |
| 折叠后视镜 | adjust_seat | `{"target": "mirror", "action": "fold"}` | Fold side mirrors |

## Slot Resolution Rules

- **Position**: One of: `主驾`, `副驾`, `后排`, `后排左侧`, `后排右侧`, `全部`, `前排`, `后座`, `副驾后`, `主驾后`. Default to `主驾`
- **Number**: Heating/ventilation/massage level 1–3. Normalize to integer
- **Direction**: One of: `上`, `下`, `前`, `后`, `左上`, `右上`, `左下`, `右下`
- When **Position is omitted** and only driver is present, default to `主驾`
- When **adjusting comfort** without level, apply medium level (2 of 3)

## Implementation Checklist

When implementing a new Seat intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve Position to valid values, normalize level to 1-3, Direction
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
