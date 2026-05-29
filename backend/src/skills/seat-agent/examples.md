# Seat Agent — Annotated Examples

## Turn 1 — Turn On Seat Heating

**User:** "打开主驾座椅加热"
**Matched Intent:** `seat_heating`
**Arguments:** `{"switch": "on", "position": "主驾"}`

**Reconstruction:** "打开主驾座椅加热"

**Action:** Enable seat heating for driver seat at default level 2.
**Response:** "主驾座椅加热已开启。"

---

## Turn 2 — Increase Seat Ventilation

**User:** "副驾通风再高一点"
**History:** 副驾 ventilation at level 1
**Matched Intent:** `seat_ventilation`
**Arguments:** `{"level": 2, "direction": "up", "position": "副驾"}`

**Reconstruction:** "把副驾座椅通风调高一点"

**Action:** Increase 副驾 ventilation from level 1 to level 2.
**Response:** "已将副驾座椅通风调高，当前为2档。"

---

## Turn 3 — Adjust Seat Position

**User:** "座椅往前一点"
**History:** Default position
**Matched Intent:** `adjust_seat`
**Arguments:** `{"direction": "forward", "position": "主驾"}`

**Reconstruction:** "把主驾座椅向前调整"

**Action:** Move driver seat forward by one step.
**Response:** "主驾座椅已向前调整。"

---

## Turn 4 — Turn Off Steering Wheel Heating

**User:** "关掉方向盘加热"
**Matched Intent:** `seat_heating`
**Arguments:** `{"switch": "off", "target": "steering_wheel"}`

**Reconstruction:** "关闭方向盘加热"

**Action:** Turn off steering wheel heating.
**Response:** "方向盘加热已关闭。"

---

## Turn 5 — Fold Mirrors

**User:** "把后视镜收起来"
**Matched Intent:** `adjust_seat`
**Arguments:** `{"target": "mirror", "action": "fold"}`

**Reconstruction:** "折叠后视镜"

**Action:** Fold both side mirrors.
**Response:** "后视镜已折叠。"

---

## Turn 6 — Turn On Seat Massage

**User:** "开个按摩吧"
**History:** Driver seat currently active
**Matched Intent:** `seat_massage`
**Arguments:** `{"switch": "on", "position": "主驾"}`

**Reconstruction:** "打开主驾座椅按摩"

**Action:** Enable seat massage at default level 2.
**Response:** "主驾座椅按摩已开启。"

---

## Turn 7 — Adjust Seat Temperature

**User:** "座椅温度调高一点"
**History:** 主驾 seat heating at level 1
**Matched Intent:** `seat_heating`
**Arguments:** `{"level": 2, "direction": "up", "position": "主驾"}`

**Reconstruction:** "把主驾座椅温度调高一点"

**Action:** Increase seat heating from level 1 to level 2.
**Response:** "主驾座椅温度已调高，当前为2档。"

---

## Turn 8 — Open Mirror Heating

**User:** "后视镜起雾了"
**Matched Intent:** `seat_heating`
**Arguments:** `{"switch": "on", "target": "mirror"}`

**Reconstruction:** "开启后视镜加热"

**Action:** Enable rearview mirror defogger.
**Response:** "后视镜加热已开启，正在除雾。"

---

## Turn 9 — Set Seat Ventilation Level

**User:** "副驾通风调到最大"
**Matched Intent:** `seat_ventilation`
**Arguments:** `{"level": 3, "position": "副驾"}`

**Reconstruction:** "把副驾座椅通风调到最高档"

**Action:** Set 副驾 ventilation to level 3.
**Response:** "已将副驾座椅通风调到最高档。"

---

## Turn 10 — Turn On Rear Heated Seat

**User:** "打开后排座椅加热"
**Matched Intent:** `seat_heating`
**Arguments:** `{"switch": "on", "position": "后排"}`

**Reconstruction:** "打开后排座椅加热"

**Action:** Enable seat heating for all rear seats at default level 2.
**Response:** "后排座椅加热已开启。"
