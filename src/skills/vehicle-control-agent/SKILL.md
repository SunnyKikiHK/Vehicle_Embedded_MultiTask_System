---
name: vehicle-control-agent
description: Implements Vehicle Control Agent intents in the vehicle embedded multi-task system. Handles physical vehicle components: windows, sunroof, trunk, wipers, headlights, fog lights, cameras, dashcam, driving mode, and engine stop/start. Use when the user mentions windows, sunroof, trunk, wipers, headlights, fog lights, camera, dashcam, driving mode, auto hold, or engine start/stop. Trigger terms: 车窗, 天窗, 遮阳帘, 后备箱, 雨刷, 大灯, 雾灯, 示宽灯, 摄像头, 行车记录仪, 驾驶模式, 自动驻车, 自动启停.
---

# Vehicle Control Agent — Physical Vehicle Components Skill

## Agent Overview

**Handles:** Physical vehicle components: windows, sunroof, trunk, wipers, headlights, fog lights, cameras, dashcam, driving mode, auto hold, and engine start/stop.
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

### Windows

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开车窗 | open_window | `{"position": "<Position>"}` | Open car windows |
| 关闭车窗 | close_window | `{"position": "<Position>"}` | Close car windows |
| 车窗上升 | window_up | `{"position": "<Position>"}` | Raise windows |
| 车窗下降 | window_down | `{"position": "<Position>"}` | Lower windows |
| 所有车窗上升 | window_all_up | `{}` | Raise all windows |
| 所有车窗下降 | window_all_down | `{}` | Lower all windows |

### Trunk

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开后备箱 | flash_lights | `{"action": "trunk_open"}` | Open trunk |
| 关闭后备箱 | flash_lights | `{"action": "trunk_close"}` | Close trunk |

### Wipers

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开雨刷器 | flash_lights | `{"action": "wiper_on"}` | Turn on wipers |
| 关闭雨刷器 | flash_lights | `{"action": "wiper_off"}` | Turn off wipers |

### Headlights

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开大灯 | set_headlights | `{"mode": "on"}` | Turn on headlights |
| 关闭大灯 | set_headlights | `{"mode": "off"}` | Turn off headlights |

### Cameras

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开环绕摄像 | open_camera | `{"type": "surround_view"}` | Turn on 360° camera |
| 关闭环绕摄像 | close_camera | `{"type": "surround_view"}` | Turn off 360° camera |
| 打开行车记录仪 | dashcam_view | `{"action": "start"}` | Turn on dashcam |
| 关闭行车记录仪 | dashcam_view | `{"action": "stop"}` | Turn off dashcam |
| 拍照 | screenshot | `{"type": "camera"}` | Take a photo |
| 开始录像 | record_video | `{"action": "start"}` | Start video recording |
| 停止录像 | record_video | `{"action": "stop"}` | Stop video recording |

### Driving & Engine

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开车门锁 | unlock_doors | `{}` | Unlock doors |
| 关闭车门锁 | lock_doors | `{}` | Lock doors |
| 打开引擎 | start_engine | `{}` | Start engine |
| 关闭引擎 | stop_engine | `{}` | Stop engine |
| 鸣笛 | honk_horn | `{}` | Honk horn |

## Slot Resolution Rules

- **Position**: One of: `主驾`, `副驾`, `后排左侧`, `后排右侧`, `后排`, `全部`, `前排`, `后座`. For window operations: `全部` means all windows
- Some intents (trunk, wipers, cameras) operate on the whole vehicle — Position slot is not used

## Safety Notes

- Window/sunroof operations may be restricted at high speed
- Trunk open/close may be restricted while driving (check vehicle state)
- Engine start/stop may require specific conditions (key present, brake pressed, etc.)

## Implementation Checklist

When implementing a new Vehicle Control intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve Position for window operations, check safety constraints
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
