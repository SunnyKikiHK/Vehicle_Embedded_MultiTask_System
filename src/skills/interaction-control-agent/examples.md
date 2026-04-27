# Interaction Control Agent — Annotated Examples

## Turn 1 — Confirm an Action

**User:** "好的"
**History:** System asked "确定要关闭空调吗？"
**Matched Intent:** `Confirm`
**Slots extracted:** none

**Reconstruction:** "确认关闭空调"

**Action:** Execute the pending action (close AC).
**Response:** "好的，已关闭空调。"

---

## Turn 2 — Cancel an Action

**User:** "算了，不用了"
**History:** System asked "是否打开座椅加热？"
**Matched Intent:** `Cancel`
**Slots extracted:** none

**Reconstruction:** "取消操作"

**Action:** Abort the pending action, return to previous state.
**Response:** "好的，已取消。"

---

## Turn 3 — Select from List

**User:** "选第二个"
**History:** System presented "找到3个结果：1. 晴天 2. 七里香 3. 稻香"
**Matched Intent:** `List_Select`
**Slots extracted:**
- `Index = 2`

**Reconstruction:** "选择第2项"

**Action:** Play the second item (七里香).
**Response:** "已选择：七里香，周杰伦，正在播放。"

---

## Turn 4 — Open Help

**User:** "打开帮助"
**Matched Intent:** `Open_Help`
**Slots extracted:** none

**Reconstruction:** "打开帮助中心"

**Action:** Launch the help center application.
**Response:** "帮助中心已打开。您可以浏览常见问题，或直接问我如何使用各项功能。"

---

## Turn 5 — Set Custom Response Word

**User:** "把应答词改成知道了"
**Matched Intent:** `Get_Answer`
**Slots extracted:**
- `Response = 知道了`

**Reconstruction:** "设置应答词为知道了"

**Action:** Validate "知道了" (not a common phrase, not reserved), save to user profile.
**Response:** "应答词已设置为'知道了'。以后您可以说'知道了'来确认操作。"

---

## Turn 6 — Delete Response Word

**User:** "删除应答词"
**History:** Custom response word is "知道了"
**Matched Intent:** `Delete_Answer_Words`
**Slots extracted:** none

**Reconstruction:** "删除自定义应答词"

**Action:** Remove custom response word, restore default confirmation words.
**Response:** "应答词已删除，已恢复默认确认方式。"

---

## Turn 7 — Open Two Items Together

**User:** "同时打开空调和音乐"
**Matched Intent:** `Open_Two_Both`
**Slots extracted:** none

**Reconstruction:** "同时打开空调和音乐"

**Action:** Send parallel commands to HVAC Agent and Media Agent.
**Response:** "好的，已同时打开空调和音乐。"

---

## Turn 8 — Cancel and Go Back

**User:** "取消"
**History:** User was navigating through a settings menu
**Matched Intent:** `Cancel`
**Slots extracted:** none

**Reconstruction:** "取消当前操作并返回"

**Action:** Exit the current menu or cancel the current operation.
**Response:** "已取消。"
