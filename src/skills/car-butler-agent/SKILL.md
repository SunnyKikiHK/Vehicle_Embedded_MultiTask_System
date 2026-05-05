---
name: car-butler-agent
description: Implements Car Butler Agent intents in the vehicle embedded multi-task system. Handles vehicle health monitoring, maintenance scheduling, car butler services, face recognition, owner services, order management, and trip recording. Use when the user mentions car health, maintenance, service, face recognition, orders, trip, calendar, feedback, or personal center. Trigger terms: 车况, 维保, 预约, 人脸识别, 车主服务, 个人中心, 订单, 途记, 日历, 投诉.
---

# Car Butler Agent — Vehicle Health & Owner Services Skill

## Agent Overview

**Handles:** Vehicle health monitoring, maintenance scheduling, car butler services, face recognition, owner services, order management, and trip recording.
**Note:** Most of these intents are handled through UI interactions or are informational queries. This agent primarily provides information and opens relevant apps/panels.

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

### Vehicle Health

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 车况检查 | system_info | `{"type": "vehicle_health"}` | Query vehicle health status |
| 查看车辆信息 | system_info | `{"type": "vehicle_info"}` | Get basic vehicle information |

### Calendar

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开日历 | system_settings | `{"action": "calendar"}` | Open calendar app |
| 查看今日日程 | today_events | `{}` | View today's calendar events |
| 添加日程 | add_event | `{"title": "<title>", "time": "<time>"}` | Add a calendar event |
| 删除日程 | delete_event | `{"event_id": "<id>"}` | Delete a calendar event |

### Notifications (Feedback/Orders)

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开通知 | show_notification | `{"title": "通知", "content": "<message>"}` | Show a notification |
| 关闭通知 | dismiss_notification | `{}` | Dismiss notification |

## Note on UI-Based Intents

Some intents in this agent (car butler service, personal center, orders, trip recording, feedback) are primarily UI interactions that open dedicated apps or panels. For these, return an appropriate tool that opens the relevant screen, or use `show_notification` to inform the user.

## Slot Resolution Rules

- **Tire**: Check tire pressure and tread depth (via `system_info`)
- **gas**: Check fuel level and range (via `system_info`)
- **range**: Check remaining electric range (for EV/hybrid)
- When **user asks about car health** without specific item, run a full vehicle health check

## Implementation Checklist

When implementing a new Car Butler intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve vehicle health queries, calendar events
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
