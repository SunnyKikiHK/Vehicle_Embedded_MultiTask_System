# Vehicle Control Agent — Annotated Examples

## Turn 1 — Open All Windows

**User:** "把车窗都打开"
**Matched Intent:** `open_window`
**Arguments:** `{"position": "全部"}`

**Reconstruction:** "打开全部车窗"

**Action:** Open all four windows simultaneously.
**Response:** "车窗已全部打开。"

---

## Turn 2 — Close Specific Window

**User:** "把主驾车窗关上"
**Matched Intent:** `close_window`
**Arguments:** `{"position": "主驾"}`

**Reconstruction:** "关闭主驾车窗"

**Action:** Close the driver side front window.
**Response:** "主驾车窗已关闭。"

---

## Turn 3 — Set Window to Specific Position

**User:** "副驾窗户开一半"
**Matched Intent:** `window_down`
**Arguments:** `{"position": "副驾", "level": 50}`

**Reconstruction:** "把副驾车窗开一半"

**Action:** Set passenger window to 50% open position.
**Response:** "副驾车窗已开到一半。"

---

## Turn 4 — Open Trunk

**User:** "打开后备箱"
**Matched Intent:** `flash_lights`
**Arguments:** `{"action": "trunk_open"}`

**Reconstruction:** "打开后备箱"

**Action:** Release trunk latch to open.
**Response:** "后备箱已打开。"

---

## Turn 5 — Open Sunroof

**User:** "开一下天窗"
**Matched Intent:** `flash_lights`
**Arguments:** `{"action": "sunroof_open"}`

**Reconstruction:** "打开天窗"

**Action:** Open the sunroof to the last-used position, or fully open if no history.
**Response:** "天窗已打开。"

---

## Turn 6 — Turn On Wipers

**User:** "开雨刷"
**Matched Intent:** `flash_lights`
**Arguments:** `{"action": "wiper_on"}`

**Reconstruction:** "打开雨刷器"

**Action:** Turn on wipers. If rain sensor is available, enable auto mode.
**Response:** "雨刷器已开启。"

---

## Turn 7 — Turn On Headlights

**User:** "开大灯"
**Matched Intent:** `set_headlights`
**Arguments:** `{"mode": "on"}`

**Reconstruction:** "打开大灯"

**Action:** Turn on headlights.
**Response:** "大灯已开启。"

---

## Turn 8 — Unlock/Lock Doors

**User:** "解锁车门"
**Matched Intent:** `unlock_doors`
**Arguments:** `{}`

**Reconstruction:** "解锁车门"

**Action:** Unlock all doors.
**Response:** "车门已解锁。"

---

## Turn 9 — Open 360 Camera

**User:** "打开环视影像"
**Matched Intent:** `open_camera`
**Arguments:** `{"type": "surround_view"}`

**Reconstruction:** "打开360度环视影像"

**Action:** Activate all four surround cameras and display stitched 360° view.
**Response:** "360°环视已开启。"

---

## Turn 10 — Take Photo

**User:** "拍张照"
**Matched Intent:** `screenshot`
**Arguments:** `{"type": "camera"}`

**Reconstruction:** "拍照"

**Action:** Capture a still image from the front dashcam and save to storage.
**Response:** "照片已保存。"

---

## Turn 11 — Start Recording

**User:** "开始录像"
**Matched Intent:** `record_video`
**Arguments:** `{"action": "start"}`

**Reconstruction:** "开始行车记录"

**Action:** Start video recording from dashcam.
**Response:** "行车记录已开启。"

---

## Turn 12 — Turn On Auto Hold

**User:** "打开自动驻车"
**Matched Intent:** `unlock_doors`
**Arguments:** `{"action": "auto_hold_on"}`

**Reconstruction:** "开启自动驻车"

**Action:** Enable auto hold — vehicle will automatically hold brakes when stopped.
**Response:** "自动驻车已开启。"
