---
name: media-agent
description: Implements Media Agent intents in the vehicle embedded multi-task system. Handles music playback, radio, news, K-song, volume control, media source switching, and all audio/video entertainment. Use when the user mentions music, songs, radio, news, volume, playback controls, Bluetooth, USB, or media. Trigger terms: 播放音乐, 下一首, 上一首, 暂停, 继续播放, 搜索歌曲, 蓝牙音乐, USB音乐, 收藏, 电台, 新闻, 音量, 单曲循环, 随机播放, 快进, 快退, 播放, 停止, K歌.
---

# Media Agent — Music, Radio & Entertainment Skill

## Agent Overview

**Handles:** Music playback, radio, news, K-song, and all audio/video control.
**Total intents: 69**
**Shared slot types:** `Name`, `Media_Source`, `Time`, `Speed`, `Quantity`, `Collect_Source`

## Core Intent Categories

### Music Search & Playback

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 音乐搜索 | Search_Music | Name, Mood, Singer, album, genre, location, Style, Scene, Keywords | Search music by various criteria |
| 播放在线音乐 | Play_Online_Music | — | Play online music |
| 播放蓝牙音乐 | Play_BT_Music | — | Play Bluetooth music |
| 播放USB音乐 | Play_USB_Music | — | Play music from USB |
| 播放相似歌曲 | Play_Similar_Music | — | Play similar songs |
| 退出相似歌曲 | Close_Play_Similar_Music | — | Exit similar song mode |

### Playback Control

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 下一首 | Media_Next | — | Next track |
| 上一首 | Media_Last | — | Previous track |
| 暂停播放 | Media_Pause | Media_Source | Pause playback |
| 继续播放 | Continue_Play | Media_Source | Resume playback |
| 重新播放 | Replay | — | Replay current track |
| 快进 | Quick_Go | Media_Source, Time | Fast forward |
| 快退 | Quick_Back | Media_Source, Time | Rewind |
| 倍速播放 | Set_Speed_By_Speed | Speed | Set playback speed |
| 从时间开始播放 | Get_exact_time_For_Play | Time | Play from specific time |

### Play Mode

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 单曲循环 | Play_repeatly | — | Enable single-track repeat |
| 列表循环 | List_Repeat | — | Enable playlist repeat |
| 随机播放 | Media_Random_Play | — | Enable shuffle play |
| 顺序播放 | Media_Order_Play | — | Enable sequential play |
| 切换播放模式 | Change_Play_Mode | — | Cycle through play modes |
| 取消当前播放模式 | Cancel_Play_Mode | — | Cancel current play mode |

### Media Source

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开播放器 | Open_Player | Media_Source | Open media player |
| 关闭播放器 | Close_Player | Media_Source | Close media player |
| 打开播放列表 | Open_Play_List | Media_Source | Open playlist |
| 关闭播放列表 | Close_Play_List | Media_Source | Close playlist |
| 播放历史记录 | Play_History | Media_Source | Play playback history |
| 打开播放历史 | Open_Play_History | Media_Source | Open playback history |
| 关闭播放历史 | Close_Play_History | Media_Source | Close playback history |
| 音质切换 | Switch_Music_Quantity | Quantity | Switch audio quality |

### Lyrics & Detail

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开歌词 | Open_o3ics | — | Show lyrics |
| 关闭歌词 | Close_o3ics | — | Hide lyrics |
| 打开播放详情 | Open_Play_Detail | Media_Source | Open playback details |
| 关闭播放详情 | Close_Play_Detail | Media_Source | Close playback details |

### Radio & Broadcast

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 电台搜索 | Search_Radio | Type, Name, Today | Search radio stations |
| 打开指定电台 | Open_Radio_By_Name | Name | Open specific radio station |
| 播放在线广播 | Play_OL_Radio | — | Play online radio |
| 播放本地电台 | Play_Local_Radio | FM, AM | Play local FM/AM radio |
| 今日热点 | Play_Hot_Radio | — | Play today's hot stations |
| 重播广播 | Replay_Broadcast | — | Replay broadcast |
| 广播搜索 | Search_Station | Type, Name | Search broadcast stations |

### News

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 新闻搜索 | Search_News | Type, Key, Person, Area, Today | Search news |
| 查询当前播放新闻 | View_Play_News | — | Query current playing news |

### K-Song

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开k歌 | Open_K | — | Open karaoke mode |
| 关闭k歌 | Close_K | — | Close karaoke mode |
| 唱歌搜索 | Select_Sing | Singer, Song | Search for karaoke song |

### Favorites

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 收藏 | Media_Collect | Media_Source | Add to favorites |
| 取消收藏 | Cancel_Media_Collect | Media_Source | Remove from favorites |
| 播放多媒体收藏 | Play_Media_Collection | Collect_Source | Play from favorites |
| 打开多媒体收藏 | Open_Media_Collection | Media_Source | Open favorites list |
| 关闭多媒体收藏 | Close_Media_Collection | Media_Source | Close favorites |

### Query

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查询当前播放歌曲 | View_Play_Music | — | Query current playing song |
| 查询当前播放歌曲歌手 | View_Play_Music_Singer | — | Query current song artist |
| 查询当前播放专辑 | View_Play_Album | — | Query current album |
| 查询当前播放内容 | View_Play_Content | Just | Query current playback info |
| 查询当前播放电台 | View_Play_Radio | — | Query current radio |
| 查询当前播放频道 | View_Play_Frequency | — | Query current frequency |
| 下载当前内容 | Download_Current_Content | — | Download current media |

## Slot Resolution Rules

- **Media_Source**: Resolve to `蓝牙`, `USB`, `在线`, `本地`, `电台`. Default to last-used source.
- **Name**: Song name or artist name. Use fuzzy search across all sources.
- **Time**: For seek, format as `mm:ss`. For fast forward/back, as `seconds`.
- **Speed**: Playback speed as decimal (e.g., `1.5`, `2.0`).
- **Collect_Source**: Source of the favorite item (same as Media_Source).
- When **user says a song name** without explicit action, treat as `Search_Music` with `Name` slot.
- When **user says just "播放"** without any qualifier, continue last played track.

## Implementation Checklist

When implementing a new Media intent:

1. **Match the intent key** (e.g., `Media_Next`) to the skill function.
2. **Determine current media source** — check what is currently playing.
3. **Execute the action** via the media service API for the current source.
4. **Return current track info** if query intent (e.g., `View_Play_Music`).
5. **Confirm** with natural response (e.g., "已切换到下一首" or "当前播放：晴天，周杰伦").
6. **Save SlotContext** to Redis with `agent=Media Agent`, `intent=<matched_intent>`, and extracted slots.

## Response Templates

```
播放: "正在为您播放{歌曲名}，{歌手}。"
下一首: "好的，已切换到下一首。"
上一首: "好的，已切换到上一首。"
暂停: "已暂停播放。"
继续: "已继续播放。"
收藏: "已收藏到我的最爱。"
搜索: "为您找到{数量}首相关歌曲：{列表}。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
