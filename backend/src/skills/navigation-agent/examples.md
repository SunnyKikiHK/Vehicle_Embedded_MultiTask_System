# Navigation Agent — Annotated Examples

## Turn 1 — Basic POI Navigation (Nearby)

**User:** "导航到最近的加油站"
**Matched Intent:** `go_poi`
**Arguments:** `{"poi": "加油站", "search_mode": "nearby"}`

**Reconstruction:** "导航到最近的加油站"

**Action:** Search nearby gas stations, start navigation to nearest.
**Response:** "已为您导航到最近的加油站，预计5分钟到达。"

---

## Turn 2 — POI Navigation (City-wide)

**User:** "导航到故宫"
**Matched Intent:** `go_poi`
**Arguments:** `{"poi": "故宫", "search_mode": "city", "city": "北京"}`

**Reconstruction:** "导航到北京故宫"

**Action:** Search for "故宫" in Beijing, start navigation.
**Response:** "已为您导航到故宫，预计15分钟到达。"

---

## Turn 3 — Navigate Home with Route Calculation

**User:** "回家"
**Matched Intent:** `go_home`
**Arguments:** `{}`

**Reconstruction:** "导航回家"

**Action:** Resolve home address from database, calculate route from current GPS, return navigation with distance and ETA.
**Response:** "好的，正在为您导航回家，目标：家，距离15.6公里，预计25分钟。"

Or if home not set:
**Response:** "尚未设置家地址，请先设置。"

---

## Turn 3b — Navigate to Company with Route Calculation

**User:** "去公司"
**Matched Intent:** `go_company`
**Arguments:** `{}`

**Reconstruction:** "导航到公司"

**Action:** Resolve company address from database, calculate route from current GPS, return navigation with distance and ETA.
**Response:** "好的，正在为您导航到公司，目标：公司，距离8.3公里，预计15分钟。"

Or if company not set:
**Response:** "尚未设置公司地址，请先设置。"

Or if GPS not available:
**Response:** "无法获取当前位置，请确保GPS已开启。"

---

## Turn 4 — Route Recalculation

**User:** "重新算路"
**History:** Active navigation to a POI
**Matched Intent:** `flush_route`
**Arguments:** `{}`

**Reconstruction:** "重新计算路线"

**Action:** Trigger route recalculation with current traffic data.
**Response:** "路线已重新规划，当前路线比原路线快10分钟。"

---

## Turn 5 — Navigate Home When Not Set

**User:** "回家"
**Matched Intent:** `go_home`
**Arguments:** `{}`

**Reconstruction:** "导航回家"

**Action:** User has not set a home address.
**Response:** "尚未设置家地址，请先对我说'把我的家设置在XXX'来设置家庭地址。"

---

## Turn 6 — Zoom Map

**User:** "放大地图"
**Matched Intent:** `nav_zoom_in`
**Arguments:** `{}`

**Reconstruction:** "放大地图"

**Action:** Increase map zoom level by one step.
**Response:** "地图已放大。"

---

## Turn 7 — Set Route Preference

**User:** "不走高速"
**History:** Active route
**Matched Intent:** `avoid_high_way`
**Arguments:** `{}`

**Reconstruction:** "切换到不走高速模式"

**Action:** Recalculate route avoiding highways.
**Response:** "好的，已切换到不走高速路线。"

---

## Turn 8 — Add Waypoint

**User:** "中途去一趟超市"
**History:** Active navigation to destination
**Matched Intent:** `add_via`
**Arguments:** `{"poi": "超市"}`

**Reconstruction:** "在途中添加途经点：超市"

**Action:** Find nearest supermarket along route, add as waypoint.
**Response:** "已添加超市为途经点，预计比原路线多10分钟。"

---

## Turn 9 — Save Current Location

**User:** "把当前位置收藏"
**Matched Intent:** `collect_location`
**Arguments:** `{}`

**Reconstruction:** "收藏当前地址"

**Action:** Get current GPS coordinates, prompt user for a name.
**Response:** "好的，当前位置已获取。请告诉我一个名称来保存这个地点。"

---

## Turn 10 — Check Traffic on Route Home

**User:** "回家路上堵吗？"
**History:** User's home address is known
**Matched Intent:** `check_route_traffic`
**Arguments:** `{"destination": "家"}`

**Reconstruction:** "查询回家路线的交通状况"

**Action:** Calculate route home, query real-time traffic data.
**Response:** "回家路线目前畅通，预计比平时多5分钟。"

---

## Turn 11 — Check Area Traffic

**User:** "故宫附近堵不堵？"
**Matched Intent:** `check_area_traffic`
**Arguments:** `{"poi": "故宫", "radius": 1000}`

**Reconstruction:** "查询故宫周边的交通状况"

**Action:** Query traffic conditions around the Palace Museum.
**Response:** "故宫周边目前畅通，道路通畅。"

---

## Turn 12 — Check City Traffic Overview

**User:** "北京现在堵不堵？"
**Matched Intent:** `check_city_traffic_overview`
**Arguments:** `{"city": "北京"}`

**Reconstruction:** "查询北京全城交通状况"

**Action:** Query city-wide traffic congestion data.
**Response:** "北京目前整体交通状况良好，部分区域缓行。"

---

## Turn 13 — Switch to 3D View

**User:** "切换到3D视图"
**Matched Intent:** `set_3d_map`
**Arguments:** `{}`

**Reconstruction:** "切换地图为3D视图"

**Action:** Toggle map to 3D perspective mode.
**Response:** "已切换到3D视图。"

---

## Turn 14 — Set Home Address

**User:** "把我的家设置在望京SOHO"
**Matched Intent:** `set_frequent_location`
**Arguments:** `{"location_type": "home", "poi": "望京SOHO"}`

**Reconstruction:** "设置望京SOHO为家庭地址"

**Action:** Search for the location and confirm with user.
**Response:** "已找到地址，请确认是否将其设置为家？"

---

## Turn 15 — Query Current Location

**User:** "我在哪？"
**Matched Intent:** `ask_where_am_i`
**Arguments:** `{}`

**Reconstruction:** "查询当前位置"

**Action:** Get current GPS coordinates and reverse geocode to address.
**Response:** "当前位置在北京市朝阳区望京街道望京SOHO。"

---

## Turn 16 — Create Travel Group

**User:** "创建一个车队"
**Matched Intent:** `build_group`
**Arguments:** `{}`

**Reconstruction:** "创建车队"

**Action:** Create a new group and generate invite code.
**Response:** "好的，已创建车队，邀请码是 ABC123。"
