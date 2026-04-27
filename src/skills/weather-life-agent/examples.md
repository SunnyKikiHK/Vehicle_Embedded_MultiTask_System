# Weather & Life Agent — Annotated Examples

## Turn 1 — Basic Weather Query

**User:** "今天天气怎么样？"
**Matched Intent:** `Query_Weather`
**Slots extracted:**
- `location` → current GPS city
- `date = 今天`

**Reconstruction:** "查询今天的天气"

**Action:** Query weather API for current city and today's date.
**Response:** "今天北京晴，25度，空气质量良，适合出行。"

---

## Turn 2 — Weather with Location

**User:** "上海明天会下雨吗？"
**Matched Intent:** `Query_Weather`
**Slots extracted:**
- `location = 上海`
- `date = 明天`
- `rain = 是` (implied by "下雨")

**Reconstruction:** "查询上海明天的天气，是否下雨"

**Action:** Query weather API for Shanghai, tomorrow, check rain probability.
**Response:** "上海明天多云转小雨，降水量30%，建议带伞。"

---

## Turn 3 — Clothing Advisory

**User:** "明天出门穿什么？"
**History:** User location known
**Matched Intent:** `Ask_Clothes`
**Slots extracted:**
- `location` → current city
- `date = 明天`

**Reconstruction:** "查询明天的穿衣建议"

**Action:** Query tomorrow's weather, generate clothing recommendation.
**Response:** "明天18度，建议穿薄外套，早晚温差大，可以带件披肩。"

---

## Turn 4 — Car Wash Advisory

**User:** "明天适合洗车吗？"
**Matched Intent:** `Ask_Car_Wash`
**Slots extracted:**
- `location` → current city
- `date = 明天`

**Reconstruction:** "查询明天是否适合洗车"

**Action:** Query tomorrow's weather, check for rain/wash advisories.
**Response:** "明天预报有小雨，不建议洗车。建议后天洗车，天气晴朗。"

---

## Turn 5 — UV Index

**User:** "今天紫外线强吗？"
**Matched Intent:** `Query_UV_Level`
**Slots extracted:**
- `location` → current city
- `date = 今天`

**Reconstruction:** "查询今天紫外线指数"

**Action:** Query UV index for current location.
**Response:** "今天紫外线指数为6，属于较强。建议外出时涂抹防晒霜。"

---

## Turn 6 — License Plate Restriction

**User:** "我的车是京A12345，明天能开吗？"
**Matched Intent:** `Query_Restrictions`
**Slots extracted:**
- `location = 北京` (inferred from license plate)
- `License = 京A12345` → last digit = 5

**Reconstruction:** "查询京A12345明天是否限行"

**Action:** Check restriction rules for Beijing, determine if 5 is restricted tomorrow.
**Response:** "明天是周一，尾号5和0限行。您的车可以正常行驶。"

---

## Turn 7 — Oil Price Query

**User:** "今天油价多少？"
**Matched Intent:** `Oil_Price`
**Slots extracted:** none

**Reconstruction:** "查询今日油价"

**Action:** Query latest fuel price data.
**Response:** "今日油价：92号汽油7.85元/升，95号汽油8.35元/升，0号柴油7.55元/升。"

---

## Turn 8 — Query Weekday

**User:** "今天星期几？"
**Matched Intent:** `Ask_Weekday`
**Slots extracted:** none

**Reconstruction:** "查询今天是星期几"

**Action:** Get current system date, determine weekday.
**Response:** "今天是星期六。"

---

## Turn 9 — Remaining Data Query

**User:** "还有多少流量？"
**Matched Intent:** `Display_Remaining_Flow`
**Slots extracted:** none

**Reconstruction:** "查询本月剩余流量"

**Action:** Query mobile data API for remaining quota.
**Response:** "本月还有3.5GB流量，预计将在15天后到期。"

---

## Turn 10 — Allergy Risk

**User:** "今天过敏风险高吗？"
**Matched Intent:** `Ask_Allergy`
**Slots extracted:**
- `location` → current city
- `date = 今天`

**Reconstruction:** "查询今天过敏风险"

**Action:** Query air quality + pollen data for current location.
**Response:** "今天北京花粉浓度较高，柳絮较多，过敏体质的朋友建议戴口罩。"
