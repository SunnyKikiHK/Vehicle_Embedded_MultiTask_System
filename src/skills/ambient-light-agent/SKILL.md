---
name: ambient-light-agent
description: Implements Ambient Light Agent intents in the vehicle embedded multi-task system. Handles all cabin lighting: ambient lights, dashboard brightness, HUD, reading lights, and screen brightness. Use when the user mentions lights, brightness, ambient, HUD, dashboard, reading lamp, or any display/lighting adjustment. Trigger terms: 氛围灯, 亮度, 仪表盘, HUD, 阅读灯, 屏幕亮度, 调亮, 调暗, 氛围灯颜色, 氛围灯主题.
---

# Ambient Light Agent — Cabin Lighting Skill

## Agent Overview

**Handles:** All lighting inside the cabin: ambient lights, dashboard brightness, HUD, reading lights, and general screen brightness.
**Total intents: 30**
**Shared slot types:** `Color`, `Theme`, `Number`, `Ratio`, `Extreme`, `Direction`, `level`

## Core Intent Categories

### Ambient Lights

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开氛围灯 | Open_Env_Light | — | Turn on ambient lighting |
| 关闭氛围灯 | Close_Env_Light | — | Turn off ambient lighting |
| 设置氛围灯颜色 | Set_Env_Light_Color | Color | Set ambient light color |
| 调节氛围灯主题 | Set_Env_Light_Theme | Theme | Set ambient light theme |
| 调低氛围灯亮度 | Dec_Env_Light_Brightness | Number, Ratio | Decrease ambient brightness |
| 调高氛围灯亮度 | Inc_Env_Light_Brightness | Number, Ratio | Increase ambient brightness |
| 设置氛围灯亮度 | Set_Env_Light_Brightness | Number, Ratio, Extreme | Set ambient brightness |
| 氛围灯自动模式 | Open_Env_Light_Auto_Mode | — | Enable auto ambient lighting |
| 关闭氛围灯自动模式 | Close_Env_Light_Auto_Mode | — | Disable auto ambient lighting |

### Dashboard

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 调暗仪表盘 | Dec_DashBoard_Brightness | Number, Ratio | Dim dashboard |
| 调亮仪表盘 | Inc_DashBoard_Brightness | Number, Ratio | Brighten dashboard |
| 仪表盘调到最暗 | Set_DashBoard_Brightness_Min | — | Minimum dashboard brightness |
| 仪表盘调到最亮 | Set_DashBoard_Brightness_Max | — | Maximum dashboard brightness |
| 设置仪表盘亮度 | Set_DashBoard_Brightness | Number, Ratio | Set dashboard brightness level |

### Screen Brightness

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 亮度调低 | Dec_Brightness | Number, Ratio | Decrease screen brightness |
| 亮度调高 | Inc_Brightness | Number, Ratio | Increase screen brightness |
| 亮度调到最低 | Set_Brightness_Min | — | Minimum screen brightness |
| 亮度调到最高 | Set_Brightness_Max | — | Maximum screen brightness |
| 设置亮度 | Set_Brightness | Number, Ratio | Set screen brightness |

### HUD

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开HUD | Open_HUD | — | Turn on HUD display |
| 关闭HUD | Close_HUD | — | Turn off HUD display |
| HUD亮度调到指定值 | Adjust_Hud_Brightness | level | Set HUD brightness level |
| 调高HUD亮度 | Inc_HUD_Brightness | — | Increase HUD brightness |
| 调低HUD亮度 | Dec_HUD_Brightness | — | Decrease HUD brightness |
| 上下调节HUD位置 | Adjust_HUD_Vert | Direction | Adjust HUD vertical position |
| 左右调节HUD位置 | Adjust_HUD_Horizon | Direction | Adjust HUD horizontal position |

### Reading Lights

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开阅读灯 | Open_Reading_Light | — | Turn on reading light |
| 关闭阅读灯 | Close_Reading_Light | — | Turn off reading light |

## Slot Resolution Rules

- **Color**: Resolve to one of the predefined ambient light colors. Common: `红色`, `蓝色`, `绿色`, `紫色`, `橙色`, `白色`, `暖白`, `多色`.
- **Theme**: Resolve to a named ambient light theme preset. Common: `浪漫`, `科技`, `自然`, `运动`, `音乐随动`, `呼吸`.
- **Number**: Brightness level 1–100 (normalized). Default to 50.
- **Ratio**: Relative adjustment. Map `高` → +20%, `低` → -20%, `最高/最低` → 100/0.
- **Extreme**: `最高` → 100%, `最低` → 0%.
- **level**: HUD brightness as integer 1–5.
- **Direction**: For HUD position adjustment: `上/下` (vertical), `左/右` (horizontal).
- When **Color is omitted** with color intent, present a color picker or apply default color.

## Implementation Checklist

When implementing a new Ambient Light intent:

1. **Match the intent key** (e.g., `Set_Env_Light_Color`) to the skill function.
2. **Resolve slot values** — normalize Color/Theme to system values, brightness to percentage.
3. **Execute the action** via the vehicle lighting API.
4. **Confirm** with a natural response (e.g., "氛围灯已切换到蓝色" or "HUD亮度已调高").
5. **Save SlotContext** to Redis with `agent=Ambient Light Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
氛围灯开: "氛围灯已开启，当前颜色{color}。"
氛围灯关: "氛围灯已关闭。"
氛围灯颜色: "氛围灯已切换到{color}。"
氛围灯主题: "氛围灯主题已切换到{theme}。"
亮度调高: "亮度已调高，当前为{level}%。"
亮度调低: "亮度已调低，当前为{level}%。"
HUD开: "HUD已开启。"
HUD关: "HUD已关闭。"
阅读灯开: "阅读灯已开启。"
阅读灯关: "阅读灯已关闭。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
