# Navigation Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 1 | Go_POI | 导航搜索 |
| 23 | Open_Nav | 打开导航 |
| 42 | Close_Nav | 关闭导航 |
| 56 | Home_Condition | 家路况 |
| 59 | Go_Home | 导航回家 |
| 60 | Nav_Set_Home | 设置家地址 |
| 61 | Nav_Set_Company | 设置公司地址 |
| 137 | Go_Company | 导航公司 |
| 154 | Company_Condition | 公司路况 |
| 22 | POI_Condition | POI路况 |
| 28 | Ahead_Condition | 查看沿途路况 |
| 340 | Target_Condition | 目的地路况 |
| 103 | Add_Via | 添加途经点 |
| 207 | Delete_Via | 删除途经点 |
| 191 | Nav_Zoom_In | 放大地图 |
| 192 | Nav_Zoom_Out | 缩小地图 |
| 33 | Nav_Zoom_In_Max | 地图最大 |
| 47 | Nav_Zoom_Out_Min | 地图最小 |
| 127 | Set_Map | 设置地图方向 |
| 205 | 3D_Map | 3D视图 |
| 113 | 2D_Map | 2D视图 |
| 329 | North_Up | 北朝上 |
| 330 | Head_Up | 车头朝上 |
| 289 | Back_Center | 回到自车位 |
| 306 | View_Small_Map | 查看小地图 |
| 355 | Close_Small_Map | 关闭小地图 |
| 176 | Open_Full_Map | 打开路线全览 |
| 366 | Close_Full_Map | 关闭路线全览 |
| 293 | Get_Route_Information | 打开路线信息 |
| 339 | Change_Route | 切换路线 |
| 338 | Flush_Route | 重新算路 |
| 231 | Switch_Main_Route | 切换到主路 |
| 184 | Switch_Side_Route | 切换到辅路 |
| 301 | Avoid_Congestion | 打开躲避拥堵 |
| 308 | Cancel_Avoid_Congestion | 关闭躲避拥堵 |
| 232 | Avoid_High_Way | 打开不走高速 |
| 385 | Cancel_Avoid_High_Way | 关闭不走高速 |
| 407 | Avoid_Limit_Line | 打开避开限行 |
| 283 | Cancel_Avoid_Limit_Line | 关闭避开限行 |
| 323 | Open_Avoid_Fee | 打开避免收费 |
| 282 | Cancel_Avoid_Fee | 关闭避免收费 |
| 227 | Speed_Fast | 打开速度最快 |
| 69 | Cancel_Speed_Fast | 关闭速度最快 |
| 229 | High_Way_First | 打开高速优先 |
| 302 | Smart_Recommend | 打开智能路线推荐 |
| 353 | Cancel_Smart_Recommend | 取消智能路线推荐 |
| 368 | Main_Route_First | 打开大路优先 |
| 375 | Cancel_Main_First | 关闭大路优先 |
| 148 | Open_Electronic_Eye | 打开电子眼 |
| 359 | Close_Electronic_Eye | 关闭电子眼 |
| 0 | Open_Cruise_Information | 打开路况信息 |
| 144 | Close_Cruise_Information | 关闭路况信息 |
| 163 | Open_AR_Nav | 打开AR导航 |
| 37 | Close_AR_Nav | 关闭AR导航 |
| 167 | Open_Nav_Broadcast | 打开导航播报 |
| 294 | Close_Nav_Broadcast | 关闭导航播报 |
| 400 | Replay_Broadcast | 重播广播 |
| 249 | Slow_Speed | 放慢播报 |
| 253 | Accelerate_Speed | 加速播报 |
| 181 | Open_Simple_Broadcast | 打开简洁播报 |
| 86 | Close_Simple_Broadcast | 关闭简洁播报 |
| 168 | Open_Commute_Nav | 打开通勤导航 |
| 132 | Close_Commute_Nav | 关闭通勤导航 |
| 5 | Open_Nav_Collections | 打开导航收藏夹 |
| 69 | Close_Nav_Collections | 关闭导航收藏夹 |
| 297 | Nav_To_Collection | 去收藏地址 |
| 298 | Collect_Target_Location | 收藏目的地 |
| 370 | Collect_Current_Location | 收藏当前地址 |
| 354 | Ask_Where | 当前位置查询 |
| 300 | Open_Map_Setting | 打开地图设置 |
| 117 | Close_Map_Setting | 关闭地图设置 |
| 300 | Change_Nav_Sign | 切换导航标志 |
| 134 | Front_Line_Detail | 前方路线引导 |
| 171 | Traffic_Incidents | 查看交通事件 |

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

| Alias | Resolves To |
|-------|------------|
| 家 / 回家 / 导航回家 | User's saved home address |
| 公司 / 回公司 / 导航公司 | User's saved company address |
| 收藏地点 | Named saved location from user's collection |

## Route Calculation Preferences

| Preference | Effect |
|------------|--------|
| 速度最快 | Minimize travel time |
| 高速优先 | Prefer highways over surface roads |
| 不走高速 | Avoid toll roads and highways |
| 躲避拥堵 | Avoid roads with real-time congestion |
| 大路优先 | Prefer arterial roads over local streets |
| 避开限行 | Avoid roads with vehicle restrictions |
| 避免收费 | Exclude toll roads |
