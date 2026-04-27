# Weather & Life Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 194 | Query_Weather | 天气查询 |
| 200 | Query_Weather | 天气查询 (duplicate ID) |
| 120 | Query_Timely_Weather | 实时查询天气 |
| 402 | Open_Weather | 打开天气 |
| 187 | Close_Weather | 关闭天气 |
| 154 | Ask_Clothes | 查询穿衣 |
| 173 | Ask_Makeup | 查询化妆 |
| 157 | Ask_Fishing | 查询钓鱼 |
| 212 | Ask_Sport | 查询运动 |
| 231 | Ask_Travel | 查询旅游 |
| 303 | Ask_Transport | 查询交通 |
| 127 | Ask_Cold_Index | 查询感冒 |
| 191 | Ask_Car_Wash | 查询洗车 |
| 372 | Ask_Allergy | 查询过敏 |
| 181 | Query_Body_Temperature | 查询体感温度 |
| 209 | Query_UV_Level | 查询紫外线 |
| 197 | Query_Date | 查询哪天限行 |
| 259 | Query_Restrictions | 查询是否限行 |
| 226 | Ask_Weekday | 查询星期 |
| 324 | Ask_Date | 查看日期 |
| 225 | Display_Remaining_Flow | 剩余流量 |
| 187 | Open_Flow | 打开流量 |
| 203 | Close_Flow | 关闭流量 |
| 358 | Open_Flow_Center | 打开流量中心 |
| 283 | Close_Flow_Center | 关闭流量中心 |
| 242 | Open_APP_Rank | 查看流量排名 |
| 226 | Close_APP_Rank | 退出流量排名 |

## Shared Slot Type Definitions

### location
```
resolution: City or area name. Use GPS city if omitted. Support synonyms (北京/北京市).
agents: Weather & Life Agent, Navigation Agent, HVAC Agent
```

### date
```
value_range: today, tomorrow, day after, or YYYY-MM-DD format
resolution: Normalize to date string. Support "今天/明天/后天/大后天".
agents: Weather & Life Agent, HVAC Agent
```

### City
```
resolution: Standard city name. Map regional names to official names.
agents: Weather & Life Agent, Navigation Agent
```

### License
```
value_range: License plate string (e.g., 京A12345, 沪B88888)
resolution: Extract from user input or vehicle profile. Validate format.
agents: Weather & Life Agent
```

## Date Offset Resolution

| User Expression | Resolved Date |
|----------------|---------------|
| 今天 | Today |
| 明天 | Tomorrow |
| 后天 | Day after tomorrow |
| 大后天 | 3 days from now |
| 本周几 | Nearest future occurrence of that weekday |
| 具体日期 | Normalized to YYYY-MM-DD |

## Weather Condition Mapping

| Weather | Icon | Advisory |
|---------|------|----------|
| 晴 | ☀️ | Good for outdoor activities |
| 多云 | ⛅ | Normal conditions |
| 阴 | ☁️ | Might rain, check forecast |
| 小雨/中雨/大雨 | 🌧️ | Bring umbrella, avoid car wash |
| 雷阵雨 | ⛈️ | Stay indoors, avoid driving |
| 雪 | ❄️ | Drive carefully, check roads |
| 雾 | 🌫️ | Low visibility, use fog lights |
| 霾 | 🌫️ | Air quality poor, close recirculation |

## License Plate Restriction Rules (Beijing Example)

| Last Digit | Restricted Day |
|------------|----------------|
| 0, 5 | Monday |
| 1, 6 | Tuesday |
| 2, 7 | Wednesday |
| 3, 8 | Thursday |
| 4, 9 | Friday |

Restrictions apply during peak hours (07:00-20:00) within the 5th Ring Road.
