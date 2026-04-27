---
name: hvac-agent
description: Implements HVAC (climate control) intents in the vehicle embedded multi-task system. Use when working on HVAC Agent skills, slot extraction, intent handling, or any code touching climate control, temperature, fan speed, defog, air circulation, or air quality. Trigger terms: HVAC, air conditioning, temperature, fan, defog, defrost, AC, heating, cooling, ventilation, purifier, recirculation.
---

# HVAC Agent — Climate Control Skill

## Agent Overview

**Handles:** Air conditioning, heating, defrosting, air quality, and ventilation systems.
**Total intents: 43**
**Shared slot types:** `Position`, `Number`, `Ratio`, `Extreme`, `Direction`, `City`, `date`

## Core Intent Categories

### Power & Mode Control

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 关闭空调 | Close_Air_Condition | Position | Turn off AC |
| 打开空调 | Open_Air_Condition | Position | Turn on AC |
| 打开空调自动模式 | Open_Air_Condition_Auto_Mode | Position | Enable auto climate |
| 关闭空调自动模式 | Close_Air_Condition_Auto_Mode | Position | Disable auto mode |
| 打开空调同步模式 | Open_Air_Condition_Sync | Position | Sync all zones |
| 关闭空调同步模式 | Close_Air_Condition_Sync | Position | Disable sync |
| 打开空调制冷 | Open_Cooling | — | Cooling mode |
| 关闭空调制冷 | Close_Cooling | — | Stop cooling |
| 打开空调制热 | Open_Heating | — | Heating mode |
| 关闭制热模式 | Close_Heating | — | Stop heating |

### Temperature Control

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 降低空调温度 | Dec_Air_Condition_Temperature | Position, Number, Ratio | Decrease temp |
| 调高空调温度 | Inc_Air_Condition_Temperature | Position, Number, Ratio | Increase temp |
| 设置空调温度 | Set_Air_Condition_Temperature | Position, Number, Ratio, Extreme | Set exact temp |
| 温度比较 | Temp_Compare | City | Compare city temps |

### Fan Speed Control

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 降低空调风力 | Dec_Air_Condition_Wind | Position, Number, Ratio | Decrease fan speed |
| 调高空调风力 | Inc_Air_Condition_Wind | Position, Number, Ratio | Increase fan speed |
| 设置空调风力 | Set_Air_Condition_Wind | Position, Number, Ratio, Extreme | Set fan speed |

### Airflow Direction

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置空调风向 | Set_Wind_Direction | Direction | Set airflow direction |
| 取消空调风向 | Cancel_Wind_Direction | Direction | Cancel wind direction |
| 打开自动风向 | Open_Wind_Auto_Mode | — | Auto airflow |
| 关闭自动风向 | Close_Wind_Auto_Mode | — | Disable auto airflow |

### Defog / Defrost

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开除雾 | Open_Air_Condition_Defog | Position | Enable defog |
| 关闭除雾 | Close_Air_Condition_Defog | Position | Disable defog |

### AC Compressor & Quick Modes

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开AC | Open_AC | — | Turn on A/C compressor |
| 关闭AC | Close_AC | — | Turn off A/C compressor |
| 一键降温 | Open_Cooling_Instant | — | Instant max cooling |
| 关闭一键降温 | Close_Cooling_Instant | — | Cancel instant cool |
| 快速升温 | Open_Heating_Instant | — | Instant max heating |

### Air Quality & Circulation

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开空气净化器 | Open_Air_Cleaner | — | Turn on purifier |
| 关闭空气净化器 | Close_Air_Cleaner | — | Turn off purifier |
| 打开内循环 | Open_Internal_Circulation | — | Internal recirculation |
| 关闭内循环 | Close_Internal_Circulation | — | Stop recirculation |
| 打开外循环 | Open_External_Circulation | — | Fresh air mode |
| 关闭外循环 | Close_External_Circulation | — | Stop fresh air |

### Queries

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查询空气 | Ask_Air_Condition | location, date, smog, PM25 | Query air quality |
| 查询湿度 | Ask_Humidity | location, date | Query humidity |
| 查询风力 | Ask_Wind | location, date, level, direction | Query wind info |

## Slot Resolution Rules

- **Position**: Resolve to `主驾`, `副驾`, `后排`, `全部` (default: `全部`). When only one occupant is implied, infer from context.
- **Number**: Temperature in `°C`, fan speed as 1–7 level. Normalize to integer.
- **Ratio**: Relative adjustment. Map `高/高一点` → +2 steps, `中` → 0, `低/低一点` → -2, `最高/最低` → max/min.
- **Extreme**: `最热/最冷/最大/最小` maps to system limits.
- **Direction**: `上/下/左/右/前/后` for seat airflow; `上下/左右` for toggle.
- When **Position is omitted** in a single-occupant vehicle, default to `主驾`.
- When **Ratio is used alone** (e.g., "高一点"), apply relative step from current value.

## Implementation Checklist

When implementing a new HVAC intent:

1. **Match the intent key** (e.g., `Inc_Air_Condition_Temperature`) to the skill function.
2. **Extract slots** using the types above — validate enum values.
3. **Resolve relative adjustments** (Ratio) against current HVAC state before executing.
4. **Handle position inference**: if user says "太热了" without position, apply to `主驾` (or `全部` for dual-zone).
5. **Execute the action** via the vehicle CAN bus / HVAC service API.
6. **Confirm** with a natural language response (e.g., "空调已关闭", "温度已调到26度").
7. **Save SlotContext** to Redis with `agent=HVAC Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
打开:  "好的，已为您打开空调。"
关闭:  "好的，空调已关闭。"
调温:  "已将温度调整到{target}度。"
调风:  "已将风力调整为{level}档。"
除雾:  "已开启除雾模式。"
加热:  "已开启制热模式。"
制冷:  "已开启制冷模式。"
内循环: "已切换到内循环模式。"
外循环: "已切换到外循环模式。"
```

## Additional Resources

- Full intent table and skill metadata: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
