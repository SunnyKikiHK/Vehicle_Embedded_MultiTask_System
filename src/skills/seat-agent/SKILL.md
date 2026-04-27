---
name: seat-agent
description: Implements Seat Agent intents in the vehicle embedded multi-task system. Handles all seat adjustments including position, heating, cooling, massage, and ventilation. Also controls steering wheel heating, rearview mirrors, and seat memory profiles. Use when the user mentions seat, adjust seat, seat heating, seat ventilation, seat massage, steering wheel, mirror, or seat position. Trigger terms: 座椅, 座位, 主驾, 副驾, 后排, 座椅加热, 座椅通风, 座椅按摩, 方向盘加热, 后视镜, 折叠, 展开.
---

# Seat Agent — Seat & Comfort Adjustment Skill

## Agent Overview

**Handles:** All seat adjustments including position, heating, cooling, massage, and ventilation. Also covers steering wheel heating and rearview mirror control.
**Total intents: 26**
**Shared slot types:** `Position`, `Number`, `Ratio`, `Extreme`, `Direction`

## Core Intent Categories

### Seat Position Adjustment

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 座椅前后调整 | Adjust_Seat_Long | Direction | Adjust seat forward/backward |
| 座椅水平调整 | Adjust_Seat_Vert | Direction | Adjust seat vertical height |

### Seat Heating

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开座椅加热 | Open_Heated_Seat | Position | Turn on seat heating |
| 关闭座椅加热 | Close_Heated_Seat | Position | Turn off seat heating |
| 调低座椅温度 | Dec_Seat_Temperature | Position, Number, Ratio | Decrease seat heat level |
| 调高座椅温度 | Inc_Seat_Temperature | Position, Number, Ratio | Increase seat heat level |
| 设置座椅温度 | Set_Seat_Temperature | Position, Number, Ratio, Extreme | Set seat temperature |

### Seat Ventilation

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开座椅通风 | Open_Seat_Ventilation | Position | Turn on seat ventilation |
| 关闭座椅通风 | Close_Seat_Ventilation | Position | Turn off seat ventilation |
| 调低座椅通风 | Dec_Seat_Ventilation | Position, Number, Ratio | Decrease ventilation level |
| 调大座椅通风 | Inc_Seat_Ventilation | Position, Number, Ratio | Increase ventilation level |
| 设置座椅通风 | Set_Seat_Ventilation | Position, Number, Ratio, Extreme | Set ventilation level |

### Seat Massage

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开座椅按摩 | Open_Seat_Massage | Position | Turn on seat massage |
| 关闭座椅按摩 | Close_Seat_Massage | Position | Turn off seat massage |
| 调低座椅按摩 | Dec_Seat_Massage | Position, Number, Ratio | Decrease massage intensity |
| 调大座椅按摩 | Inc_Seat_Massage | Position, Number, Ratio | Increase massage intensity |
| 设置座椅按摩 | Set_Seat_Massage | Position, Number, Ratio, Extreme | Set massage mode/intensity |

### Steering Wheel Heating

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置方向盘温度 | Set_Steer_Temperature | Number, Ratio, Extreme | Set steering wheel heat |
| 调低方向盘温度 | Dec_Steer_Temperature | Number, Ratio | Decrease steering heat |
| 调高方向盘温度 | Inc_Steer_Temperature | Number, Ratio | Increase steering heat |
| 打开方向盘加热 | Open_Heated_Steer | — | Turn on steering wheel heat |
| 关闭方向盘加热 | Close_Heated_Steer | — | Turn off steering wheel heat |

### Rearview Mirrors

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开后视镜加热 | Open_Rearview_Mirror_Heating | — | Turn on mirror defogger |
| 关闭后视镜加热 | Close_Rearview_Mirror_Heating | — | Turn off mirror defogger |
| 展开后视镜 | Open_Rearview_Mirror | — | Unfold side mirrors |
| 折叠后视镜 | Close_Rearview_Mirror | — | Fold side mirrors |

## Slot Resolution Rules

- **Position**: Resolve to `主驾`, `副驾`, `后排`, `后排左侧`, `后排右侧`, `全部`. Default to `主驾` if not specified.
- **Number**: Heating/ventilation level 1–3, or temperature in °C. Normalize to integer.
- **Ratio**: Relative adjustment. Map `高` → +1, `低` → -1, `最高/最低` → max/min.
- **Extreme**: `最高` → level 3, `最低` → level 1, `最热/最冷` for temperature.
- **Direction**: For seat adjustment, `前` → forward, `后` → backward, `上` → raise, `下` → lower.
- When **Position is omitted** and only driver is present, default to `主驾`.
- When **adjusting comfort** without level, apply medium level (2 of 3).

## Implementation Checklist

When implementing a new Seat intent:

1. **Match the intent key** (e.g., `Open_Heated_Seat`) to the skill function.
2. **Resolve Position** — default to `主驾` if not specified.
3. **Resolve relative adjustments** (Ratio) against current seat state.
4. **Execute the action** via the vehicle CAN bus / seat control API.
5. **Confirm** with a natural response (e.g., "座椅加热已开启" or "主驾座椅通风调到2档").
6. **Save SlotContext** to Redis with `agent=Seat Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
加热开启: "主驾座椅加热已开启。"
加热关闭: "主驾座椅加热已关闭。"
通风开启: "主驾座椅通风已开启。"
按摩开启: "主驾座椅按摩已开启。"
方向盘加热: "方向盘加热已开启。"
后视镜展开: "后视镜已展开。"
后视镜折叠: "后视镜已折叠。"
后视镜加热: "后视镜加热已开启。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
