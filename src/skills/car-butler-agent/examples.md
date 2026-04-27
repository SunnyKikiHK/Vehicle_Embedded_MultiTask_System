# Car Butler Agent — Annotated Examples

## Turn 1 — Check Vehicle Health

**User:** "检查一下车况"
**Matched Intent:** `Check_Car_Condition`
**Slots extracted:**
- `total` → full check (all items)

**Reconstruction:** "进行全面车况检查"

**Action:** Query all vehicle health indicators via CAN bus.
**Response:** "车况检查完成：\n- 轮胎：正常，前胎2.3bar，后胎2.4bar\n- 油量：剩余40%，约可行驶320公里\n- 总里程：28,500公里\n- 电瓶：正常，12.8V\n- 下次保养：还有3,000公里，建议3个月后保养\n\n车况良好，请放心行驶。"

---

## Turn 2 — Check Specific Item

**User:** "轮胎怎么样？"
**Matched Intent:** `Check_Car_Condition`
**Slots extracted:**
- `Tire` → tire check only

**Reconstruction:** "检查轮胎状况"

**Action:** Query tire pressure and tread depth from TPMS.
**Response:** "轮胎状况：\n- 左前：2.3bar，胎纹深度8.2mm\n- 右前：2.4bar，胎纹深度8.0mm\n- 左后：2.3bar，胎纹深度7.8mm\n- 右后：2.4bar，胎纹深度7.9mm\n\n轮胎状态良好。"

---

## Turn 3 — Book Maintenance

**User:** "预约下周的保养"
**Matched Intent:** `Reserve_Maintenance`
**Slots extracted:**
- `date = 下周` (or specific date)

**Reconstruction:** "预约下周保养服务"

**Action:** Check available slots, book appointment, confirm with user.
**Response:** "已为您预约下周三上午10点的保养服务。请问需要选择哪些保养项目？"

---

## Turn 4 — Cancel Appointment

**User:** "取消保养预约"
**History:** Active maintenance appointment
**Matched Intent:** `Cancel_Reserve`
**Slots extracted:** none

**Reconstruction:** "取消保养预约"

**Action:** Cancel the booked appointment, release slot.
**Response:** "保养预约已取消。如需重新预约，请告诉我。"

---

## Turn 5 — Face Recognition Enrollment

**User:** "录入人脸"
**Matched Intent:** `Record_Face`
**Slots extracted:** none

**Reconstruction:** "开始录入人脸识别"

**Action:** Launch face enrollment process, guide user to position face correctly.
**Response:** "请将面部对准摄像头，保持自然表情，距离约30厘米。录入完成后将自动保存。"

---

## Turn 6 — View Pending Orders

**User:** "看看我有什么订单"
**Matched Intent:** `View_Unend_Order`
**Slots extracted:** none

**Reconstruction:** "查看未完成的订单"

**Action:** Query order management system for pending orders.
**Response:** "您有2个未完成订单：\n1. 保养服务 — 已预约3月15日\n2. 洗车服务 — 已预约3月10日"

---

## Turn 7 — Submit Feedback

**User:** "提个建议"
**Matched Intent:** `Complains_And_Suggestions`
**Slots extracted:** none

**Reconstruction:** "提交投诉与建议"

**Action:** Open feedback form, prompt user for details.
**Response:** "感谢您的反馈。请告诉我您的建议或意见，我将转达给相关部门。"

---

## Turn 8 — Open Trip Recording

**User:** "开始记录行程"
**Matched Intent:** `Create_Trip_Record`
**Slots extracted:** none

**Reconstruction:** "新建旅途记录"

**Action:** Initialize a new trip recording session with GPS tracking.
**Response:** "旅途记录已启动。行程结束后请说'结束行程'来保存记录。"

---

## Turn 9 — Check Fuel/Range

**User:** "还能跑多远？"
**Matched Intent:** `Check_Car_Condition`
**Slots extracted:**
- `gas` → fuel/range check

**Reconstruction:** "查询剩余续航里程"

**Action:** Query fuel level and calculate remaining range.
**Response:** "当前剩余燃油约40%，预计可行驶320公里。建议在油量低于15%前加油。"
