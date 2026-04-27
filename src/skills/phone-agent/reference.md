# Phone Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 270 | Open_Phone | 打开电话 |
| 405 | Call_Phone | 拨打电话 |
| 31 | Call_Number | 拨打指定电话 |
| 172 | Call_Phone_By_Contact | 拨打指定人号码 |
| 424 | Call_Phone_By_Contact_Label | 按联系人和标签拨打 |
| 325 | Call_Yellow_Page | 拨打黄页 |
| 351 | Call_Select_SubStr | 按号码段选择号码 |
| 214 | Call_Emergency | 拨打紧急电话 |
| 313 | Answer_Phone | 接听电话 |
| 341 | Reject_Phone | 拒接电话 |
| 320 | Silent_Phone | 来电静音 |
| 263 | Quit_Phone | 退出电话 |
| 403 | Call_Back | 回拨 |
| 264 | View_Call_Record | 查看通话记录 |
| 105 | View_Send_Record | 查看拨打记录 |
| 161 | View_Already_Call | 查看已接来电 |
| 387 | View_Not_Call | 查看未接来电 |
| 346 | Get_Contact | 查看联系人 |
| 93 | Sync_Contact | 同步联系人 |
| 314 | Open_Message | 打开消息 |
| 100 | Close_Message | 关闭消息 |
| 419 | View_Unread_Message | 查看未读消息 |
| 160 | View_All_Message | 查看所有消息 |
| 39 | Close_Phone_Connection | 断开手机连接 |
| 153 | Open_Phone_Connection | 打开手机连接 |
| 228 | Open_Bluetooth | 打开蓝牙 |
| 285 | Close_Bluetooth | 关闭蓝牙 |
| 412 | Open_Spot | 打开热点 |
| 352 | Close_Spot | 关闭热点 |
| 326 | Open_WIFI | 打开WIFI |
| 233 | Close_WIFI | 关闭WIFI |
| 115 | Open_Wireless_Charge | 打开无线充电 |
| 114 | Close_Wireless_Charge | 关闭无线充电 |

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

| Category | Example Queries |
|----------|---------------|
| 出租车 | 打车, 叫出租 |
| 拖车 | 抛锚, 事故, 救援 |
| 急救 | 受伤, 医疗 |
| 路边救援 | 爆胎, 没电, 没油 |
| 保险 | 事故报案 |
