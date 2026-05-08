# Car System Agent Design Proposal

> Based on analysis of 440 intents from `config/class.txt` and `config/slot_intent.json`
>
> Generated: 2025-05

---

## Overview

This document proposes **14 specialized agents** for a car voice assistant system. Each agent handles a self-contained domain, owns its own skill set, and manages its own dialogue state. This modular design ensures maintainability, clear ownership, and independent scaling.

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                    Arbitration Agent                     │
│         (Classifies: task vs. non-task)                │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
   ┌───────────┴────────────┬──────────────┬──────────────┐
   │                        │              │              │
   ▼                        ▼              ▼              ▼
Navigation  HVAC Agent   Seat Agent  Media Agent  System Agent
Agent                        │              │              │
   │                    Ambient      Phone Agent   Info Agent
   │                    Light Agent                Service Agent
   │                        │              │              │
   │                   Vehicle     User Profile    Car Butler
   │                  Control Agent                  Agent
   │                        │              │              │
   └────────────────────────┴──────────────┴──────────────┘
```

---

## Agent 1 — Navigation Agent

**Handles:** All map, route planning, and location-based services.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 1 | 导航搜索 | Go_POI | POI, City, Target, index | Search and navigate to a POI |
| 23 | 打开导航 | Open_Nav | — | Open the navigation app |
| 42 | 关闭导航 | Close_Nav | — | Close navigation |
| 56 | 家路况 | Home_Condition | — | Check traffic on route home |
| 59 | 导航回家 | Go_Home | — | Navigate to saved home address |
| 60 | 设置家地址 | Nav_Set_Home | 家POI, index | Set or update home address |
| 61 | 设置公司地址 | Nav_Set_Company | 公司POI, index | Set or update company address |
| 137 | 导航公司 | Go_Company | — | Navigate to saved company |
| 154 | 公司路况 | Company_Condition | — | Check traffic on route to company |
| 22 | POI路况 | POI_Condition | POI | Check traffic at a specific POI |
| 28 | 查看沿途路况 | Ahead_Condition | POI | Check traffic along the route |
| 340 | 目的地路况 | Target_Condition | — | Check traffic at destination |
| 103 | 添加途经点 | Add_Via | POI, Via, index | Add waypoint to route |
| 207 | 删除途经点 | Delete_Via | — | Remove waypoint |
| 191 | 放大地图 | Nav_Zoom_In | — | Zoom in map |
| 192 | 缩小地图 | Nav_Zoom_Out | — | Zoom out map |
| 33 | 地图最大 | Nav_Zoom_In_Max | — | Maximize map zoom |
| 47 | 地图最小 | Nav_Zoom_Out_Min | — | Minimize map zoom |
| 127 | 设置地图方向 | Set_Map | — | Set map orientation |
| 205 | 3D视图 | 3D_Map | — | Switch to 3D map view |
| 113 | 2D视图 | 2D_Map | — | Switch to 2D map view |
| 329 | 北朝上 | North_Up | — | North-up map orientation |
| 330 | 车头朝上 | Head_Up | — | Heading-up orientation |
| 289 | 回到自车位 | Back_Center | — | Return to current position |
| 306 | 查看小地图 | View_Small_Map | — | Show mini-map |
| 355 | 关闭小地图 | Close_Small_Map | — | Hide mini-map |
| 176 | 打开路线全览 | Open_Full_Map | — | Show full route overview |
| 366 | 关闭路线全览 | Close_Full_Map | — | Hide route overview |
| 293 | 打开路线信息 | Get_Route_Information | Target | Get detailed route info |
| 339 | 切换路线 | Change_Route | — | Switch to alternate route |
| 338 | 重新算路 | Flush_Route | — | Recalculate route |
| 231 | 切换到主路 | Switch_Main_Route | — | Prefer main road |
| 184 | 切换到辅路 | Switch_Side_Route | — | Prefer side road |
| 301 | 打开躲避拥堵 | Avoid_Congestion | — | Enable congestion avoidance |
| 308 | 关闭躲避拥堵 | Cancel_Avoid_Congestion | — | Disable congestion avoidance |
| 232 | 打开不走高速 | Avoid_High_Way | — | Avoid highways |
| 385 | 关闭不走高速 | Cancel_Avoid_High_Way | — | Cancel avoid highway |
| 407 | 打开避开限行 | Avoid_Limit_Line | — | Avoid restricted zones |
| 283 | 关闭避开限行 | Cancel_Avoid_Limit_Line | — | Cancel avoid restricted zones |
| 323 | 打开避免收费 | Open_Avoid_Fee | — | Enable toll avoidance |
| 282 | 关闭避免收费 | Cancel_Avoid_Fee | — | Disable toll avoidance |
| 227 | 打开速度最快 | Speed_Fast | — | Enable fastest route mode |
| 69 | 关闭速度最快 | Cancel_Speed_Fast | — | Disable fastest route |
| 229 | 打开高速优先 | High_Way_First | — | Prefer highways |
| 302 | 打开智能路线推荐 | Smart_Recommend | — | Enable smart route recommendation |
| 353 | 取消智能路线推荐 | Cancel_Smart_Recommend | — | Disable smart recommendation |
| 368 | 打开大路优先 | Main_Route_First | — | Prefer main roads |
| 375 | 关闭大路优先 | Cancel_Main_First | — | Cancel main road preference |
| 148 | 打开电子眼 | Open_Electronic_Eye | — | Show speed cameras |
| 359 | 关闭电子眼 | Close_Electronic_Eye | — | Hide speed cameras |
| 134 | 前方路线引导 | Front_Line_Detail | — | Show upcoming route guidance |
| 171 | 查看交通事件 | Traffic_Incidents | — | View traffic incidents |
| 0 | 打开路况信息 | Open_Cruise_Information | — | Enable traffic info overlay |
| 144 | 关闭路况信息 | Close_Cruise_Information | — | Disable traffic info |
| 163 | 打开AR导航 | Open_AR_Nav | — | Enable AR navigation |
| 37 | 关闭AR导航 | Close_AR_Nav | — | Disable AR navigation |
| 167 | 打开导航播报 | Open_Nav_Broadcast | — | Enable navigation TTS |
| 294 | 关闭导航播报 | Close_Nav_Broadcast | — | Disable navigation TTS |
| 400 | 重播广播 | Replay_Broadcast | — | Repeat last navigation prompt |
| 249 | 放慢播报 | Slow_Speed | — | Slow down TTS speed |
| 253 | 加速播报 | Accelerate_Speed | — | Speed up TTS |
| 181 | 打开简洁播报 | Open_Simple_Broadcast | — | Enable concise prompts |
| 86 | 关闭简洁播报 | Close_Simple_Broadcast | — | Disable concise prompts |
| 168 | 打开通勤导航 | Open_Commute_Nav | — | Enable commute navigation |
| 132 | 关闭通勤导航 | Close_Commute_Nav | — | Disable commute navigation |
| 5 | 打开导航收藏夹 | Open_Nav_Collections | — | Open saved locations |
| 69 | 关闭导航收藏夹 | Close_Nav_Collections | — | Close saved locations |
| 297 | 去收藏地址 | Nav_To_Collection | — | Navigate to saved location |
| 298 | 收藏目的地 | Collect_Target_Location | — | Save destination |
| 370 | 收藏当前地址 | Collect_Current_Location | — | Save current location |
| 354 | 当前位置查询 | Ask_Where | — | Query current GPS location |
| 300 | 打开地图设置 | Open_Map_Setting | — | Open map settings |
| 117 | 关闭地图设置 | Close_Map_Setting | — | Close map settings |
| 300 | 切换导航标志 | Change_Nav_Sign | — | Change navigation sign style |

**Total intents: 74**

---

## Agent 2 — Media Agent

**Handles:** Music playback, radio, news, K-song, and all audio/video control.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 2 | 音乐搜索 | Search_Music | Name, charts, Mood, Singer, Singer2, Age, Language, album, genre, location, Style, Scene, Content, type, Keywords, exclude, TV, variety_show, Song | Search music by various criteria |
| 363 | 播放在线音乐 | Play_Online_Music | — | Play online music |
| 114 | 播放蓝牙音乐 | Play_BT_Music | — | Play Bluetooth music |
| 208 | 播放USB音乐 | Play_USB_Music | — | Play music from USB |
| 215 | 播放相似歌曲 | Play_Similar_Music | — | Play similar songs |
| 288 | 退出相似歌曲 | Close_Play_Similar_Music | — | Exit similar song mode |
| 433 | 打开k歌 | Open_K | — | Open karaoke mode |
| 434 | 关闭k歌 | Close_K | — | Close karaoke mode |
| 431 | 唱歌搜索 | Select_Sing | Singer, Song | Search for karaoke song |
| 150 | 新闻搜索 | Search_News | Type, Key, Person, Area, Today | Search news |
| 99 | 播放历史记录 | Play_History | Media_Source | Play playback history |
| 109 | 打开播放历史 | Open_Play_History | Media_Source | Open playback history |
| 299 | 关闭播放历史 | Close_Play_History | Media_Source | Close playback history |
| 196 | 单曲循环 | Play_repeatly | — | Enable single-track repeat |
| 223 | 列表循环 | List_Repeat | — | Enable playlist repeat |
| 221 | 随机播放 | Media_Random_Play | — | Enable shuffle play |
| 366 | 顺序播放 | Media_Order_Play | — | Enable sequential play |
| 25 | 切换播放模式 | Change_Play_Mode | — | Cycle through play modes |
| 19 | 取消当前播放模式 | Cancel_Play_Mode | — | Cancel current play mode |
| 8 | 快进 | Quick_Go | Media_Source, Time | Fast forward |
| 139 | 快退 | Quick_Back | Media_Source, Time | Rewind |
| 178 | 下一首 | Media_Next | — | Next track |
| 250 | 上一首 | Media_Last | — | Previous track |
| 44 | 暂停播放 | Media_Pause | Media_Source | Pause playback |
| 119 | 继续播放 | Continue_Play | Media_Source | Resume playback |
| 317 | 重新播放 | Replay | — | Replay current track |
| 166 | 倍速播放 | Set_Speed_By_Speed | speed | Set playback speed |
| 130 | 音质切换 | Switch_Music_Quantity | Quantity | Switch audio quality |
| 198 | 收藏 | Media_Collect | Media_Source | Add to favorites |
| 219 | 取消收藏 | Cancel_Media_Collect | Media_Source | Remove from favorites |
| 312 | 播放多媒体收藏 | Play_Media_Collection | Collect_Source | Play from favorites |
| 257 | 打开多媒体收藏 | Open_Media_Collection | Media_Source | Open favorites list |
| 258 | 关闭多媒体收藏 | Close_Media_Collection | Media_Source | Close favorites |
| 10 | 打开播放详情 | Open_Play_Detail | Media_Source | Open playback details |
| 34 | 关闭播放详情 | Close_Play_Detail | Media_Source | Close playback details |
| 51 | 电台搜索 | Search_Radio | Type, Key, Person, Name, Today | Search radio stations |
| 50 | 打开指定电台 | Open_Radio_By_Name | Name | Open specific radio station |
| 142 | 播放在线广播 | Play_OL_Radio | — | Play online radio |
| 72 | 播放本地电台 | Play_Local_Radio | FM, AM | Play local FM/AM radio |
| 386 | 今日热点 | Play_Hot_Radio | — | Play today's hot stations |
| 401 | 重播广播 | Replay_Broadcast | — | Replay broadcast |
| 265 | 查询当前播放电台 | View_Play_Radio | — | Query current radio |
| 264 | 查询当前播放频道 | View_Play_Frequency | — | Query current frequency |
| 427 | 查询当前播放歌曲 | View_Play_Music | — | Query current playing song |
| 422 | 查询当前播放歌曲歌手 | View_Play_Music_Singer | — | Query current song artist |
| 346 | 查询当前播放专辑 | View_Play_Album | — | Query current album |
| 277 | 查询当前播放内容 | View_Play_Content | Just | Query current playback info |
| 148 | 查询当前播放新闻 | View_Play_News | — | Query current news |
| 73 | 下载当前内容 | Download_Current_Content | — | Download current media |
| 160 | 从时间开始播放 | Get_exact_time_For_Play | time | Play from specific time |
| 85 | 广播搜索 | Search_Station | Type, Name | Search broadcast stations |
| 102 | 打开歌词 | Open_o3ics | — | Show lyrics |
| 321 | 关闭歌词 | Close_o3ics | — | Hide lyrics |
| 102 | 打开播放器 | Open_Player | Media_Source | Open media player |
| 169 | 关闭播放器 | Close_Player | Media_Source | Close media player |
| 307 | 打开播放列表 | Open_Play_List | Media_Source | Open playlist |
| 170 | 关闭播放列表 | Close_Play_List | Media_Source | Close playlist |

**Total intents: 69**

---

## Agent 3 — HVAC Agent (Climate Control)

**Handles:** Air conditioning, heating, defrosting, air quality, and ventilation systems.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 14 | 关闭空调 | Close_Air_Condition | Position | Turn off air conditioning |
| 88 | 打开空调 | Open_Air_Condition | Position | Turn on air conditioning |
| 12 | 打开空调自动模式 | Open_Air_Condition_Auto_Mode | Position | Enable auto climate mode |
| 140 | 关闭空调自动模式 | Close_Air_Condition_Auto_Mode | Position | Disable auto mode |
| 161 | 打开空调同步模式 | Open_Air_Condition_Sync | Position | Enable synchronized zone control |
| 279 | 关闭空调同步模式 | Close_Air_Condition_Sync | Position | Disable sync mode |
| 162 | 打开空调制冷 | Open_Cooling | — | Enable cooling mode |
| 290 | 关闭空调制冷 | Close_Cooling | — | Disable cooling mode |
| 193 | 打开空调制热 | Open_Heating | — | Enable heating mode |
| 371 | 关闭制热模式 | Close_Heating | — | Disable heating mode |
| 50 | 打开除雾 | Open_Air_Condition_Defog | Position | Enable defog mode |
| 195 | 关闭除雾 | Close_Air_Condition_Defog | Position | Disable defog mode |
| 16 | 降低空调温度 | Dec_Air_Condition_Temperature | Position, Number, Ratio | Decrease temperature |
| 136 | 调高空调温度 | Inc_Air_Condition_Temperature | Position, Number, Ratio | Increase temperature |
| 15 | 设置空调温度 | Set_Air_Condition_Temperature | Position, Number, Ratio, Extreme | Set exact temperature |
| 17 | 降低空调风力 | Dec_Air_Condition_Wind | Position, Number, Ratio | Decrease fan speed |
| 45 | 调高空调风力 | Inc_Air_Condition_Wind | Position, Number, Ratio | Increase fan speed |
| 83 | 设置空调风力 | Set_Air_Condition_Wind | Position, Number, Ratio, Extreme | Set fan speed |
| 183 | 设置空调风向 | Set_Wind_Direction | Direction | Set airflow direction |
| 266 | 取消空调风向 | Cancel_Wind_Direction | Direction | Cancel wind direction |
| 283 | 打开自动风向 | Open_Wind_Auto_Mode | — | Enable auto airflow |
| 395 | 关闭自动风向 | Close_Wind_Auto_Mode | — | Disable auto airflow |
| 71 | 打开AC | Open_AC | — | Turn on A/C compressor |
| 70 | 关闭AC | Close_AC | — | Turn off A/C compressor |
| 139 | 关闭一键降温 | Close_Cooling_Instant | — | Cancel instant cool |
| 319 | 一键降温 | Open_Cooling_Instant | — | Instant maximum cooling |
| 360 | 快速升温 | Open_Heating_Instant | — | Instant maximum heating |
| 26 | 查询空气 | Ask_Air_Condition | location, date, smog, PM25 | Query air quality |
| 66 | 查询湿度 | Ask_Humidity | location, date | Query humidity |
| 260 | 查询风力 | Ask_Wind | location, date, level, direction | Query wind info |
| 211 | 打开空气净化器 | Open_Air_Cleaner | — | Turn on air purifier |
| 94 | 关闭空气净化器 | Close_Air_Cleaner | — | Turn off air purifier |
| 280 | 打开内循环 | Open_Internal_Circulation | — | Enable internal air recirculation |
| 253 | 关闭内循环 | Close_Internal_Circulation | — | Disable internal recirculation |
| 389 | 打开外循环 | Open_External_Circulation | — | Enable fresh air mode |
| 401 | 关闭外循环 | Close_External_Circulation | — | Disable fresh air mode |
| 327 | 打开空调应用 | Open_Air_Condition_APP | — | Open AC companion app |
| 188 | 关闭空调应用 | Close_Air_Condition_APP | — | Close AC companion app |
| 375 | 温度比较 | Temp_Compare | City | Compare temperatures across cities |

**Total intents: 43**

---

## Agent 4 — Seat Agent

**Handles:** All seat adjustments including position, heating, cooling, massage, and ventilation.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 21 | 座椅前后调整 | Adjust_Seat_Long | Direction | Adjust seat forward/backward |
| 245 | 座椅水平调整 | Adjust_Seat_Vert | Direction | Adjust seat vertical height |
| 192 | 打开座椅加热 | Open_Heated_Seat | Position | Turn on seat heating |
| 206 | 关闭座椅加热 | Close_Heated_Seat | Position | Turn off seat heating |
| 123 | 调低座椅温度 | Dec_Seat_Temperature | Position, Number, Ratio | Decrease seat heat level |
| 63 | 调高座椅温度 | Inc_Seat_Temperature | Position, Number, Ratio | Increase seat heat level |
| 30 | 设置座椅温度 | Set_Seat_Temperature | Position, Number, Ratio, Extreme | Set seat temperature |
| 165 | 打开座椅通风 | Open_Seat_Ventilation | Position | Turn on seat ventilation |
| 141 | 关闭座椅通风 | Close_Seat_Ventilation | Position | Turn off seat ventilation |
| 96 | 调低座椅通风 | Dec_Seat_Ventilation | Position, Number, Ratio | Decrease ventilation level |
| 79 | 调大座椅通风 | Inc_Seat_Ventilation | Position, Number, Ratio | Increase ventilation level |
| 37 | 设置座椅通风 | Set_Seat_Ventilation | Position, Number, Ratio, Extreme | Set seat ventilation |
| 234 | 打开座椅按摩 | Open_Seat_Massage | Position | Turn on seat massage |
| 78 | 关闭座椅按摩 | Close_Seat_Massage | Position | Turn off seat massage |
| 71 | 调低座椅按摩 | Dec_Seat_Massage | Position, Number, Ratio | Decrease massage intensity |
| 151 | 调大座椅按摩 | Inc_Seat_Massage | Position, Number, Ratio | Increase massage intensity |
| 47 | 设置座椅按摩 | Set_Seat_Massage | Position, Number, Ratio, Extreme | Set massage mode/intensity |
| 28 | 设置方向盘温度 | Set_Steer_Temperature | Number, Ratio, Extreme | Set steering wheel heat |
| 98 | 调低方向盘温度 | Dec_Steer_Temperature | Number, Ratio | Decrease steering heat |
| 261 | 调高方向盘温度 | Inc_Steer_Temperature | Number, Ratio | Increase steering heat |
| 205 | 打开方向盘加热 | Open_Heated_Steer | — | Turn on steering wheel heat |
| 204 | 关闭方向盘加热 | Close_Heated_Steer | — | Turn off steering wheel heat |
| 153 | 打开后视镜加热 | Open_Rearview_Mirror_Heating | — | Turn on mirror defogger |
| 377 | 关闭后视镜加热 | Close_Rearview_Mirror_Heating | — | Turn off mirror defogger |
| 236 | 展开后视镜 | Open_Rearview_Mirror | — | Unfold side mirrors |
| 351 | 折叠后视镜 | Close_Rearview_Mirror | — | Fold side mirrors |

**Total intents: 26**

---

## Agent 5 — Ambient Light Agent

**Handles:** All lighting inside the cabin: ambient lights, dashboard brightness, HUD, reading lights.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 63 | 打开氛围灯 | Open_Env_Light | — | Turn on ambient lighting |
| 16 | 关闭氛围灯 | Close_Env_Light | — | Turn off ambient lighting |
| 56 | 设置氛围灯颜色 | Set_Env_Light_Color | Color | Set ambient light color |
| 121 | 调节氛围灯主题 | Set_Env_Light_Theme | Theme | Set ambient light theme |
| 123 | 调低氛围灯亮度 | Dec_Env_Light_Brightness | Number, Ratio | Decrease ambient brightness |
| 176 | 调高氛围灯亮度 | Inc_Env_Light_Brightness | Number, Ratio | Increase ambient brightness |
| 124 | 设置氛围灯亮度 | Set_Env_Light_Brightness | Number, Ratio, Extreme | Set ambient brightness |
| 366 | 氛围灯自动模式 | Open_Env_Light_Auto_Mode | — | Enable auto ambient lighting |
| 413 | 关闭氛围灯自动模式 | Close_Env_Light_Auto_Mode | — | Disable auto ambient lighting |
| 91 | 调暗仪表盘 | Dec_DashBoard_Brightness | Number, Ratio | Dim dashboard |
| 91 | 调亮仪表盘 | Inc_DashBoard_Brightness | Number, Ratio | Brighten dashboard |
| 269 | 仪表盘调到最暗 | Set_DashBoard_Brightness_Min | — | Minimum dashboard brightness |
| 268 | 仪表盘调到最亮 | Set_DashBoard_Brightness_Max | — | Maximum dashboard brightness |
| 276 | 设置仪表盘亮度 | Set_DashBoard_Brightness | Number, Ratio | Set dashboard brightness level |
| 38 | 亮度调低 | Dec_Brightness | Number, Ratio | Decrease screen brightness |
| 189 | 亮度调高 | Inc_Brightness | Number, Ratio | Increase screen brightness |
| 127 | 亮度调到最低 | Set_Brightness_Min | — | Minimum screen brightness |
| 273 | 亮度调到最高 | Set_Brightness_Max | — | Maximum screen brightness |
| 157 | 设置亮度 | Set_Brightness | Number, Ratio | Set screen brightness |
| 147 | 打开HUD | Open_HUD | — | Turn on HUD display |
| 275 | 关闭HUD | Close_HUD | — | Turn off HUD display |
| 73 | HUD亮度调到指定值 | Adjust_Hud_Brightness | level | Set HUD brightness level |
| 174 | 调高HUD亮度 | Inc_HUD_Brightness | — | Increase HUD brightness |
| 423 | 调低HUD亮度 | Dec_HUD_Brightness | — | Decrease HUD brightness |
| 332 | 上下调节HUD位置 | Adjust_HUD_Vert | Direction | Adjust HUD vertical position |
| 416 | 左右调节HUD位置 | Adjust_HUD_Horizon | Direction | Adjust HUD horizontal position |
| 147 | 打开阅读灯 | Open_Reading_Light | — | Turn on reading light |
| 335 | 关闭阅读灯 | Close_Reading_Light | — | Turn off reading light |

**Total intents: 30**

---

## Agent 6 — Vehicle Control Agent

**Handles:** Physical vehicle components: windows, sunroof, trunk, wipers, lights, cameras.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 35 | 打开车窗 | Open_Window | Position | Open car windows |
| 62 | 关闭车窗 | Close_Window | Position | Close car windows |
| 61 | 设置车窗 | Set_Window | Position, Ratio | Set window to specific position |
| 160 | 打开通风模式 | Open_Window_Diagonal | — | Open windows in diagonal mode |
| 397 | 关闭通风模式 | Close_Window_Diagonal | — | Close diagonal ventilation |
| 97 | 关闭天窗 | Close_Dormer | — | Close sunroof |
| 304 | 打开天窗 | Open_Dormer | — | Open sunroof |
| 106 | 打开遮阳帘 | Open_Sunshade | — | Open sunshade |
| 201 | 关闭遮阳帘 | Close_Sunshade | — | Close sunshade |
| 135 | 打开后备箱 | Open_Trunk | — | Open trunk |
| 410 | 关闭后备箱 | Close_Trunk | — | Close trunk |
| 95 | 打开雨刷器 | Open_Wiper | — | Turn on wipers |
| 368 | 关闭雨刷器 | Close_Wiper | — | Turn off wipers |
| 254 | 打开大灯 | Open_Headlamp | — | Turn on headlights |
| 182 | 关闭大灯 | Close_Headlamp | — | Turn off headlights |
| 89 | 打开近光灯 | Open_Low_Beam | — | Turn on low beam |
| 378 | 关闭近光灯 | Close_Low_Beam | — | Turn off low beam |
| 67 | 打开远光灯 | Open_High_Beam | — | Turn on high beam |
| 251 | 关闭远光灯 | Close_High_Beam | — | Turn off high beam |
| 105 | 打开前雾灯 | Open_Front_Fog_Light | — | Turn on front fog lights |
| 396 | 关闭前雾灯 | Close_Front_Fog_Light | — | Turn off front fog lights |
| 118 | 打开后雾灯 | Open_Back_Fog_Light | — | Turn on rear fog lights |
| 29 | 关闭后雾灯 | Close_Back_Fog_Light | — | Turn off rear fog lights |
| 105 | 打开雾灯 | Open_Fog_Light | — | Turn on all fog lights |
| 185 | 关闭雾灯 | Close_Fog_Light | — | Turn off all fog lights |
| 381 | 打开示宽灯 | Open_Marker_Light | — | Turn on marker lights |
| 425 | 关闭示宽灯 | Close_Marker_Light | — | Turn off marker lights |
| 164 | 打开自动大灯 | Open_ADAPTIVE_HEAPLAMP | — | Enable auto headlight |
| 345 | 关闭自动大灯 | Close_ADAPTIVE_HEAPLAMP | — | Disable auto headlight |
| 343 | 打开环绕摄像 | Open_Surround_View | — | Turn on 360° camera |
| 109 | 关闭环绕摄像 | Close_Surround_View | — | Turn off 360° camera |
| 243 | 打开指定摄像头 | Set_Surround_View | Camera | Open specific camera view |
| 200 | 打开行车记录仪 | Open_DashCam | — | Turn on dashcam |
| 156 | 关闭行车记录仪 | Close_DashCam | — | Turn off dashcam |
| 6 | 开始录音 | Record_Audio | — | Start audio recording |
| 318 | 停止录音 | Stop_Audio | — | Stop audio recording |
| 13 | 开始录像 | Record_Video | — | Start video recording |
| 343 | 停止录像 | Stop_Video | — | Stop video recording |
| 293 | 拍照 | Take_Photo | — | Take a photo |
| 52 | 设置驾驶模式 | Set_Driving_Mode | Mode | Set driving mode (eco, sport, etc.) |
| 232 | 打开自动驻车 | Open_AutoHold | — | Enable auto parking hold |
| 405 | 关闭自动驻车 | Close_AutoHold | — | Disable auto parking hold |
| 278 | 打开自动启停 | Open_Engine_AutoStop | — | Enable auto start-stop |
| 408 | 关闭自动启停 | Close_Engine_AutoStop | — | Disable auto start-stop |

**Total intents: 46**

---

## Agent 7 — Phone Agent

**Handles:** All phone-related operations: calls, contacts, messages, and connection management.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 270 | 打开电话 | Open_Phone | — | Open phone app |
| 405 | 拨打电话 | Call_Phone | — | Make a call |
| 31 | 拨打指定电话 | Call_Number | Phone_Number | Dial specific number |
| 172 | 拨打指定人号码 | Call_Phone_By_Contact | Contact | Call a contact by name |
| 424 | 按联系人和标签拨打 | Call_Phone_By_Contact_Label | Contact, label | Call by contact + phone label |
| 325 | 拨打黄页 | Call_Yellow_Page | Yellow | Call a yellow page number |
| 351 | 按号码段选择号码 | Call_Select_SubStr | SubStr | Select number by prefix |
| 214 | 拨打紧急电话 | Call_Emergency | Emergency | Call emergency services |
| 313 | 接听电话 | Answer_Phone | — | Answer incoming call |
| 341 | 拒接电话 | Reject_Phone | — | Reject incoming call |
| 320 | 来电静音 | Silent_Phone | — | Mute current call |
| 263 | 退出电话 | Quit_Phone | — | End current call |
| 403 | 回拨 | Call_Back | — | Call back last missed call |
| 264 | 查看通话记录 | View_Call_Record | — | View call history |
| 105 | 查看拨打记录 | View_Send_Record | — | View outgoing calls |
| 161 | 查看已接来电 | View_Already_Call | — | View answered calls |
| 387 | 查看未接来电 | View_Not_Call | — | View missed calls |
| 346 | 查看联系人 | Get_Contact | — | Get contact list |
| 93 | 同步联系人 | Sync_Contact | — | Sync contacts |
| 314 | 打开消息 | Open_Message | — | Open messages |
| 100 | 关闭消息 | Close_Message | — | Close messages |
| 419 | 未读消息 | View_Unread_Message | — | View unread messages |
| 160 | 所有消息 | View_All_Message | — | View all messages |
| 39 | 断开手机连接 | Close_Phone_Connection | — | Disconnect phone |
| 153 | 打开手机连接 | Open_Phone_Connection | — | Connect phone |
| 228 | 打开蓝牙 | Open_Bluetooth | — | Enable Bluetooth |
| 285 | 关闭蓝牙 | Close_Bluetooth | — | Disable Bluetooth |
| 412 | 打开热点 | Open_Spot | — | Turn on hotspot |
| 352 | 关闭热点 | Close_Spot | — | Turn off hotspot |
| 326 | 打开WIFI | Open_WIFI | — | Enable WiFi |
| 233 | 关闭WIFI | Close_WIFI | — | Disable WiFi |
| 115 | 打开无线充电 | Open_Wireless_Charge | — | Enable wireless charging |
| 114 | 关闭无线充电 | Close_Wireless_Charge | — | Disable wireless charging |

**Total intents: 34**

---

## Agent 8 — Weather & Life Agent

**Handles:** Weather queries, life advisory (clothing, travel, car wash, fishing, etc.).

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 194 | 天气查询 | Query_Weather | location, date, sun, rain, snow, fog, quilt | Query weather conditions |
| 200 | 天气查询 | Query_Weather | location, date, sun, rain, snow, fog, quilt | Query weather (duplicate ID) |
| 120 | 实时查询天气 | Query_Timely_Weather | location | Query real-time weather |
| 402 | 打开天气 | Open_Weather | — | Open weather app |
| 187 | 关闭天气 | Close_Weather | — | Close weather app |
| 154 | 查询穿衣 | Ask_Clothes | location, date, dressing, scarf, hat, coat, t_shirt | Clothing recommendation |
| 173 | 查询化妆 | Ask_Makeup | location, date | Makeup suggestion |
| 157 | 查询钓鱼 | Ask_Fishing | location, date | Fishing conditions |
| 212 | 查询运动 | Ask_Sport | location, date | Sports conditions |
| 231 | 查询旅游 | Ask_Travel | location, date | Travel advisory |
| 303 | 查询交通 | Ask_Transport | location, date | Transportation info |
| 127 | 查询感冒 | Ask_Cold_Index | location, date | Cold risk index |
| 191 | 查询洗车 | Ask_Car_Wash | location, date | Car wash recommendation |
| 372 | 查询过敏 | Ask_Allergy | location, date | Allergy risk |
| 181 | 查询体感温度 | Query_Body_Temperature | location, date | Feels-like temperature |
| 209 | 查询紫外线 | Query_UV_Level | location, date, sunscreen | UV index |
| 224 | 油价查询 | Oil_Price | — | Query fuel prices |
| 197 | 查询哪天限行 | Query_Date | City, License | Query license plate restrictions |
| 259 | 查询是否限行 | Query_Restrictions | location, date | Check if restricted today |
| 226 | 查询星期 | Ask_Weekday | — | Query current weekday |
| 324 | 查看日期 | Ask_Date | — | Query current date |
| 225 | 剩余流量 | Display_Remaining_Flow | — | Check remaining data plan |
| 187 | 打开流量 | Open_Flow | — | Enable mobile data |
| 203 | 关闭流量 | Close_Flow | — | Disable mobile data |
| 358 | 打开流量中心 | Open_Flow_Center | — | Open data management |
| 283 | 关闭流量中心 | Close_Flow_Center | — | Close data center |
| 242 | 查看流量排名 | Open_APP_Rank | — | View data usage ranking |
| 226 | 退出流量排名 | Close_APP_Rank | — | Exit data ranking |

**Total intents: 30**

---

## Agent 9 — User Profile Agent

**Handles:** Voice assistant personalization: wake words, timbre, speech speed, dialogue mode, and onboarding.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 75 | 设置为女声 | Set_Timbre_Female | — | Set female voice |
| 76 | 仅主驾可唤醒 | Only_Main | — | Only driver can wake assistant |
| 315 | 主副驾可唤醒 | Main_And_Vice | — | Both driver and passenger can wake |
| 20 | 切换音色 | Change_Timbre | — | Switch voice timbre |
| 406 | 设置为男声 | Set_Timbre_Male | — | Set male voice |
| 302 | 设置为童声 | Set_Timbre_Child | — | Set child voice |
| 239 | 设置为默认 | Set_Timbre_Default | — | Reset to default voice |
| 116 | 设置为指定音色 | Set_Voice | Voice | Set a specific voice preset |
| 292 | 切换语音风格 | Set_Voice_Style | Style | Switch voice style (e.g., energetic, calm) |
| 286 | 设置语速 | Set_Speech_By_Speed | speed | Set TTS speech rate |
| 129 | 修改为指定唤醒词 | Set_Wakeup_Words | Wake | Set custom wake word |
| 216 | 询问修改唤醒词 | Ask_Wakeup_Words | — | Ask about wake word modification |
| 362 | 删除唤醒词 | Delete_Wakeup_Words | — | Delete custom wake word |
| 349 | 开启免唤醒 | Open_Free_Wakeup | — | Enable continuous listening (no wake word) |
| 331 | 关闭免唤醒 | Close_Free_Wakeup | — | Disable continuous listening |
| 388 | 开启连续对话 | Open_Continuous_Dialogue | — | Enable multi-turn dialogue |
| 310 | 关闭连续对话 | Close_Continuous_Dialogue | — | Disable multi-turn dialogue |
| 391 | 设置对话时长 | Set_Continuous_Dialogue | Time | Set dialogue session duration |
| 415 | 打开在线语音 | Open_Online_NLU | — | Enable cloud NLU processing |
| 333 | 关闭在线语音 | Close_Online_NLU | — | Disable cloud NLU |
| 256 | 打开语音设置 | Open_Sds_Config | — | Open voice assistant settings |
| 390 | 关闭语音设置 | Close_Sds_Config | — | Close voice settings |
| 41 | 查看交互式学习 | View_Learning_Content | — | View interactive learning content |
| 254 | 打开交互学习 | Open_Interactive_Learning | — | Open interactive tutorial |
| 361 | 关闭交互学习 | Close_Interactive_Learning | — | Close interactive tutorial |
| 111 | 打开语音训练营 | Open_Training_Camp | — | Open voice training camp |
| 224 | 关闭语音训练营 | Close_Training_Cmap | — | Close voice training camp |
| 212 | 打开语音技能介绍 | Open_Skill_Instruction | — | Open skill introduction |
| 218 | 关闭语音技能介绍 | Close_Skill_Instruction | — | Close skill introduction |
| 420 | 打开语音唤醒 | Open_Voice_Wakeup | — | Enable voice wake |
| 242 | 关闭语音唤醒 | Close_Voice_Wakeup | — | Disable voice wake |
| 409 | 打开安全提醒 | Open_Safety_Alarm | — | Enable safety alerts |
| 77 | 关闭安全提醒 | Close_Safety_Alarm | — | Disable safety alerts |

**Total intents: 35**

---

## Agent 10 — System Settings Agent

**Handles:** App management, desktop UI, system theme, card layout, screen control, scene modes.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 40 | 打开系统设置 | Open_System_Config | One_Level, Two_Level | Open system settings |
| 48 | 关闭系统设置 | Close_System_Config | One_Level, Two_Level | Close system settings |
| 195 | 打开应用 | Open_App | app | Open a specific app |
| 80 | 关闭应用 | Close_App | app | Close a specific app |
| 275 | 打开应用列表 | Open_App_List | — | Open app list |
| 320 | 关闭应用列表 | Close_App_List | — | Close app list |
| 129 | 下载应用 | Download_App | app | Download an app |
| 218 | 打开应用商城 | Open_APP_Store | — | Open app store |
| 364 | 关闭应用商城 | Close_APP_Store | — | Close app store |
| 53 | 设置桌面样式 | Set_Desktop_Style | Desktop | Change desktop theme/style |
| 100 | 关闭主题 | Set_System_Theme_By_Mode | mode | Set day/night theme |
| 178 | 切换卡片位置 | Set_Card_Position | Position | Rearrange home screen cards |
| 337 | 回到主页 | Back_To_Home | — | Return to home screen |
| 379 | 打开屏幕 | Open_Screen | — | Turn on display |
| 244 | 关闭屏幕 | Close_Screen | — | Turn off display |
| 392 | 打开投屏 | Open_ScreenCast | — | Enable screen casting |
| 202 | 关闭投屏 | Close_ScreenCast | — | Disable screen casting |
| 246 | 打开长视频 | Open_Long_Video | — | Open long video app |
| 269 | 关闭长视频 | Close_Long_Video | — | Close long video app |
| 124 | 打开小程序应用 | Open_Mini_App | Mini_app | Open a mini app |
| 19 | 关闭小程序应用 | Close_Mini_App | Mini_app | Close a mini app |
| 418 | 打开小程序中心 | Open_Mini_App_Center | — | Open mini app center |
| 7 | 关闭小程序中心 | Close_Mini_App_Center | — | Close mini app center |
| 334 | 打开情景模式 | Open_Scene_Center | — | Open scene mode center |
| 272 | 关闭情景模式 | Close_Scene_Center | — | Close scene mode center |
| 306 | 打开指定场景 | Open_Preset_Scene | Scene | Activate a preset scene |
| 271 | 退出指定场景 | Close_Preset_Scene | Scene | Deactivate a scene |
| 146 | 打开睡眠模式 | Open_Snooze_Mode | Minute | Enable sleep mode (auto-off timer) |
| 358 | 关闭睡眠模式 | Close_Snooze_Mode | — | Cancel sleep mode |
| 167 | 模糊表达打开睡眠模式 | Open_Snooze_Mode_Fuzzy | — | Vague request to enable sleep mode |
| 347 | 模糊表达关闭睡眠模式 | Close_Snooze_Mode_Fuzzy | — | Vague request to cancel sleep mode |
| 54 | 设置桌面样式 | Set_Desktop_Style | Desktop | Customize desktop layout |

**Total intents: 36**

---

## Agent 11 — Car Butler Agent

**Handles:** Vehicle health monitoring, maintenance scheduling, car butler services, and face recognition.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 432 | 车况检查 | Check_Car_Condition | Tire, gas, range, total, Maintenance | Query vehicle health status |
| 435 | 打开车辆管家 | Open_Bulter | — | Open car butler service |
| 436 | 关闭车辆管家 | Close_Bulter | — | Close car butler service |
| 437 | 预约维保 | Reserve_Maintenance | — | Book maintenance appointment |
| 438 | 取消预约 | Cancel_Reserve | — | Cancel maintenance appointment |
| 309 | 录入人脸识别 | Record_Face | — | Register face for driver profile |
| 220 | 打开车主服务 | Open_Owner_Service | — | Open owner services |
| 239 | 关闭车主服务 | Close_Owner_Service | — | Close owner services |
| 383 | 打开个人中心 | Open_Personal_Center | — | Open personal center |
| 34 | 关闭个人中心 | Close_Personal_Center | — | Close personal center |
| 381 | 投诉与建议 | Complains_And_Suggestions | — | File complaint or suggestion |
| 107 | 打开反馈 | Open_Feedback | — | Open feedback form |
| 394 | 关闭反馈 | Close_Feedback | — | Close feedback form |
| 110 | 查看已完成订单 | View_Already_Order | — | View completed orders |
| 235 | 查看未完成订单 | View_Unend_Order | — | View pending orders |
| 414 | 查看所有订单 | View_All_Order | — | View all orders |
| 116 | 打开订单中心 | Open_Order_Center | — | Open order center |
| 134 | 关闭订单中心 | Close_Order_Center | — | Close order center |
| 108 | 打开途记软件 | Open_Record_App | — | Open trip recording app |
| 295 | 关闭途记软件 | Close_Record_App | — | Close trip recording app |
| 93 | 新建旅途记录 | Create_Trip_Record | — | Start a new trip record |
| 92 | 打开日历 | Open_Calendar | — | Open calendar |
| 10 | 关闭日历 | Close_Calendar | — | Close calendar |

**Total intents: 24**

---

## Agent 12 — Group Travel Agent

**Handles:** Team/group travel features: route sharing, meetup coordination, and group member tracking.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 87 | 加入组队 | Join_Group | — | Join a travel group |
| 241 | 创建组队 | Build_Group | — | Create a new group |
| 297 | 退出组队 | Quit_Group | — | Leave current group |
| 383 | 打开组队 | Open_Group | — | Open group travel interface |
| 84 | 设置集结地 | Ask_Meeting_Place | — | Query group meetup location |
| 374 | 去汇合地点 | Go_Meeting_Place | — | Navigate to meetup point |
| 381 | 查看成员位置 | Group_Member_Location | — | View locations of group members |

**Total intents: 7**

---

## Agent 13 — Interaction Control Agent

**Handles:** General UI interaction: confirmations, cancellations, selections, help, and general app navigation.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 428 | 确定 | Confirm | — | Confirm current selection |
| 430 | 取消 | Cancel | — | Cancel current operation |
| 429 | 列表选择 | List_Select | Index | Select from a numbered list |
| 8 | 同时打开 | Open_Two_Both | — | Open two items simultaneously |
| 267 | 同时关闭 | Close_Two_Both | — | Close two items simultaneously |
| 398 | 打开帮助 | Open_Help | — | Open help center |
| 43 | 关闭帮助 | Close_Help | — | Close help center |
| 393 | 询问修改应答词 | Ask_Answer_Words | — | Ask about custom response words |
| 289 | 修改为指定应答词 | Get_Answer | Response | Set a custom response phrase |
| 417 | 删除应答词 | Delete_Answer_Words | — | Delete custom response word |

**Total intents: 10**

---

## Agent 14 — Info Query Agent

**Handles:** Quick informational queries that don't fit other domains: time, location, quick status.

**Skill Table:**

| Intent ID | Intent Name | English Key | Slots | Description |
|-----------|-------------|-------------|-------|-------------|
| 354 | 当前位置查询 | Ask_Where | — | Where am I? |
| 225 | 查询星期 | Ask_Weekday | — | What day is it? |
| 324 | 查看日期 | Ask_Date | — | What's today's date? |
| 91 | 打开天气 | Open_Weather | — | Open weather widget |
| 26 | 查询空气 | Ask_Air_Condition | location, smog, PM25 | Air quality query |
| 66 | 查询湿度 | Ask_Humidity | location, date | Humidity query |
| 209 | 查询紫外线 | Query_UV_Level | location, sunscreen | UV index query |

**Total intents: 7**

---

## Summary Table

| # | Agent Name | Intent Count | Primary Domain |
|---|---|---|---|
| 1 | Navigation Agent | 74 | Map, routes, POI, traffic |
| 2 | Media Agent | 69 | Music, radio, video, K-song |
| 3 | HVAC Agent | 43 | Air conditioning, temperature |
| 4 | Seat Agent | 26 | Seat, steering, mirror controls |
| 5 | Ambient Light Agent | 30 | Lights, HUD, brightness |
| 6 | Vehicle Control Agent | 46 | Windows, trunk, wipers, lights, cameras |
| 7 | Phone Agent | 34 | Calls, contacts, messages, BT/WiFi |
| 8 | Weather & Life Agent | 30 | Weather, clothing, travel, life advisory |
| 9 | User Profile Agent | 35 | Voice, timbre, wake words, dialogue mode |
| 10 | System Settings Agent | 36 | Apps, display, scenes, desktop |
| 11 | Car Butler Agent | 24 | Vehicle health, maintenance, orders |
| 12 | Group Travel Agent | 7 | Group travel, meetup, location sharing |
| 13 | Interaction Control Agent | 10 | Confirm, cancel, select, help |
| 14 | Info Query Agent | 7 | Quick time/location/status queries |
| — | **Unknown** | **1** | Unclassified / fallback |
| | **Total** | **440** | |

---

## Implementation Recommendations

### 1. Agent Communication Pattern
Each agent should communicate via a **shared message bus**. The arbitration agent dispatches to the correct agent based on the classified intent.

```
Arbitration → [Message Bus] → Target Agent → DM Skill → [Response]
```

### 2. MCP Server Consolidation

The MCP servers have been consolidated to run 14 servers instead of 20, with each server handling multiple logical domains:

| Port | Server | Consolidated Domains |
|------|--------|---------------------|
| 8001 | `nav_server.py` | Navigation + Map + Group Travel |
| 8002 | `vehicle_server.py` | Vehicle Control + Car Butler |
| 8003 | `ac_server.py` | Air Conditioning (HVAC) |
| 8004 | `media_server.py` | Media + Radio + Music |
| 8005 | `phone_server.py` | Phone + Messages + Bluetooth/WiFi |
| 8006 | `calendar_server.py` | Calendar |
| 8007 | `weather_server.py` | Weather + Info Query |
| 8008 | `interior_server.py` | Windows + Lights + Seats |
| 8009 | `hud_server.py` | HUD Display |
| 8010 | `system_server.py` | System Settings + Voice |
| 8011 | `wireless_server.py` | WiFi + Bluetooth (dedicated) |
| 8012 | `camera_server.py` | Cameras + Dashcam |
| 8013 | `interaction_server.py` | UI Interaction |
| 8014 | `app_server.py` | App Management |

### 3. Dialogue Management (DM) per Agent
Each agent owns its own DM module. Example for Navigation Agent:

```
function_call/dm/navigation/
├── route.py          # Route planning skills
├── poi.py            # POI search skills
├── map.py            # Map control skills
└── traffic.py        # Traffic query skills
```

### 4. Shared Slot Schema
Slots should be normalized across agents using the schemas from `slot_intent.json`:

| Slot Type | Examples | Agent Handling |
|---|---|---|
| Position | 主驾, 副驾, 后排 | Seat Agent, HVAC Agent |
| Number/Ratio | 温度, 风速, 亮度 | All agents with adjustable settings |
| POI | 餐厅, 加油站 | Navigation Agent |
| Media_Source | 蓝牙, USB, 在线 | Media Agent |
| City/Location | 城市名 | Weather Agent, Navigation Agent |
| Time | 分钟, 时间 | User Profile, Media |
| Mode | 驾驶模式, 场景 | System Settings, Vehicle Control |

### 5. Priority Routing
Agents should have a **fallback cascade** when slots are ambiguous:

```
Navigation Agent → Intent unknown → Fallback to Media Agent
Media Agent → Song not found → Fallback to Weather Agent
All → Intent unknown → Trigger rejection with default NLG
```

### 6. Multi-User Concurrency

Each user gets isolated MCP connections via the `MCPClient`:

```python
# Each (user_id, server_name) pair gets its own transport and session
await mcp_client.connect(server_url, user_id="user123", server_name="nav_server")
await mcp_client.connect(server_url, user_id="user456", server_name="nav_server")
# Both users can call tools simultaneously without interference
```
