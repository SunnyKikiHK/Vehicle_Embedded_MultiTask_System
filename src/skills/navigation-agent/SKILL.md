---
name: navigation-agent
description: Implements Navigation Agent intents in the vehicle embedded multi-task system. Handles map, route planning, POI search, navigation, traffic conditions, saved addresses, and all navigation-related controls. Use when the user mentions navigation, maps, routes, directions, driving, traffic, home/company addresses, or waypoints. Trigger terms: 导航, 地图, 路线, 搜索地点, 去某地, 回家, 回公司, 途经点, 路况, 躲避拥堵, 放大地图, 缩小地图, 导航设置, 偏航, 重新算路.
---

# Navigation Agent — Route Planning & Map Control Skill

## Agent Overview

**Handles:** Map display, route planning, POI search, navigation guidance, traffic conditions, and saved addresses.
**Total intents: 74**
**Shared slot types:** `POI`, `City`, `Target`, `index`, `Via`, `date`

## Core Intent Categories

### POI Search & Navigation

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 导航搜索 | Go_POI | POI, City, Target, index | Search and navigate to a POI |
| 打开导航 | Open_Nav | — | Open navigation app |
| 关闭导航 | Close_Nav | — | Close navigation |
| 查看沿途路况 | Ahead_Condition | POI | Check traffic along route |
| 目的地路况 | Target_Condition | — | Check traffic at destination |
| 家路况 | Home_Condition | — | Check traffic on route home |
| 公司路况 | Company_Condition | — | Check traffic on route to company |
| POI路况 | POI_Condition | POI | Check traffic at specific POI |

### Route Planning

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 导航回家 | Go_Home | — | Navigate to saved home address |
| 导航公司 | Go_Company | — | Navigate to saved company |
| 设置家地址 | Nav_Set_Home | 家POI, index | Set or update home address |
| 设置公司地址 | Nav_Set_Company | 公司POI, index | Set or update company address |
| 添加途经点 | Add_Via | POI, Via, index | Add waypoint to route |
| 删除途经点 | Delete_Via | — | Remove waypoint |
| 重新算路 | Flush_Route | — | Recalculate route |
| 切换路线 | Change_Route | — | Switch to alternate route |
| 打开路线信息 | Get_Route_Information | Target | Get detailed route info |
| 打开路线全览 | Open_Full_Map | — | Show full route overview |
| 关闭路线全览 | Close_Full_Map | — | Hide route overview |

### Map Display Control

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 放大地图 | Nav_Zoom_In | — | Zoom in map |
| 缩小地图 | Nav_Zoom_Out | — | Zoom out map |
| 地图最大 | Nav_Zoom_In_Max | — | Maximize map zoom |
| 地图最小 | Nav_Zoom_Out_Min | — | Minimize map zoom |
| 回到自车位 | Back_Center | — | Return to current GPS position |
| 查看小地图 | View_Small_Map | — | Show mini-map |
| 关闭小地图 | Close_Small_Map | — | Hide mini-map |
| 设置地图方向 | Set_Map | — | Set map orientation |
| 3D视图 | 3D_Map | — | Switch to 3D map view |
| 2D视图 | 2D_Map | — | Switch to 2D map view |
| 北朝上 | North_Up | — | North-up map orientation |
| 车头朝上 | Head_Up | — | Heading-up orientation |

### Route Preferences

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 切换到主路 | Switch_Main_Route | — | Prefer main road |
| 切换到辅路 | Switch_Side_Route | — | Prefer side road |
| 打开速度最快 | Speed_Fast | — | Enable fastest route mode |
| 关闭速度最快 | Cancel_Speed_Fast | — | Disable fastest route |
| 打开高速优先 | High_Way_First | — | Prefer highways |
| 打开智能路线推荐 | Smart_Recommend | — | Enable smart route recommendation |
| 取消智能路线推荐 | Cancel_Smart_Recommend | — | Disable smart recommendation |
| 打开大路优先 | Main_Route_First | — | Prefer main roads |
| 关闭大路优先 | Cancel_Main_First | — | Cancel main road preference |

### Traffic Avoidance

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开躲避拥堵 | Avoid_Congestion | — | Enable congestion avoidance |
| 关闭躲避拥堵 | Cancel_Avoid_Congestion | — | Disable congestion avoidance |
| 打开不走高速 | Avoid_High_Way | — | Avoid highways |
| 关闭不走高速 | Cancel_Avoid_High_Way | — | Cancel avoid highway |
| 打开避开限行 | Avoid_Limit_Line | — | Avoid restricted zones |
| 关闭避开限行 | Cancel_Avoid_Limit_Line | — | Cancel avoid restricted zones |
| 打开避免收费 | Open_Avoid_Fee | — | Enable toll avoidance |
| 关闭避免收费 | Cancel_Avoid_Fee | — | Disable toll avoidance |

### Safety & Guidance Display

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开电子眼 | Open_Electronic_Eye | — | Show speed cameras |
| 关闭电子眼 | Close_Electronic_Eye | — | Hide speed cameras |
| 打开路况信息 | Open_Cruise_Information | — | Enable traffic info overlay |
| 关闭路况信息 | Close_Cruise_Information | — | Disable traffic info |
| 打开AR导航 | Open_AR_Nav | — | Enable AR navigation |
| 关闭AR导航 | Close_AR_Nav | — | Disable AR navigation |
| 前方路线引导 | Front_Line_Detail | — | Show upcoming route guidance |
| 查看交通事件 | Traffic_Incidents | — | View traffic incidents |

### Navigation Broadcast

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开导航播报 | Open_Nav_Broadcast | — | Enable navigation TTS |
| 关闭导航播报 | Close_Nav_Broadcast | — | Disable navigation TTS |
| 重播广播 | Replay_Broadcast | — | Repeat last navigation prompt |
| 放慢播报 | Slow_Speed | — | Slow down TTS speed |
| 加速播报 | Accelerate_Speed | — | Speed up TTS |
| 打开简洁播报 | Open_Simple_Broadcast | — | Enable concise prompts |
| 关闭简洁播报 | Close_Simple_Broadcast | — | Disable concise prompts |

### Commute & Saved Places

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开通勤导航 | Open_Commute_Nav | — | Enable commute navigation |
| 关闭通勤导航 | Close_Commute_Nav | — | Disable commute navigation |
| 打开导航收藏夹 | Open_Nav_Collections | — | Open saved locations |
| 关闭导航收藏夹 | Close_Nav_Collections | — | Close saved locations |
| 去收藏地址 | Nav_To_Collection | — | Navigate to saved location |
| 收藏目的地 | Collect_Target_Location | — | Save destination |
| 收藏当前地址 | Collect_Current_Location | — | Save current location |

### Position & Settings

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 当前位置查询 | Ask_Where | — | Query current GPS location |
| 打开地图设置 | Open_Map_Setting | — | Open map settings |
| 关闭地图设置 | Close_Map_Setting | — | Close map settings |
| 切换导航标志 | Change_Nav_Sign | — | Change navigation sign style |

## Slot Resolution Rules

- **POI**: Match against local database. If ambiguous, present ranked list with `index` slot for disambiguation.
- **City**: Normalize to standard city name. If omitted, use current GPS city.
- **Target**: The destination POI. Can be implicit (e.g., "回家" → home address).
- **Via**: Intermediate waypoint before reaching Target.
- **index**: When presenting a list, the user selects by number. Default to index 1 if not specified.
- When **user says a location name** without "导航", treat it as `Go_POI` intent.
- When **user says a category** (e.g., "找个加油站") without POI name, trigger POI search with category as keyword.

## Implementation Checklist

When implementing a new Navigation intent:

1. **Match the intent key** (e.g., `Go_Home`) to the skill function.
2. **Resolve POI/address** via the map service API.
3. **Check current route state** — if a route is active, apply changes to it; otherwise start a new route.
4. **Execute the action** via the navigation service.
5. **Confirm** with a natural response (e.g., "已为您导航回家，预计30分钟" or "路线已重新规划").
6. **Save SlotContext** to Redis with `agent=Navigation Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
开始导航: "已为您规划路线，目的地{poi}，预计{time}到达。"
回家: "好的，正在导航回{home_address}，预计{time}。"
回公司: "好的，正在导航到公司，预计{time}。"
路况: "当前路线{status}，预计比平时{delta}。"
收藏地址: "已将{location}收藏到{saved_category}。"
放大/缩小: "地图已{放大/缩小}。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
