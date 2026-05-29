# Vehicle Control Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Open_Window | open_window | `{"position": "..."}` | 打开车窗 |
|| Close_Window | close_window | `{"position": "..."}` | 关闭车窗 |
|| Set_Window | window_down | `{"position": "...", "level": N}` | 设置车窗 |
|| Open_Window_Diagonal | open_window | `{"mode": "diagonal"}` | 打开通风模式 |
|| Close_Window_Diagonal | close_window | `{"mode": "normal"}` | 关闭通风模式 |
|| Open_Dormer | flash_lights | `{"action": "sunroof_open"}` | 打开天窗 |
|| Close_Dormer | flash_lights | `{"action": "sunroof_close"}` | 关闭天窗 |
|| Open_Trunk | flash_lights | `{"action": "trunk_open"}` | 打开后备箱 |
|| Close_Trunk | flash_lights | `{"action": "trunk_close"}` | 关闭后备箱 |
|| Open_Wiper | flash_lights | `{"action": "wiper_on"}` | 打开雨刷器 |
|| Close_Wiper | flash_lights | `{"action": "wiper_off"}` | 关闭雨刷器 |
|| Open_Headlamp | set_headlights | `{"mode": "on"}` | 打开大灯 |
|| Close_Headlamp | set_headlights | `{"mode": "off"}` | 关闭大灯 |
|| Open_Low_Beam | set_headlights | `{"mode": "low_beam"}` | 打开近光灯 |
|| Close_Low_Beam | set_headlights | `{"mode": "off"}` | 关闭近光灯 |
|| Open_High_Beam | set_headlights | `{"mode": "high_beam"}` | 打开远光灯 |
|| Close_High_Beam | set_headlights | `{"mode": "low_beam"}` | 关闭远光灯 |
|| Open_Fog_Light | set_headlights | `{"mode": "fog_on"}` | 打开雾灯 |
|| Close_Fog_Light | set_headlights | `{"mode": "fog_off"}` | 关闭雾灯 |
|| Open_Surround_View | open_camera | `{"type": "surround_view"}` | 打开环绕摄像 |
|| Close_Surround_View | close_camera | `{"type": "surround_view"}` | 关闭环绕摄像 |
|| Set_Surround_View | open_camera | `{"type": "..."}` | 打开指定摄像头 |
|| Open_DashCam | dashcam_view | `{"action": "start"}` | 打开行车记录仪 |
|| Close_DashCam | dashcam_view | `{"action": "stop"}` | 关闭行车记录仪 |
|| Take_Photo | screenshot | `{"type": "camera"}` | 拍照 |
|| Record_Video | record_video | `{"action": "start"}` | 开始录像 |
|| Stop_Video | record_video | `{"action": "stop"}` | 停止录像 |
|| Record_Audio | record_video | `{"action": "audio_start"}` | 开始录音 |
|| Stop_Audio | record_video | `{"action": "audio_stop"}` | 停止录音 |
|| Set_Driving_Mode | lock_doors | `{"mode": "..."}` | 设置驾驶模式 |
|| Open_AutoHold | lock_doors | `{"action": "auto_hold_on"}` | 打开自动驻车 |
|| Close_AutoHold | lock_doors | `{"action": "auto_hold_off"}` | 关闭自动驻车 |
|| Open_Engine_AutoStop | start_engine | `{"mode": "auto_start_stop"}` | 打开自动启停 |
|| Close_Engine_AutoStop | start_engine | `{"mode": "auto_start_stop_off"}` | 关闭自动启停 |
|| Open_Engine | start_engine | `{}` | 打开引擎 |
|| Close_Engine | stop_engine | `{}` | 关闭引擎 |

## Shared Slot Type Definitions

### Position
```
enum: 主驾, 副驾, 左后, 右后, 全部
resolution: Resolve to specific window zone. Default to 全部.
agents: Vehicle Control Agent, HVAC Agent, Seat Agent
```

### Mode
```
enum: 经济, 舒适, 运动, 雪地, 越野, 节能
resolution: Driving mode. Default to 舒适.
agents: Vehicle Control Agent
```

### Camera
```
enum: 前视, 后视, 左视, 右视, 360°, 行车记录仪, 全景
resolution: Camera view identifier. Default to 360°.
agents: Vehicle Control Agent
```

## Window Position Mapping

|| Position | Windows Affected |
|----------|-----------------|
| 主驾 | Driver side front window |
| 副驾 | Passenger side front window |
| 左后 | Rear left window |
| 右后 | Rear right window |
| 全部 | All four windows |

## Diagonal Ventilation Mode

|| Pattern | Open Windows |
|---------|--------------|
| Left diagonal | Front-left + Rear-right |
| Right diagonal | Front-right + Rear-left |

## Driving Mode Characteristics

|| Mode | Engine Response | Transmission | Fuel Efficiency | Notes |
|------|----------------|--------------|-----------------|-------|
| 经济 | Gentle | Early upshift | Best | Eco driving |
| 舒适 | Normal | Normal | Normal | Default |
| 运动 | Aggressive | Hold gears | Lower | Performance |
| 雪地 | Limited | Start in 2nd | — | Reduce wheel spin |
| 越野 | Maximum | Low gear | — | Off-road traction |

## Camera Views

|| Camera | Description |
|--------|-------------|
| 前视 | Front bumper camera |
| 后视 | Rear camera |
| 左视 | Left side camera |
| 右视 | Right side camera |
| 360° | All four cameras stitched together |
| 行车记录仪 | Front-facing dashcam |
