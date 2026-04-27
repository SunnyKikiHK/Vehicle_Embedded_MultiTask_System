# System Settings Agent — Annotated Examples

## Turn 1 — Open an App

**User:** "打开音乐App"
**Matched Intent:** `Open_App`
**Slots extracted:**
- `app = 音乐`

**Reconstruction:** "打开音乐应用"

**Action:** Search and launch the music application.
**Response:** "已打开音乐应用。"

---

## Turn 2 — Set Desktop Style

**User:** "切换到卡片式桌面"
**Matched Intent:** `Set_Desktop_Style`
**Slots extracted:**
- `Desktop = 卡片式`

**Reconstruction:** "切换桌面样式为卡片式"

**Action:** Apply "卡片式" desktop layout preset.
**Response:** "桌面样式已切换为卡片式。"

---

## Turn 3 — Open Scene Mode

**User:** "打开回家模式"
**Matched Intent:** `Open_Preset_Scene`
**Slots extracted:**
- `Scene = 回家`

**Reconstruction:** "开启回家情景模式"

**Action:** Apply the "回家" preset: HVAC to 24°C, ambient light to warm white 60%, resume media, start navigation home.
**Response:** "已开启回家情景模式。空调已调到24度，正在为您导航回家。"

---

## Turn 4 — Set Sleep Timer

**User:** "30分钟后睡觉"
**Matched Intent:** `Open_Snooze_Mode`
**Slots extracted:**
- `Minute = 30`

**Reconstruction:** "设置30分钟睡眠定时器"

**Action:** Start a 30-minute sleep timer that will dim the screen and mute media.
**Response:** "好的，已设置30分钟后进入睡眠模式。"

---

## Turn 5 — Cancel Sleep Timer

**User:** "取消睡眠模式"
**History:** Sleep timer active
**Matched Intent:** `Close_Snooze_Mode`
**Slots extracted:** none

**Reconstruction:** "取消睡眠定时器"

**Action:** Cancel the active sleep timer.
**Response:** "睡眠定时器已取消。"

---

## Turn 6 — Enable Screen Casting

**User:** "打开投屏"
**Matched Intent:** `Open_ScreenCast`
**Slots extracted:** none

**Reconstruction:** "开启手机投屏"

**Action:** Enable screen casting mode, start searching for nearby devices.
**Response:** "投屏已开启，正在搜索设备。请在手机上选择投屏到车载系统。"

---

## Turn 7 — Back to Home Screen

**User:** "回主页"
**Matched Intent:** `Back_To_Home`
**Slots extracted:** none

**Reconstruction:** "返回主页"

**Action:** Dismiss current app/view and return to home screen.
**Response:** "正在返回主页。"

---

## Turn 8 — Close All Apps and Set Scene

**User:** "开启影院模式"
**Matched Intent:** `Open_Preset_Scene`
**Slots extracted:**
- `Scene = 影院`

**Reconstruction:** "开启影院情景模式"

**Action:** Apply the "影院" preset: HVAC to 25°C quiet mode, lights off, open video app, dim screen.
**Response:** "已开启影院模式。空调已调至静音，氛围灯已关闭，正在打开视频应用。"

---

## Turn 9 — Open Mini App

**User:** "打开小程序"
**Matched Intent:** `Open_Mini_App_Center`
**Slots extracted:** none

**Reconstruction:** "打开小程序中心"

**Action:** Launch the mini app center.
**Response:** "小程序中心已打开。"

---

## Turn 10 — Turn Off Screen

**User:** "关掉屏幕"
**Matched Intent:** `Close_Screen`
**Slots extracted:** none

**Reconstruction:** "关闭屏幕"

**Action:** Turn off the display (system stays running in background).
**Response:** "屏幕已关闭。"
