# HVAC Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 14 | Close_Air_Condition | 关闭空调 |
| 88 | Open_Air_Condition | 打开空调 |
| 12 | Open_Air_Condition_Auto_Mode | 打开空调自动模式 |
| 140 | Close_Air_Condition_Auto_Mode | 关闭空调自动模式 |
| 161 | Open_Air_Condition_Sync | 打开空调同步模式 |
| 279 | Close_Air_Condition_Sync | 关闭空调同步模式 |
| 162 | Open_Cooling | 打开空调制冷 |
| 290 | Close_Cooling | 关闭空调制冷 |
| 193 | Open_Heating | 打开空调制热 |
| 371 | Close_Heating | 关闭制热模式 |
| 50 | Open_Air_Condition_Defog | 打开除雾 |
| 195 | Close_Air_Condition_Defog | 关闭除雾 |
| 16 | Dec_Air_Condition_Temperature | 降低空调温度 |
| 136 | Inc_Air_Condition_Temperature | 调高空调温度 |
| 15 | Set_Air_Condition_Temperature | 设置空调温度 |
| 17 | Dec_Air_Condition_Wind | 降低空调风力 |
| 45 | Inc_Air_Condition_Wind | 调高空调风力 |
| 83 | Set_Air_Condition_Wind | 设置空调风力 |
| 183 | Set_Wind_Direction | 设置空调风向 |
| 266 | Cancel_Wind_Direction | 取消空调风向 |
| 283 | Open_Wind_Auto_Mode | 打开自动风向 |
| 395 | Close_Wind_Auto_Mode | 关闭自动风向 |
| 71 | Open_AC | 打开AC |
| 70 | Close_AC | 关闭AC |
| 139 | Close_Cooling_Instant | 关闭一键降温 |
| 319 | Open_Cooling_Instant | 一键降温 |
| 360 | Open_Heating_Instant | 快速升温 |
| 26 | Ask_Air_Condition | 查询空气 |
| 66 | Ask_Humidity | 查询湿度 |
| 260 | Ask_Wind | 查询风力 |
| 211 | Open_Air_Cleaner | 打开空气净化器 |
| 94 | Close_Air_Cleaner | 关闭空气净化器 |
| 280 | Open_Internal_Circulation | 打开内循环 |
| 253 | Close_Internal_Circulation | 关闭内循环 |
| 389 | Open_External_Circulation | 打开外循环 |
| 401 | Close_External_Circulation | 关闭外循环 |
| 327 | Open_Air_Condition_APP | 打开空调应用 |
| 188 | Close_Air_Condition_APP | 关闭空调应用 |
| 375 | Temp_Compare | 温度比较 |

## Shared Slot Type Definitions

### Position
```
enum: 主驾, 副驾, 后排, 后排左侧, 后排右侧, 全部, 前排, 后座, 副驾后, 主驾后
resolution: Resolve to a concrete position. Default to 主驾 if not specified.
agents: HVAC Agent, Seat Agent, Vehicle Control Agent
```

### Number
```
value_range: type=number
resolution: Normalize to integer; infer unit from context (°C for temperature, level for fan)
agents: HVAC Agent, Seat Agent, Ambient Light Agent, System Settings Agent
```

### Ratio
```
resolution: Map relative descriptors to numeric steps: 高→+3, 中→0, 低→-3, 最高→max, 最低→min
agents: HVAC Agent, Seat Agent, Ambient Light Agent, System Settings Agent, Media Agent
```

### Extreme
```
enum: 最高, 最低, 最大, 最小, 最热, 最冷, 最强, 最弱
agents: HVAC Agent, Seat Agent, Ambient Light Agent
```

### Direction
```
enum: 上, 下, 左, 右, 前, 后, 左上, 右上, 左下, 右下, 前后, 上下, 左右
agents: Seat Agent, Ambient Light Agent, HVAC Agent
```

## Temperature Ranges

| Zone | Min | Max | Default |
|------|-----|-----|---------|
| 主驾 | 16°C | 32°C | 24°C |
| 副驾 | 16°C | 32°C | 24°C |
| 后排 | 16°C | 32°C | 24°C |
| 全部 | 16°C | 32°C | 24°C |

## Fan Speed Levels

Levels 1–7 (auto mode maps 0–7 internally).

| Ratio Term | Step Delta |
|-----------|-----------|
| 低 / 低一点 | -2 |
| 中 | 0 (centered) |
| 高 / 高一点 | +2 |
| 再高 / 再低 | +1 / -1 from current |
| 最高 / 最低 | max (7) / min (1) |

## Airflow Direction Mapping

| Direction Slot | Airflow Target |
|---------------|---------------|
| 上 | Face (upper vents) |
| 下 | Body (lower vents) |
| 前 | Front windshield defrost |
| 后 | Rear passengers |
| 左/右 | Left/right side vents |
| 上下 | All vents |
| 前后 | Front + rear |

## AC Compressor State

A/C compressor can be ON/OFF independently of fan. In eco mode, compressor may auto-engage. Always query current state before toggling.
