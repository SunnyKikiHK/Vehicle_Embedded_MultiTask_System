# Group Travel Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Join_Group | join_group | `{"code": "..."}` | 加入组队 |
|| Build_Group | build_group | `{}` | 创建组队 |
|| Quit_Group | quit_group | `{}` | 退出组队 |
|| Open_Group | open_group | `{}` | 打开组队 |
|| Ask_Meeting_Place | ask_meeting_place | `{"location": "..."}` | 设置集结地 |
|| Go_Meeting_Place | go_meeting_place | `{}` | 去汇合地点 |
|| Group_Member_Location | group_member_location | `{}` | 查看成员位置 |

## Shared Slot Type Definitions

### location
```
resolution: Meeting point GPS coordinates or named POI. Resolve via map service.
agents: Group Travel Agent, Navigation Agent, Weather & Life Agent
```

### POI
```
resolution: Named place for meetup. Match against POI database or use raw text as query.
agents: Group Travel Agent, Navigation Agent
```

## Group Capacity

|| Parameter | Limit |
|-----------|-------|
| Max group size | 10 members |
| Group code length | 6 alphanumeric characters |
| Location update frequency | Every 30 seconds |
| Group history retention | 7 days after trip ends |

## Group States

|| State | Description |
|-------|-------------|
| ACTIVE | Group trip in progress, all features enabled |
| PAUSED | Group paused, location sharing paused |
| ENDED | Trip completed, group archived |

## Invite Methods

|| Method | Description |
|--------|-------------|
| 邀请码 | 6-character alphanumeric code |
| QR Code | Scannable QR from group leader's app |
| NFC | Tap phone to share invite (nearby devices) |
| WeChat/Link | Deep link to join group |
