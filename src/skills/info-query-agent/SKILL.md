---
name: info-query-agent
description: Implements Info Query Agent intents in the vehicle embedded multi-task system. Handles quick informational queries that don't fit other domains: time, location, date, weather basics, air quality, and humidity. This is the fallback agent for vague queries. Use when the user asks about time, date, current location, weather basics, air quality, or humidity. Trigger terms: 现在几点, 今天几号, 星期几, 我在哪, 当前位置, 天气怎么样, 空气质量, 湿度.
---

# Info Query Agent — Quick Informational Queries Skill

## Agent Overview

**Handles:** Quick informational queries that don't fit other domains: time, location, date, weather basics, air quality, and humidity. This is the fallback/default agent for vague queries.
**Total intents: 7**
**Shared slot types:** `location`, `date`

## Core Intent Categories

### Time & Date

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 当前位置查询 | Ask_Where | — | Query current GPS location |
| 查询星期 | Ask_Weekday | — | Query current weekday |
| 查看日期 | Ask_Date | — | Query current date |

### Weather Basics

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开天气 | Open_Weather | — | Open weather widget |

### Air Quality & Environment

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查询空气 | Ask_Air_Condition | location, smog, PM25 | Air quality query |
| 查询湿度 | Ask_Humidity | location, date | Humidity query |
| 查询紫外线 | Query_UV_Level | location, sunscreen | UV index query |

## Slot Resolution Rules

- **location**: Always current GPS location for Info Query Agent. No default fallback.
- **date**: Always "now" for Info Query Agent. No date offset support.
- This agent is the **fallback** — when the router cannot confidently classify an intent into a domain agent, it routes to Info Query Agent with a low confidence score.
- If the query contains enough signal to route elsewhere (e.g., "播放音乐" → Media Agent), this agent should not be selected.

## Intent Disambiguation

When the user gives a vague query, Info Query Agent should attempt to disambiguate:

- "播放" without source → Media Agent
- "导航" without destination → Navigation Agent
- "空调" without action → HVAC Agent

If truly unclassifiable, respond with a helpful default.

## Implementation Checklist

When implementing a new Info Query intent:

1. **Match the intent key** (e.g., `Ask_Where`) to the skill function.
2. **Query system APIs** — GPS, clock, weather service.
3. **Format response** with clear, concise information.
4. **Confirm** with a natural response.
5. **Save SlotContext** to Redis with `agent=Info Query Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
当前位置: "您目前在{road_name}，附近有{poi}，属于{location_area}。"
星期: "今天是{weekday}，{date}。"
日期: "今天是{year}年{month}月{day}日。"
空气质量: "当前空气质量{grade}，PM2.5指数为{value}，{advice}。"
湿度: "当前相对湿度为{humidity}%，{feeling}。"
天气: "当前{weather}，{temperature}度，体感温度{feels_like}度。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
