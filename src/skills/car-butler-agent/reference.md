# Car Butler Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 432 | Check_Car_Condition | 车况检查 |
| 435 | Open_Bulter | 打开车辆管家 |
| 436 | Close_Bulter | 关闭车辆管家 |
| 437 | Reserve_Maintenance | 预约维保 |
| 438 | Cancel_Reserve | 取消预约 |
| 309 | Record_Face | 录入人脸识别 |
| 220 | Open_Owner_Service | 打开车主服务 |
| 239 | Close_Owner_Service | 关闭车主服务 |
| 383 | Open_Personal_Center | 打开个人中心 |
| 34 | Close_Personal_Center | 关闭个人中心 |
| 381 | Complains_And_Suggestions | 投诉与建议 |
| 107 | Open_Feedback | 打开反馈 |
| 394 | Close_Feedback | 关闭反馈 |
| 110 | View_Already_Order | 查看已完成订单 |
| 235 | View_Unend_Order | 查看未完成订单 |
| 414 | View_All_Order | 查看所有订单 |
| 116 | Open_Order_Center | 打开订单中心 |
| 134 | Close_Order_Center | 关闭订单中心 |
| 108 | Open_Record_App | 打开途记软件 |
| 295 | Close_Record_App | 关闭途记软件 |
| 93 | Create_Trip_Record | 新建旅途记录 |
| 92 | Open_Calendar | 打开日历 |
| 10 | Close_Calendar | 关闭日历 |

## Car Condition Check Items

| Check Item | Normal Range | Warning Threshold | Critical Threshold |
|------------|-------------|-------------------|-------------------|
| Tire Pressure | 2.2-2.5 bar | < 2.0 or > 2.7 | < 1.8 or > 3.0 |
| Fuel Level | > 10% | < 10% | < 5% |
| Battery Voltage | 12.4-13.5V | 12.0-12.3V | < 12.0V |
| Coolant Temp | 80-100°C | 100-105°C | > 105°C |
| Oil Life | > 20% | 10-20% | < 10% |
| Brake Fluid | > 20% | 10-20% | < 10% |

## Maintenance Schedule (Typical)

| Item | Interval | Warning (Remaining) |
|------|----------|-------------------|
| Oil Change | 10,000 km / 12 months | < 1,000 km or < 1 month |
| Tire Rotation | 10,000 km | < 1,000 km |
| Brake Inspection | 20,000 km | < 2,000 km |
| Air Filter | 20,000 km | < 2,000 km |
| Coolant | 40,000 km / 24 months | < 3,000 km |
| Spark Plugs | 40,000 km | < 4,000 km |
