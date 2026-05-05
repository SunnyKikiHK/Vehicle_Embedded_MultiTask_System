---
name: phone-agent
description: Implements Phone Agent intents in the vehicle embedded multi-task system. Handles all phone-related operations: calls, contacts, messages, Bluetooth management, and device connections. Use when the user mentions calling, contacts, phone, messages, Bluetooth, WiFi, hotspot, or device connections. Trigger terms: 打电话, 拨号, 联系人, 通话, 蓝牙, 连接, 热点, WiFi, 无线充电, 消息, 接听, 拒接, 来电.
---

# Phone Agent — Calls, Contacts & Device Management Skill

## Agent Overview

**Handles:** All phone-related operations: calls, contacts, messages, and connection management (Bluetooth, WiFi, hotspot, wireless charging).
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

### Phone App & Calls

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 拨打电话 | make_call | `{"number": "<Phone_Number>"}` | Make a call |
| 拨打指定人号码 | dial_contact | `{"name": "<Contact>"}` | Call a contact by name |
| 接听电话 | answer_call | `{}` | Answer incoming call |
| 拒接电话 | reject_call | `{}` | Reject incoming call |
| 挂断电话 | end_call | `{}` | End current call |
| 查看未接来电 | missed_calls | `{}` | View missed calls |
| 查看通话记录 | recent_calls | `{}` | View call history |

### Messages

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 查看未读消息 | unread_messages | `{}` | View unread messages |
| 查看所有消息 | read_messages | `{}` | View all messages |
| 删除消息 | delete_message | `{"message_id": "<id>"}` | Delete a message |
| 回复消息 | reply_message | `{"message_id": "<id>", "content": "<text>"}` | Reply to a message |

### Device Connections

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开蓝牙 | bluetooth_on | `{}` | Enable Bluetooth |
| 关闭蓝牙 | bluetooth_off | `{}` | Disable Bluetooth |
| 打开WIFI | wifi_on | `{}` | Enable WiFi |
| 关闭WIFI | wifi_off | `{}` | Disable WiFi |
| 连接蓝牙设备 | connect_bluetooth | `{"device": "<name>"}` | Connect to a Bluetooth device |
| 断开蓝牙设备 | disconnect_bluetooth | `{"device": "<name>"}` | Disconnect a Bluetooth device |

## Slot Resolution Rules

- **Contact**: Search contacts by name. Support fuzzy matching. If multiple matches, present numbered list
- **Phone_Number**: Full phone number string. Validate format
- When **user says a name** without explicit call intent, treat as `dial_contact`
- When **user says a number** directly, treat as `make_call`
- **Safety**: Emergency calls should always be permitted

## Implementation Checklist

When implementing a new Phone intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve Contact or Phone_Number
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
