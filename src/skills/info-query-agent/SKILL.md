---
name: info-query-agent
description: Implements Info Query Agent intents in the vehicle embedded multi-task system. Handles quick informational queries that don't fit other domains: time, location, date, weather basics, air quality, and humidity. This is the fallback agent for vague queries. Use when the user asks about time, date, current location, weather basics, air quality, or humidity. Trigger terms: 现在几点, 今天几号, 星期几, 我在哪, 当前位置, 天气怎么样, 空气质量, 湿度.
---

# Info Query Agent — Quick Informational Queries Skill

## Agent Overview

**Handles:** Quick informational queries that don't fit other domains: time, location, date, weather basics, air quality, and humidity. This is the fallback/default agent for vague queries.
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

### Time & Date

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 当前位置查询 | ask_where | `{}` | Query current GPS location |
| 查询星期 | get_weather | `{"type": "weekday"}` | Query current weekday |
| 查看日期 | get_weather | `{"type": "date"}` | Query current date |

### Weather Basics

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 查询天气 | get_weather | `{}` | Get current weather |
| 查询空气质量 | get_weather | `{"type": "air_quality"}` | Get air quality info |
| 查询湿度 | get_weather | `{"type": "humidity"}` | Get humidity info |

## Slot Resolution Rules

- **location**: Always current GPS location for Info Query Agent. No default fallback
- **date**: Always "now" for Info Query Agent. No date offset support
- This agent is the **fallback** — when the router cannot confidently classify an intent, it routes here with low confidence

## Intent Disambiguation

When the user gives a vague query, Info Query Agent should attempt to disambiguate:

- "播放" without source → Media Agent
- "导航" without destination → Navigation Agent
- "空调" without action → HVAC Agent

If truly unclassifiable, respond with a helpful default.

## Implementation Checklist

When implementing a new Info Query intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve location, date for queries
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
