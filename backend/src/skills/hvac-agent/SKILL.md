---
name: hvac-agent
description: Implements HVAC (climate control) intents in the vehicle embedded multi-task system. Use when working on HVAC Agent skills, slot extraction, intent handling, or any code touching climate control, temperature, fan speed, defog, air circulation, or air quality. Trigger terms: HVAC, air conditioning, temperature, fan, defog, defrost, AC, heating, cooling, ventilation, purifier, recirculation.
---

# HVAC Agent — Climate Control Skill

## Agent Overview

**Handles:** Air conditioning, heating, defrosting, air quality, and ventilation systems.
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

### Power & Mode Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 关闭空调 | ac_off | `{}` | Turn off AC |
| 打开空调 | ac_on | `{}` | Turn on AC |
| 打开空调自动模式 | ac_auto | `{}` | Enable auto climate |
| 关闭空调自动模式 | ac_auto | `{"mode": "manual"}` | Disable auto mode |
| 打开空调同步模式 | sync_ac | `{"mode": "sync"}` | Sync all zones |
| 关闭空调同步模式 | sync_ac | `{"mode": "unsync"}` | Disable sync |
| 打开空调制冷 | set_ac_mode | `{"mode": "cooling"}` | Cooling mode |
| 关闭空调制冷 | set_ac_mode | `{"mode": "off"}` | Stop cooling |
| 打开空调制热 | set_ac_mode | `{"mode": "heating"}` | Heating mode |
| 关闭制热模式 | set_ac_mode | `{"mode": "off"}` | Stop heating |

### Temperature Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 降低空调温度 | set_temperature | `{"temperature": <Number>, "direction": "down"}` | Decrease temp |
| 调高空调温度 | set_temperature | `{"temperature": <Number>, "direction": "up"}` | Increase temp |
| 设置空调温度 | set_temperature | `{"temperature": <Number>}` | Set exact temp (°C) |

### Fan Speed Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 降低空调风力 | set_fan_speed | `{"level": <Number>, "direction": "down"}` | Decrease fan speed |
| 调高空调风力 | set_fan_speed | `{"level": <Number>, "direction": "up"}` | Increase fan speed |
| 设置空调风力 | set_fan_speed | `{"level": <Number>}` | Set fan speed (1-7) |

### Airflow Direction

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 设置空调风向 | set_ac_mode | `{"direction": "<Direction>"}` | Set airflow direction |
| 取消空调风向 | set_ac_mode | `{"direction": "auto"}` | Cancel wind direction |
| 打开自动风向 | set_ac_mode | `{"direction": "auto"}` | Auto airflow |
| 关闭自动风向 | set_ac_mode | `{"direction": "manual"}` | Disable auto airflow |

### Defog / Defrost

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开除雾 | defrost | `{"mode": "defog"}` | Enable defog |
| 关闭除雾 | defrost | `{"mode": "off"}` | Disable defog |
| 打开除霜 | defrost | `{"mode": "defrost"}` | Enable defrost |

### AC Compressor & Quick Modes

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开AC | ac_on | `{}` | Turn on A/C compressor |
| 关闭AC | ac_off | `{}` | Turn off A/C compressor |

## Slot Resolution Rules

- **Number**: Temperature in °C (typically 16-30), fan speed as 1–7 level
- **Direction**: One of: `上`, `下`, `左`, `右`, `前`, `后`, `左上`, `右上`, `左下`, `右下`, `上下`, `左右`, `前后`
- **Position**: One of: `主驾`, `副驾`, `后排`, `后排左侧`, `后排右侧`, `全部`, `前排`, `后座`. Default to `全部`
- When **Position is omitted** in a single-occupant vehicle, default to `主驾`

## Implementation Checklist

When implementing a new HVAC intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — normalize Temperature (16-30°C), fan speed (1-7), Direction, Position
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
