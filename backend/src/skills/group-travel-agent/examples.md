# Group Travel Agent — Annotated Examples

## Turn 1 — Create a Group

**User:** "创建车队"
**Matched Intent:** `build_group`
**Arguments:** `{}`

**Reconstruction:** "创建新的组队"

**Action:** Create a new group, generate invite code, set user as leader.
**Response:** "车队已创建，您的邀请码是AB12CD。请分享给队友，他们可以说'加入车队'并输入邀请码。"

---

## Turn 2 — Join a Group

**User:** "加入车队AB12CD"
**Matched Intent:** `join_group`
**Arguments:** `{"code": "AB12CD"}`

**Reconstruction:** "加入车队AB12CD"

**Action:** Validate invite code, add user to group, start location sharing with consent.
**Response:** "已成功加入车队，当前车队共4人。您已成为队员，请遵守车队安排。"

---

## Turn 3 — Set Meetup Point

**User:** "在前面的服务区集合"
**History:** Active group trip
**Matched Intent:** `ask_meeting_place`
**Arguments:** `{"location": "服务区"}`

**Reconstruction:** "设置前方服务区为汇合地点"

**Action:** Find nearest service area, set as meetup point, notify all members.
**Response:** "已设置前方15公里的休息区为汇合地点，已通知所有队员。"

---

## Turn 4 — Navigate to Meetup Point

**User:** "导航到汇合点"
**History:** Meetup point set
**Matched Intent:** `go_meeting_place`
**Arguments:** `{}`

**Reconstruction:** "导航到已设置的汇合地点"

**Action:** Get meetup point coordinates from group state, start navigation.
**Response:** "正在导航到汇合地点休息区，距离约15公里，预计12分钟到达。"

---

## Turn 5 — View Member Locations

**User:** "看看队友都在哪？"
**History:** Active group with 4 members
**Matched Intent:** `group_member_location`
**Arguments:** `{}`

**Reconstruction:** "查看车队成员当前位置"

**Action:** Query location of all group members, compute relative positions.
**Response:** "车队成员位置：
- 张三：距您8公里，前方高速
- 李四：距您12公里，前方
- 王五：距您5公里，左后方服务区"

---

## Turn 6 — Exit Group

**User:** "退出车队"
**History:** Active group membership
**Matched Intent:** `quit_group`
**Arguments:** `{}`

**Reconstruction:** "退出当前车队"

**Action:** Remove user from group, stop location sharing, end navigation if it was group-related.
**Response:** "已退出车队。期待下次同行，祝您一路平安。"
