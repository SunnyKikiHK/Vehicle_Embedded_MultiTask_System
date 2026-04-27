---
name: group-travel-agent
description: Implements Group Travel Agent intents in the vehicle embedded multi-task system. Handles team/group travel features: route sharing, meetup coordination, and group member tracking. Use when the user mentions group travel, team driving, car pool, convoy, meetup, share route, or group location. Trigger terms: 组队, 加入车队, 创建组队, 退出组队, 集结地, 汇合, 成员位置.
---

# Group Travel Agent — Team Travel & Location Sharing Skill

## Agent Overview

**Handles:** Team/group travel features: route sharing, meetup coordination, and group member tracking.
**Total intents: 7**
**Shared slot types:** `location`, `POI`

## Core Intent Categories

### Group Management

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 加入组队 | Join_Group | — | Join a travel group |
| 创建组队 | Build_Group | — | Create a new group |
| 退出组队 | Quit_Group | — | Leave current group |
| 打开组队 | Open_Group | — | Open group travel interface |

### Meetup

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置集结地 | Ask_Meeting_Place | — | Query group meetup location |
| 去汇合地点 | Go_Meeting_Place | — | Navigate to meetup point |

### Location Sharing

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查看成员位置 | Group_Member_Location | — | View locations of group members |

## Slot Resolution Rules

- **location**: Meeting point or member location. Resolve to GPS coordinates.
- **POI**: Named place for meetup.
- When **creating a group**, the user becomes the group leader and can invite others.
- When **joining a group**, the user needs a group code or NFC/QR invitation.
- When **setting a meetup point**, the group leader nominates a location and all members are notified.
- All location sharing requires explicit user consent.

## Implementation Checklist

When implementing a new Group Travel intent:

1. **Match the intent key** (e.g., `Build_Group`) to the skill function.
2. **Execute the action** via the group travel service API.
3. **Confirm** with a natural response (e.g., "车队已创建，请分享邀请码给队友").
4. **Save SlotContext** to Redis with `agent=Group Travel Agent`, `intent=<matched_intent>`, and extracted slots.

## Privacy & Safety Notes

- Group location sharing requires opt-in from all members.
- Location data should not be shared with third parties.
- Real-time tracking should be disabled when group trip ends.

## Response Templates

```
创建组队: "车队已创建，您的邀请码是{code}，请分享给队友。"
加入组队: "已成功加入车队，当前车队共{member_count}人。"
退出组队: "已退出车队，期待下次同行。"
设置集结地: "已设置汇合地点为{location}，已通知所有队员。"
去汇合点: "正在导航到汇合地点{location}，距离约{distance}公里。"
查看位置: "车队成员位置：\n- 张三：距您{dist}公里，前方\n- 李四：距您{dist}公里，左后方"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
