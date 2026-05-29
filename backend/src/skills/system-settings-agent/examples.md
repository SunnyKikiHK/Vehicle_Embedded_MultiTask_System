# System Settings Agent — Annotated Examples

## Turn 1 — Open an App

**User:** "打开音乐App"
**Matched Intent:** `open_app`
**Arguments:** `{"name": "音乐"}`

**Reconstruction:** "打开音乐应用"

**Action:** Search and launch the music application.
**Response:** "已打开音乐应用。"

---

## Turn 2 — Close an App

**User:** "关闭这个应用"
**Matched Intent:** `close_app`
**Arguments:** `{"name": "当前应用"}`

**Reconstruction:** "关闭当前应用"

**Action:** Close the current foreground application.
**Response:** "已关闭当前应用。"

---

## Turn 3 — Back to Home Screen

**User:** "回主页"
**Matched Intent:** `system_settings`
**Arguments:** `{"action": "home"}`

**Reconstruction:** "返回主页"

**Action:** Dismiss current app/view and return to home screen.
**Response:** "正在返回主页。"

---

## Turn 4 — Take Screenshot

**User:** "截屏"
**Matched Intent:** `screenshot_screen`
**Arguments:** `{}`

**Reconstruction:** "截取屏幕"

**Action:** Capture current screen and save to gallery.
**Response:** "截屏已保存。"

---

## Turn 5 — Show Notification

**User:** (system notification)
**Matched Intent:** `show_notification`
**Arguments:** `{"title": "提醒", "content": "您的预约保养时间到了"}`

**Reconstruction:** 显示通知

**Action:** Display a notification to the user.
**Response:** (notification appears on screen)

---

## Turn 6 — Dismiss Notification

**User:** "知道了"
**History:** Notification displayed
**Matched Intent:** `dismiss_notification`
**Arguments:** `{}`

**Reconstruction:** "关闭通知"

**Action:** Dismiss the current notification.
**Response:** (notification dismissed)

---

## Turn 7 — Language Setting

**User:** "把语言改成英文"
**Matched Intent:** `language_setting`
**Arguments:** `{"language": "英文"}`

**Reconstruction:** "设置系统语言为英文"

**Action:** Change system language to English.
**Response:** "系统语言已切换为英文。"

---

## Turn 8 — Open System Settings

**User:** "打开系统设置"
**Matched Intent:** `system_settings`
**Arguments:** `{}`

**Reconstruction:** "打开系统设置"

**Action:** Open the system settings panel.
**Response:** "已打开系统设置。"

---

## Turn 9 — Sound Settings

**User:** "打开声音设置"
**Matched Intent:** `sound_setting`
**Arguments:** `{}`

**Reconstruction:** "打开声音设置"

**Action:** Open sound settings panel.
**Response:** "已打开声音设置。"

---

## Turn 10 — Reset Settings

**User:** "恢复默认设置"
**Matched Intent:** `reset_settings`
**Arguments:** `{}`

**Reconstruction:** "恢复系统默认设置"

**Action:** Reset all settings to factory defaults.
**Response:** "已恢复默认设置。"
