# Ambient Light Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 63 | Open_Env_Light | 打开氛围灯 |
| 16 | Close_Env_Light | 关闭氛围灯 |
| 56 | Set_Env_Light_Color | 设置氛围灯颜色 |
| 121 | Set_Env_Light_Theme | 调节氛围灯主题 |
| 123 | Dec_Env_Light_Brightness | 调低氛围灯亮度 |
| 176 | Inc_Env_Light_Brightness | 调高氛围灯亮度 |
| 124 | Set_Env_Light_Brightness | 设置氛围灯亮度 |
| 366 | Open_Env_Light_Auto_Mode | 氛围灯自动模式 |
| 413 | Close_Env_Light_Auto_Mode | 关闭氛围灯自动模式 |
| 91 | Dec_DashBoard_Brightness | 调暗仪表盘 |
| 91 | Inc_DashBoard_Brightness | 调亮仪表盘 |
| 269 | Set_DashBoard_Brightness_Min | 仪表盘调到最暗 |
| 268 | Set_DashBoard_Brightness_Max | 仪表盘调到最亮 |
| 276 | Set_DashBoard_Brightness | 设置仪表盘亮度 |
| 38 | Dec_Brightness | 亮度调低 |
| 189 | Inc_Brightness | 亮度调高 |
| 127 | Set_Brightness_Min | 亮度调到最低 |
| 273 | Set_Brightness_Max | 亮度调到最高 |
| 157 | Set_Brightness | 设置亮度 |
| 147 | Open_HUD | 打开HUD |
| 275 | Close_HUD | 关闭HUD |
| 73 | Adjust_Hud_Brightness | HUD亮度调到指定值 |
| 174 | Inc_HUD_Brightness | 调高HUD亮度 |
| 423 | Dec_HUD_Brightness | 调低HUD亮度 |
| 332 | Adjust_HUD_Vert | 上下调节HUD位置 |
| 416 | Adjust_HUD_Horizon | 左右调节HUD位置 |
| 147 | Open_Reading_Light | 打开阅读灯 |
| 335 | Close_Reading_Light | 关闭阅读灯 |

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

| Device | Min | Max | Default | Unit |
|--------|-----|-----|---------|------|
| Screen | 0% | 100% | 50% | percentage |
| Dashboard | 0% | 100% | 60% | percentage |
| Ambient Light | 0% | 100% | 40% | percentage |
| HUD | Level 1 | Level 5 | Level 3 | discrete |

## Relative Adjustment Mapping

| Ratio Term | Delta from Current |
|-----------|-------------------|
| 低 / 低一点 | -20% |
| 中 | 0 (centered) |
| 高 / 高一点 | +20% |
| 最高 / 最低 | 100% / 0% |

## Ambient Light Color Wavelengths (Reference)

| Color | Approximate RGB | Effect |
|-------|---------------|--------|
| 红色 | R255 G0 B0 | Warm, energetic |
| 蓝色 | R0 G100 B255 | Cool, calming |
| 绿色 | R0 G255 B100 | Natural, relaxing |
| 紫色 | R150 G0 B255 | Ambient, soothing |
| 橙色 | R255 G150 B0 | Warm, cozy |
| 白色 | R255 G255 B255 | Clean, neutral |
| 暖白 | R255 G240 B200 | Cozy, warm |
| 粉色 | R255 G100 B150 | Romantic, soft |
