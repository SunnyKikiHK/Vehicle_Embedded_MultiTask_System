# Vehicle Control Agent — Annotated Examples

## Turn 1 — Open All Windows

**User:** "把车窗都打开"
**Matched Intent:** `Open_Window`
**Slots extracted:**
- `Position = 全部`

**Reconstruction:** "打开全部车窗"

**Action:** Open all four windows simultaneously.
**Response:** "车窗已全部打开。"

---

## Turn 2 — Close Specific Window

**User:** "把主驾车窗关上"
**Matched Intent:** `Close_Window`
**Slots extracted:**
- `Position = 主驾`

**Reconstruction:** "关闭主驾车窗"

**Action:** Close the driver side front window.
**Response:** "主驾车窗已关闭。"

---

## Turn 3 — Set Window to Specific Position

**User:** "副驾窗户开一半"
**Matched Intent:** `Set_Window`
**Slots extracted:**
- `Position = 副驾`
- `Ratio = 50%` (half)

**Reconstruction:** "把副驾车窗开一半"

**Action:** Set passenger window to 50% open position.
**Response:** "副驾车窗已开到一半。"

---

## Turn 4 — Open Trunk

**User:** "打开后备箱"
**Matched Intent:** `Open_Trunk`
**Slots extracted:** none

**Reconstruction:** "打开后备箱"

**Action:** Release trunk latch to open.
**Response:** "后备箱已打开。"

---

## Turn 5 — Open Sunroof

**User:** "开一下天窗"
**Matched Intent:** `Open_Dormer`
**Slots extracted:** none

**Reconstruction:** "打开天窗"

**Action:** Open the sunroof to the last-used position, or fully open if no history.
**Response:** "天窗已打开。"

---

## Turn 6 — Turn On Wipers

**User:** "开雨刷"
**Matched Intent:** `Open_Wiper`
**Slots extracted:** none

**Reconstruction:** "打开雨刷器"

**Action:** Turn on wipers. If rain sensor is available, enable auto mode; otherwise use normal speed.
**Response:** "雨刷器已开启。"

---

## Turn 7 — Turn On Headlights

**User:** "开大灯"
**Matched Intent:** `Open_Headlamp`
**Slots extracted:** none

**Reconstruction:** "打开大灯"

**Action:** Turn on the main headlights (both high and low beam off, but the system is armed). Actually, `Open_Headlamp` typically means the position/drl lights. Use `Open_Low_Beam` for actual low beam.
**Response:** "大灯已开启。"

---

## Turn 8 — Switch Driving Mode

**User:** "切换到运动模式"
**Matched Intent:** `Set_Driving_Mode`
**Slots extracted:**
- `Mode = 运动`

**Reconstruction:** "切换驾驶模式为运动模式"

**Action:** Switch driving mode to sport — more aggressive throttle response, hold gears longer.
**Response:** "驾驶模式已切换到运动模式。"

---

## Turn 9 — Open 360 Camera

**User:** "打开环视影像"
**Matched Intent:** `Open_Surround_View`
**Slots extracted:** none

**Reconstruction:** "打开360度环视影像"

**Action:** Activate all four surround cameras and display stitched 360° view on the head unit.
**Response:** "360°环视已开启。"

---

## Turn 10 — Take Photo

**User:** "拍张照"
**Matched Intent:** `Take_Photo`
**Slots extracted:** none

**Reconstruction:** "拍照"

**Action:** Capture a still image from the front dashcam and save to storage.
**Response:** "照片已保存。"

---

## Turn 11 — Turn On Auto Hold

**User:** "打开自动驻车"
**Matched Intent:** `Open_AutoHold`
**Slots extracted:** none

**Reconstruction:** "开启自动驻车"

**Action:** Enable auto hold — vehicle will automatically hold brakes when stopped.
**Response:** "自动驻车已开启。"

---

## Turn 12 — Open Fog Lights

**User:** "开雾灯"
**Matched Intent:** `Open_Fog_Light`
**Slots extracted:** none

**Reconstruction:** "打开雾灯"

**Action:** Turn on both front and rear fog lights.
**Response:** "雾灯已开启。"

---

## Turn 13 — Close All Windows

**User:** "把窗户都关上"
**Matched Intent:** `Close_Window`
**Slots extracted:**
- `Position = 全部`

**Reconstruction:** "关闭全部车窗"

**Action:** Close all four windows.
**Response:** "车窗已全部关闭。"
