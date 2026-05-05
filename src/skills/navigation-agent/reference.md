# Navigation Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Go_POI | go_poi | `{"poi": "...", "city": "..."}` | 导航搜索 |
|| Open_Nav | open_nav | `{}` | 打开导航 |
|| Close_Nav | close_nav | `{}` | 关闭导航 |
|| Home_Condition | home_condition | `{}` | 家路况 |
|| Go_Home | go_home | `{}` | 导航回家 |
|| Nav_Set_Home | nav_set_home | `{"poi": "..."}` | 设置家地址 |
|| Nav_Set_Company | nav_set_company | `{"poi": "..."}` | 设置公司地址 |
|| Go_Company | go_company | `{}` | 导航公司 |
|| Company_Condition | company_condition | `{}` | 公司路况 |
|| POI_Condition | poi_condition | `{"poi": "..."}` | POI路况 |
|| Ahead_Condition | ahead_condition | `{"poi": "..."}` | 查看沿途路况 |
|| Target_Condition | target_condition | `{}` | 目的地路况 |
|| Add_Via | add_via | `{"poi": "..."}` | 添加途经点 |
|| Delete_Via | delete_via | `{}` | 删除途经点 |
|| Nav_Zoom_In | nav_zoom_in | `{}` | 放大地图 |
|| Nav_Zoom_Out | nav_zoom_out | `{}` | 缩小地图 |
|| Nav_Zoom_In_Max | nav_zoom_in_max | `{}` | 地图最大 |
|| Nav_Zoom_Out_Min | nav_zoom_out_min | `{}` | 地图最小 |
|| 3D_Map | set_3d_map | `{}` | 3D视图 |
|| 2D_Map | set_2d_map | `{}` | 2D视图 |
|| North_Up | set_north_up | `{}` | 北朝上 |
|| Head_Up | set_head_up | `{}` | 车头朝上 |
|| Back_Center | back_to_center | `{}` | 回到自车位 |
|| View_Small_Map | view_small_map | `{}` | 查看小地图 |
|| Close_Small_Map | close_small_map | `{}` | 关闭小地图 |
|| Open_Full_Map | open_full_map | `{}` | 打开路线全览 |
|| Close_Full_Map | close_full_map | `{}` | 关闭路线全览 |
|| Get_Route_Information | get_route_information | `{}` | 打开路线信息 |
|| Change_Route | change_route | `{}` | 切换路线 |
|| Flush_Route | flush_route | `{}` | 重新算路 |
|| Switch_Main_Route | switch_main_route | `{}` | 切换到主路 |
|| Switch_Side_Route | switch_side_route | `{}` | 切换到辅路 |
|| Avoid_Congestion | avoid_congestion | `{}` | 打开躲避拥堵 |
|| Cancel_Avoid_Congestion | cancel_avoid_congestion | `{}` | 关闭躲避拥堵 |
|| Avoid_High_Way | avoid_high_way | `{}` | 打开不走高速 |
|| Cancel_Avoid_High_Way | cancel_avoid_high_way | `{}` | 关闭不走高速 |
|| Avoid_Limit_Line | avoid_limit_line | `{}` | 打开避开限行 |
|| Cancel_Avoid_Limit_Line | cancel_avoid_limit_line | `{}` | 关闭避开限行 |
|| Open_Avoid_Fee | open_avoid_fee | `{}` | 打开避免收费 |
|| Cancel_Avoid_Fee | cancel_avoid_fee | `{}` | 关闭避免收费 |
|| Speed_Fast | speed_fast | `{}` | 打开速度最快 |
|| Cancel_Speed_Fast | cancel_speed_fast | `{}` | 关闭速度最快 |
|| High_Way_First | highway_first | `{}` | 打开高速优先 |
|| Smart_Recommend | smart_recommend | `{}` | 打开智能路线推荐 |
|| Cancel_Smart_Recommend | cancel_smart_recommend | `{}` | 取消智能路线推荐 |
|| Main_Route_First | main_route_first | `{}` | 打开大路优先 |
|| Cancel_Main_First | cancel_main_first | `{}` | 关闭大路优先 |
|| Open_Electronic_Eye | open_electronic_eye | `{}` | 打开电子眼 |
|| Close_Electronic_Eye | close_electronic_eye | `{}` | 关闭电子眼 |
|| Open_Cruise_Information | open_cruise_information | `{}` | 打开路况信息 |
|| Close_Cruise_Information | close_cruise_information | `{}` | 关闭路况信息 |
|| Open_AR_Nav | open_ar_nav | `{}` | 打开AR导航 |
|| Close_AR_Nav | close_ar_nav | `{}` | 关闭AR导航 |
|| Front_Line_Detail | front_line_detail | `{}` | 前方路线引导 |
|| Traffic_Incidents | traffic_incidents | `{}` | 查看交通事件 |
|| Open_Nav_Broadcast | open_nav_broadcast | `{}` | 打开导航播报 |
|| Close_Nav_Broadcast | close_nav_broadcast | `{}` | 关闭导航播报 |
|| Replay_Broadcast | replay_broadcast | `{}` | 重播广播 |
|| Slow_Broadcast_Speed | slow_broadcast_speed | `{}` | 放慢播报 |
|| Accelerate_Broadcast_Speed | accelerate_broadcast_speed | `{}` | 加速播报 |
|| Open_Simple_Broadcast | open_simple_broadcast | `{}` | 打开简洁播报 |
|| Close_Simple_Broadcast | close_simple_broadcast | `{}` | 关闭简洁播报 |
|| Open_Commute_Nav | open_commute_nav | `{}` | 打开通勤导航 |
|| Close_Commute_Nav | close_commute_nav | `{}` | 关闭通勤导航 |
|| Open_Nav_Collections | open_nav_collections | `{}` | 打开导航收藏夹 |
|| Close_Nav_Collections | close_nav_collections | `{}` | 关闭导航收藏夹 |
|| Nav_To_Collection | nav_to_collection | `{}` | 去收藏地址 |
|| Collect_Target_Location | collect_target_location | `{}` | 收藏目的地 |
|| Collect_Current_Location | collect_current_location | `{}` | 收藏当前地址 |
|| Ask_Where | ask_where | `{}` | 当前位置查询 |
|| Open_Map_Setting | open_map_setting | `{}` | 打开地图设置 |
|| Close_Map_Setting | close_map_setting | `{}` | 关闭地图设置 |
|| Change_Nav_Sign | change_nav_sign | `{}` | 切换导航标志 |
|| Join_Group | join_group | `{}` | 加入组队 |
|| Build_Group | build_group | `{}` | 创建组队 |
|| Quit_Group | quit_group | `{}` | 退出组队 |
|| Open_Group | open_group | `{}` | 打开组队 |
|| Ask_Meeting_Place | ask_meeting_place | `{}` | 设置集结地 |
|| Go_Meeting_Place | go_meeting_place | `{}` | 去汇合地点 |
|| Group_Member_Location | group_member_location | `{}` | 查看成员位置 |

## Shared Slot Type Definitions

### POI
```
resolution: Match against local POI database. Fuzzy matching enabled. Return ranked list if ambiguous.
agents: Navigation Agent
```

### City
```
resolution: Normalize to standard city name (e.g., 北京市 → 北京). Use GPS city if omitted.
agents: Navigation Agent, Weather & Life Agent
```

### Target
```
resolution: The destination POI. Can be implicit (回家 → home address, 公司 → company address).
agents: Navigation Agent
```

### Via
```
resolution: Intermediate waypoint. Resolve like Target POI.
agents: Navigation Agent
```

### index
```
value_range: positive integer (1-based)
resolution: When a list is presented, use index to select. Default to 1 if omitted.
agents: Navigation Agent
```

## Saved Address Resolution

|| Alias | Resolves To |
|-------|------------|
| 家 / 回家 / 导航回家 | User's saved home address |
| 公司 / 回公司 / 导航公司 | User's saved company address |
| 收藏地点 | Named saved location from user's collection |

## Route Calculation Preferences

|| Preference | Effect |
||-----------|--------|
| 速度最快 | Minimize travel time |
| 高速优先 | Prefer highways over surface roads |
| 不走高速 | Avoid toll roads and highways |
| 躲避拥堵 | Avoid roads with real-time congestion |
| 大路优先 | Prefer arterial roads over local streets |
| 避开限行 | Avoid roads with vehicle restrictions |
| 避免收费 | Exclude toll roads |
