---
name: navigation-agent
description: Implements Navigation Agent intents in the vehicle embedded multi-task system. Handles map, route planning, POI search, navigation, traffic conditions, saved addresses, and all navigation-related controls. Use when the user mentions navigation, maps, routes, directions, driving, traffic, home/company addresses, or waypoints. Trigger terms: 导航, 地图, 路线, 搜索地点, 去某地, 回家, 回公司, 途经点, 路况, 躲避拥堵, 放大地图, 缩小地图, 导航设置, 偏航, 重新算路, 附近, 当前位置, 集结, 组队.
---

# Navigation Agent — Route Planning & Map Control Skill

## Agent Overview

**Handles:** Map display, route planning, POI search, navigation guidance, traffic conditions, and saved addresses.
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

### POI Search & Navigation

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 导航搜索 | go_poi | `{"poi": "<POI>", "search_mode": "<nearby\|city>", "city": "<City>", "poi_type": "<Type>", "index": <N>}` | Search and navigate to a POI |
| 设置家地址 | set_frequent_location | `{"location_type": "home", "poi": "<POI>"}` | Set or update home address |
| 设置公司地址 | set_frequent_location | `{"location_type": "company", "poi": "<POI>"}` | Set or update company address |
| 查询家/公司地址 | check_frequent_location | `{"location_type": "<home\|company>"}` | Check saved home/company address |
| 删除家/公司地址 | delete_frequent_location | `{"location_type": "<home\|company>"}` | Delete saved home/company address |
| 收藏当前位置 | collect_location | `{"poi": "<POI>"}` | Save current GPS location or specific POI to favorites |
| 查看收藏列表 | list_collected_locations | `{}` | List all collected/favorite locations |
| 删除收藏地点 | delete_collected_locations | `{"location_id": <N>}` | Delete a specific collected location |
| 打开导航 | open_nav | `{}` | Open navigation app |
| 关闭导航 | close_nav | `{}` | Close navigation |

### Traffic Conditions

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 周边路况 | check_area_traffic | `{"poi": "<POI>", "radius": <meters>}` | Check traffic around a POI or current location |
| 沿途路况 | check_route_traffic | `{"origin": "<lng,lat>", "destination": "<Destination>"}` | Check traffic along route to destination |
| 全城路况 | check_city_traffic_overview | `{"city": "<City>"}` | Get city-wide traffic overview |
| 家路况 | home_condition | `{}` | Check traffic on route home |
| 公司路况 | company_condition | `{}` | Check traffic on route to company |

### Route Planning

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 导航回家 | go_home | `{}` | Navigate to saved home address. Requires home address to be set via `set_frequent_location`. Calculates route from current GPS and returns distance/ETA. |
| 导航公司 | go_company | `{}` | Navigate to saved company address. Requires company address to be set via `set_frequent_location`. Calculates route from current GPS and returns distance/ETA. |
| 添加途经点 | add_via | `{"poi": "<POI>", "via_index": <N>}` | Add waypoint to route |
| 删除途经点 | delete_via | `{}` | Remove waypoint |
| 重新算路 | flush_route | `{}` | Recalculate route |
| 切换路线 | change_route | `{}` | Switch to alternate route |
| 打开路线信息 | get_route_information | `{}` | Get detailed route info |
| 打开路线全览 | open_full_map | `{}` | Show full route overview |
| 关闭路线全览 | close_full_map | `{}` | Hide route overview |

### Map Display Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 放大地图 | nav_zoom_in | `{}` | Zoom in map |
| 缩小地图 | nav_zoom_out | `{}` | Zoom out map |
| 回到自车位 | back_to_center | `{}` | Return to current GPS position |
| 查看小地图 | view_small_map | `{}` | Show mini-map |
| 关闭小地图 | close_small_map | `{}` | Hide mini-map |
| 设置地图方向 | set_head_up | `{}` | Set map orientation |
| 3D视图 | set_3d_map | `{}` | Switch to 3D map view |
| 2D视图 | set_2d_map | `{}` | Switch to 2D map view |
| 北朝上 | set_north_up | `{}` | North-up map orientation |
| 车头朝上 | set_head_up | `{}` | Heading-up orientation |

### Route Preferences

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 切换到主路 | switch_main_route | `{}` | Prefer main road |
| 切换到辅路 | switch_side_route | `{}` | Prefer side road |
| 打开速度最快 | speed_fast | `{}` | Enable fastest route mode |
| 关闭速度最快 | cancel_speed_fast | `{}` | Disable fastest route |
| 打开高速优先 | highway_first | `{}` | Prefer highways |
| 打开智能路线推荐 | smart_recommend | `{}` | Enable smart route recommendation |
| 取消智能路线推荐 | cancel_smart_recommend | `{}` | Disable smart recommendation |
| 打开大路优先 | main_route_first | `{}` | Prefer main roads |
| 关闭大路优先 | cancel_main_first | `{}` | Cancel main road preference |

### Traffic Avoidance

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开躲避拥堵 | avoid_congestion | `{}` | Enable congestion avoidance |
| 关闭躲避拥堵 | cancel_avoid_congestion | `{}` | Disable congestion avoidance |
| 打开不走高速 | avoid_high_way | `{}` | Avoid highways |
| 关闭不走高速 | cancel_avoid_high_way | `{}` | Cancel avoid highway |
| 打开避开限行 | avoid_limit_line | `{}` | Avoid restricted zones |
| 关闭避开限行 | cancel_avoid_limit_line | `{}` | Cancel avoid restricted zones |
| 打开避免收费 | open_avoid_fee | `{}` | Enable toll avoidance |
| 关闭避免收费 | cancel_avoid_fee | `{}` | Disable toll avoidance |

### Safety & Guidance Display

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开电子眼 | open_electronic_eye | `{}` | Show speed cameras |
| 关闭电子眼 | close_electronic_eye | `{}` | Hide speed cameras |
| 打开路况信息 | open_cruise_information | `{}` | Enable traffic info overlay |
| 关闭路况信息 | close_cruise_information | `{}` | Disable traffic info |
| 打开AR导航 | open_ar_nav | `{}` | Enable AR navigation |
| 关闭AR导航 | close_ar_nav | `{}` | Disable AR navigation |
| 前方路线引导 | front_line_detail | `{}` | Show upcoming route guidance |

### Navigation Broadcast

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开导航播报 | open_nav_broadcast | `{}` | Enable navigation TTS |
| 关闭导航播报 | close_nav_broadcast | `{}` | Disable navigation TTS |
| 重播广播 | replay_broadcast | `{}` | Repeat last navigation prompt |
| 放慢播报 | slow_broadcast_speed | `{}` | Slow down TTS speed |
| 加速播报 | accelerate_broadcast_speed | `{}` | Speed up TTS |
| 打开简洁播报 | open_simple_broadcast | `{}` | Enable concise prompts |
| 关闭简洁播报 | close_simple_broadcast | `{}` | Disable concise prompts |

### Commute & Saved Places

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开通勤导航 | open_commute_nav | `{}` | Enable commute navigation |
| 关闭通勤导航 | close_commute_nav | `{}` | Disable commute navigation |
| 打开导航收藏夹 | open_nav_collections | `{}` | Open saved locations |
| 关闭导航收藏夹 | close_nav_collections | `{}` | Close saved locations |
| 去收藏地址 | nav_to_collection | `{}` | Navigate to saved location |
| 收藏目的地 | collect_target_location | `{}` | Save destination |

### Error Handling Notes

- **go_home / go_company**: Returns error if home/company address is not set. User must first set the address via `set_frequent_location`.
- **go_home / go_company**: Returns error if GPS location cannot be obtained.
- **go_home / go_company**: Returns error if route calculation fails (network/API error).

### Position & Settings

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 当前位置查询 | ask_where_am_i | `{}` | Query current GPS location |
| 打开地图设置 | open_map_setting | `{}` | Open map settings |
| 关闭地图设置 | close_map_setting | `{}` | Close map settings |
| 切换导航标志 | change_nav_sign | `{}` | Change navigation sign style |

### Group Travel

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 加入组队 | join_group | `{}` | Join a travel group |
| 创建组队 | build_group | `{}` | Create a new group |
| 退出组队 | quit_group | `{}` | Leave current group |
| 打开组队 | open_group | `{}` | Open group travel interface |
| 设置集结地 | ask_meeting_place | `{}` | Query group meetup location |
| 去汇合地点 | go_meeting_place | `{}` | Navigate to meetup point |
| 查看成员位置 | group_member_location | `{}` | View locations of group members |

## Slot Resolution Rules

### POI Resolution
- The clean name/keyword of the place (e.g., "加油站", "故宫").
- For `go_poi`, `set_frequent_location`, `collect_location`: Use Amap API to search and resolve POI names to coordinates
- **Important**: Never include spatial words like "附近的" or "最近的" in the poi parameter AND do not input POI for a tool if user's query imply current location OR does not contain a location.

### search_mode
- `"nearby"`: Use when user says "nearest", "closest", "around me" (附近的, 最近的). Searches within 5000m radius
- `"city"`: Use when user specifies a city or a specific famous landmark. Searches within the specified city

### location_type
- Must be `"home"` or `"company"` for frequent location operations
- `set_frequent_location`: Sets the home or company address for the user
- `check_frequent_location`: Query saved home/company address
- `delete_frequent_location`: Delete saved home/company address

### Address Setting Logic
- `set_frequent_location` with `poi`: Search the provided POI name via Amap API
- `set_frequent_location` without `poi`: Use current vehicle GPS location

### Navigation Logic
- `go_home` / `go_company`: Requires the address to be set first via `set_frequent_location`
- If address not set, return error asking user to set it first
- If GPS not available, return error

### Default Values
- `radius`: Default 1000m for area traffic, 5000m for POI search
- `index`: Default 1 (first result) for POI selection

### Intent Matching
- When **user says a location name** without "导航", treat it as `go_poi` intent
- When **user says a category** (e.g., "找个加油站") without POI name, trigger POI search with category as keyword
- When **user says "回家" or "去公司"**, treat as `go_home` or `go_company` intent

## Implementation Checklist

When implementing a new Navigation intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve POI, City, search_mode, etc
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
