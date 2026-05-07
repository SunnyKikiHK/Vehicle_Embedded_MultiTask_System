# Skill to MCP Server Mapping

>This document maps the **14 Skills** (intent classification) to the **14 Consolidated MCP Servers** (execution layer).

## Architecture Overview

- **Skills**: LLM-based intent understanding and slot extraction
- **MCP Servers**: Vehicle hardware control via CAN bus / APIs
- **Consolidation**: Multiple logical servers sharing the same port are merged into single server scripts

## Server Consolidation Summary

| Port | Server Script | Logical Servers Combined | Tools Count |
|------|---------------|-------------------------|-------------|
| 8001 | `nav_server.py` | nav_server + map_server | 74 |
| 8002 | `vehicle_server.py` | vehicle_server (standalone) | 9 |
| 8003 | `ac_server.py` | ac_server (standalone) | 8 |
| 8004 | `media_server.py` | media_server + radio_server + music_server | 19 |
| 8005 | `phone_server.py` | phone_server + message_server + wireless_server | 18 |
| 8006 | `calendar_server.py` | calendar_server (standalone) | 5 |
| 8007 | `weather_server.py` | weather_server (standalone) | 3 |
| 8008 | `interior_server.py` | window_server + light_server + seat_server | 19 |
| 8009 | `hud_server.py` | hud_server (standalone) | 4 |
| 8010 | `system_server.py` | system_server (standalone) | 6 |
| 8011 | `wireless_server.py` | wireless_server (standalone) | 6 |
| 8012 | `camera_server.py` | camera_server (standalone) | 5 |
| 8013 | `interaction_server.py` | interaction_server (standalone) | 5 |
| 8014 | `app_server.py` | app_server (standalone) | 4 |

---

## Complete Mapping Table

| Skill | Intents | MCP Server(s) | Notes |
|-------|---------|---------------|-------|
| `phone-agent` | 34 | `phone_server.py` (port 8005) | Calls, contacts, messages, Bluetooth, WiFi |
| `navigation-agent` | 74 | `nav_server.py` (port 8001) | Routes, POI, saved places, map display |
| `media-agent` | 69 | `media_server.py` (port 8004) | Music, radio, news, K-song, volume |
| `hvac-agent` | 43 | `ac_server.py` (port 8003) | Climate control, temperature, ventilation |
| `seat-agent` | 26 | `interior_server.py` (port 8008) | Seat position, heating, massage, mirrors |
| `ambient-light-agent` | 30 | `interior_server.py` (port 8008) + `hud_server.py` (port 8009) | Ambient lights, brightness, HUD |
| `weather-life-agent` | 30 | `weather_server.py` (port 8007) | Weather, life advisory, data |
| `system-settings-agent` | 36 | `system_server.py` (port 8010) | Apps, themes, scenes, system settings |
| `vehicle-control-agent` | 46 | `vehicle_server.py` (port 8002) + `camera_server.py` (port 8012) | Windows, lights, cameras, driving mode |
| `group-travel-agent` | 7 | `nav_server.py` (port 8001) | Shared - route sharing via nav |
| `interaction-control-agent` | 10 | `interaction_server.py` (port 8013) | General UI interaction: confirm, cancel, select, help |
| `user-profile-agent` | 35 | `system_server.py` (port 8010) | Shared - voice settings |
| `car-butler-agent` | 24 | `vehicle_server.py` (port 8002) + `calendar_server.py` (port 8006) | Health, orders, calendar |
| `info-query-agent` | 7 | `weather_server.py` (port 8007) | Shared - time/date via weather |

---

## MCP Server Details

### 1. `nav_server.py` (port 8001) — Navigation, Map & Group Travel

**Consolidated from:** `nav_server.py` + `map_server.py`

| Skill | Intents |
|-------|---------|
| `navigation-agent` | `Go_POI`, `Open_Nav`, `Close_Nav`, `Go_Home`, `Go_Company`, `Nav_Set_Home`, `Nav_Set_Company`, `Add_Via`, `Delete_Via`, `Flush_Route`, `Change_Route`, `Get_Route_Information`, `Open_Full_Map`, `Close_Full_Map`, `Switch_Main_Route`, `Switch_Side_Route`, `Speed_Fast`, `Cancel_Speed_Fast`, `High_Way_First`, `Smart_Recommend`, `Cancel_Smart_Recommend`, `Main_Route_First`, `Cancel_Main_First`, `Avoid_Congestion`, `Cancel_Avoid_Congestion`, `Avoid_High_Way`, `Cancel_Avoid_High_Way`, `Avoid_Limit_Line`, `Cancel_Avoid_Limit_Line`, `Open_Avoid_Fee`, `Cancel_Avoid_Fee`, `Open_Electronic_Eye`, `Close_Electronic_Eye`, `Open_Cruise_Information`, `Close_Cruise_Information`, `Open_AR_Nav`, `Close_AR_Nav`, `Front_Line_Detail`, `Traffic_Incidents`, `Open_Nav_Broadcast`, `Close_Nav_Broadcast`, `Replay_Broadcast`, `Slow_Speed`, `Accelerate_Speed`, `Open_Simple_Broadcast`, `Close_Simple_Broadcast`, `Open_Commute_Nav`, `Close_Commute_Nav`, `Open_Nav_Collections`, `Close_Nav_Collections`, `Nav_To_Collection`, `Collect_Target_Location`, `Collect_Current_Location`, `Ask_Where`, `Open_Map_Setting`, `Close_Map_Setting`, `Change_Nav_Sign`, `Ahead_Condition`, `Target_Condition`, `Home_Condition`, `Company_Condition`, `POI_Condition`, `Nav_Zoom_In`, `Nav_Zoom_Out`, `Nav_Zoom_In_Max`, `Nav_Zoom_Out_Min`, `Back_Center`, `View_Small_Map`, `Close_Small_Map`, `3D_Map`, `2D_Map`, `North_Up`, `Head_Up` |
| `group-travel-agent` | `Join_Group`, `Build_Group`, `Quit_Group`, `Open_Group`, `Ask_Meeting_Place`, `Go_Meeting_Place`, `Group_Member_Location` |

### 2. `vehicle_server.py` (port 8002) — Vehicle Control

| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Get_Vehicle_Speed`, `Get_Fuel_Level`, `Get_Battery_Status`, `Lock_Doors`, `Unlock_Doors`, `Start_Engine`, `Stop_Engine`, `Honk_Horn`, `Flash_Lights` |
| `car-butler-agent` | `Check_Car_Condition`, `Open_Bulter`, `Close_Bulter`, `Reserve_Maintenance`, `Cancel_Reserve`, `Record_Face`, `Open_Personal_Center`, `Close_Personal_Center`, `Open_Owner_Service`, `Close_Owner_Service`, `Open_Feedback`, `Close_Feedback`, `Complains_And_Suggestions`, `View_Already_Order`, `View_Unend_Order`, `View_All_Order`, `Open_Order_Center`, `Close_Order_Center`, `Open_Record_App`, `Close_Record_App`, `Create_Trip_Record` |

### 3. `ac_server.py` (port 8003) — Air Conditioning

| Skill | Intents |
|-------|---------|
| `hvac-agent` | `Ac_On`, `Ac_Off`, `Set_Temperature`, `Set_Fan_Speed`, `Set_Ac_Mode`, `Ac_Auto`, `Defrost`, `Sync_Ac` |

### 4. `media_server.py` (port 8004) — Media, Radio & Music

**Consolidated from:** `media_server.py` + `radio_server.py` + `music_server.py`

| Skill | Intents |
|-------|---------|
| `media-agent` | `Play_Media`, `Pause_Media`, `Stop_Media`, `Next_Track`, `Previous_Track`, `Set_Volume`, `Mute_Volume`, `Unmute_Volume`, `Search_Music`, `Play_Music`, `Play_Playlist`, `Like_Song`, `Tune_Radio`, `Scan_Radio`, `Save_Radio_Station`, `Preset_Radio`, `Radio_On`, `Radio_Off` |

### 5. `phone_server.py` (port 8005) — Phone, Messages & Device Connections

**Consolidated from:** `phone_server.py` + `message_server.py` + `wireless_server.py`

| Skill | Intents |
|-------|---------|
| `phone-agent` | `Make_Call`, `Dial_Contact`, `Answer_Call`, `Reject_Call`, `End_Call`, `Recent_Calls`, `Missed_Calls`, `Send_Message`, `Read_Messages`, `Unread_Messages`, `Delete_Message`, `Reply_Message`, `Bluetooth_On`, `Bluetooth_Off`, `Wifi_On`, `Wifi_Off`, `Connect_Bluetooth`, `Disconnect_Bluetooth` |

### 6. `calendar_server.py` (port 8006) — Calendar & Scheduling

| Skill | Intents |
|-------|---------|
| `car-butler-agent` | `Add_Event`, `View_Calendar`, `Delete_Event`, `Update_Event`, `Today_Events` |

### 7. `weather_server.py` (port 8007) — Weather & Life

| Skill | Intents |
|-------|---------|
| `weather-life-agent` | `Get_Weather`, `Get_Forecast`, `Weather_Alert` |
| `info-query-agent` | `Ask_Where`, `Ask_Weekday`, `Ask_Date`, `Ask_Air_Condition`, `Ask_Humidity`, `Query_UV_Level` |

### 8. `interior_server.py` (port 8008) — Windows, Lights & Seats

**Consolidated from:** `window_server.py` + `light_server.py` + `seat_server.py`

| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Open_Window`, `Close_Window`, `Window_Up`, `Window_Down`, `Window_All_Up`, `Window_All_Down` |
| `ambient-light-agent` | `Set_Interior_Lights`, `Set_Headlights`, `Lights_On`, `Lights_Off`, `Set_Reading_Light` |
| `seat-agent` | `Adjust_Seat`, `Seat_Position`, `Seat_Heating`, `Seat_Ventilation`, `Seat_Massage`, `Recline_Seat`, `Seat_Memory` |

### 9. `hud_server.py` (port 8009) — HUD Display

| Skill | Intents |
|-------|---------|
| `ambient-light-agent` | `Hud_On`, `Hud_Off`, `Hud_Brightness`, `Hud_Mode` |

### 10. `system_server.py` (port 8010) — System Settings & Voice

| Skill | Intents |
|-------|---------|
| `system-settings-agent` | `System_Info`, `System_Settings`, `Language_Setting`, `Display_Setting`, `Sound_Setting`, `Reset_Settings`, `App_List`, `App_Install`, `App_Uninstall`, `App_Update` |
| `user-profile-agent` | `Set_Timbre_Female`, `Set_Timbre_Male`, `Set_Timbre_Child`, `Set_Timbre_Default`, `Change_Timbre`, `Set_Voice`, `Set_Voice_Style`, `Set_Wakeup_Words`, `Ask_Wakeup_Words`, `Delete_Wakeup_Words`, `Open_Free_Wakeup`, `Close_Free_Wakeup`, `Open_Continuous_Dialogue`, `Close_Continuous_Dialogue`, `Set_Continuous_Dialogue`, `Only_Main`, `Main_And_Vice`, `Set_Speech_By_Speed`, `Open_Online_NLU`, `Close_Online_NLU`, `Open_Sds_Config`, `Close_Sds_Config`, `View_Learning_Content`, `Open_Interactive_Learning`, `Close_Interactive_Learning`, `Open_Training_Camp`, `Close_Training_Cmap`, `Open_Skill_Instruction`, `Close_Skill_Instruction`, `Open_Voice_Wakeup`, `Close_Voice_Wakeup`, `Open_Safety_Alarm`, `Close_Safety_Alarm` |

### 11. `wireless_server.py` (port 8011) — WiFi & Bluetooth

| Skill | Intents |
|-------|---------|
| `phone-agent` | `Wifi_On_Wireless`, `Wifi_Off_Wireless`, `Bluetooth_On_Wireless`, `Bluetooth_Off_Wireless`, `Connect_Bluetooth_Wireless`, `Disconnect_Bluetooth_Wireless` |

### 12. `camera_server.py` (port 8012) — Cameras & Recording

| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Open_Camera`, `Close_Camera`, `Screenshot`, `Record_Video`, `Dashcam_View` |

### 13. `interaction_server.py` (port 8013) — General UI Interaction

| Skill | Intents |
|-------|---------|
| `interaction-control-agent` | `Screenshot_Screen`, `Show_Notification`, `Dismiss_Notification`, `Open_App_Interaction`, `Close_App_Interaction` |

### 14. `app_server.py` (port 8014) — Application Management

| Skill | Intents |
|-------|---------|
| `system-settings-agent` | `App_List_App`, `App_Install_App`, `App_Uninstall_App`, `App_Update_App` |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Skills** | 14 |
| **Total MCP Servers** | 14 (consolidated from 20) |
| **Shared Servers** | 4 (`nav_server`, `weather_server`, `system_server`, `vehicle_server`) |
| **Standalone Servers** | 10 |
| **Skills without Servers** | 0 |

---

## Shared Server Usage

| MCP Server | Used By |
|------------|---------|
| `nav_server.py` (port 8001) | `navigation-agent`, `group-travel-agent` |
| `vehicle_server.py` (port 8002) | `vehicle-control-agent`, `car-butler-agent` |
| `weather_server.py` (port 8007) | `weather-life-agent`, `info-query-agent` |
| `system_server.py` (port 8010) | `system-settings-agent`, `user-profile-agent` |
| `interior_server.py` (port 8008) | `vehicle-control-agent`, `seat-agent`, `ambient-light-agent` |
| `hud_server.py` (port 8009) | `ambient-light-agent` |
| `camera_server.py` (port 8012) | `vehicle-control-agent` |
| `calendar_server.py` (port 8006) | `car-butler-agent` |
| `interaction_server.py` (port 8013) | `interaction-control-agent` |
| `phone_server.py` (port 8005) | `phone-agent` |
| `media_server.py` (port 8004) | `media-agent` |
| `ac_server.py` (port 8003) | `hvac-agent` |
| `wireless_server.py` (port 8011) | `phone-agent` |
| `app_server.py` (port 8014) | `system-settings-agent` |

---

## Tool Naming Convention

All MCP tools use `snake_case` naming:

```
nav_server:     go_poi, open_nav, close_nav, nav_zoom_in, ...
vehicle_server: get_vehicle_speed, lock_doors, honk_horn, ...
ac_server:      ac_on, ac_off, set_temperature, defrost, ...
media_server:   play_media, next_track, set_volume, tune_radio, ...
phone_server:   make_call, answer_call, send_message, bluetooth_on, ...
calendar_server: add_event, view_calendar, today_events, ...
weather_server: get_weather, get_forecast, weather_alert, ...
interior_server: open_window, set_interior_lights, adjust_seat, ...
hud_server:     hud_on, hud_off, hud_brightness, hud_mode, ...
system_server:  system_info, system_settings, app_list, ...
wireless_server: wifi_on_wireless, bluetooth_on_wireless, ...
camera_server:  open_camera, screenshot, record_video, ...
interaction_server: screenshot_screen, show_notification, ...
app_server:     app_list_app, app_install_app, ...
```
