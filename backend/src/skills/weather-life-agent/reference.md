# Weather & Life Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Query_Weather | get_weather | `{"location": "...", "date": "..."}` | 天气查询 |
|| Query_Timely_Weather | get_weather | `{"location": "..."}` | 实时查询天气 |
|| Open_Weather | get_weather | `{}` | 打开天气 |
|| Ask_Clothes | get_weather | `{"advisory": "clothing"}` | 查询穿衣 |
|| Ask_Makeup | get_weather | `{"advisory": "makeup"}` | 查询化妆 |
|| Ask_Fishing | get_weather | `{"advisory": "fishing"}` | 查询钓鱼 |
|| Ask_Sport | get_weather | `{"advisory": "sport"}` | 查询运动 |
|| Ask_Travel | get_weather | `{"advisory": "travel"}` | 查询旅游 |
|| Ask_Transport | get_weather | `{"advisory": "transport"}` | 查询交通 |
|| Ask_Cold_Index | get_weather | `{"advisory": "cold_index"}` | 查询感冒 |
|| Ask_Car_Wash | get_weather | `{"advisory": "car_wash"}` | 查询洗车 |
|| Ask_Allergy | get_weather | `{"advisory": "allergy"}` | 查询过敏 |
|| Query_Body_Temperature | get_weather | `{"advisory": "feels_like"}` | 查询体感温度 |
|| Query_UV_Level | get_weather | `{"advisory": "uv_index"}` | 查询紫外线 |
|| Query_Weather | get_forecast | `{"date": "..."}` | 天气预报 |
|| Query_Date | get_weather | `{"type": "oil_price"}` | 油价查询 |
|| Query_Date | get_weather | `{"type": "restriction", "city": "...", "plate": "..."}` | 查询哪天限行 |
|| Query_Restrictions | get_weather | `{"type": "restriction_check"}` | 查询是否限行 |
|| Ask_Weekday | get_weather | `{"type": "weekday"}` | 查询星期 |
|| Ask_Date | get_weather | `{"type": "date"}` | 查看日期 |
|| Display_Remaining_Flow | get_weather | `{"type": "data_remaining"}` | 剩余流量 |
|| Query_Date | get_weather | `{"type": "weather_alert"}` | 天气预警 |

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

|| User Expression | Resolved Date |
|----------------|---------------|
| 今天 | Today |
| 明天 | Tomorrow |
| 后天 | Day after tomorrow |
| 大后天 | 3 days from now |
| 本周几 | Nearest future occurrence of that weekday |
| 具体日期 | Normalized to YYYY-MM-DD |

## Weather Condition Mapping

|| Weather | Icon | Advisory |
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

|| Last Digit | Restricted Day |
|------------|----------------|
| 0, 5 | Monday |
| 1, 6 | Tuesday |
| 2, 7 | Wednesday |
| 3, 8 | Thursday |
| 4, 9 | Friday |

Restrictions apply during peak hours (07:00-20:00) within the 5th Ring Road.
