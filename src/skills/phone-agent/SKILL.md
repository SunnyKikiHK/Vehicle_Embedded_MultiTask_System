---
name: phone-agent
description: Implements Phone Agent intents in the vehicle embedded multi-task system. Handles all phone-related operations: calls, contacts, messages, Bluetooth management, and device connections. Use when the user mentions calling, contacts, phone, messages, Bluetooth, WiFi, hotspot, or device connections. Trigger terms: 打电话, 拨号, 联系人, 通话, 蓝牙, 连接, 热点, WiFi, 无线充电, 消息, 接听, 拒接, 来电.
---

# Phone Agent — Calls, Contacts & Device Management Skill

## Agent Overview

**Handles:** All phone-related operations: calls, contacts, messages, and connection management (Bluetooth, WiFi, hotspot, wireless charging).
**Total intents: 34**
**Shared slot types:** `Contact`, `Phone_Number`, `label`

## Core Intent Categories

### Phone App & Calls

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开电话 | Open_Phone | — | Open phone app |
| 拨打电话 | Call_Phone | — | Make a call |
| 拨打指定电话 | Call_Number | Phone_Number | Dial specific number |
| 拨打指定人号码 | Call_Phone_By_Contact | Contact | Call a contact by name |
| 按联系人和标签拨打 | Call_Phone_By_Contact_Label | Contact, label | Call by contact + phone label |
| 拨打黄页 | Call_Yellow_Page | Yellow | Call a yellow page number |
| 按号码段选择号码 | Call_Select_SubStr | SubStr | Select number by prefix |
| 拨打紧急电话 | Call_Emergency | Emergency | Call emergency services |

### Call Management

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 接听电话 | Answer_Phone | — | Answer incoming call |
| 拒接电话 | Reject_Phone | — | Reject incoming call |
| 来电静音 | Silent_Phone | — | Mute current call |
| 退出电话 | Quit_Phone | — | End current call |
| 回拨 | Call_Back | — | Call back last missed call |

### Call History

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查看通话记录 | View_Call_Record | — | View call history |
| 查看拨打记录 | View_Send_Record | — | View outgoing calls |
| 查看已接来电 | View_Already_Call | — | View answered calls |
| 查看未接来电 | View_Not_Call | — | View missed calls |

### Contacts

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查看联系人 | Get_Contact | — | Get contact list |
| 同步联系人 | Sync_Contact | — | Sync contacts |

### Messages

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开消息 | Open_Message | — | Open messages |
| 关闭消息 | Close_Message | — | Close messages |
| 未读消息 | View_Unread_Message | — | View unread messages |
| 所有消息 | View_All_Message | — | View all messages |

### Device Connections

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 断开手机连接 | Close_Phone_Connection | — | Disconnect phone |
| 打开手机连接 | Open_Phone_Connection | — | Connect phone |
| 打开蓝牙 | Open_Bluetooth | — | Enable Bluetooth |
| 关闭蓝牙 | Close_Bluetooth | — | Disable Bluetooth |
| 打开热点 | Open_Spot | — | Turn on hotspot |
| 关闭热点 | Close_Spot | — | Turn off hotspot |
| 打开WIFI | Open_WIFI | — | Enable WiFi |
| 关闭WIFI | Close_WIFI | — | Disable WiFi |
| 打开无线充电 | Open_Wireless_Charge | — | Enable wireless charging |
| 关闭无线充电 | Close_Wireless_Charge | — | Disable wireless charging |

## Slot Resolution Rules

- **Contact**: Search contacts by name. Support fuzzy matching. If multiple matches, present numbered list.
- **Phone_Number**: Full phone number string. Validate format.
- **label**: Phone number label: `手机`, `公司`, `住宅`, `其他`.
- **SubStr**: Phone number prefix for filtering (e.g., `010` for Beijing area code).
- **Yellow**: Yellow page service name or category (e.g., `出租车`, `拖车`, `急救`).
- **Emergency**: Emergency service type: `120`, `110`, `119`. Handle "紧急电话" as the general intent.
- When **user says a name** without explicit call intent, treat as `Call_Phone_By_Contact`.
- When **user says a number** directly, treat as `Call_Number`.
- **Safety**: Emergency calls should always be permitted regardless of vehicle state.

## Implementation Checklist

When implementing a new Phone intent:

1. **Match the intent key** (e.g., `Call_Phone_By_Contact`) to the skill function.
2. **Resolve Contact** — search contacts by name, present selection if ambiguous.
3. **Execute the action** via the phone/Bluetooth service API.
4. **Confirm** with a natural response (e.g., "正在拨打张三的移动电话" or "蓝牙已开启").
5. **Save SlotContext** to Redis with `agent=Phone Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
拨打电话: "正在拨打{contact}的{label}。"
指定号码: "正在拨打{number}。"
接听: "已接听来电。"
拒接: "已拒接来电。"
挂断: "通话已结束。"
蓝牙开: "蓝牙已开启。"
蓝牙关: "蓝牙已关闭。"
热点开: "热点已开启。"
热点关: "热点已关闭。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
