# Vehicle Control Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 35 | Open_Window | 打开车窗 |
| 62 | Close_Window | 关闭车窗 |
| 61 | Set_Window | 设置车窗 |
| 160 | Open_Window_Diagonal | 打开通风模式 |
| 397 | Close_Window_Diagonal | 关闭通风模式 |
| 97 | Close_Dormer | 关闭天窗 |
| 304 | Open_Dormer | 打开天窗 |
| 106 | Open_Sunshade | 打开遮阳帘 |
| 201 | Close_Sunshade | 关闭遮阳帘 |
| 135 | Open_Trunk | 打开后备箱 |
| 410 | Close_Trunk | 关闭后备箱 |
| 95 | Open_Wiper | 打开雨刷器 |
| 368 | Close_Wiper | 关闭雨刷器 |
| 254 | Open_Headlamp | 打开大灯 |
| 182 | Close_Headlamp | 关闭大灯 |
| 89 | Open_Low_Beam | 打开近光灯 |
| 378 | Close_Low_Beam | 关闭近光灯 |
| 67 | Open_High_Beam | 打开远光灯 |
| 251 | Close_High_Beam | 关闭远光灯 |
| 105 | Open_Front_Fog_Light | 打开前雾灯 |
| 396 | Close_Front_Fog_Light | 关闭前雾灯 |
| 118 | Open_Back_Fog_Light | 打开后雾灯 |
| 29 | Close_Back_Fog_Light | 关闭后雾灯 |
| 105 | Open_Fog_Light | 打开雾灯 |
| 185 | Close_Fog_Light | 关闭雾灯 |
| 381 | Open_Marker_Light | 打开示宽灯 |
| 425 | Close_Marker_Light | 关闭示宽灯 |
| 164 | Open_ADAPTIVE_HEAPLAMP | 打开自动大灯 |
| 345 | Close_ADAPTIVE_HEAPLAMP | 关闭自动大灯 |
| 343 | Open_Surround_View | 打开环绕摄像 |
| 109 | Close_Surround_View | 关闭环绕摄像 |
| 243 | Set_Surround_View | 打开指定摄像头 |
| 200 | Open_DashCam | 打开行车记录仪 |
| 156 | Close_DashCam | 关闭行车记录仪 |
| 6 | Record_Audio | 开始录音 |
| 318 | Stop_Audio | 停止录音 |
| 13 | Record_Video | 开始录像 |
| 343 | Stop_Video | 停止录像 |
| 293 | Take_Photo | 拍照 |
| 52 | Set_Driving_Mode | 设置驾驶模式 |
| 232 | Open_AutoHold | 打开自动驻车 |
| 405 | Close_AutoHold | 关闭自动驻车 |
| 278 | Open_Engine_AutoStop | 打开自动启停 |
| 408 | Close_Engine_AutoStop | 关闭自动启停 |

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

| Position | Windows Affected |
|----------|-----------------|
| 主驾 | Driver side front window |
| 副驾 | Passenger side front window |
| 左后 | Rear left window |
| 右后 | Rear right window |
| 全部 | All four windows |

## Diagonal Ventilation Mode

| Pattern | Open Windows |
|---------|--------------|
| Left diagonal | Front-left + Rear-right |
| Right diagonal | Front-right + Rear-left |

## Driving Mode Characteristics

| Mode | Engine Response | Transmission | Fuel Efficiency | Notes |
|------|----------------|--------------|-----------------|-------|
| 经济 | Gentle | Early upshift | Best | Eco driving |
| 舒适 | Normal | Normal | Normal | Default |
| 运动 | Aggressive | Hold gears | Lower | Performance |
| 雪地 | Limited | Start in 2nd | — | Reduce wheel spin |
| 越野 | Maximum | Low gear | — | Off-road traction |

## Camera Views

| Camera | Description |
|--------|-------------|
| 前视 | Front bumper camera |
| 后视 | Rear camera |
| 左视 | Left side camera |
| 右视 | Right side camera |
| 360° | All four cameras stitched together |
| 行车记录仪 | Front-facing dashcam |
