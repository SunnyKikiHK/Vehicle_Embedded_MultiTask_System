# Phone Agent — Annotated Examples

## Turn 1 — Call Contact by Name

**User:** "给张三打个电话"
**Matched Intent:** `Call_Phone_By_Contact`
**Slots extracted:**
- `Contact = 张三`

**Reconstruction:** "拨打张三的电话"

**Action:** Search contact "张三", get primary number (手机 label), initiate call.
**Response:** "正在拨打张三的手机。"

---

## Turn 2 — Call with Specific Label

**User:** "给李四打公司电话"
**Matched Intent:** `Call_Phone_By_Contact_Label`
**Slots extracted:**
- `Contact = 李四`
- `label = 公司`

**Reconstruction:** "拨打李四的公司电话"

**Action:** Search contact "李四", get company number, initiate call.
**Response:** "正在拨打李四的公司电话。"

---

## Turn 3 — Dial a Number Directly

**User:** "拨打 010-1234-5678"
**Matched Intent:** `Call_Number`
**Slots extracted:**
- `Phone_Number = 01012345678`

**Reconstruction:** "拨打 010-1234-5678"

**Action:** Dial the specified number directly.
**Response:** "正在拨打 010-1234-5678。"

---

## Turn 4 — Answer Incoming Call

**User:** "接听"
**History:** Incoming call from 王五
**Matched Intent:** `Answer_Phone`
**Slots extracted:** none

**Reconstruction:** "接听来电"

**Action:** Answer the incoming call.
**Response:** "已接听来电。"

---

## Turn 5 — Reject Call

**User:** "拒接"
**History:** Incoming call
**Matched Intent:** `Reject_Phone`
**Slots extracted:** none

**Reconstruction:** "拒接来电"

**Action:** Reject the incoming call.
**Response:** "已拒接来电。"

---

## Turn 6 — End Current Call

**User:** "挂断"
**History:** Active call
**Matched Intent:** `Quit_Phone`
**Slots extracted:** none

**Reconstruction:** "结束通话"

**Action:** Terminate the current call.
**Response:** "通话已结束。"

---

## Turn 7 — Call Back Last Missed Call

**User:** "回拨"
**History:** Last missed call from 赵六
**Matched Intent:** `Call_Back`
**Slots extracted:** none

**Reconstruction:** "回拨上一个未接来电"

**Action:** Retrieve last missed call number, initiate call.
**Response:** "正在回拨赵六。"

---

## Turn 8 — Emergency Call

**User:** "拨打紧急电话"
**Matched Intent:** `Call_Emergency`
**Slots extracted:**
- `Emergency` → defaults to `110` (police, most common vehicle emergency)

**Reconstruction:** "拨打紧急电话"

**Action:** Initiate emergency call. Note: user should confirm intent for safety.
**Response:** "正在拨打紧急电话。"

---

## Turn 9 — Toggle Bluetooth

**User:** "开蓝牙"
**Matched Intent:** `Open_Bluetooth`
**Slots extracted:** none

**Reconstruction:** "开启蓝牙"

**Action:** Enable Bluetooth adapter.
**Response:** "蓝牙已开启，正在搜索已配对设备。"

---

## Turn 10 — Enable Hotspot

**User:** "打开热点"
**Matched Intent:** `Open_Spot`
**Slots extracted:** none

**Reconstruction:** "开启WiFi热点"

**Action:** Enable the vehicle's WiFi hotspot.
**Response:** "热点已开启。请在手机上连接该热点。"

---

## Turn 11 — View Missed Calls

**User:** "看看谁打过电话"
**Matched Intent:** `View_Not_Call`
**Slots extracted:** none

**Reconstruction:** "查看未接来电"

**Action:** Retrieve missed call log, present as numbered list.
**Response:** "您有3个未接来电：1. 王五，2. 李四，3. 赵六。"
