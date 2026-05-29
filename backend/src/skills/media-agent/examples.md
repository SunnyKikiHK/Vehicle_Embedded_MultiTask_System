# Media Agent — Annotated Examples

## Turn 1 — Search and Play by Song Name

**User:** "播放七里香"
**Matched Intent:** `search_music`
**Arguments:** `{"keyword": "七里香"}`

**Reconstruction:** "播放七里香"

**Action:** Search for "七里香" across all sources, play first result.
**Response:** "正在为您播放七里香，周杰伦。"

---

## Turn 2 — Search by Artist

**User:** "放一首周杰伦的歌"
**Matched Intent:** `search_music`
**Arguments:** `{"artist": "周杰伦"}`

**Reconstruction:** "播放周杰伦的歌曲"

**Action:** Search songs by 周杰伦, play first result.
**Response:** "为您播放周杰伦的晴天。"

---

## Turn 3 — Switch Playback Source

**User:** "播放USB音乐"
**Matched Intent:** `play_media`
**Arguments:** `{"source": "usb"}`

**Reconstruction:** "切换到USB音乐播放"

**Action:** Switch media source to USB, resume playback.
**Response:** "已切换到USB音乐。"

---

## Turn 4 — Playback Control (Pause)

**User:** "暂停一下"
**History:** Music playing
**Matched Intent:** `pause_media`
**Arguments:** `{}`

**Reconstruction:** "暂停当前播放"

**Action:** Pause playback on current source.
**Response:** "已暂停。"

---

## Turn 5 — Resume Playback

**User:** "继续"
**History:** Music was paused
**Matched Intent:** `play_media`
**Arguments:** `{"action": "resume"}`

**Reconstruction:** "继续播放"

**Action:** Resume playback from paused position.
**Response:** "已继续播放。"

---

## Turn 6 — Play Next Track

**User:** "下一首"
**Matched Intent:** `next_track`
**Arguments:** `{}`

**Reconstruction:** "播放下一首"

**Action:** Skip to next track in current playlist.
**Response:** "好的，已切换到下一首：晴天。"

---

## Turn 7 — Play Mode Change

**User:** "单曲循环"
**History:** Playing some song
**Matched Intent:** `like_song`
**Arguments:** `{"action": "repeat_one"}`

**Reconstruction:** "开启单曲循环模式"

**Action:** Set repeat mode to single-track repeat.
**Response:** "已开启单曲循环。"

---

## Turn 8 — Switch Play Mode

**User:** "随机播放"
**Matched Intent:** `play_playlist`
**Arguments:** `{"mode": "shuffle"}`

**Reconstruction:** "开启随机播放模式"

**Action:** Enable shuffle mode, reorder playlist randomly.
**Response:** "已开启随机播放。"

---

## Turn 9 — Fast Forward

**User:** "快进30秒"
**History:** Playing a song
**Matched Intent:** `play_media`
**Arguments:** `{"seek": 30}`

**Reconstruction:** "快进30秒"

**Action:** Seek forward 30 seconds from current position.
**Response:** "已快进30秒。"

---

## Turn 10 — Query Current Track

**User:** "现在放的是什么歌？"
**Matched Intent:** `play_media`
**Arguments:** `{"action": "query"}`

**Reconstruction:** "查询当前播放歌曲"

**Action:** Query current playback info from media service.
**Response:** "当前播放的是：七里香，周杰伦，来自专辑七里香。"

---

## Turn 11 — Collect Current Song

**User:** "收藏这首歌"
**History:** Playing some song
**Matched Intent:** `like_song`
**Arguments:** `{"action": "add"}`

**Reconstruction:** "收藏当前播放歌曲"

**Action:** Add current track to favorites collection.
**Response:** "已收藏到我的最爱。"

---

## Turn 12 — Tune Radio

**User:** "播放交通广播"
**Matched Intent:** `tune_radio`
**Arguments:** `{"station": "交通广播"}`

**Reconstruction:** "搜索并播放交通广播"

**Action:** Search for traffic radio station, start playback.
**Response:** "正在播放交通广播FM103.9。"

---

## Turn 13 — Volume Control

**User:** "音量调大一点"
**History:** Current volume at 30%
**Matched Intent:** `set_volume`
**Arguments:** `{"level": 40, "direction": "up"}`

**Reconstruction:** "调高音量"

**Action:** Increase volume by 10%.
**Response:** "已调高音量，当前为40%。"
