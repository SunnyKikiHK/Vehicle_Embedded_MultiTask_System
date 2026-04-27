# User Profile Agent — Annotated Examples

## Turn 1 — Switch to Female Voice

**User:** "换成女声"
**Matched Intent:** `Set_Timbre_Female`
**Slots extracted:** none

**Reconstruction:** "切换到女声音色"

**Action:** Set TTS voice to female preset.
**Response:** "已切换到女声。您觉得这个声音怎么样？"

---

## Turn 2 — Set Custom Wake Word

**User:** "把唤醒词改成小汽车"
**Matched Intent:** `Set_Wakeup_Words`
**Slots extracted:**
- `Wake = 小汽车`

**Reconstruction:** "修改唤醒词为小汽车"

**Action:** Update wake word to "小汽车", prompt user to confirm by saying it.
**Response:** "好的，请对我说两遍'小汽车'来完成唤醒词设置。"

---

## Turn 3 — Enable Continuous Dialogue

**User:** "开启连续对话"
**Matched Intent:** `Open_Continuous_Dialogue`
**Slots extracted:**
- `Time = 5` (default)

**Reconstruction:** "开启连续对话模式"

**Action:** Enable continuous dialogue with default 5-minute session.
**Response:** "连续对话已开启，接下来5分钟内无需说唤醒词即可连续对话。"

---

## Turn 4 — Set Speech Speed

**User:** "语速调快一点"
**Matched Intent:** `Set_Speech_By_Speed`
**Slots extracted:**
- `Speed = 120%` (faster than normal)

**Reconstruction:** "将语速调整为120%"

**Action:** Increase TTS speed from 100% to 120%.
**Response:** "语速已加快。"

---

## Turn 5 — Change Voice Style

**User:** "切换到磁性男声"
**Matched Intent:** `Set_Voice_Style`
**Slots extracted:**
- `Style = 磁性`

**Reconstruction:** "切换语音风格为磁性"

**Action:** Set voice style to "磁性" — deeper tone with more resonance.
**Response:** "语音风格已切换为磁性男声。"

---

## Turn 6 — Only Allow Driver Wake-up

**User:** "设置只有我能唤醒"
**Matched Intent:** `Only_Main`
**Slots extracted:** none

**Reconstruction:** "设置仅主驾可唤醒语音助手"

**Action:** Configure wake-up zone to driver seat only.
**Response:** "已设置仅主驾可唤醒语音助手。"

---

## Turn 7 — Open Voice Settings

**User:** "打开语音设置"
**Matched Intent:** `Open_Sds_Config`
**Slots extracted:** none

**Reconstruction:** "打开语音助手设置"

**Action:** Launch the voice assistant settings app/page.
**Response:** "语音设置已打开。"

---

## Turn 8 — Disable Voice Wake-up

**User:** "把语音唤醒关掉"
**Matched Intent:** `Close_Voice_Wakeup`
**Slots extracted:** none

**Reconstruction:** "关闭语音唤醒功能"

**Action:** Disable the voice wake-up trigger entirely.
**Response:** "语音唤醒已关闭。您可以在设置中重新开启。"

---

## Turn 9 — Set Custom Voice Preset

**User:** "切换到小晴的声音"
**Matched Intent:** `Set_Voice`
**Slots extracted:**
- `Voice = 小晴`

**Reconstruction:** "切换到小晴音色"

**Action:** Load and apply the "小晴" voice pack.
**Response:** "已切换到小晴的声音。"
