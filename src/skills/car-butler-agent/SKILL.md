---
name: car-butler-agent
description: Implements Car Butler Agent intents in the vehicle embedded multi-task system. Handles vehicle health monitoring, maintenance scheduling, car butler services, face recognition, owner services, order management, and trip recording. Use when the user mentions car health, maintenance, service, face recognition, orders, trip, calendar, feedback, or personal center. Trigger terms: 车况, 维保, 预约, 人脸识别, 车主服务, 个人中心, 订单, 途记, 日历, 投诉.
---

# Car Butler Agent — Vehicle Health & Owner Services Skill

## Agent Overview

**Handles:** Vehicle health monitoring, maintenance scheduling, car butler services, face recognition, owner services, order management, and trip recording.
**Total intents: 24**
**No shared slot types required.**

## Core Intent Categories

### Vehicle Health

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 车况检查 | Check_Car_Condition | Tire, gas, range, total, Maintenance | Query vehicle health status |

### Car Butler Service

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开车辆管家 | Open_Bulter | — | Open car butler service |
| 关闭车辆管家 | Close_Bulter | — | Close car butler service |
| 预约维保 | Reserve_Maintenance | — | Book maintenance appointment |
| 取消预约 | Cancel_Reserve | — | Cancel maintenance appointment |

### Identity & Profile

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 录入人脸识别 | Record_Face | — | Register face for driver profile |
| 打开个人中心 | Open_Personal_Center | — | Open personal center |
| 关闭个人中心 | Close_Personal_Center | — | Close personal center |

### Owner Services

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开车主服务 | Open_Owner_Service | — | Open owner services |
| 关闭车主服务 | Close_Owner_Service | — | Close owner services |
| 打开反馈 | Open_Feedback | — | Open feedback form |
| 关闭反馈 | Close_Feedback | — | Close feedback form |
| 投诉与建议 | Complains_And_Suggestions | — | File complaint or suggestion |

### Order Management

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查看已完成订单 | View_Already_Order | — | View completed orders |
| 查看未完成订单 | View_Unend_Order | — | View pending orders |
| 查看所有订单 | View_All_Order | — | View all orders |
| 打开订单中心 | Open_Order_Center | — | Open order center |
| 关闭订单中心 | Close_Order_Center | — | Close order center |

### Trip Recording

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开途记软件 | Open_Record_App | — | Open trip recording app |
| 关闭途记软件 | Close_Record_App | — | Close trip recording app |
| 新建旅途记录 | Create_Trip_Record | — | Start a new trip record |

### Calendar

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开日历 | Open_Calendar | — | Open calendar |
| 关闭日历 | Close_Calendar | — | Close calendar |

## Slot Resolution Rules

- **Tire**: Check tire pressure and tread depth.
- **gas**: Check fuel level and range.
- **range**: Check remaining electric range (for EV/hybrid).
- **total**: Full vehicle health check.
- **Maintenance**: Check maintenance due date and remaining life.
- When **user asks about car health** without specific item, run a full `Check_Car_Condition`.
- Face recognition enrollment requires a guided setup process.

## Implementation Checklist

When implementing a new Car Butler intent:

1. **Match the intent key** (e.g., `Check_Car_Condition`) to the skill function.
2. **Query vehicle state** via the CAN bus or vehicle service API.
3. **Format the response** with clear health status indicators.
4. **Confirm** with a natural response (e.g., "车况检查完成，一切正常").
5. **Save SlotContext** to Redis with `agent=Car Butler Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
车况检查: "车况检查结果：\n- 轮胎：{tire_status}\n- 油量/电量：{fuel_status}\n- 总里程：{odometer}公里\n- 下次保养：{maintenance_status}\n\n{summary}。"
预约维保: "已为您预约{date}的保养服务，请准时到店。"
人脸录入: "请将面部对准摄像头，保持自然表情。"
反馈: "感谢您的反馈，我们会认真处理。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
