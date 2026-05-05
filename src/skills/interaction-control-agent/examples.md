# Interaction Control Agent — Annotated Examples

## Turn 1 — Confirm an Action

**User:** "好的"
**History:** System asked "确定要关闭空调吗？"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "确认", "content": "操作已确认"}`

**Reconstruction:** "确认关闭空调"

**Action:** Execute the pending action (close AC).
**Response:** "好的，已关闭空调。"

---

## Turn 2 — Cancel an Action

**User:** "算了，不用了"
**History:** System asked "是否打开座椅加热？"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "取消", "content": "操作已取消"}`

**Reconstruction:** "取消操作"

**Action:** Abort the pending action, return to previous state.
**Response:** "好的，已取消。"

---

## Turn 3 — Select from List

**User:** "选第二个"
**History:** System presented "找到3个结果：1. 晴天 2. 七里香 3. 稻香"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "选择", "content": "已选择第2项"}`

**Reconstruction:** "选择第2项"

**Action:** Play the second item (七里香).
**Response:** "已选择：七里香，周杰伦，正在播放。"

---

## Turn 4 — Open Help

**User:** "打开帮助"
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "帮助", "content": "帮助中心已打开"}`

**Reconstruction:** "打开帮助中心"

**Action:** Launch the help center application.
**Response:** "帮助中心已打开。您可以浏览常见问题，或直接问我如何使用各项功能。"

---

## Turn 5 — Dismiss Notification

**User:** "知道了"
**History:** Notification displayed
**Matched Intent:** `dismiss_notification`
**Arguments:** `{}`

**Reconstruction:** "关闭通知"

**Action:** Dismiss the current notification.
**Response:** (notification dismissed)"
