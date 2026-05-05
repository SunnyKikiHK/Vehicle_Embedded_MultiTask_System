# Info Query Agent — Annotated Examples

## Turn 1 — Query Current Location

**User:** "我现在在哪？"
**Matched Intent:** `ask_where`
**Arguments:** `{}`

**Reconstruction:** "查询当前位置"

**Action:** Get current GPS coordinates, reverse geocode to road name and area.
**Response:** "您目前位于北京市朝阳区东四环中路，远洋天地小区附近。"

---

## Turn 2 — Query Weekday

**User:** "今天星期几？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "weekday"}`

**Reconstruction:** "查询今天是星期几"

**Action:** Get system date, determine weekday.
**Response:** "今天是星期六。"

---

## Turn 3 — Query Date

**User:** "今天几号？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "date"}`

**Reconstruction:** "查询今日日期"

**Action:** Get system date, format as Chinese date string.
**Response:** "今天是2026年4月25日。"

---

## Turn 4 — Query Air Quality

**User:** "外面空气质量怎么样？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "air_quality"}`

**Reconstruction:** "查询当前空气质量"

**Action:** Query air quality API for current location, get AQI, PM2.5, smog level.
**Response:** "当前空气质量为良，AQI指数68，PM2.5浓度45μg/m³，适合户外活动。"

---

## Turn 5 — Query Humidity

**User:** "湿度多少？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "humidity"}`

**Reconstruction:** "查询当前湿度"

**Action:** Query weather service for current humidity.
**Response:** "当前相对湿度为55%，体感舒适。"

---

## Turn 6 — Get Current Weather

**User:** "看一下天气"
**Matched Intent:** `get_weather`
**Arguments:** `{}`

**Reconstruction:** "查看当前天气"

**Action:** Query current weather for location.
**Response:** "当前北京晴，25度，适合出行。"

---

## Turn 7 — Fallback for Vague Query

**User:** "有什么能帮我的？"
**Matched Intent:** (fallback)
**Arguments:** `{}`

**Reconstruction:** "查询可用功能"

**Action:** Return a helpful summary of available voice commands across all agents.
**Response:** "我可以帮您：
- 导航：说'导航到某地'
- 空调：说'打开空调'或'调温度'
- 音乐：说'播放歌曲'
- 电话：说'打电话给某人'
- 天气：说'今天天气怎么样'

请问有什么需要帮助的吗？"
