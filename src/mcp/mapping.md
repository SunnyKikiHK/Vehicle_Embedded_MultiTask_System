# Skill to MCP Server Mapping

This document maps the **14 Skills** (intent classification) to the **20 MCP Servers** (execution layer).

## Architecture Overview

- **Skills**: LLM-based intent understanding and slot extraction
- **MCP Servers**: Vehicle hardware control via CAN bus / APIs

---

## Complete Mapping Table

| Skill | Intents | MCP Server(s) | Notes |
|-------|---------|---------------|-------|
| `phone-agent` | 34 | `phone_server.py`, `message_server.py`, `wireless_server.py` | Calls, contacts, Bluetooth, WiFi, hotspot |
| `navigation-agent` | 74 | `nav_server.py`, `map_server.py` | Routes, POI, saved places |
| `media-agent` | 69 | `music_server.py`, `radio_server.py`, `media_server.py` | Music, radio, news, K-song |
| `hvac-agent` | 43 | `ac_server.py` | Climate control, temperature, ventilation |
| `seat-agent` | 26 | `seat_server.py` | Seat position, heating, massage, mirrors |
| `ambient-light-agent` | 30 | `light_server.py`, `hud_server.py` | Ambient lights, brightness, HUD |
| `weather-life-agent` | 30 | `weather_server.py` | Weather, life advisory, data |
| `system-settings-agent` | 36 | `system_server.py`, `app_server.py` | Apps, themes, scenes, voice |
| `vehicle-control-agent` | 46 | `vehicle_server.py`, `camera_server.py`, `window_server.py` | Windows, lights, cameras, driving mode |
| `group-travel-agent` | 7 | `nav_server.py` | Shared - route sharing via nav |
| `interaction-control-agent` | 10 | `interaction_server.py` | General UI interaction: confirm, cancel, select, help |
| `user-profile-agent` | 35 | `system_server.py` | Shared - voice settings |
| `car-butler-agent` | 24 | `vehicle_server.py`, `calendar_server.py` | Health, orders, calendar |
| `info-query-agent` | 7 | `weather_server.py` | Shared - time/date via weather |

---

## MCP Server Details

### 1. `map_server.py` — Map Display
| Skill | Intents |
|-------|---------|
| `navigation-agent` | `Nav_Zoom_In`, `Nav_Zoom_Out`, `Nav_Zoom_In_Max`, `Nav_Zoom_Out_Min`, `Back_Center`, `View_Small_Map`, `Close_Small_Map`, `3D_Map`, `2D_Map`, `North_Up`, `Head_Up` |

### 2. `nav_server.py` — Navigation & Routing
| Skill | Intents |
|-------|---------|
| `navigation-agent` | `Go_POI`, `Open_Nav`, `Close_Nav`, `Go_Home`, `Go_Company`, `Nav_Set_Home`, `Nav_Set_Company`, `Add_Via`, `Delete_Via`, `Flush_Route`, `Change_Route`, `Get_Route_Information`, `Open_Full_Map`, `Close_Full_Map`, `Switch_Main_Route`, `Switch_Side_Route`, `Speed_Fast`, `Cancel_Speed_Fast`, `High_Way_First`, `Smart_Recommend`, `Cancel_Smart_Recommend`, `Main_Route_First`, `Cancel_Main_First`, `Avoid_Congestion`, `Cancel_Avoid_Congestion`, `Avoid_High_Way`, `Cancel_Avoid_High_Way`, `Avoid_Limit_Line`, `Cancel_Avoid_Limit_Line`, `Open_Avoid_Fee`, `Cancel_Avoid_Fee`, `Open_Electronic_Eye`, `Close_Electronic_Eye`, `Open_Cruise_Information`, `Close_Cruise_Information`, `Open_AR_Nav`, `Close_AR_Nav`, `Front_Line_Detail`, `Traffic_Incidents`, `Open_Nav_Broadcast`, `Close_Nav_Broadcast`, `Replay_Broadcast`, `Slow_Speed`, `Accelerate_Speed`, `Open_Simple_Broadcast`, `Close_Simple_Broadcast`, `Open_Commute_Nav`, `Close_Commute_Nav`, `Open_Nav_Collections`, `Close_Nav_Collections`, `Nav_To_Collection`, `Collect_Target_Location`, `Collect_Current_Location`, `Ask_Where`, `Open_Map_Setting`, `Close_Map_Setting`, `Change_Nav_Sign`, `Ahead_Condition`, `Target_Condition`, `Home_Condition`, `Company_Condition`, `POI_Condition` |
| `group-travel-agent` | `Join_Group`, `Build_Group`, `Quit_Group`, `Open_Group`, `Ask_Meeting_Place`, `Go_Meeting_Place`, `Group_Member_Location` |

### 3. `ac_server.py` — Air Conditioning
| Skill | Intents |
|-------|---------|
| `hvac-agent` | `Close_Air_Condition`, `Open_Air_Condition`, `Open_Air_Condition_Auto_Mode`, `Close_Air_Condition_Auto_Mode`, `Open_Air_Condition_Sync`, `Close_Air_Condition_Sync`, `Open_Cooling`, `Close_Cooling`, `Open_Heating`, `Close_Heating`, `Dec_Air_Condition_Temperature`, `Inc_Air_Condition_Temperature`, `Set_Air_Condition_Temperature`, `Temp_Compare`, `Dec_Air_Condition_Wind`, `Inc_Air_Condition_Wind`, `Set_Air_Condition_Wind`, `Set_Wind_Direction`, `Cancel_Wind_Direction`, `Open_Wind_Auto_Mode`, `Close_Wind_Auto_Mode`, `Open_Air_Condition_Defog`, `Close_Air_Condition_Defog`, `Open_AC`, `Close_AC`, `Open_Cooling_Instant`, `Close_Cooling_Instant`, `Open_Heating_Instant`, `Open_Air_Cleaner`, `Close_Air_Cleaner`, `Open_Internal_Circulation`, `Close_Internal_Circulation`, `Open_External_Circulation`, `Close_External_Circulation`, `Ask_Air_Condition`, `Ask_Humidity`, `Ask_Wind` |

### 4. `music_server.py` — Music Playback
| Skill | Intents |
|-------|---------|
| `media-agent` | `Search_Music`, `Play_Online_Music`, `Play_BT_Music`, `Play_USB_Music`, `Play_Similar_Music`, `Close_Play_Similar_Music`, `Media_Next`, `Media_Last`, `Media_Pause`, `Continue_Play`, `Replay`, `Quick_Go`, `Quick_Back`, `Set_Speed_By_Speed`, `Get_exact_time_For_Play`, `Play_repeatly`, `List_Repeat`, `Media_Random_Play`, `Media_Order_Play`, `Change_Play_Mode`, `Cancel_Play_Mode`, `Open_o3ics`, `Close_o3ics`, `Open_Play_Detail`, `Close_Play_Detail`, `Switch_Music_Quantity`, `View_Play_Music`, `View_Play_Music_Singer`, `View_Play_Album`, `View_Play_Content`, `Download_Current_Content` |

### 5. `radio_server.py` — Radio & Broadcast
| Skill | Intents |
|-------|---------|
| `media-agent` | `Search_Radio`, `Open_Radio_By_Name`, `Play_OL_Radio`, `Play_Local_Radio`, `Play_Hot_Radio`, `Replay_Broadcast`, `Search_Station`, `Search_News`, `View_Play_News`, `Open_K`, `Close_K`, `Select_Sing` |

### 6. `media_server.py` — Media Library
| Skill | Intents |
|-------|---------|
| `media-agent` | `Open_Player`, `Close_Player`, `Open_Play_List`, `Close_Play_List`, `Play_History`, `Open_Play_History`, `Close_Play_History`, `Media_Collect`, `Cancel_Media_Collect`, `Play_Media_Collection`, `Open_Media_Collection`, `Close_Media_Collection`, `View_Play_Radio`, `View_Play_Frequency` |

### 7. `phone_server.py` — Phone & Calls
| Skill | Intents |
|-------|---------|
| `phone-agent` | `Open_Phone`, `Call_Phone`, `Call_Number`, `Call_Phone_By_Contact`, `Call_Phone_By_Contact_Label`, `Call_Yellow_Page`, `Call_Select_SubStr`, `Call_Emergency`, `Answer_Phone`, `Reject_Phone`, `Silent_Phone`, `Quit_Phone`, `Call_Back`, `View_Call_Record`, `View_Send_Record`, `View_Already_Call`, `View_Not_Call`, `Get_Contact`, `Sync_Contact` |

### 8. `message_server.py` — Messages
| Skill | Intents |
|-------|---------|
| `phone-agent` | `Open_Message`, `Close_Message`, `View_Unread_Message`, `View_All_Message` |

### 9. `wireless_server.py` — Wireless Connectivity
| Skill | Intents |
|-------|---------|
| `phone-agent` | `Close_Phone_Connection`, `Open_Phone_Connection`, `Open_Bluetooth`, `Close_Bluetooth`, `Open_Spot`, `Close_Spot`, `Open_WIFI`, `Close_WIFI`, `Open_Wireless_Charge`, `Close_Wireless_Charge` |

### 10. `light_server.py` — Ambient Lighting
| Skill | Intents |
|-------|---------|
| `ambient-light-agent` | `Open_Env_Light`, `Close_Env_Light`, `Set_Env_Light_Color`, `Set_Env_Light_Theme`, `Dec_Env_Light_Brightness`, `Inc_Env_Light_Brightness`, `Set_Env_Light_Brightness`, `Open_Env_Light_Auto_Mode`, `Close_Env_Light_Auto_Mode`, `Dec_DashBoard_Brightness`, `Inc_DashBoard_Brightness`, `Set_DashBoard_Brightness_Min`, `Set_DashBoard_Brightness_Max`, `Set_DashBoard_Brightness`, `Dec_Brightness`, `Inc_Brightness`, `Set_Brightness_Min`, `Set_Brightness_Max`, `Set_Brightness`, `Open_Reading_Light`, `Close_Reading_Light` |

### 11. `hud_server.py` — HUD Display
| Skill | Intents |
|-------|---------|
| `ambient-light-agent` | `Open_HUD`, `Close_HUD`, `Adjust_Hud_Brightness`, `Inc_HUD_Brightness`, `Dec_HUD_Brightness`, `Adjust_HUD_Vert`, `Adjust_HUD_Horizon` |

### 12. `seat_server.py` — Seat Control
| Skill | Intents |
|-------|---------|
| `seat-agent` | `Adjust_Seat_Long`, `Adjust_Seat_Vert`, `Open_Heated_Seat`, `Close_Heated_Seat`, `Dec_Seat_Temperature`, `Inc_Seat_Temperature`, `Set_Seat_Temperature`, `Open_Seat_Ventilation`, `Close_Seat_Ventilation`, `Dec_Seat_Ventilation`, `Inc_Seat_Ventilation`, `Set_Seat_Ventilation`, `Open_Seat_Massage`, `Close_Seat_Massage`, `Dec_Seat_Massage`, `Inc_Seat_Massage`, `Set_Seat_Massage`, `Set_Steer_Temperature`, `Dec_Steer_Temperature`, `Inc_Steer_Temperature`, `Open_Heated_Steer`, `Close_Heated_Steer`, `Open_Rearview_Mirror_Heating`, `Close_Rearview_Mirror_Heating`, `Open_Rearview_Mirror`, `Close_Rearview_Mirror` |

### 13. `weather_server.py` — Weather & Life
| Skill | Intents |
|-------|---------|
| `weather-life-agent` | `Query_Weather`, `Query_Timely_Weather`, `Open_Weather`, `Close_Weather`, `Ask_Clothes`, `Ask_Makeup`, `Ask_Fishing`, `Ask_Sport`, `Ask_Travel`, `Ask_Transport`, `Ask_Cold_Index`, `Ask_Car_Wash`, `Ask_Allergy`, `Query_Body_Temperature`, `Query_UV_Level`, `Oil_Price`, `Query_Date`, `Query_Restrictions`, `Ask_Weekday`, `Ask_Date`, `Display_Remaining_Flow`, `Open_Flow`, `Close_Flow`, `Open_Flow_Center`, `Close_Flow_Center`, `Open_APP_Rank`, `Close_APP_Rank` |
| `info-query-agent` | `Ask_Where`, `Ask_Weekday`, `Ask_Date`, `Ask_Air_Condition`, `Ask_Humidity`, `Query_UV_Level` |

### 14. `system_server.py` — System & Voice Settings
| Skill | Intents |
|-------|---------|
| `system-settings-agent` | `Open_System_Config`, `Close_System_Config`, `Set_Desktop_Style`, `Set_System_Theme_By_Mode`, `Set_Card_Position`, `Back_To_Home`, `Open_Screen`, `Close_Screen`, `Open_ScreenCast`, `Close_ScreenCast`, `Open_Scene_Center`, `Close_Scene_Center`, `Open_Preset_Scene`, `Close_Preset_Scene`, `Open_Snooze_Mode`, `Close_Snooze_Mode`, `Open_Snooze_Mode_Fuzzy`, `Close_Snooze_Mode_Fuzzy` |
| `user-profile-agent` | `Set_Timbre_Female`, `Set_Timbre_Male`, `Set_Timbre_Child`, `Set_Timbre_Default`, `Change_Timbre`, `Set_Voice`, `Set_Voice_Style`, `Set_Wakeup_Words`, `Ask_Wakeup_Words`, `Delete_Wakeup_Words`, `Open_Free_Wakeup`, `Close_Free_Wakeup`, `Open_Continuous_Dialogue`, `Close_Continuous_Dialogue`, `Set_Continuous_Dialogue`, `Only_Main`, `Main_And_Vice`, `Set_Speech_By_Speed`, `Open_Online_NLU`, `Close_Online_NLU`, `Open_Sds_Config`, `Close_Sds_Config`, `View_Learning_Content`, `Open_Interactive_Learning`, `Close_Interactive_Learning`, `Open_Training_Camp`, `Close_Training_Cmap`, `Open_Skill_Instruction`, `Close_Skill_Instruction`, `Open_Voice_Wakeup`, `Close_Voice_Wakeup`, `Open_Safety_Alarm`, `Close_Safety_Alarm` |

### 15. `app_server.py` — Application Management
| Skill | Intents |
|-------|---------|
| `system-settings-agent` | `Open_App`, `Close_App`, `Open_App_List`, `Close_App_List`, `Download_App`, `Open_APP_Store`, `Close_APP_Store`, `Open_Long_Video`, `Close_Long_Video`, `Open_Mini_App`, `Close_Mini_App`, `Open_Mini_App_Center`, `Close_Mini_App_Center` |

### 16. `window_server.py` — Windows & Sunroof
| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Open_Window`, `Close_Window`, `Set_Window`, `Open_Window_Diagonal`, `Close_Window_Diagonal`, `Close_Dormer`, `Open_Dormer`, `Open_Sunshade`, `Close_Sunshade` |

### 17. `camera_server.py` — Cameras & Recording
| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Open_Surround_View`, `Close_Surround_View`, `Set_Surround_View`, `Open_DashCam`, `Close_DashCam`, `Record_Audio`, `Stop_Audio`, `Record_Video`, `Stop_Video`, `Take_Photo` |

### 18. `vehicle_server.py` — Vehicle Control
| Skill | Intents |
|-------|---------|
| `vehicle-control-agent` | `Open_Trunk`, `Close_Trunk`, `Open_Wiper`, `Close_Wiper`, `Open_Headlamp`, `Close_Headlamp`, `Open_Low_Beam`, `Close_Low_Beam`, `Open_High_Beam`, `Close_High_Beam`, `Open_ADAPTIVE_HEAPLAMP`, `Close_ADAPTIVE_HEAPLAMP`, `Open_Front_Fog_Light`, `Close_Front_Fog_Light`, `Open_Back_Fog_Light`, `Close_Back_Fog_Light`, `Open_Fog_Light`, `Close_Fog_Light`, `Open_Marker_Light`, `Close_Marker_Light`, `Set_Driving_Mode`, `Open_AutoHold`, `Close_AutoHold`, `Open_Engine_AutoStop`, `Close_Engine_AutoStop` |
| `car-butler-agent` | `Check_Car_Condition`, `Open_Bulter`, `Close_Bulter`, `Reserve_Maintenance`, `Cancel_Reserve`, `Record_Face`, `Open_Personal_Center`, `Close_Personal_Center`, `Open_Owner_Service`, `Close_Owner_Service`, `Open_Feedback`, `Close_Feedback`, `Complains_And_Suggestions`, `View_Already_Order`, `View_Unend_Order`, `View_All_Order`, `Open_Order_Center`, `Close_Order_Center`, `Open_Record_App`, `Close_Record_App`, `Create_Trip_Record` |

### 19. `calendar_server.py` — Calendar & Scheduling
| Skill | Intents |
|-------|---------|
| `car-butler-agent` | `Open_Calendar`, `Close_Calendar` |

### 20. `interaction_server.py` — General UI Interaction
| Skill | Intents |
|-------|---------|
| `interaction-control-agent` | `Confirm`, `Cancel`, `List_Select`, `Open_Two_Both`, `Close_Two_Both`, `Open_Help`, `Close_Help`, `Ask_Answer_Words`, `Get_Answer`, `Delete_Answer_Words` |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Skills** | 14 |
| **Total MCP Servers** | 20 |
| **Shared Servers** | 4 (`nav_server`, `weather_server`, `system_server`, `vehicle_server`) |
| **Standalone Servers** | 16 |
| **Skills without Servers** | 0 |

---

## Shared Server Usage

| MCP Server | Used By |
|------------|---------|
| `nav_server.py` | `navigation-agent`, `group-travel-agent` |
| `weather_server.py` | `weather-life-agent`, `info-query-agent` |
| `system_server.py` | `system-settings-agent`, `user-profile-agent` |
| `vehicle_server.py` | `vehicle-control-agent`, `car-butler-agent` |