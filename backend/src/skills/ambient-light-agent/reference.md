# Ambient Light Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Open_Env_Light | set_interior_lights | `{"switch": "on"}` | 打开氛围灯 |
|| Close_Env_Light | set_interior_lights | `{"switch": "off"}` | 关闭氛围灯 |
|| Set_Env_Light_Color | set_interior_lights | `{"color": "..."}` | 设置氛围灯颜色 |
|| Set_Env_Light_Theme | set_interior_lights | `{"theme": "..."}` | 调节氛围灯主题 |
|| Dec_Env_Light_Brightness | set_interior_lights | `{"level": N, "direction": "down"}` | 调低氛围灯亮度 |
|| Inc_Env_Light_Brightness | set_interior_lights | `{"level": N, "direction": "up"}` | 调高氛围灯亮度 |
|| Set_Env_Light_Brightness | set_interior_lights | `{"level": N}` | 设置氛围灯亮度 |
|| Open_Env_Light_Auto_Mode | set_interior_lights | `{"mode": "auto"}` | 氛围灯自动模式 |
|| Close_Env_Light_Auto_Mode | set_interior_lights | `{"mode": "manual"}` | 关闭氛围灯自动模式 |
|| Dec_DashBoard_Brightness | set_interior_lights | `{"target": "dashboard", "level": N, "direction": "down"}` | 调暗仪表盘 |
|| Inc_DashBoard_Brightness | set_interior_lights | `{"target": "dashboard", "level": N, "direction": "up"}` | 调亮仪表盘 |
|| Set_DashBoard_Brightness_Min | set_interior_lights | `{"target": "dashboard", "level": 0}` | 仪表盘调到最暗 |
|| Set_DashBoard_Brightness_Max | set_interior_lights | `{"target": "dashboard", "level": 100}` | 仪表盘调到最亮 |
|| Set_DashBoard_Brightness | set_interior_lights | `{"target": "dashboard", "level": N}` | 设置仪表盘亮度 |
|| Dec_Brightness | set_interior_lights | `{"target": "screen", "level": N, "direction": "down"}` | 亮度调低 |
|| Inc_Brightness | set_interior_lights | `{"target": "screen", "level": N, "direction": "up"}` | 亮度调高 |
|| Set_Brightness_Min | set_interior_lights | `{"target": "screen", "level": 0}` | 亮度调到最低 |
|| Set_Brightness_Max | set_interior_lights | `{"target": "screen", "level": 100}` | 亮度调到最高 |
|| Set_Brightness | set_interior_lights | `{"target": "screen", "level": N}` | 设置亮度 |
|| Open_HUD | hud_on | `{}` | 打开HUD |
|| Close_HUD | hud_off | `{}` | 关闭HUD |
|| Adjust_Hud_Brightness | hud_brightness | `{"level": N}` | HUD亮度调到指定值 |
|| Inc_HUD_Brightness | hud_brightness | `{"direction": "up"}` | 调高HUD亮度 |
|| Dec_HUD_Brightness | hud_brightness | `{"direction": "down"}` | 调低HUD亮度 |
|| Adjust_HUD_Vert | hud_mode | `{"direction": "vertical", "position": "上/下"}` | 上下调节HUD位置 |
|| Adjust_HUD_Horizon | hud_mode | `{"direction": "horizontal", "position": "左/右"}` | 左右调节HUD位置 |
|| Open_Reading_Light | set_reading_light | `{"switch": "on"}` | 打开阅读灯 |
|| Close_Reading_Light | set_reading_light | `{"switch": "off"}` | 关闭阅读灯 |

## Shared Slot Type Definitions

### Color
```
enum: 红色, 蓝色, 绿色, 紫色, 橙色, 黄色, 白色, 暖白, 粉色, 青色, 多色
resolution: Match to nearest available system color. Default to 白色.
agents: Ambient Light Agent
```

### Theme
```
enum: 浪漫, 科技, 自然, 运动, 音乐随动, 呼吸, 星空, 落日, 极光
resolution: Match to nearest available theme preset. Default to 科技.
agents: Ambient Light Agent
```

### Number
```
value_range: 1-100 (brightness percentage)
resolution: Normalize to percentage. Default to 50%.
agents: Ambient Light Agent, System Settings Agent, HVAC Agent
```

### Ratio
```
resolution: Relative adjustment: 高→+20%, 中→0, 低→-20%, 最高→max, 最低→min
agents: Ambient Light Agent, HVAC Agent, Seat Agent, System Settings Agent
```

### level
```
value_range: 1-5 (HUD brightness)
resolution: HUD brightness level. Default to 3 (medium).
agents: Ambient Light Agent
```

## Brightness Ranges by Device

|| Device | Min | Max | Default | Unit |
|--------|-----|-----|---------|------|
| Screen | 0% | 100% | 50% | percentage |
| Dashboard | 0% | 100% | 60% | percentage |
| Ambient Light | 0% | 100% | 40% | percentage |
| HUD | Level 1 | Level 5 | Level 3 | discrete |

## Relative Adjustment Mapping

|| Ratio Term | Delta from Current |
|-----------|-------------------|
| 低 / 低一点 | -20% |
| 中 | 0 (centered) |
| 高 / 高一点 | +20% |
| 最高 / 最低 | 100% / 0% |

## Ambient Light Color Wavelengths (Reference)

|| Color | Approximate RGB | Effect |
|-------|---------------|--------|
| 红色 | R255 G0 B0 | Warm, energetic |
| 蓝色 | R0 G100 B255 | Cool, calming |
| 绿色 | R0 G255 B100 | Natural, relaxing |
| 紫色 | R150 G0 B255 | Ambient, soothing |
| 橙色 | R255 G150 B0 | Warm, cozy |
| 白色 | R255 G255 B255 | Clean, neutral |
| 暖白 | R255 G240 B200 | Cozy, warm |
| 粉色 | R255 G100 B150 | Romantic, soft |
