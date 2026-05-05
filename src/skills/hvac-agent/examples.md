# HVAC Agent — Annotated Examples

## Turn 1 — Basic Temperature Adjustment

**User:** "把温度调到24度"
**Matched Intent:** `set_temperature`
**Arguments:** `{"temperature": 24}`

**Action:** Set HVAC temperature to 24°C.
**Response:** "已为您将温度调整到24度。"

---

## Turn 2 — Relative Temperature with Coreference

**User:** "再高一点"
**History:** Previous temperature was 22°C
**Matched Intent:** `set_temperature`
**Arguments:** `{"temperature": 24, "direction": "up"}`

**Reconstruction:** "把温度再调高一点"

**Action:** Increment temperature by 2°C (22°C → 24°C).
**Response:** "好的，已将温度调高到24度。"

---

## Turn 3 — Turning Off via Pronoun

**User:** "关掉它"
**History:** AC was on for main driver
**Matched Intent:** `ac_off`
**Arguments:** `{}`

**Reconstruction:** "关闭空调"

**Action:** Turn off AC.
**Response:** "好的，空调已关闭。"

---

## Turn 4 — Fan Speed Adjustment

**User:** "风力太小了"
**History:** Current fan speed at level 2
**Matched Intent:** `set_fan_speed`
**Arguments:** `{"level": 4, "direction": "up"}`

**Reconstruction:** "把风力调高一点"

**Action:** Increase fan speed from level 2 to level 4.
**Response:** "好的，已将风力调高。"

---

## Turn 5 — Defrost with Position

**User:** "前挡风玻璃起雾了"
**Matched Intent:** `defrost`
**Arguments:** `{"mode": "defog"}`

**Reconstruction:** "打开空调除雾模式"

**Action:** Enable defrost mode for front windshield.
**Response:** "已开启除雾模式，请稍候。"

---

## Turn 6 — Quick Mode (Instant Cool)

**User:** "太热了，快降温"
**Matched Intent:** `ac_on`
**Arguments:** `{"mode": "max_cool"}`

**Reconstruction:** "一键降温模式"

**Action:** Set all zones to max cooling (16°C), max fan.
**Response:** "正在为您快速降温，请稍候。"

---

## Turn 7 — Circulation Mode Switch

**User:** "换外循环"
**History:** AC was on with internal recirculation active
**Matched Intent:** `ac_on`
**Arguments:** `{"mode": "external"}`

**Reconstruction:** "切换到外循环模式"

**Action:** Switch to external fresh air mode.
**Response:** "已切换到外循环模式。"

---

## Turn 8 — Query Air Quality

**User:** "现在外面空气质量怎么样？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "air_quality"}`

**Reconstruction:** "查询当前空气质量"

**Action:** Fetch AQI and PM2.5 for current location.
**Response:** "目前空气质量为良，PM2.5指数为45，可以放心开窗。"

---

## Turn 9 — Temperature Compare

**User:** "北京和上海现在哪个更热？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "temperature_compare", "cities": ["北京", "上海"]}`

**Reconstruction:** "比较北京和上海当前的温度"

**Action:** Query temperature for both cities, return comparison.
**Response:** "北京当前25度，上海28度，上海比北京高3度。"
