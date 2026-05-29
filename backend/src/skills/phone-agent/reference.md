# Phone Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Call_Phone | make_call | `{}` | 拨打电话 |
|| Call_Number | make_call | `{"number": "..."}` | 拨打指定电话 |
|| Call_Phone_By_Contact | dial_contact | `{"name": "..."}` | 拨打指定人号码 |
|| Call_Phone_By_Contact_Label | dial_contact | `{"name": "...", "label": "..."}` | 按联系人和标签拨打 |
|| Call_Emergency | make_call | `{"type": "emergency", "number": "..."}` | 拨打紧急电话 |
|| Answer_Phone | answer_call | `{}` | 接听电话 |
|| Reject_Phone | reject_call | `{}` | 拒接电话 |
|| Quit_Phone | end_call | `{}` | 退出电话 |
|| Call_Back | make_call | `{"type": "callback"}` | 回拨 |
|| View_Not_Call | missed_calls | `{}` | 查看未接来电 |
|| View_Call_Record | recent_calls | `{}` | 查看通话记录 |
|| View_Already_Call | recent_calls | `{}` | 查看已接来电 |
|| View_Send_Record | recent_calls | `{}` | 查看拨打记录 |
|| Get_Contact | recent_calls | `{}` | 查看联系人 |
|| Sync_Contact | recent_calls | `{"action": "sync"}` | 同步联系人 |
|| View_Unread_Message | unread_messages | `{}` | 查看未读消息 |
|| View_All_Message | read_messages | `{}` | 查看所有消息 |
|| Open_Bluetooth | bluetooth_on | `{}` | 打开蓝牙 |
|| Close_Bluetooth | bluetooth_off | `{}` | 关闭蓝牙 |
|| Open_WIFI | wifi_on | `{}` | 打开WIFI |
|| Close_WIFI | wifi_off | `{}` | 关闭WIFI |
|| Open_Spot | wifi_on | `{"mode": "hotspot"}` | 打开热点 |
|| Close_Spot | wifi_off | `{"mode": "hotspot"}` | 关闭热点 |
|| Open_Phone_Connection | connect_bluetooth | `{}` | 打开手机连接 |
|| Close_Phone_Connection | disconnect_bluetooth | `{}` | 断开手机连接 |

## Shared Slot Type Definitions

### Contact
```
resolution: Match against synced contacts. Fuzzy search supported. Return list if ambiguous.
agents: Phone Agent
```

### Phone_Number
```
value_range: 3-15 digits, optionally with country code (+86)
resolution: Validate format. Normalize by adding country code if missing.
agents: Phone Agent
```

### label
```
enum: 手机, 公司, 住宅, 其他
resolution: Phone number label for multi-number contacts. Default to 手机.
agents: Phone Agent
```

### Emergency
```
enum: 120, 110, 119, 122
resolution: Emergency service. Always permitted regardless of vehicle state.
agents: Phone Agent
```

## Phone Number Labels Priority

When a contact has multiple phone numbers, the default label priority for calling is: `手机 > 公司 > 住宅 > 其他`.

## Yellow Page Categories

|| Category | Example Queries |
|----------|---------------|
| 出租车 | 打车, 叫出租 |
| 拖车 | 抛锚, 事故, 救援 |
| 急救 | 受伤, 医疗 |
| 路边救援 | 爆胎, 没电, 没油 |
| 保险 | 事故报案 |
