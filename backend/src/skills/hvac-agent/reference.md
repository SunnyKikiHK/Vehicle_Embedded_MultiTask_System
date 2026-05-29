# HVAC Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Close_Air_Condition | ac_off | `{}` | 关闭空调 |
|| Open_Air_Condition | ac_on | `{}` | 打开空调 |
|| Open_Air_Condition_Auto_Mode | ac_auto | `{}` | 打开空调自动模式 |
|| Close_Air_Condition_Auto_Mode | ac_auto | `{"mode": "manual"}` | 关闭空调自动模式 |
|| Open_Air_Condition_Sync | sync_ac | `{"mode": "sync"}` | 打开空调同步模式 |
|| Close_Air_Condition_Sync | sync_ac | `{"mode": "unsync"}` | 关闭空调同步模式 |
|| Open_Cooling | set_ac_mode | `{"mode": "cooling"}` | 打开空调制冷 |
|| Close_Cooling | set_ac_mode | `{"mode": "off"}` | 关闭空调制冷 |
|| Open_Heating | set_ac_mode | `{"mode": "heating"}` | 打开空调制热 |
|| Close_Heating | set_ac_mode | `{"mode": "off"}` | 关闭制热模式 |
|| Open_Air_Condition_Defog | defrost | `{"mode": "defog"}` | 打开除雾 |
|| Close_Air_Condition_Defog | defrost | `{"mode": "off"}` | 关闭除雾 |
|| Dec_Air_Condition_Temperature | set_temperature | `{"direction": "down"}` | 降低空调温度 |
|| Inc_Air_Condition_Temperature | set_temperature | `{"direction": "up"}` | 调高空调温度 |
|| Set_Air_Condition_Temperature | set_temperature | `{"temperature": N}` | 设置空调温度 |
|| Dec_Air_Condition_Wind | set_fan_speed | `{"direction": "down"}` | 降低空调风力 |
|| Inc_Air_Condition_Wind | set_fan_speed | `{"direction": "up"}` | 调高空调风力 |
|| Set_Air_Condition_Wind | set_fan_speed | `{"level": N}` | 设置空调风力 |
|| Set_Wind_Direction | set_ac_mode | `{"direction": "..."}` | 设置空调风向 |
|| Cancel_Wind_Direction | set_ac_mode | `{"direction": "auto"}` | 取消空调风向 |
|| Open_Wind_Auto_Mode | set_ac_mode | `{"direction": "auto"}` | 打开自动风向 |
|| Close_Wind_Auto_Mode | set_ac_mode | `{"direction": "manual"}` | 关闭自动风向 |
|| Open_AC | ac_on | `{}` | 打开AC |
|| Close_AC | ac_off | `{}` | 关闭AC |
|| Open_Cooling_Instant | ac_on | `{"mode": "max_cool"}` | 一键降温 |
|| Open_Heating_Instant | ac_on | `{"mode": "max_heat"}` | 快速升温 |
|| Ask_Air_Condition | get_weather | `{"type": "air_quality"}` | 查询空气 |
|| Ask_Humidity | get_weather | `{"type": "humidity"}` | 查询湿度 |
|| Ask_Wind | get_weather | `{"type": "wind"}` | 查询风力 |
|| Temp_Compare | get_weather | `{"type": "compare", "cities": [...]}` | 温度比较 |

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

|| Zone | Min | Max | Default |
|------|-----|-----|---------|
| 主驾 | 16°C | 32°C | 24°C |
| 副驾 | 16°C | 32°C | 24°C |
| 后排 | 16°C | 32°C | 24°C |
| 全部 | 16°C | 32°C | 24°C |

## Fan Speed Levels

Levels 1–7 (auto mode maps 0–7 internally).

|| Ratio Term | Step Delta |
|-----------|-----------|
| 低 / 低一点 | -2 |
| 中 | 0 (centered) |
| 高 / 高一点 | +2 |
| 再高 / 再低 | +1 / -1 from current |
| 最高 / 最低 | max (7) / min (1) |

## Airflow Direction Mapping

|| Direction Slot | Airflow Target |
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
