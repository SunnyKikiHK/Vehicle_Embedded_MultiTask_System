# HVAC Agent — Annotated Examples

## Turn 1 — Basic Temperature Adjustment

**User:** "把温度调到24度"
**Matched Intent:** `Set_Air_Condition_Temperature`
**Slots extracted:**
- `Number = 24`
- `Position` → inferred as `主驾` (default, single occupant context)
- `Ratio` → not present
- `Extreme` → not present

**Action:** Set HVAC zone `主驾` temperature to 24°C.
**Response:** "已为您将温度调整到24度。"

---

## Turn 2 — Relative Temperature with Coreference

**User:** "再高一点"
**History:** Turn 1 extracted `Temperature=22, Position=主驾`
**Matched Intent:** `Inc_Air_Condition_Temperature`
**Slots extracted:**
- `Position = 主驾` (from history)
- `Ratio = 高一点` → +2 step delta from current 22°C → target 24°C
- `Number` → not present (relative)

**Reconstruction:** "把主驾温度再调高一点"

**Action:** Increment `主驾` temperature by 2 steps (22°C → 24°C).
**Response:** "好的，已将温度调高到24度。"

---

## Turn 3 — Turning Off via Pronoun

**User:** "关掉它"
**History:** Turn 1 was `Open_Air_Condition, Position=主驾`
**Matched Intent:** `Close_Air_Condition`
**Slots extracted:**
- `Position = 主驾` (from history — "它" refers to the AC at 主驾)

**Reconstruction:** "关闭主驾空调"

**Action:** Turn off AC for zone `主驾`.
**Response:** "好的，空调已关闭。"

---

## Turn 4 — Fan Speed Adjustment

**User:** "风力太小了"
**History:** Current fan speed at level 2
**Matched Intent:** `Inc_Air_Condition_Wind`
**Slots extracted:**
- `Position = 全部` (no specific zone mentioned)
- `Ratio = 高一点` → +2 step delta from level 2 → level 4

**Reconstruction:** "把风力调高一点"

**Action:** Increase fan speed from level 2 to level 4 for all zones.
**Response:** "好的，已将风力调高。"

---

## Turn 5 — Defrost with Position

**User:** "前挡风玻璃起雾了"
**Matched Intent:** `Open_Air_Condition_Defog`
**Slots extracted:**
- `Position = 前排` (defog targets front windshield → front zones)

**Reconstruction:** "打开前排空调除雾模式"

**Action:** Enable defrost mode for front windshield + front seats.
**Response:** "已开启除雾模式，请稍候。"

---

## Turn 6 — Quick Mode (Instant Cool)

**User:** "太热了，快降温"
**Matched Intent:** `Open_Cooling_Instant`
**Slots extracted:**
- `Position = 主驾` (default)

**Reconstruction:** "一键降温模式"

**Action:** Set all zones to max cooling (16°C), max fan, AC on, fresh air off.
**Response:** "正在为您快速降温，请稍候。"

---

## Turn 7 — Circulation Mode Switch

**User:** "换外循环"
**History:** AC was on with `内循环` active
**Matched Intent:** `Close_Internal_Circulation` + `Open_External_Circulation`
**Slots extracted:** none (mode switch)

**Reconstruction:** "切换到外循环模式"

**Action:** Close internal recirculation, open external fresh air.
**Response:** "已切换到外循环模式。"

---

## Turn 8 — Query Air Quality

**User:** "现在外面空气质量怎么样？"
**Matched Intent:** `Ask_Air_Condition`
**Slots extracted:**
- `location` → current GPS location (default)
- `date` → now (current time)
- `smog` → implied (yes/no)
- `PM25` → implied (fetch value)

**Reconstruction:** "查询当前位置的空气质量指数"

**Action:** Fetch AQI, PM2.5, smog index for current location.
**Response:** "目前空气质量为良，PM2.5指数为45，可以放心开窗。"

---

## Turn 9 — Temperature Compare

**User:** "北京和上海现在哪个更热？"
**Matched Intent:** `Temp_Compare`
**Slots extracted:**
- `City = ["北京", "上海"]`

**Reconstruction:** "比较北京和上海当前的温度"

**Action:** Query temperature for both cities, return comparison.
**Response:** "北京当前25度，上海28度，上海比北京高3度。"
