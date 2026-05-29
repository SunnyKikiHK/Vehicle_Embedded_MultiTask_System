# Ambient Light Agent — Annotated Examples

## Turn 1 — Turn On Ambient Lights

**User:** "打开氛围灯"
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"switch": "on"}`

**Reconstruction:** "打开氛围灯"

**Action:** Enable ambient lighting at default brightness 40%, last used color.
**Response:** "氛围灯已开启，当前为白色。"

---

## Turn 2 — Change Ambient Light Color

**User:** "氛围灯换成蓝色"
**History:** Ambient lights on
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"color": "蓝色"}`

**Reconstruction:** "把氛围灯颜色切换为蓝色"

**Action:** Change ambient light color to blue across all zones.
**Response:** "氛围灯已切换到蓝色。"

---

## Turn 3 — Set Ambient Light Theme

**User:** "切换到浪漫主题"
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"theme": "浪漫"}`

**Reconstruction:** "切换氛围灯主题为浪漫"

**Action:** Apply "浪漫" theme preset (soft pink/purple gradient with slow breathing effect).
**Response:** "氛围灯主题已切换到浪漫模式。"

---

## Turn 4 — Increase Screen Brightness

**User:** "屏幕亮一点"
**History:** Current brightness 30%
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"target": "screen", "level": 50, "direction": "up"}`

**Reconstruction:** "把屏幕亮度调高"

**Action:** Increase screen brightness from 30% to 50%.
**Response:** "屏幕亮度已调高，当前为50%。"

---

## Turn 5 — Turn Off HUD

**User:** "关掉HUD"
**Matched Intent:** `hud_off`
**Arguments:** `{}`

**Reconstruction:** "关闭HUD显示"

**Action:** Disable HUD display.
**Response:** "HUD已关闭。"

---

## Turn 6 — Adjust HUD Position

**User:** "HUD往上一点"
**Matched Intent:** `hud_mode`
**Arguments:** `{"direction": "vertical", "position": "上"}`

**Reconstruction:** "把HUD位置向上调整"

**Action:** Move HUD display upward by one step.
**Response:** "HUD位置已向上调整。"

---

## Turn 7 — Set Ambient Light Brightness

**User:** "氛围灯调到最亮"
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"level": 100}`

**Reconstruction:** "把氛围灯亮度调到最高"

**Action:** Set ambient light brightness to 100%.
**Response:** "氛围灯亮度已调到最高。"

---

## Turn 8 — Dashboard Brightness

**User:** "仪表盘暗一点"
**History:** Dashboard brightness 80%
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"target": "dashboard", "level": 60, "direction": "down"}`

**Reconstruction:** "把仪表盘亮度调暗"

**Action:** Decrease dashboard brightness from 80% to 60%.
**Response:** "仪表盘亮度已调暗，当前为60%。"

---

## Turn 9 — Turn On Reading Light

**User:** "开一下阅读灯"
**Matched Intent:** `set_reading_light`
**Arguments:** `{"switch": "on"}`

**Reconstruction:** "打开阅读灯"

**Action:** Turn on the reading light for the front cabin area.
**Response:** "阅读灯已开启。"

---

## Turn 10 — Turn Off All Lights

**User:** "把所有灯关掉"
**Matched Intent:** `set_interior_lights`
**Arguments:** `{"switch": "off"}`

**Reconstruction:** "关闭氛围灯"

**Action:** Turn off ambient lighting. (Dashboard/HUD brightness is separate.)
**Response:** "氛围灯已关闭。"
