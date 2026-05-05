# System Settings Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Open_System_Config | system_settings | `{}` | 打开系统设置 |
|| Close_System_Config | system_settings | `{"action": "close"}` | 关闭系统设置 |
|| Open_App | open_app | `{"name": "..."}` | 打开应用 |
|| Close_App | close_app | `{"name": "..."}` | 关闭应用 |
|| Open_App_List | app_list | `{}` | 打开应用列表 |
|| Close_App_List | app_list | `{"action": "close"}` | 关闭应用列表 |
|| Download_App | app_install | `{"name": "..."}` | 下载应用 |
|| Open_APP_Store | open_app | `{"name": "应用商城"}` | 打开应用商城 |
|| Close_APP_Store | close_app | `{"name": "应用商城"}` | 关闭应用商城 |
|| Back_To_Home | system_settings | `{"action": "home"}` | 回到主页 |
|| Open_Screen | system_settings | `{"action": "screen_on"}` | 打开屏幕 |
|| Close_Screen | system_settings | `{"action": "screen_off"}` | 关闭屏幕 |
|| Set_Desktop_Style | display_setting | `{"style": "..."}` | 设置桌面样式 |
|| Set_System_Theme_By_Mode | display_setting | `{"mode": "..."}` | 设置主题模式 |
|| Set_Card_Position | display_setting | `{"position": N}` | 切换卡片位置 |
|| Open_ScreenCast | system_settings | `{"action": "screencast_on"}` | 打开投屏 |
|| Close_ScreenCast | system_settings | `{"action": "screencast_off"}` | 关闭投屏 |
|| Open_Long_Video | open_app | `{"name": "长视频"}` | 打开长视频 |
|| Close_Long_Video | close_app | `{"name": "长视频"}` | 关闭长视频 |
|| Open_Mini_App | open_app | `{"name": "..."}` | 打开小程序应用 |
|| Close_Mini_App | close_app | `{"name": "..."}` | 关闭小程序应用 |
|| Open_Mini_App_Center | open_app | `{"name": "小程序中心"}` | 打开小程序中心 |
|| Close_Mini_App_Center | close_app | `{"name": "小程序中心"}` | 关闭小程序中心 |
|| Open_Scene_Center | system_settings | `{"action": "scene_center"}` | 打开情景模式 |
|| Close_Scene_Center | system_settings | `{"action": "scene_center_close"}` | 关闭情景模式 |
|| Open_Preset_Scene | system_settings | `{"scene": "..."}` | 打开指定场景 |
|| Close_Preset_Scene | system_settings | `{"scene": "off"}` | 退出指定场景 |
|| Open_Snooze_Mode | system_settings | `{"timer": N}` | 打开睡眠模式 |
|| Close_Snooze_Mode | system_settings | `{"timer": 0}` | 关闭睡眠模式 |
|| Set_Desktop_Style | language_setting | `{"language": "..."}` | 语言设置 |
|| Set_Desktop_Style | sound_setting | `{}` | 声音设置 |
|| Set_Desktop_Style | reset_settings | `{}` | 恢复默认设置 |

## Shared Slot Type Definitions

### app
```
resolution: Match against installed application list. Fuzzy search supported.
agents: System Settings Agent
```

### Desktop
```
enum: 经典, 简洁, 卡片式, 导航式
resolution: Map to desktop style preset. Default to last-used.
agents: System Settings Agent
```

### mode
```
enum: 白天, 夜间, 自动
resolution: System theme mode. Default to 自动.
agents: System Settings Agent
```

### Scene
```
enum: 回家, 上班, 约会, 露营, 影院, 运动, 静音
resolution: Scene preset name. Default to last-used.
agents: System Settings Agent
```

### Mini_app
```
resolution: Match against available mini programs. Fuzzy search supported.
agents: System Settings Agent
```

### Minute
```
value_range: 5-120 minutes
resolution: Sleep timer duration. Default to 30 minutes.
agents: System Settings Agent
```

## Scene Preset Definitions

|| Scene | HVAC | Lighting | Media | Navigation |
|-------|------|----------|-------|------------|
| 回家 | 24°C, auto | Warm white, 60% | Resume playlist | Route home |
| 上班 | 22°C, auto | Daylight, 80% | News | Route to office |
| 约会 | 24°C, soft | Pink/purple, 40% | Soft music | — |
| 露营 | Off | Dim, 20% | — | — |
| 影院 | 25°C, quiet | Off | Video app | — |
| 运动 | 22°C, fresh | Bright, 70% | Workout playlist | — |
| 静音 | 25°C | — | Mute | — |

## Sleep Timer Behavior

When sleep timer is set, the system will automatically perform a shutdown sequence after `Minute` minutes:
1. Save current state
2. Close active media
3. Dim/disable screen
4. Enable wake word only

The user can cancel at any time.
