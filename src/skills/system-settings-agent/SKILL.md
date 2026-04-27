---
name: system-settings-agent
description: Implements System Settings Agent intents in the vehicle embedded multi-task system. Handles app management, desktop UI, system theme, card layout, screen control, scene modes, and sleep timer. Use when the user mentions apps, settings, desktop, theme, screen, scene mode, sleep timer, or mini programs. Trigger terms: 系统设置, 应用, 桌面, 主题, 卡片, 屏幕, 情景模式, 睡眠模式, 小程序, 投屏.
---

# System Settings Agent — Apps, Display & Scene Modes Skill

## Agent Overview

**Handles:** App management, desktop UI, system theme, card layout, screen control, scene modes, and sleep timer.
**Total intents: 36**
**Shared slot types:** `app`, `Desktop`, `mode`, `Scene`, `Mini_app`, `Position`, `One_Level`, `Two_Level`, `Minute`

## Core Intent Categories

### System Settings

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开系统设置 | Open_System_Config | One_Level, Two_Level | Open system settings |
| 关闭系统设置 | Close_System_Config | One_Level, Two_Level | Close system settings |

### App Management

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开应用 | Open_App | app | Open a specific app |
| 关闭应用 | Close_App | app | Close a specific app |
| 打开应用列表 | Open_App_List | — | Open app list |
| 关闭应用列表 | Close_App_List | — | Close app list |
| 下载应用 | Download_App | app | Download an app |
| 打开应用商城 | Open_APP_Store | — | Open app store |
| 关闭应用商城 | Close_APP_Store | — | Close app store |

### Desktop & Display

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置桌面样式 | Set_Desktop_Style | Desktop | Set desktop theme/style |
| 关闭主题 | Set_System_Theme_By_Mode | mode | Set day/night theme |
| 切换卡片位置 | Set_Card_Position | Position | Rearrange home screen cards |
| 回到主页 | Back_To_Home | — | Return to home screen |
| 打开屏幕 | Open_Screen | — | Turn on display |
| 关闭屏幕 | Close_Screen | — | Turn off display |

### Screen Casting

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开投屏 | Open_ScreenCast | — | Enable screen casting |
| 关闭投屏 | Close_ScreenCast | — | Disable screen casting |

### Video Apps

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开长视频 | Open_Long_Video | — | Open long video app |
| 关闭长视频 | Close_Long_Video | — | Close long video app |

### Mini Programs

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开小程序应用 | Open_Mini_App | Mini_app | Open a mini app |
| 关闭小程序应用 | Close_Mini_App | Mini_app | Close a mini app |
| 打开小程序中心 | Open_Mini_App_Center | — | Open mini app center |
| 关闭小程序中心 | Close_Mini_App_Center | — | Close mini app center |

### Scene Modes

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开情景模式 | Open_Scene_Center | — | Open scene mode center |
| 关闭情景模式 | Close_Scene_Center | — | Close scene mode center |
| 打开指定场景 | Open_Preset_Scene | Scene | Activate a preset scene |
| 退出指定场景 | Close_Preset_Scene | Scene | Deactivate a scene |

### Sleep Timer

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开睡眠模式 | Open_Snooze_Mode | Minute | Enable sleep mode (auto-off timer) |
| 关闭睡眠模式 | Close_Snooze_Mode | — | Cancel sleep mode |
| 模糊表达打开睡眠模式 | Open_Snooze_Mode_Fuzzy | — | Vague request to enable sleep mode |
| 模糊表达关闭睡眠模式 | Close_Snooze_Mode_Fuzzy | — | Vague request to cancel sleep mode |

## Slot Resolution Rules

- **app**: Application name. Match against installed application list.
- **Desktop**: Desktop style preset: `经典`, `简洁`, `卡片式`, `导航式`. Default to last-used.
- **mode**: Day/night theme: `白天`, `夜间`, `自动`. Default to `自动`.
- **Scene**: Named scene preset: `回家`, `上班`, `约会`, `露营`, `影院`. Default to last-used.
- **Mini_app**: Mini program name. Match against available mini apps.
- **Position**: Card position index on home screen (1-based).
- **Minute**: Sleep timer duration in minutes. Range 5–120. Default to 30.
- When **app is not found**, return a helpful list of available apps.
- Scene presets (`Open_Preset_Scene`) typically combine multiple settings: HVAC, lighting, media, etc.

## Implementation Checklist

When implementing a new System Settings intent:

1. **Match the intent key** (e.g., `Open_App`) to the skill function.
2. **Resolve app/Mini_app** — match against available applications.
3. **Execute the action** via the system settings API.
4. **Confirm** with a natural response (e.g., "已打开{app}" or "情景模式{scene}已开启").
5. **Save SlotContext** to Redis with `agent=System Settings Agent`, `intent=<matched_intent>`, and extracted slots.

## Scene Preset Behavior

A scene preset applies a coordinated set of settings. Example "回家" scene:
- HVAC: 24°C, auto mode
- Ambient light: warm white, 60%
- Media: continue last playlist
- Navigation: route home (if not already navigating)

## Response Templates

```
应用打开: "已打开{app}。"
应用关闭: "{app}已关闭。"
桌面切换: "桌面样式已切换到{desktop}。"
回到主页: "正在返回主页。"
屏幕开关: "屏幕已{开启/关闭}。"
投屏开: "投屏已开启，正在搜索设备。"
情景模式开: "已开启{scene}情景模式。"
睡眠模式开: "睡眠模式已设置，{minute}分钟后将自动关闭。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
