---
name: navigation-agent
description: Implements Navigation Agent intents in the vehicle embedded multi-task system. Handles map, route planning, POI search, navigation, traffic conditions, saved addresses, and all navigation-related controls. Use when the user mentions navigation, maps, routes, directions, driving, traffic, home/company addresses, or waypoints. Trigger terms: 导航, 地图, 路线, 搜索地点, 去某地, 回家, 回公司, 途经点, 路况, 躲避拥堵, 放大地图, 缩小地图, 导航设置, 偏航, 重新算路, 附近, 当前位置, 收藏, 删除收藏
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
| 导航搜索 | go_poi | `{"poi": "<POI>", "search_mode": "<nearby\|city>", "city": "<City>", "poi_type": "<Type>", "index": <N>}` | Search for a named place (加油站, 故宫, 望京SOHO) and show its location. Also triggered when user says a location name without explicitly saying "回家" or "去公司". Keywords: 导航去, 带我去, 送我到, 怎么去, 去哪儿 |
| 设置家地址 | set_frequent_location | `{"location_type": "home", "poi": "<POI>"}` | Save or update the home address. User must explicitly say "设置/设为/改成" home address. NOT for navigation — use `go_home` to navigate home. |
| 设置公司地址 | set_frequent_location | `{"location_type": "company", "poi": "<POI>"}` | Save or update the company address. User must explicitly say "设置/设为/改成" company address. NOT for navigation — use `go_company` to navigate to company. |
| 查询家/公司地址 | check_frequent_location | `{"location_type": "<home\|company>"}` | Look up a saved home or company address (does not navigate). |
| 删除家/公司地址 | delete_frequent_location | `{"location_type": "<home\|company>"}` | Permanently delete a saved home or company address. |
| 收藏当前GPS位置 | collect_location | `{"poi": "<POI>"}` | Save a named place or the current GPS location to the **收藏夹** (favorites list). Use when user says "收藏XX" or "把XX加入收藏". |
| 查看收藏列表 | list_collected_locations | `{}` | Show all saved locations in the 收藏夹 (favorites). Triggered when user says "查看收藏" or "我的收藏夹里有什么". |
| 删除收藏地点 | delete_collected_locations | `{"poi": "<POI>"}` | Remove a location from the 收藏夹 (favorites) by its name or address. Pass the POI name (e.g., `{"poi": "望京SOHO"}`) and the system resolves it via Amap, then deletes by name+address match (mirrors collect_location). Falls back to coordinate proximity (~100m) if name+address don't match. If `poi` is omitted, deletes ALL collected locations. Triggered by "删除收藏", "把XX从收藏删掉", "把XX删了". **This is NOT about home/company — it is about the favorites list.** |
| 打开导航 | open_nav | `{}` | Launch/open the navigation app. |
| 关闭导航 | close_nav | `{}` | Exit/close the navigation app entirely (not just minimize the map). |

### Traffic Conditions

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 周边路况 | check_area_traffic | `{"poi": "<POI>", "radius": <meters>}` | Check real-time congestion level around a **specific place or area** (e.g., 故宫周边, 三环内, 海淀区). Also used when user asks about congestion on a ring road or specific road segment. Default radius 1000m. |
| 沿途路况 | check_route_traffic | `{"origin": "<POI\|lng,lat\|home\|company\|null>", "destination": "<POI\|lng,lat\|home\|company>"}` | Check traffic **along the planned route** between two points.(e.g., "去XX的路上堵不堵"). Both origin and destination accept: POI name (resolved via Amap), coordinate string "lng,lat", saved address alias "home" or "company", or omitted (defaults to current GPS for origin). Examples: `{"origin": "home", "destination": "望京SOHO"}`, `{"destination": "company"}`, `{"origin": "home", "destination": "company"}`. Returns distance, ETA, and congestion on the route. |
| 全城/核心区路况 | check_city_traffic_overview | `{"city": "<City>"}` | Get a macro-level traffic overview for a city's **core central area** (核心区域, 市中心, 城区). NOT for specific roads, ring roads, or named districts — use `check_area_traffic` for those. Only supports Beijing, Shanghai, Guangzhou, Shenzhen. |
| 家路况 | home_condition | `{}` | Check real-time traffic on the route from current location to the saved home address. Returns route distance (km), estimated time (minutes), traffic lights count, and strategy. Triggered by "回家堵不堵", "家那边路况怎么样", "回家路上堵吗". Requires home address to be set first. |
| 公司路况 | company_condition | `{}` | Check real-time traffic on the route from current location to the saved company address. Returns route distance (km), estimated time (minutes), traffic lights count, and strategy. Triggered by "去公司堵不堵", "公司那边路况怎么样", "上班路上堵吗". Requires company address to be set first. |

### Route Planning

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 导航回家 | go_home | `{}` | Start turn-by-turn navigation to the saved home address. Triggered by "回家", "带我回家", "回父母家", "回爸妈那". Requires home address to be set first. |
| 导航公司 | go_company | `{}` | Start turn-by-turn navigation to the saved company address. Triggered by "去公司", "导航去公司", "上班去". Requires company address to be set first. |
| 添加途经点 | add_via | `{"poi": "<POI>", "via_index": <N>}` | Insert a **temporary stop** (便利店, 加油站, 银行) into an existing route on the way to a destination. Triggered when user says "先去XX再去YY", "途经XX", "顺路去XX", "在YY的途中去XX". This modifies the current route, not just searching a place. |
| 删除途经点 | delete_via | `{}` | Remove the current waypoint from the route. |
| 重新算路 | flush_route | `{}` | Recalculate the entire route from scratch using fresh traffic data. Use when user says "重新算路", "重新规划", "换条路线重新导航", or wants a new route because the current one is slow/bad. |
| 切换路线 | change_route | `{}` | Switch to an **already-generated alternate route** (备选路线). Use when there are multiple routes available and user wants to switch between them, not regenerate. |
| 打开路线信息 | get_route_information | `{}` | Show detailed info about the current route: distance, ETA, tolls, number of traffic lights, route steps. |
| 打开路线全览 | open_full_map | `{}` | Open a bird's-eye view of the entire route on the map. |
| 关闭路线全览 | close_full_map | `{}` | Close the route overview map view. |

### Map Display Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 放大地图 | nav_zoom_in | `{}` | Increase zoom level (zoom in) to see more detail. Use when user wants a closer view of a small area. |
| 缩小地图 | nav_zoom_out | `{}` | Decrease zoom level (zoom out) to see a wider area. Use when user wants to see more of the surroundings or a larger region. |
| 回到自车位 | back_to_center | `{}` | Re-center the map on the vehicle's current GPS position and follow the car. Triggered when "回到车位", "回到我当前位置", "回到中心". |
| 查看小地图 | view_small_map | `{}` | Open a small floating mini-map overlay. |
| 关闭小地图 | close_small_map | `{}` | Dismiss the mini-map overlay. |
| 北朝上 | set_north_up | `{}` | Lock the map so north is always pointing up (compass north-up orientation). |
| 车头朝上 | set_head_up | `{}` | Rotate the map so the vehicle's heading always points toward the top of the screen (heading-up). Triggered by "车头朝上", "让车头指向屏幕上方". |
| 2D视图 | set_2d_map | `{}` | Switch map to 2D flat view. |
| 3D视图 | set_3d_map | `{}` | Switch map to 3D perspective view. |

### Route Preferences

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 切换到主路 | switch_main_route | `{}` | **Switch the current route** to prefer main arterial roads over side streets. Use when user says "切换到主路", "走大路不要小巷", "prefer main roads". This changes the active route's strategy. |
| 切换到辅路 | switch_side_route | `{}` | **Switch the current route** to prefer side/auxiliary roads. Use when user says "走辅路", "不走高架走地面". This changes the active route's strategy. |
| 开启速度最快 | speed_fast | `{}` | Enable **speed-priority mode** for all future route calculations (long-term preference). |
| 关闭速度最快 | cancel_speed_fast | `{}` | Turn off speed-priority mode. |
| 开启高速优先 | highway_first | `{}` | Prefer highways and elevated roads in route planning (高速, 高架桥). Use when user says "走高架", "走高速". |
| 开启不走高速 | avoid_high_way | `{}` | AVOID highways and elevated roads — prefer surface roads. Triggered by "不走高速", "不要高架", "避开高速". |
| 关闭不走高速 | cancel_avoid_high_way | `{}` | Cancel avoid-highway setting. |
| 开启智能路线推荐 | smart_recommend | `{}` | Enable AI-powered smart route recommendation. |
| 关闭智能路线推荐 | cancel_smart_recommend | `{}` | Disable smart route recommendation. |
| 开启大路优先 | main_route_first | `{}` | Prefer broad main roads over narrow alleys in route planning (大路优先, 不想钻小巷). This is a route **planning preference** set for future routes, not switching the current route. |
| 关闭大路优先 | cancel_main_first | `{}` | Cancel main road preference. |

### Traffic Avoidance

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开躲避拥堵 | avoid_congestion | `{}` | Enable automatic congestion avoidance for route planning. |
| 关闭躲避拥堵 | cancel_avoid_congestion | `{}` | Turn off congestion avoidance. |
| 打开避开限行 | avoid_limit_line | `{}` | Enable restricted zone/license plate avoidance. |
| 关闭避开限行 | cancel_avoid_limit_line | `{}` | Turn off restricted zone avoidance. |
| 打开避免收费 | open_avoid_fee | `{}` | Avoid toll roads in route planning to save money. Triggered by "避开收费", "不走收费路段". |
| 关闭避免收费 | cancel_avoid_fee | `{}` | Turn off toll avoidance. |

### Safety & Guidance Display

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开电子眼 | open_electronic_eye | `{}` | Show speed cameras, red-light cameras, and traffic monitoring points on the map. |
| 关闭电子眼 | close_electronic_eye | `{}` | Hide speed/traffic cameras from the map. |
| 打开路况信息叠加 | open_cruise_information | `{}` | Enable dynamic traffic info overlay (real-time traffic colors, flow density) on the map. Triggered by "打开路况", "显示实时车流", "看实时的车流密度分布". |
| 关闭路况信息叠加 | close_cruise_information | `{}` | Turn off the traffic info overlay. |
| 打开AR导航 | open_ar_nav | `{}` | Launch augmented reality navigation mode using the camera feed. |
| 关闭AR导航 | close_ar_nav | `{}` | Exit AR navigation mode. |
| 前方路线引导 | front_line_detail | `{}` | Read out detailed guidance for the upcoming turn/intersection: "前方500米左转，进入XX路". Use when user says "播报一下前面的路况", "前方怎么走". |

### Navigation Broadcast

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开导航播报 | open_nav_broadcast | `{}` | Enable voice guidance (TTS) for navigation. |
| 关闭导航播报 | close_nav_broadcast | `{}` | Mute all navigation voice guidance. |
| 重播广播 | replay_broadcast | `{}` | Repeat the last navigation instruction that was just given. Use when user says "再说一遍", "重复一下上一句". |
| 放慢播报速度 | slow_broadcast_speed | `{}` | Slow down the TTS speaking rate. Use when user says "说慢点". |
| 加速播报速度 | accelerate_broadcast_speed | `{}` | Speed up the TTS speaking rate. Use when user says "说快点", "加快语速". |
| 打开简洁播报 | open_simple_broadcast | `{}` | Switch to concise mode: only key turns and alerts, skip extra narration. |
| 关闭简洁播报 | close_simple_broadcast | `{}` | Return to full detailed voice guidance. |

### Commute & Saved Places

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开通勤导航 | open_commute_nav | `{}` | Enable automatic commute mode: pre-configured regular commute routes (e.g., "下班自动回家", "早高峰自动导航到公司"). Triggered by "开启通勤导航", "通勤打卡导航". |
| 关闭通勤导航 | close_commute_nav | `{}` | Disable automatic commute mode. |
| 打开导航收藏夹 | open_nav_collections | `{}` | Open the favorites/collections panel in the navigation UI. |
| 关闭导航收藏夹 | close_nav_collections | `{}` | Close the favorites panel. |
| 去收藏地址 | nav_to_collection | `{}` | Navigate to a location **already saved in the favorites list**. Use when user says "去我收藏的XX", "导航到收藏的XX". |
| 收藏目的地 | collect_target_location | `{}` | Save the **currently set/active destination** (正在导航的目的地) to the favorites list. Use when user says "把这里收藏", "收藏这个景点/目的地". Different from `collect_location` which saves any named place. |

### Position & Settings

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 当前位置查询 | ask_where_am_i | `{}` | Query the vehicle's current GPS coordinates and display the address. Use when user says "我在哪", "当前位置", "现在在哪". |
| 打开地图设置 | open_map_setting | `{}` | Open the navigation settings menu (units, map style, voice settings, etc.). |
| 关闭地图设置 | close_map_setting | `{}` | Close the navigation settings menu. |
| 切换导航标志 | change_nav_sign | `{}` | Change the style/appearance of navigation direction signs on screen (e.g., change arrow style, sign design). |

## Slot Resolution Rules

### POI Resolution
- The clean name/keyword of the place (e.g., "加油站", "故宫", "望京SOHO").
- For `go_poi`, `set_frequent_location`, `collect_location`: Use Amap API to search and resolve POI names to coordinates.
- **Important**: Never include spatial words like "附近的" or "最近的" in the poi parameter. Do NOT provide poi if the user's query implies current location or does not mention a specific place.

### search_mode
- `"nearby"`: Use when user says "nearest", "closest", "around me" (附近的, 最近的). Searches within 5000m radius.
- `"city"`: Use when user specifies a city or a specific famous landmark. Searches within the specified city.

### location_type
- Must be `"home"` or `"company"` for frequent location operations.
- `set_frequent_location`: Sets the home or company address for the user.
- `check_frequent_location`: Query saved home/company address.
- `delete_frequent_location`: Delete saved home/company address.

### Address Setting Logic
- `set_frequent_location` with `poi`: Search the provided POI name via Amap API.
- `set_frequent_location` without `poi`: Use current vehicle GPS location.

### Navigation Logic
- `go_home` / `go_company`: Requires the address to be set first via `set_frequent_location`.
- If address not set, return error asking user to set it first.
- If GPS not available, return error.

### Default Values
- `radius`: Default 1000m for area traffic, 5000m for POI search.
- `index`: Default 1 (first result) for POI selection.

### Intent Matching
- When **user says a location name** without "回家" or "去公司", treat it as `go_poi` intent.
- When **user says a category** (e.g., "找个加油站") without POI name, trigger POI search with category as keyword.
- When **user says "回家" or "去公司"**, treat as `go_home` or `go_company` intent.

## Disambiguation Rules (CRITICAL — read carefully)

### `go_home` vs `set_frequent_location` vs `collect_location`

| User says... | Tool to use | Reason |
|---|---|---|
| "回家" / "带我回家" / "导航回家" / "回父母家" | `go_home` | Intent is NAVIGATION to home |
| "把家地址设为X" / "把家庭地址改成X" / "设置家庭地址" | `set_frequent_location` | Intent is SAVING/updating address |
| "收藏这个位置作为家" | `collect_location` | Intent is saving to favorites, not setting home |
| "收藏当前位置" / "把XX加入收藏" | `collect_location` | Intent is adding to favorites list |

**Reconstruction Warning:** The query reconstructor may prepend "导航到" to a "回家" intent (e.g., "导航到设置为家庭地址的故宫博物院"). When you see a query that contains "回家" **AND** also mentions "设置", **always prefer `go_home`** when the primary intent is navigating home.

**Decision Tree:**
1. Does the query ask to **navigate TO** somewhere? → `go_home` / `go_company` / `go_poi`
2. Does the query ask to **SAVE or UPDATE** an address? → `set_frequent_location`
3. Does the query ask to **ADD to favorites**? → `collect_location` or `collect_target_location`
4. Does the query ask to **REMOVE from favorites**? → `delete_collected_locations`
5. Does the query ask to **VIEW favorites**? → `list_collected_locations`

### `collect_location` vs `collect_target_location`

| Scenario | Tool to use |
|---|---|
| User wants to save a named place or current GPS to favorites | `collect_location` |
| User wants to save the currently navigated destination to favorites | `collect_target_location` |

Trigger words for `collect_target_location`: "收藏目的地", "把这里收藏", "收藏这个景点/餐厅/商场". When in doubt, prefer `collect_location`.

### `delete_collected_locations` vs `delete_frequent_location`

| Scenario | Tool to use |
|---|---|
| User wants to delete from the **favorites/收藏夹** list | `delete_collected_locations` |
| User wants to delete the saved **home or company** address | `delete_frequent_location` |

Trigger words for `delete_collected_locations`: "删除收藏", "从收藏删掉", "清空收藏夹", "删掉收藏的XX", "把XX从收藏夹删除".

### `add_via` vs `go_poi`

**This is the most commonly confused pair.** Use `add_via` when the user:
- Mentions **two or more destinations** (先去XX再去YY)
- Uses words like "顺路", "途经", "中途", "路上"
- Is already on a route and wants to add a stop
- Says "先去XX" without explicitly ending the navigation session

Use `go_poi` when the user is **searching for a single place** with no mention of a second destination or stop.

| User says... | Tool to use |
|---|---|
| "先去趟银行再去公司" / "先去接个人再回家" | `add_via` |
| "搜索附近的加油站" | `go_poi` |
| "送我到XX，顺便去YY" | `add_via` |
| "带我去XX" (single destination) | `go_poi` |
| "路过XX加个油再去YY" | `add_via` |

### `switch_main_route` vs `main_route_first`

**`switch_main_route`** changes the **currently active route** to prefer main roads.
**`main_route_first`** sets a **planning preference** for all future routes.

| User says... | Tool to use |
|---|---|
| "把路线切换到只走大路" | `switch_main_route` |
| "尽量走高架和大路" | `main_route_first` |
| "开启大路优先，不想钻小巷" | `main_route_first` |

### `avoid_high_way` vs `switch_side_route`

**`avoid_high_way`** avoids highways in route planning (不走高速/高架).
**`switch_side_route`** prefers side roads on the current route.

| User says... | Tool to use |
|---|---|
| "不走高速，走地面" | `avoid_high_way` |
| "走高架桥会不会很堵？今晚不走高架了" | `avoid_high_way` |
| "尽量走辅路地面，不要高架" | `switch_side_route` |
| "我喜欢走高架" | `highway_first` |

### `check_area_traffic` vs `check_route_traffic` vs `check_city_traffic_overview`

| Scenario | Tool to use |
|---|---|
| Congestion around a specific **place** or **road segment** (e.g., "故宫周边", "三环", "五环", "这条路") | `check_area_traffic` |
| Congestion **along the route to a destination** (e.g., "去XX的路上堵不堵") | `check_route_traffic` |
| Macro congestion overview for a **city's core area** (市中心, 北京城区) | `check_city_traffic_overview` |

### `back_to_center` vs `set_head_up` vs `set_north_up`

| User says... | Tool to use | Reason |
|---|---|---|
| "回到车位" / "回到中心" / "切回去让我看到车子" | `back_to_center` | Re-center map on GPS and follow car |
| "车头朝上" / "让车头指向屏幕上方" / "不管车往哪转箭头永远向上" | `set_head_up` | Rotate map so heading points up |
| "北朝上" | `set_north_up` | Lock north to top of screen |

### `flush_route` vs `change_route` vs `get_route_information`

| User says... | Tool to use |
|---|---|
| "重新算路" / "重新规划路线" / "原来那条太慢了，重新生成" | `flush_route` |
| "切换到备选路线" / "换条路走" (when alternate routes exist) | `change_route` |
| "查看路线详情" / "这条路有多少公里" / "预计多久到" | `get_route_information` |

### `open_cruise_information` vs `open_electronic_eye`

| User says... | Tool to use |
|---|---|
| "显示实时车流密度" / "打开路况信息" / "显示路况叠加层" | `open_cruise_information` |
| "打开电子眼" / "显示测速照相" | `open_electronic_eye` |

### `replay_broadcast` vs `slow_broadcast_speed` vs `accelerate_broadcast_speed`

| User says... | Tool to use |
|---|---|
| "再说一遍" / "重复上一句" / "没听清，再说一次" | `replay_broadcast` |
| "说慢点" / "播报慢一点" | `slow_broadcast_speed` |
| "说快点" / "加快语速" | `accelerate_broadcast_speed` |

### `close_nav` vs `close_small_map` vs `close_full_map`

| User says... | Tool to use |
|---|---|
| "收起地图" / "关闭导航" / "退出导航" | `close_nav` |
| "关闭小地图" | `close_small_map` |
| "关闭路线全览" | `close_full_map` |

### Error Handling Notes

- **go_home / go_company**: Returns error if home/company address is not set. User must first set the address via `set_frequent_location`.
- **go_home / go_company**: Returns error if GPS location cannot be obtained.
- **go_home / go_company**: Returns error if route calculation fails (network/API error).

## Implementation Checklist

When implementing a new Navigation intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve POI, City, search_mode, etc
3. **Validate** all slot values against the Slot Resolution Rules
4. **Check disambiguation rules** for similar tool pairs (especially add_via/go_poi, switch_main_route/main_route_first, avoid_high_way/switch_side_route)
5. **Output** the JSON with reasoning, tool_name, and arguments
