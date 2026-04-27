# Seat Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 21 | Adjust_Seat_Long | 座椅前后调整 |
| 245 | Adjust_Seat_Vert | 座椅水平调整 |
| 192 | Open_Heated_Seat | 打开座椅加热 |
| 206 | Close_Heated_Seat | 关闭座椅加热 |
| 123 | Dec_Seat_Temperature | 调低座椅温度 |
| 63 | Inc_Seat_Temperature | 调高座椅温度 |
| 30 | Set_Seat_Temperature | 设置座椅温度 |
| 165 | Open_Seat_Ventilation | 打开座椅通风 |
| 141 | Close_Seat_Ventilation | 关闭座椅通风 |
| 96 | Dec_Seat_Ventilation | 调低座椅通风 |
| 79 | Inc_Seat_Ventilation | 调大座椅通风 |
| 37 | Set_Seat_Ventilation | 设置座椅通风 |
| 234 | Open_Seat_Massage | 打开座椅按摩 |
| 78 | Close_Seat_Massage | 关闭座椅按摩 |
| 71 | Dec_Seat_Massage | 调低座椅按摩 |
| 151 | Inc_Seat_Massage | 调大座椅按摩 |
| 47 | Set_Seat_Massage | 设置座椅按摩 |
| 28 | Set_Steer_Temperature | 设置方向盘温度 |
| 98 | Dec_Steer_Temperature | 调低方向盘温度 |
| 261 | Inc_Steer_Temperature | 调高方向盘温度 |
| 205 | Open_Heated_Steer | 打开方向盘加热 |
| 204 | Close_Heated_Steer | 关闭方向盘加热 |
| 153 | Open_Rearview_Mirror_Heating | 打开后视镜加热 |
| 377 | Close_Rearview_Mirror_Heating | 关闭后视镜加热 |
| 236 | Open_Rearview_Mirror | 展开后视镜 |
| 351 | Close_Rearview_Mirror | 折叠后视镜 |

## Seat Comfort Levels

All comfort features (heating, ventilation, massage) use levels 1–3.

| Level | Heating Effect | Ventilation Effect | Massage Effect |
|-------|---------------|-------------------|----------------|
| 1 | Low warmth | Low airflow | Gentle |
| 2 | Medium warmth | Medium airflow | Moderate |
| 3 | High warmth | High airflow | Strong |

## Relative Adjustment Mapping

| Ratio Term | Delta from Current |
|-----------|-------------------|
| 低 / 低一点 / 再低点 | -1 |
| 高 / 高一点 / 再高点 | +1 |
| 最高 / 最低 | Max (3) / Min (1) |
| 关闭 | Turn off (0) |

## Position Mapping

| User Expression | Resolved Position |
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

- `Open_Rearview_Mirror`: Unfold both side mirrors simultaneously.
- `Close_Rearview_Mirror`: Fold both side mirrors simultaneously.
- If mirrors are already in desired state, respond with current state (no error).
