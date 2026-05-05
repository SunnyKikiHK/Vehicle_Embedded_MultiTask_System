---
name: media-agent
description: Implements Media Agent intents in the vehicle embedded multi-task system. Handles music playback, radio, news, K-song, volume control, media source switching, and all audio/video entertainment. Use when the user mentions music, songs, radio, news, volume, playback controls, Bluetooth, USB, or media. Trigger terms: 播放音乐, 下一首, 上一首, 暂停, 继续播放, 搜索歌曲, 蓝牙音乐, USB音乐, 收藏, 电台, 新闻, 音量, 单曲循环, 随机播放, 快进, 快退, 播放, 停止, K歌.
---

# Media Agent — Music, Radio & Entertainment Skill

## Agent Overview

**Handles:** Music playback, radio, news, K-song, and all audio/video control.
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

### Music Search & Playback

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 搜索歌曲 | search_music | `{"keyword": "<Name>"}` | Search music by name |
| 播放音乐 | play_music | `{}` | Play music |
| 暂停播放 | pause_media | `{}` | Pause playback |
| 继续播放 | play_media | `{}` | Resume playback |
| 下一首 | next_track | `{}` | Next track |
| 上一首 | previous_track | `{}` | Previous track |

### Playback Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 暂停 | pause_media | `{}` | Pause playback |
| 播放 | play_media | `{}` | Start/resume playback |
| 停止 | stop_media | `{}` | Stop playback |
| 下一首 | next_track | `{}` | Next track |
| 上一首 | previous_track | `{}` | Previous track |

### Volume Control

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 调高音量 | set_volume | `{"level": <Number>, "direction": "up"}` | Increase volume |
| 调低音量 | set_volume | `{"level": <Number>, "direction": "down"}` | Decrease volume |
| 设置音量 | set_volume | `{"level": <Number>}` | Set volume (0-100) |
| 静音 | mute_volume | `{}` | Mute volume |
| 取消静音 | unmute_volume | `{}` | Unmute volume |

### Play Mode

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 单曲循环 | play_playlist | `{"mode": "repeat_one"}` | Enable single-track repeat |
| 列表循环 | play_playlist | `{"mode": "repeat_all"}` | Enable playlist repeat |
| 随机播放 | play_playlist | `{"mode": "shuffle"}` | Enable shuffle play |
| 收藏歌曲 | like_song | `{}` | Add current song to favorites |

### Radio

| Intent | Tool Name | Arguments | Description |
|--------|-----------|-----------|-------------|
| 打开电台 | radio_on | `{}` | Turn on radio |
| 关闭电台 | radio_off | `{}` | Turn off radio |
| 搜索电台 | scan_radio | `{}` | Scan for radio stations |
| 调到指定电台 | tune_radio | `{"frequency": "<FM/AM>"}` | Tune to specific station |
| 预设电台 | preset_radio | `{"preset": <Number>}` | Select preset station |
| 保存电台 | save_radio_station | `{"frequency": "<FM/AM>"}` | Save current station |

## Slot Resolution Rules

- **Media_Source**: One of: `蓝牙`, `USB`, `在线`, `本地`, `FM`, `AM`, `AUX`, `SD卡`, `WiFi`, `音乐`, `广播`. Default to last-used source
- **Name**: Song name or artist name. Use fuzzy search
- **Direction**: One of: `上`, `下` for volume adjustment
- When **user says a song name** without explicit action, treat as `search_music`

## Implementation Checklist

When implementing a new Media intent:

1. **Identify the intent** from the user's request
2. **Extract slot values** — resolve Media_Source, Name, Direction
3. **Validate** all slot values against the Slot Resolution Rules
4. **Output** the JSON with reasoning, tool_name, and arguments
