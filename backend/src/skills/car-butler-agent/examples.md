# Car Butler Agent — Annotated Examples

## Turn 1 — Check Vehicle Health

**User:** "检查一下车况"
**Matched Intent:** `system_info`
**Arguments:** `{"type": "vehicle_health"}`

**Reconstruction:** "进行全面车况检查"

**Action:** Query all vehicle health indicators via CAN bus.
**Response:** "车况检查完成：
- 轮胎：正常，前胎2.3bar，后胎2.4bar
- 油量：剩余40%，约可行驶320公里
- 总里程：28,500公里
- 电瓶：正常，12.8V
- 下次保养：还有3,000公里，建议3个月后保养

车况良好，请放心行驶。"

---

## Turn 2 — Check Specific Item

**User:** "轮胎怎么样？"
**Matched Intent:** `system_info`
**Arguments:** `{"type": "tire"}`

**Reconstruction:** "检查轮胎状况"

**Action:** Query tire pressure and tread depth from TPMS.
**Response:** "轮胎状况：
- 左前：2.3bar，胎纹深度8.2mm
- 右前：2.4bar，胎纹深度8.0mm
- 左后：2.3bar，胎纹深度7.8mm
- 右后：2.4bar，胎纹深度7.9mm

轮胎状态良好。"

---

## Turn 3 — Check Fuel/Range

**User:** "还能跑多远？"
**Matched Intent:** `system_info`
**Arguments:** `{"type": "fuel_range"}`

**Reconstruction:** "查询剩余续航里程"

**Action:** Query fuel level and calculate remaining range.
**Response:** "当前剩余燃油约40%，预计可行驶320公里。建议在油量低于15%前加油。"

---

## Turn 4 — View Vehicle Info

**User:** "查看车辆信息"
**Matched Intent:** `system_info`
**Arguments:** `{"type": "vehicle_info"}`

**Reconstruction:** "查询车辆基本信息"

**Action:** Query vehicle information (model, plate, odometer).
**Response:** "车辆信息：
- 车型：某车型2024款
- 车牌：京A12345
- 总里程：28,500公里"

---

## Turn 5 — Show Notification

**User:** (system notification display)
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "保养提醒", "content": "您的预约保养时间到了"}`

**Reconstruction:** 显示保养提醒通知

**Action:** Display a notification to the user.
**Response:** (notification appears on screen)

---

## Turn 6 — Dismiss Notification

**User:** "知道了"
**History:** Notification displayed
**Matched Intent:** `dismiss_notification`
**Arguments:** `{}`

**Reconstruction:** "关闭通知"

**Action:** Dismiss the current notification.
**Response:** (notification dismissed)
