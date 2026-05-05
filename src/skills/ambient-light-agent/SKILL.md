---
name: ambient-light-agent
description: Implements Ambient Light Agent intents in the vehicle embedded multi-task system. Handles all cabin lighting: ambient lights, dashboard brightness, HUD, reading lights, and screen brightness. Use when the user mentions lights, brightness, ambient, HUD, dashboard, reading lamp, or any display/lighting adjustment. Trigger terms: 氛围灯, 亮度, 仪表盘, HUD, 阅读灯, 屏幕亮度, 调亮, 调暗, 氛围灯颜色, 氛围灯主题.
---

# Ambient Light Agent — Cabin Lighting Skill

## Agent Overview

**Handles:** All lighting inside the cabin: ambient lights, dashboard brightness, HUD, reading lights, and general screen brightness.
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

### Ambient Lights

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开氛围灯 | set_interior_lights | `{"switch": "on"}` | Turn on ambient lighting |
| 关闭氛围灯 | set_interior_lights | `{"switch": "off"}` | Turn off ambient lighting |
| 设置氛围灯颜色 | set_interior_lights | `{"color": "<Color>"}` | Set ambient light color |
| 调节氛围灯主题 | set_interior_lights | `{"theme": "<Theme>"}` | Set ambient light theme |
| 调低氛围灯亮度 | set_interior_lights | `{"level": "<Number>", "direction": "down"}` | Decrease ambient brightness |
| 调高氛围灯亮度 | set_interior_lights | `{"level": "<Number>", "direction": "up"}` | Increase ambient brightness |
| 设置氛围灯亮度 | set_interior_lights | `{"level": "<Number>"}` | Set ambient brightness (0-100) |
| 氛围灯自动模式 | set_interior_lights | `{"mode": "auto"}` | Enable auto ambient lighting |
| 关闭氛围灯自动模式 | set_interior_lights | `{"mode": "manual"}` | Disable auto ambient lighting |

### Dashboard

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 调暗仪表盘 | set_interior_lights | `{"target": "dashboard", "level": "<Number>", "direction": "down"}` | Dim dashboard |
| 调亮仪表盘 | set_interior_lights | `{"target": "dashboard", "level": "<Number>", "direction": "up"}` | Brighten dashboard |
| 仪表盘调到最暗 | set_interior_lights | `{"target": "dashboard", "level": 0}` | Minimum dashboard brightness |
| 仪表盘调到最亮 | set_interior_lights | `{"target": "dashboard", "level": 100}` | Maximum dashboard brightness |
| 设置仪表盘亮度 | set_interior_lights | `{"target": "dashboard", "level": "<Number>"}` | Set dashboard brightness (0-100) |

### HUD

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开HUD | hud_on | `{}` | Turn on HUD display |
| 关闭HUD | hud_off | `{}` | Turn off HUD display |
| HUD亮度调到指定值 | hud_brightness | `{"level": "<level>"}` | Set HUD brightness (1-5) |
| 调高HUD亮度 | hud_brightness | `{"direction": "up"}` | Increase HUD brightness |
| 调低HUD亮度 | hud_brightness | `{"direction": "down"}` | Decrease HUD brightness |
| 上下调节HUD位置 | hud_mode | `{"direction": "vertical", "position": "<Direction>"}` | Adjust HUD vertical position |
| 左右调节HUD位置 | hud_mode | `{"direction": "horizontal", "position": "<Direction>"}` | Adjust HUD horizontal position |

### Reading Lights

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开阅读灯 | set_reading_light | `{"switch": "on"}` | Turn on reading light |
| 关闭阅读灯 | set_reading_light | `{"switch": "off"}` | Turn off reading light |

## Slot Resolution Rules

- **Color**: One of: `红`, `绿`, `蓝`, `黄`, `紫`, `橙`, `粉`, `白`, `暖白`, `冷白`, `青色`, `棕色`, `自定义`
- **Theme**: One of: `浪漫`, `激情`, `清凉`, `温暖`, `科技`, `自然`, `星辰`, `霓虹`, `日落`, `森林`, `海洋`
- **Number**: Brightness level 0–100. Default to 50.
- **level (HUD)**: Integer 1–5
- **Direction**: One of: `上`, `下`, `左`, `右`, `前`, `后`, `左上`, `右上`, `左下`, `右下`
- When **Color is omitted**, apply default color or present a color picker.

## Implementation Checklist

When implementing a new Ambient Light intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — normalize Color/Theme to valid values, brightness to 0-100, Direction
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
