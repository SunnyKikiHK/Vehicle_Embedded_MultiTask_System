# Weather & Life Agent — Annotated Examples

## Turn 1 — Basic Weather Query

**User:** "今天天气怎么样？"
**Matched Intent:** `get_weather`
**Arguments:** `{"date": "今天"}`

**Reconstruction:** "查询今天的天气"

**Action:** Query weather API for current city and today's date.
**Response:** "今天北京晴，25度，空气质量良，适合出行。"

---

## Turn 2 — Weather with Location

**User:** "上海明天会下雨吗？"
**Matched Intent:** `get_weather`
**Arguments:** `{"location": "上海", "date": "明天", "detail": "rain"}`

**Reconstruction:** "查询上海明天的天气，是否下雨"

**Action:** Query weather API for Shanghai, tomorrow, check rain probability.
**Response:** "上海明天多云转小雨，降水量30%，建议带伞。"

---

## Turn 3 — Clothing Advisory

**User:** "明天出门穿什么？"
**History:** User location known
**Matched Intent:** `get_weather`
**Arguments:** `{"date": "明天", "advisory": "clothing"}`

**Reconstruction:** "查询明天的穿衣建议"

**Action:** Query tomorrow's weather, generate clothing recommendation.
**Response:** "明天18度，建议穿薄外套，早晚温差大，可以带件披肩。"

---

## Turn 4 — Car Wash Advisory

**User:** "明天适合洗车吗？"
**Matched Intent:** `get_weather`
**Arguments:** `{"date": "明天", "advisory": "car_wash"}`

**Reconstruction:** "查询明天是否适合洗车"

**Action:** Query tomorrow's weather, check for rain/wash advisories.
**Response:** "明天预报有小雨，不建议洗车。建议后天洗车，天气晴朗。"

---

## Turn 5 — UV Index

**User:** "今天紫外线强吗？"
**Matched Intent:** `get_weather`
**Arguments:** `{"advisory": "uv_index"}`

**Reconstruction:** "查询今天紫外线指数"

**Action:** Query UV index for current location.
**Response:** "今天紫外线指数为6，属于较强。建议外出时涂抹防晒霜。"

---

## Turn 6 — Weather Forecast

**User:** "这周末天气怎么样？"
**Matched Intent:** `get_forecast`
**Arguments:** `{"date": "周末"}`

**Reconstruction:** "查询这周末的天气预报"

**Action:** Query weather forecast for the weekend.
**Response:** "周六晴，28度；周日多云，26度，适宜出行。"

---

## Turn 7 — Weather Alert

**User:** "有没有天气预警？"
**Matched Intent:** `weather_alert`
**Arguments:** `{}`

**Reconstruction:** "查询天气预警"

**Action:** Query for any active weather alerts.
**Response:** "当前无天气预警。"

---

## Turn 8 — Query Weekday

**User:** "今天星期几？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "weekday"}`

**Reconstruction:** "查询今天是星期几"

**Action:** Get current system date, determine weekday.
**Response:** "今天是星期六。"

---

## Turn 9 — Date Query

**User:** "今天几号？"
**Matched Intent:** `get_weather`
**Arguments:** `{"type": "date"}`

**Reconstruction:** "查询今天是几号"

**Action:** Get current date.
**Response:** "今天是2026年5月3日。"
