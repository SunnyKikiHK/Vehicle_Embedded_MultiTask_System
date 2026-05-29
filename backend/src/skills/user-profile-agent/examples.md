# User Profile Agent — Annotated Examples

**Note:** User profile agent intents are primarily voice/TTS settings. These typically don't map directly to MCP tools but are handled through the voice assistant configuration. Below are examples showing the expected output format.

## Turn 1 — Switch to Female Voice

**User:** "换成女声"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "语音设置", "content": "已切换到女声"}`

**Reconstruction:** "切换到女声音色"

**Action:** Set TTS voice to female preset.
**Response:** "已切换到女声。您觉得这个声音怎么样？"

---

## Turn 2 — Adjust Speech Speed

**User:** "语速调快一点"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "语音设置", "content": "语速已加快"}`

**Reconstruction:** "将语速调整为较快"

**Action:** Increase TTS speed.
**Response:** "语速已加快。"

---

## Turn 3 — Show Notification for Settings

**User:** "打开语音设置"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "设置", "content": "语音设置已打开"}`

**Reconstruction:** "打开语音助手设置"

**Action:** Launch the voice assistant settings app/page.
**Response:** "语音设置已打开。"
