# Media Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Search_Music | search_music | `{"keyword": "...", "artist": "..."}` | 音乐搜索 |
|| Play_Online_Music | play_music | `{"source": "online"}` | 播放在线音乐 |
|| Play_BT_Music | play_music | `{"source": "bluetooth"}` | 播放蓝牙音乐 |
|| Play_USB_Music | play_media | `{"source": "usb"}` | 播放USB音乐 |
|| Play_Similar_Music | play_music | `{"action": "similar"}` | 播放相似歌曲 |
|| Media_Next | next_track | `{}` | 下一首 |
|| Media_Last | previous_track | `{}` | 上一首 |
|| Media_Pause | pause_media | `{}` | 暂停播放 |
|| Continue_Play | play_media | `{"action": "resume"}` | 继续播放 |
|| Replay | play_media | `{"action": "replay"}` | 重新播放 |
|| Quick_Go | play_media | `{"seek": N}` | 快进 |
|| Quick_Back | play_media | `{"seek": -N}` | 快退 |
|| Set_Speed_By_Speed | play_media | `{"speed": N}` | 倍速播放 |
|| Play_repeatly | like_song | `{"action": "repeat_one"}` | 单曲循环 |
|| List_Repeat | play_playlist | `{"mode": "repeat_all"}` | 列表循环 |
|| Media_Random_Play | play_playlist | `{"mode": "shuffle"}` | 随机播放 |
|| Media_Order_Play | play_playlist | `{"mode": "sequential"}` | 顺序播放 |
|| Search_Radio | scan_radio | `{"keyword": "..."}` | 电台搜索 |
|| Open_Radio_By_Name | tune_radio | `{"station": "..."}` | 打开指定电台 |
|| Play_OL_Radio | play_media | `{"source": "online_radio"}` | 播放在线广播 |
|| Play_Local_Radio | play_media | `{"source": "fm/am"}` | 播放本地电台 |
|| Media_Collect | like_song | `{"action": "add"}` | 收藏 |
|| Cancel_Media_Collect | like_song | `{"action": "remove"}` | 取消收藏 |
|| Play_Media_Collection | play_music | `{"source": "favorites"}` | 播放多媒体收藏 |
|| View_Play_Music | play_media | `{"action": "query"}` | 查询当前播放歌曲 |
|| View_Play_Music_Singer | play_media | `{"action": "query_artist"}` | 查询当前播放歌曲歌手 |
|| View_Play_Album | play_media | `{"action": "query_album"}` | 查询当前播放专辑 |
|| View_Play_Radio | play_media | `{"action": "query_radio"}` | 查询当前播放电台 |
|| Search_News | play_media | `{"source": "news"}` | 新闻搜索 |
|| Open_o3ics | play_media | `{"action": "lyrics_on"}` | 打开歌词 |
|| Close_o3ics | play_media | `{"action": "lyrics_off"}` | 关闭歌词 |
|| Open_Play_Detail | play_media | `{"action": "details_on"}` | 打开播放详情 |
|| Close_Play_Detail | play_media | `{"action": "details_off"}` | 关闭播放详情 |
|| Download_Current_Content | play_media | `{"action": "download"}` | 下载当前内容 |

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

|| Criteria | Weight | Notes |
|----------|--------|-------|
| Name | High | Primary match field |
| Singer | High | Primary match field |
| Album | Medium | Secondary |
| Genre | Medium | For browse/radio mode |
| Mood / Style / Scene | Medium | For recommendation |
| Language | Low | Filter |
| Age | Low | Filter |
