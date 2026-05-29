---
name: system-settings-agent
description: Implements System Settings Agent intents in the vehicle embedded multi-task system. Handles app management, desktop UI, system theme, card layout, screen control, scene modes, and sleep timer. Use when the user mentions apps, settings, desktop, theme, screen, scene mode, sleep timer, or mini programs. Trigger terms: 系统设置, 应用, 桌面, 主题, 卡片, 屏幕, 情景模式, 睡眠模式, 小程序, 投屏.
---

# System Settings Agent — Apps, Display & Scene Modes Skill

## Agent Overview

**Handles:** App management, desktop UI, system theme, card layout, screen control, scene modes, and sleep timer.
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

### System Settings

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开系统设置 | system_settings | `{}` | Open system settings |
| 语言设置 | language_setting | `{"language": "<lang>"}` | Set system language |
| 声音设置 | sound_setting | `{}` | Open sound settings |
| 显示设置 | display_setting | `{}` | Open display settings |
| 恢复默认设置 | reset_settings | `{}` | Reset all settings to default |

### App Management

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开应用 | open_app | `{"name": "<app>"}` | Open a specific app |
| 关闭应用 | close_app | `{"name": "<app>"}` | Close a specific app |
| 查看应用列表 | app_list | `{}` | List installed apps |
| 安装应用 | app_install | `{"name": "<app>"}` | Install an app |
| 卸载应用 | app_uninstall | `{"name": "<app>"}` | Uninstall an app |

### Desktop & Display

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 回到主页 | system_settings | `{"action": "home"}` | Return to home screen |
| 打开屏幕 | system_settings | `{"action": "screen_on"}` | Turn on display |
| 关闭屏幕 | system_settings | `{"action": "screen_off"}` | Turn off display |

### Screenshot

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 截屏 | screenshot_screen | `{}` | Take a screenshot |

### Notifications

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 显示通知 | show_notification | `{"title": "<title>", "content": "<content>"}` | Show a notification |
| 关闭通知 | dismiss_notification | `{}` | Dismiss current notification |

## Slot Resolution Rules

- **app**: Application name. Match against installed application list
- When **app is not found**, return a helpful list of available apps

## Implementation Checklist

When implementing a new System Settings intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve app name
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
