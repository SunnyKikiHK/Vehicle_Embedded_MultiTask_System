---
name: weather-life-agent
description: Implements Weather & Life Agent intents in the vehicle embedded multi-task system. Handles weather queries, life advisory (clothing, travel, car wash), fuel prices, license plate restrictions, date/time queries, and mobile data management. Use when the user mentions weather, temperature, rain, clothing, travel, car wash, oil price, license plate, date, week, or mobile data. Trigger terms: 天气, 查询, 穿衣, 洗车, 钓鱼, 运动, 紫外线, 油价, 限行, 星期, 日期, 流量.
---

# Weather & Life Agent — Weather, Life Advisory & Data Management Skill

## Agent Overview

**Handles:** Weather queries, life advisory (clothing, travel, car wash), fuel prices, license plate restrictions, date/time queries, and mobile data management.
**Total intents: 30**
**Shared slot types:** `location`, `date`, `sun`, `rain`, `fog`, `City`, `License`

## Core Intent Categories

### Weather Query

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 天气查询 | Query_Weather | location, date, sun, rain, snow, fog, quilt | Query weather conditions |
| 实时查询天气 | Query_Timely_Weather | location | Query real-time weather |
| 打开天气 | Open_Weather | — | Open weather app |
| 关闭天气 | Close_Weather | — | Close weather app |

### Life Advisory

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查询穿衣 | Ask_Clothes | location, date, dressing, scarf, hat, coat, t_shirt | Clothing recommendation |
| 查询化妆 | Ask_Makeup | location, date | Makeup suggestion |
| 查询钓鱼 | Ask_Fishing | location, date | Fishing conditions |
| 查询运动 | Ask_Sport | location, date | Sports conditions |
| 查询旅游 | Ask_Travel | location, date | Travel advisory |
| 查询交通 | Ask_Transport | location, date | Transportation info |
| 查询感冒 | Ask_Cold_Index | location, date | Cold risk index |
| 查询洗车 | Ask_Car_Wash | location, date | Car wash recommendation |
| 查询过敏 | Ask_Allergy | location, date | Allergy risk |
| 查询体感温度 | Query_Body_Temperature | location, date | Feels-like temperature |
| 查询紫外线 | Query_UV_Level | location, date, sunscreen | UV index |

### Vehicle & Life

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 油价查询 | Oil_Price | — | Query fuel prices |
| 查询哪天限行 | Query_Date | City, License | Query license plate restrictions |
| 查询是否限行 | Query_Restrictions | location, date | Check if restricted today |

### Time & Date

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查询星期 | Ask_Weekday | — | Query current weekday |
| 查看日期 | Ask_Date | — | Query current date |

### Mobile Data

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 剩余流量 | Display_Remaining_Flow | — | Check remaining data plan |
| 打开流量 | Open_Flow | — | Enable mobile data |
| 关闭流量 | Close_Flow | — | Disable mobile data |
| 打开流量中心 | Open_Flow_Center | — | Open data management |
| 关闭流量中心 | Close_Flow_Center | — | Close data center |
| 查看流量排名 | Open_APP_Rank | — | View data usage ranking |
| 退出流量排名 | Close_APP_Rank | — | Exit data ranking |

## Slot Resolution Rules

- **location**: City or area name. If omitted, use current GPS location.
- **date**: Day offset or date string. Support "今天", "明天", "后天", or a date. Default to "今天".
- **City**: Standard city name. Used for license plate restriction queries.
- **License**: License plate number string. Extract from user input or prompt.
- **sunscreen**: Boolean — does user need sunscreen recommendation? Inferred from UV + location.
- When **user asks weather without location**, use current GPS location.
- When **user asks about restrictions**, extract license plate from user vehicle profile if not explicitly stated.

## Implementation Checklist

When implementing a new Weather & Life intent:

1. **Match the intent key** (e.g., `Query_Weather`) to the skill function.
2. **Resolve location** — default to current GPS city if not specified.
3. **Resolve date** — support "今天/明天/后天" and absolute dates.
4. **Query external APIs** as needed (weather, fuel price, restriction data).
5. **Confirm** with a natural response (e.g., "今天北京晴，25度，适合洗车").
6. **Save SlotContext** to Redis with `agent=Weather & Life Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
天气: "今天{location}{weather}，{temperature}度，{additional_info}。"
穿衣: "今天{location}{temperature}度，建议{wearing_advice}。"
洗车: "{result}: {reason}。"
限行: "{date}{city}限行尾号{尾号}。"
油价: "今日油价：92号{price_92}元/升，95号{price_95}元/升。"
流量: "本月剩余流量{remaining}GB。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
