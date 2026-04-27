# Media Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 2 | Search_Music | 音乐搜索 |
| 363 | Play_Online_Music | 播放在线音乐 |
| 114 | Play_BT_Music | 播放蓝牙音乐 |
| 208 | Play_USB_Music | 播放USB音乐 |
| 215 | Play_Similar_Music | 播放相似歌曲 |
| 288 | Close_Play_Similar_Music | 退出相似歌曲 |
| 433 | Open_K | 打开k歌 |
| 434 | Close_K | 关闭k歌 |
| 431 | Select_Sing | 唱歌搜索 |
| 150 | Search_News | 新闻搜索 |
| 99 | Play_History | 播放历史记录 |
| 109 | Open_Play_History | 打开播放历史 |
| 299 | Close_Play_History | 关闭播放历史 |
| 196 | Play_repeatly | 单曲循环 |
| 223 | List_Repeat | 列表循环 |
| 221 | Media_Random_Play | 随机播放 |
| 366 | Media_Order_Play | 顺序播放 |
| 25 | Change_Play_Mode | 切换播放模式 |
| 19 | Cancel_Play_Mode | 取消当前播放模式 |
| 8 | Quick_Go | 快进 |
| 139 | Quick_Back | 快退 |
| 178 | Media_Next | 下一首 |
| 250 | Media_Last | 上一首 |
| 44 | Media_Pause | 暂停播放 |
| 119 | Continue_Play | 继续播放 |
| 317 | Replay | 重新播放 |
| 166 | Set_Speed_By_Speed | 倍速播放 |
| 130 | Switch_Music_Quantity | 音质切换 |
| 198 | Media_Collect | 收藏 |
| 219 | Cancel_Media_Collect | 取消收藏 |
| 312 | Play_Media_Collection | 播放多媒体收藏 |
| 257 | Open_Media_Collection | 打开多媒体收藏 |
| 258 | Close_Media_Collection | 关闭多媒体收藏 |
| 10 | Open_Play_Detail | 打开播放详情 |
| 34 | Close_Play_Detail | 关闭播放详情 |
| 51 | Search_Radio | 电台搜索 |
| 50 | Open_Radio_By_Name | 打开指定电台 |
| 142 | Play_OL_Radio | 播放在线广播 |
| 72 | Play_Local_Radio | 播放本地电台 |
| 386 | Play_Hot_Radio | 今日热点 |
| 401 | Replay_Broadcast | 重播广播 |
| 265 | View_Play_Radio | 查询当前播放电台 |
| 264 | View_Play_Frequency | 查询当前播放频道 |
| 427 | View_Play_Music | 查询当前播放歌曲 |
| 422 | View_Play_Music_Singer | 查询当前播放歌曲歌手 |
| 346 | View_Play_Album | 查询当前播放专辑 |
| 277 | View_Play_Content | 查询当前播放内容 |
| 148 | View_Play_News | 查询当前播放新闻 |
| 73 | Download_Current_Content | 下载当前内容 |
| 160 | Get_exact_time_For_Play | 从时间开始播放 |
| 85 | Search_Station | 广播搜索 |
| 102 | Open_o3ics | 打开歌词 |
| 321 | Close_o3ics | 关闭歌词 |
| 102 | Open_Player | 打开播放器 |
| 169 | Close_Player | 关闭播放器 |
| 307 | Open_Play_List | 打开播放列表 |
| 170 | Close_Play_List | 关闭播放列表 |

## Shared Slot Type Definitions

### Media_Source
```
enum: 蓝牙, USB, 在线, 本地, 电台
resolution: Resolve to current or last-used source. Default to 在线.
agents: Media Agent
```

### Name
```
resolution: Match song name or artist. Fuzzy search across all sources.
agents: Media Agent
```

### Time
```
value_range: mm:ss or seconds
resolution: Normalize to seconds for playback seek operations.
agents: Media Agent
```

### Speed
```
value_range: decimal (e.g., 0.5, 1.0, 1.5, 2.0)
resolution: Playback speed multiplier. Default to 1.0 (normal speed).
agents: Media Agent
```

### Quantity
```
enum: 高, 中, 低, 标准, 无损, HIFI
resolution: Audio quality level. Default to last-used or standard.
agents: Media Agent
```

### Collect_Source
```
resolution: Source where the favorite item is stored (same as Media_Source).
agents: Media Agent
```

## Media Source Priority

When user doesn't specify a source, actions apply to the currently active source. Priority order: `在线 > 蓝牙 > USB > 本地 > 电台`.

## Search Criteria Weighting

| Criteria | Weight | Notes |
|----------|--------|-------|
| Name | High | Primary match field |
| Singer | High | Primary match field |
| Album | Medium | Secondary |
| Genre | Medium | For browse/radio mode |
| Mood / Style / Scene | Medium | For recommendation |
| Language | Low | Filter |
| Age | Low | Filter |
