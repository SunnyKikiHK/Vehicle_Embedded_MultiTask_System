# System Settings Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 40 | Open_System_Config | 打开系统设置 |
| 48 | Close_System_Config | 关闭系统设置 |
| 195 | Open_App | 打开应用 |
| 80 | Close_App | 关闭应用 |
| 275 | Open_App_List | 打开应用列表 |
| 320 | Close_App_List | 关闭应用列表 |
| 129 | Download_App | 下载应用 |
| 218 | Open_APP_Store | 打开应用商城 |
| 364 | Close_APP_Store | 关闭应用商城 |
| 53 | Set_Desktop_Style | 设置桌面样式 |
| 100 | Set_System_Theme_By_Mode | 关闭主题 |
| 178 | Set_Card_Position | 切换卡片位置 |
| 337 | Back_To_Home | 回到主页 |
| 379 | Open_Screen | 打开屏幕 |
| 244 | Close_Screen | 关闭屏幕 |
| 392 | Open_ScreenCast | 打开投屏 |
| 202 | Close_ScreenCast | 关闭投屏 |
| 246 | Open_Long_Video | 打开长视频 |
| 269 | Close_Long_Video | 关闭长视频 |
| 124 | Open_Mini_App | 打开小程序应用 |
| 19 | Close_Mini_App | 关闭小程序应用 |
| 418 | Open_Mini_App_Center | 打开小程序中心 |
| 7 | Close_Mini_App_Center | 关闭小程序中心 |
| 334 | Open_Scene_Center | 打开情景模式 |
| 272 | Close_Scene_Center | 关闭情景模式 |
| 306 | Open_Preset_Scene | 打开指定场景 |
| 271 | Close_Preset_Scene | 退出指定场景 |
| 146 | Open_Snooze_Mode | 打开睡眠模式 |
| 358 | Close_Snooze_Mode | 关闭睡眠模式 |
| 167 | Open_Snooze_Mode_Fuzzy | 模糊表达打开睡眠模式 |
| 347 | Close_Snooze_Mode_Fuzzy | 模糊表达关闭睡眠模式 |
| 54 | Set_Desktop_Style | 设置桌面样式 |

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

| Scene | HVAC | Lighting | Media | Navigation |
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
