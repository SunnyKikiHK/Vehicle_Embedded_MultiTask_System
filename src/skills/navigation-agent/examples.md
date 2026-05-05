# Navigation Agent — Annotated Examples

## Turn 1 — Basic POI Navigation

**User:** "导航到最近的加油站"
**Matched Intent:** `go_poi`
**Arguments:** `{"poi": "加油站"}`
**City:** inferred from GPS (current city)

**Reconstruction:** "导航到最近的加油站"

**Action:** Search nearby gas stations, start navigation to nearest.
**Response:** "已为您导航到最近的加油站，预计5分钟到达。"

---

## Turn 2 — Navigate Home with Implicit Destination

**User:** "回家"
**Matched Intent:** `go_home`
**Arguments:** `{}`

**Reconstruction:** "导航回家"

**Action:** Resolve home address from user profile, start navigation.
**Response:** "好的，正在导航回家，预计25分钟到达。"

---

## Turn 3 — Route Recalculation

**User:** "重新算路"
**History:** Active navigation to a POI
**Matched Intent:** `flush_route`
**Arguments:** `{}`

**Reconstruction:** "重新计算路线"

**Action:** Trigger route recalculation with current traffic data.
**Response:** "路线已重新规划，当前路线比原路线快10分钟。"

---

## Turn 4 — Zoom Map

**User:** "放大地图"
**Matched Intent:** `nav_zoom_in`
**Arguments:** `{}`

**Reconstruction:** "放大地图"

**Action:** Increase map zoom level by one step.
**Response:** "地图已放大。"

---

## Turn 5 — Set Route Preference

**User:** "不走高速"
**History:** Active route
**Matched Intent:** `avoid_high_way`
**Arguments:** `{}`

**Reconstruction:** "切换到不走高速模式"

**Action:** Recalculate route avoiding highways.
**Response:** "好的，已切换到不走高速路线。"

---

## Turn 6 — Add Waypoint

**User:** "中途去一趟超市"
**History:** Active navigation to destination
**Matched Intent:** `add_via`
**Arguments:** `{"poi": "超市"}`

**Reconstruction:** "在途中添加途经点：超市"

**Action:** Find nearest supermarket along route, add as waypoint.
**Response:** "已添加超市为途经点，预计比原路线多10分钟。"

---

## Turn 7 — Save Current Location

**User:** "把当前位置收藏"
**Matched Intent:** `collect_current_location`
**Arguments:** `{}`

**Reconstruction:** "收藏当前地址"

**Action:** Get current GPS coordinates, prompt user for a name.
**Response:** "好的，当前位置已获取。请告诉我一个名称来保存这个地点。"

---

## Turn 8 — Check Traffic

**User:** "回家路上堵吗？"
**History:** User's home address is known
**Matched Intent:** `home_condition`
**Arguments:** `{}`

**Reconstruction:** "查询回家路线的交通状况"

**Action:** Calculate route home, query real-time traffic data.
**Response:** "回家路线目前畅通，预计比平时多5分钟。"

---

## Turn 9 — Switch to 3D View

**User:** "切换到3D视图"
**Matched Intent:** `set_3d_map`
**Arguments:** `{}`

**Reconstruction:** "切换地图为3D视图"

**Action:** Toggle map to 3D perspective mode.
**Response:** "已切换到3D视图。"
