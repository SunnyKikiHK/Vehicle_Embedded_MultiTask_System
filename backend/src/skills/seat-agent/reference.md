# Seat Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Adjust_Seat_Long | adjust_seat | `{"direction": "forward/backward", "position": "..."}` | 座椅前后调整 |
|| Adjust_Seat_Vert | adjust_seat | `{"direction": "up/down", "position": "..."}` | 座椅水平调整 |
|| Open_Heated_Seat | seat_heating | `{"switch": "on", "position": "..."}` | 打开座椅加热 |
|| Close_Heated_Seat | seat_heating | `{"switch": "off", "position": "..."}` | 关闭座椅加热 |
|| Dec_Seat_Temperature | seat_heating | `{"level": N, "direction": "down", "position": "..."}` | 调低座椅温度 |
|| Inc_Seat_Temperature | seat_heating | `{"level": N, "direction": "up", "position": "..."}` | 调高座椅温度 |
|| Set_Seat_Temperature | seat_heating | `{"level": N, "position": "..."}` | 设置座椅温度 |
|| Open_Seat_Ventilation | seat_ventilation | `{"switch": "on", "position": "..."}` | 打开座椅通风 |
|| Close_Seat_Ventilation | seat_ventilation | `{"switch": "off", "position": "..."}` | 关闭座椅通风 |
|| Dec_Seat_Ventilation | seat_ventilation | `{"level": N, "direction": "down", "position": "..."}` | 调低座椅通风 |
|| Inc_Seat_Ventilation | seat_ventilation | `{"level": N, "direction": "up", "position": "..."}` | 调大座椅通风 |
|| Set_Seat_Ventilation | seat_ventilation | `{"level": N, "position": "..."}` | 设置座椅通风 |
|| Open_Seat_Massage | seat_massage | `{"switch": "on", "position": "..."}` | 打开座椅按摩 |
|| Close_Seat_Massage | seat_massage | `{"switch": "off", "position": "..."}` | 关闭座椅按摩 |
|| Dec_Seat_Massage | seat_massage | `{"level": N, "direction": "down", "position": "..."}` | 调低座椅按摩 |
|| Inc_Seat_Massage | seat_massage | `{"level": N, "direction": "up", "position": "..."}` | 调大座椅按摩 |
|| Set_Seat_Massage | seat_massage | `{"level": N, "position": "..."}` | 设置座椅按摩 |
|| Open_Heated_Steer | seat_heating | `{"switch": "on", "target": "steering_wheel"}` | 打开方向盘加热 |
|| Close_Heated_Steer | seat_heating | `{"switch": "off", "target": "steering_wheel"}` | 关闭方向盘加热 |
|| Open_Rearview_Mirror | adjust_seat | `{"target": "mirror", "action": "unfold"}` | 展开后视镜 |
|| Close_Rearview_Mirror | adjust_seat | `{"target": "mirror", "action": "fold"}` | 折叠后视镜 |

## Seat Comfort Levels

All comfort features (heating, ventilation, massage) use levels 1–3.

|| Level | Heating Effect | Ventilation Effect | Massage Effect |
|-------|---------------|-------------------|----------------|
| 1 | Low warmth | Low airflow | Gentle |
| 2 | Medium warmth | Medium airflow | Moderate |
| 3 | High warmth | High airflow | Strong |

## Relative Adjustment Mapping

|| Ratio Term | Delta from Current |
|-----------|-------------------|
| 低 / 低一点 / 再低点 | -1 |
| 高 / 高一点 / 再高点 | +1 |
| 最高 / 最低 | Max (3) / Min (1) |
| 关闭 | Turn off (0) |

## Position Mapping

|| User Expression | Resolved Position |
|----------------|------------------|
| 主驾 / 驾驶位 | 主驾 |
| 副驾 / 副驾驶 | 副驾 |
| 后排 / 后座 | 后排 |
| 后排左侧 | 后排左侧 |
| 后排右侧 | 后排右侧 |
| (omitted, driver only) | 主驾 |
| (omitted, multi-occupant) | 全部 |

## Steering Wheel Temperature

Steering wheel heating operates on the same 1–3 level system as seat heating.

## Mirror Folding Behavior

- `unfold`: Unfold both side mirrors simultaneously.
- `fold`: Fold both side mirrors simultaneously.
- If mirrors are already in desired state, respond with current state (no error).
