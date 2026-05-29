---
name: group-travel-agent
description: Implements Group Travel Agent intents in the vehicle embedded multi-task system. Handles team/group travel features: route sharing, meetup coordination, and group member tracking. Use when the user mentions group travel, team driving, car pool, convoy, meetup, share route, or group location. Trigger terms: 组队, 加入车队, 创建组队, 退出组队, 集结地, 汇合, 成员位置.
---

# Group Travel Agent — Team Travel & Location Sharing Skill

## Agent Overview

**Handles:** Team/group travel features: route sharing, meetup coordination, and group member tracking.
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

### Group Management

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 加入组队 | join_group | `{}` | Join a travel group |
| 创建组队 | build_group | `{}` | Create a new group |
| 退出组队 | quit_group | `{}` | Leave current group |
| 打开组队 | open_group | `{}` | Open group travel interface |

### Meetup

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 设置集结地 | ask_meeting_place | `{}` | Query group meetup location |
| 去汇合地点 | go_meeting_place | `{}` | Navigate to meetup point |

### Location Sharing

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 查看成员位置 | group_member_location | `{}` | View locations of group members |

## Slot Resolution Rules

- **location**: Meeting point or member location. Resolve to GPS coordinates
- **POI**: Named place for meetup
- When **creating a group**, the user becomes the group leader
- When **joining a group**, the user needs a group code or NFC/QR invitation
- When **setting a meetup point**, the group leader nominates a location

## Privacy & Safety Notes

- Group location sharing requires opt-in from all members
- Location data should not be shared with third parties
- Real-time tracking should be disabled when group trip ends

## Implementation Checklist

When implementing a new Group Travel intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve location, POI for meetup
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
