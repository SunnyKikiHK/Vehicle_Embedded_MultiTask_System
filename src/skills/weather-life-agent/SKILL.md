---
name: weather-life-agent
description: Implements Weather & Life Agent intents in the vehicle embedded multi-task system. Handles weather queries, life advisory (clothing, travel, car wash), fuel prices, license plate restrictions, date/time queries, and mobile data management. Use when the user mentions weather, temperature, rain, clothing, travel, car wash, oil price, license plate, date, week, or mobile data. Trigger terms: 天气, 查询, 穿衣, 洗车, 钓鱼, 运动, 紫外线, 油价, 限行, 星期, 日期, 流量.
---

# Weather & Life Agent — Weather, Life Advisory & Data Management Skill

## Agent Overview

**Handles:** Weather queries, life advisory (clothing, travel, car wash), fuel prices, license plate restrictions, date/time queries, and mobile data management.
## Expected Output Format

The LLM should return a JSON object with the following structure:

```json
{
  "reasoning": "Brief explanation of why this tool was selected",
  "tool_name": "actual_mcp_tool_name",
  "arguments": {
    "slot_name_1": "slot_value_1",
    "slot_name_2": "slot_value_2",
    ...
  }
}
```

If no arguments are needed, use an empty object `{}`.

## Core Intent Categories

### Weather Query

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 天气查询 | get_weather | `{"location": "<location>", "date": "<date>"}` | Query weather conditions |
| 天气预报 | get_forecast | `{"location": "<location>", "date": "<date>"}` | Query weather forecast |
| 天气预警 | weather_alert | `{"location": "<location>"}` | Get weather alerts |
| 打开天气 | get_weather | `{}` | Open weather app and show current weather |

### Life Advisory

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 查询穿衣 | get_weather | `{"location": "<location>", "advisory": "clothing"}` | Clothing recommendation |
| 查询洗车 | get_weather | `{"location": "<location>", "advisory": "car_wash"}` | Car wash recommendation |
| 查询紫外线 | get_weather | `{"location": "<location>", "advisory": "uv_index"}` | UV index query |

### Vehicle & Life

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 油价查询 | get_weather | `{"type": "oil_price"}` | Query fuel prices |
| 查询限行 | get_weather | `{"type": "restriction", "city": "<City>", "plate": "<License>"}` | Query license plate restrictions |

### Time & Date

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 查询星期 | get_weather | `{"type": "weekday"}` | Query current weekday |
| 查看日期 | get_weather | `{"type": "date"}` | Query current date |

## Slot Resolution Rules

- **location**: City or area name. If omitted, use current GPS location
- **date**: One of: `今天`, `明天`, `后天`, `大后天`, `昨天`, `前天`, `本周`, `下周`, `周末`, `工作日`. Default to `今天`
- **City**: Standard city name. Used for license plate restriction queries
- **License**: License plate number string. Extract from user input or prompt
- When **user asks weather without location**, use current GPS location

## Implementation Checklist

When implementing a new Weather & Life intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve location, date
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
