---
name: vehicle-control-agent
description: Implements Vehicle Control Agent intents in the vehicle embedded multi-task system. Handles physical vehicle components: windows, sunroof, trunk, wipers, headlights, fog lights, cameras, dashcam, driving mode, and engine stop/start. Use when the user mentions windows, sunroof, trunk, wipers, headlights, fog lights, camera, dashcam, driving mode, auto hold, or engine start/stop. Trigger terms: 车窗, 天窗, 遮阳帘, 后备箱, 雨刷, 大灯, 雾灯, 示宽灯, 摄像头, 行车记录仪, 驾驶模式, 自动驻车, 自动启停.
---

# Vehicle Control Agent — Physical Vehicle Components Skill

## Agent Overview

**Handles:** Physical vehicle components: windows, sunroof, trunk, wipers, headlights, fog lights, cameras, dashcam, driving mode, auto hold, and engine start/stop.
**Total intents: 46**
**Shared slot types:** `Position`, `Ratio`, `Mode`, `Camera`, `Direction`

## Core Intent Categories

### Windows

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开车窗 | Open_Window | Position | Open car windows |
| 关闭车窗 | Close_Window | Position | Close car windows |
| 设置车窗 | Set_Window | Position, Ratio | Set window to specific position |
| 打开通风模式 | Open_Window_Diagonal | — | Open windows in diagonal mode |
| 关闭通风模式 | Close_Window_Diagonal | — | Close diagonal ventilation |

### Sunroof & Sunshade

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 关闭天窗 | Close_Dormer | — | Close sunroof |
| 打开天窗 | Open_Dormer | — | Open sunroof |
| 打开遮阳帘 | Open_Sunshade | — | Open sunshade |
| 关闭遮阳帘 | Close_Sunshade | — | Close sunshade |

### Trunk

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开后备箱 | Open_Trunk | — | Open trunk |
| 关闭后备箱 | Close_Trunk | — | Close trunk |

### Wipers

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开雨刷器 | Open_Wiper | — | Turn on wipers |
| 关闭雨刷器 | Close_Wiper | — | Turn off wipers |

### Headlights

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开大灯 | Open_Headlamp | — | Turn on headlights |
| 关闭大灯 | Close_Headlamp | — | Turn off headlights |
| 打开近光灯 | Open_Low_Beam | — | Turn on low beam |
| 关闭近光灯 | Close_Low_Beam | — | Turn off low beam |
| 打开远光灯 | Open_High_Beam | — | Turn on high beam |
| 关闭远光灯 | Close_High_Beam | — | Turn off high beam |
| 打开自动大灯 | Open_ADAPTIVE_HEAPLAMP | — | Enable auto headlight |
| 关闭自动大灯 | Close_ADAPTIVE_HEAPLAMP | — | Disable auto headlight |

### Fog Lights

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开前雾灯 | Open_Front_Fog_Light | — | Turn on front fog lights |
| 关闭前雾灯 | Close_Front_Fog_Light | — | Turn off front fog lights |
| 打开后雾灯 | Open_Back_Fog_Light | — | Turn on rear fog lights |
| 关闭后雾灯 | Close_Back_Fog_Light | — | Turn off rear fog lights |
| 打开雾灯 | Open_Fog_Light | — | Turn on all fog lights |
| 关闭雾灯 | Close_Fog_Light | — | Turn off all fog lights |

### Other Exterior Lights

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开示宽灯 | Open_Marker_Light | — | Turn on marker lights |
| 关闭示宽灯 | Close_Marker_Light | — | Turn off marker lights |

### Cameras

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开环绕摄像 | Open_Surround_View | — | Turn on 360° camera |
| 关闭环绕摄像 | Close_Surround_View | — | Turn off 360° camera |
| 打开指定摄像头 | Set_Surround_View | Camera | Open specific camera view |
| 打开行车记录仪 | Open_DashCam | — | Turn on dashcam |
| 关闭行车记录仪 | Close_DashCam | — | Turn off dashcam |

### Recording

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 开始录音 | Record_Audio | — | Start audio recording |
| 停止录音 | Stop_Audio | — | Stop audio recording |
| 开始录像 | Record_Video | — | Start video recording |
| 停止录像 | Stop_Video | — | Stop video recording |
| 拍照 | Take_Photo | — | Take a photo |

### Driving & Engine

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置驾驶模式 | Set_Driving_Mode | Mode | Set driving mode (eco, sport, etc.) |
| 打开自动驻车 | Open_AutoHold | — | Enable auto parking hold |
| 关闭自动驻车 | Close_AutoHold | — | Disable auto parking hold |
| 打开自动启停 | Open_Engine_AutoStop | — | Enable auto start-stop |
| 关闭自动启停 | Close_Engine_AutoStop | — | Disable auto start-stop |

## Slot Resolution Rules

- **Position**: Resolve to `主驾`, `副驾`, `左后`, `右后`, `全部`. For window operations: `全部` means all windows.
- **Ratio**: For `Set_Window`, the window opening percentage (0–100%).
- **Mode**: Driving mode enum: `经济`, `舒适`, `运动`, `雪地`, `越野`. Default to `舒适`.
- **Camera**: Camera view: `前视`, `后视`, `左视`, `右视`, `360°`, `行车记录仪`.
- **Direction**: For sunroof: `开` → open, `关` → close; for wipers: auto-detect speed.
- **Window diagonal mode**: Opens front-left + rear-right or front-right + rear-left for cross-ventilation.
- Some intents (trunk, wipers, cameras) operate on the whole vehicle — Position slot is not used.
- For **sunroof**, the position is always all zones; no partial open by position.

## Implementation Checklist

When implementing a new Vehicle Control intent:

1. **Match the intent key** (e.g., `Open_Window`) to the skill function.
2. **Check safety constraints** — some operations require the vehicle to be in park or at low speed.
3. **Execute the action** via the vehicle CAN bus control API.
4. **Confirm** with a natural response (e.g., "车窗已全部关闭" or "后备箱已打开").
5. **Save SlotContext** to Redis with `agent=Vehicle Control Agent`, `intent=<matched_intent>`, and extracted slots.

## Safety Notes

- Window/sunroof operations may be restricted at high speed.
- Trunk open/close may be restricted while driving (check vehicle state).
- Some markets restrict high beam use — follow local regulations.

## Response Templates

```
车窗开: "车窗已{打开/关闭}。"
天窗开: "天窗已{打开/关闭}。"
后备箱开: "后备箱已打开。"
后备箱关: "后备箱已关闭。"
雨刷开: "雨刷器已开启。"
雨刷关: "雨刷器已关闭。"
大灯开: "大灯已开启。"
雾灯开: "雾灯已开启。"
摄像头开: "360°环视已开启。"
驾驶模式: "驾驶模式已切换到{mode}模式。"
自动驻车开: "自动驻车已开启。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
