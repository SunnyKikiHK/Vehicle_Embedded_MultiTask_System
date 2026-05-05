# Car Butler Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Check_Car_Condition | system_info | `{"type": "full"}` | 车况检查 |
|| Check_Car_Condition | system_info | `{"type": "tire"}` | 检查轮胎 |
|| Check_Car_Condition | system_info | `{"type": "fuel"}` | 检查油量 |
|| Open_Calendar | system_settings | `{"action": "calendar"}` | 打开日历 |
|| today_events | today_events | `{}` | 查看今日日程 |
|| add_event | add_event | `{"title": "...", "time": "..."}` | 添加日程 |
|| delete_event | delete_event | `{"event_id": "..."}` | 删除日程 |
|| show_notification | show_notification | `{"title": "...", "content": "..."}` | 显示通知 |
|| dismiss_notification | dismiss_notification | `{}` | 关闭通知 |

## Car Condition Check Items

|| Check Item | Normal Range | Warning Threshold | Critical Threshold |
|------------|-------------|-------------------|-------------------|
| Tire Pressure | 2.2-2.5 bar | < 2.0 or > 2.7 | < 1.8 or > 3.0 |
| Fuel Level | > 10% | < 10% | < 5% |
| Battery Voltage | 12.4-13.5V | 12.0-12.3V | < 12.0V |
| Coolant Temp | 80-100°C | 100-105°C | > 105°C |
| Oil Life | > 20% | 10-20% | < 10% |
| Brake Fluid | > 20% | 10-20% | < 10% |

## Maintenance Schedule (Typical)

|| Item | Interval | Warning (Remaining) |
|------|----------|-------------------|
| Oil Change | 10,000 km / 12 months | < 1,000 km or < 1 month |
| Tire Rotation | 10,000 km | < 1,000 km |
| Brake Inspection | 20,000 km | < 2,000 km |
| Air Filter | 20,000 km | < 2,000 km |
| Coolant | 40,000 km / 24 months | < 3,000 km |
| Spark Plugs | 40,000 km | < 4,000 km |
