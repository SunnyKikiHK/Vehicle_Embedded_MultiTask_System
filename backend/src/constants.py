LOG_DIR = "src/logs"
SERVER_LOG_PATH = "src/logs/server.log"
NAV_TEST_LOG_PATH = "src/logs/nav_test.log"
DATA_ROOT = "src/data"
SKILLS_ROOT = "src/skills"
CLASSIFIER_SAMPLE_PATH = "src/data/classifier_samples.json"
ROUTER_SAMPLE_PATH = "src/data/router_samples.json"
NAV_INTENT_SAMPLE_PATH = "src/data/nav_intent_samples.json"
RECONSTRUCTOR_SAMPLE_PATH = "src/data/reconstructor_samples.json"
EVAL_DIR = "src/evaluation"

AGENT_MAPPING = {
    "hvac-agent": "HVAC Agent",
    "navigation-agent": "Navigation Agent",
    "media-agent": "Media Agent",
    "seat-agent": "Seat Agent",
    "ambient-light-agent": "Ambient Light Agent",
    "vehicle-control-agent": "Vehicle Control Agent",
    "phone-agent": "Phone Agent",
    "weather-life-agent": "Weather & Life Agent",
    "user-profile-agent": "User Profile Agent",
    "system-settings-agent": "System Settings Agent",
    "car-butler-agent": "Car Butler Agent",
    "group-travel-agent": "Group Travel Agent",
}

# Tool result templates for common operations
TOOL_RESPONSE_TEMPLATES: dict[str, str] = {
    # Navigation templates
    "go_poi": "好的，正在为您导航到 {destination}，地址是 {address}。",
    "set_frequent_location": "{message}。",
    "collect_location": "{message}。",
    "open_nav": "好的，导航已打开。",
    "close_nav": "好的，导航已关闭。",
    "go_home": "好的，正在为您导航回家，目标：{destination}，距离{distance}，预计{duration}。",
    "go_company": "好的，正在为您导航到公司，目标：{destination}，距离{distance}，预计{duration}。",
    "flush_route": "好的，路线已重新规划。",
    "change_route": "好的，已切换到备选路线。",
    "open_ar_nav": "好的，AR导航已开启。",
    "close_ar_nav": "好的，AR导航已关闭。",
    "open_full_map": "好的，路线全览已打开。",
    "close_full_map": "好的，路线全览已关闭。",
    # Group Travel templates
    "join_group": "好的，已加入组队。",
    "build_group": "好的，已创建车队，邀请码是 {invite_code}。",
    "quit_group": "好的，已退出车队。",
    "open_group": "好的，组队界面已打开。",
    "go_meeting_place": "好的，正在导航到汇合地点。",
    "ask_meeting_place": "好的，请设置集结地点。",
    # Traffic templates
    "check_area_traffic": "{message}。",
    "check_route_traffic": "{message}。",
    "check_city_traffic_overview": "{message}。",
    "home_condition": "{message}。",
    "company_condition": "{message}。",
    # Route preferences templates
    "switch_main_route": "好的，已切换到主路优先。",
    "switch_side_route": "好的，已切换到辅路优先。",
    "speed_fast": "好的，已开启速度最快模式。",
    "cancel_speed_fast": "好的，已关闭速度最快模式。",
    "highway_first": "好的，已开启高速优先。",
    "smart_recommend": "好的，已开启智能路线推荐。",
    "cancel_smart_recommend": "好的，已关闭智能路线推荐。",
    "main_route_first": "好的，已开启大路优先。",
    "cancel_main_first": "好的，已关闭大路优先。",
    "avoid_congestion": "好的，已开启躲避拥堵。",
    "cancel_avoid_congestion": "好的，已关闭躲避拥堵。",
    "avoid_high_way": "好的，已开启不走高速模式。",
    "cancel_avoid_high_way": "好的，已关闭不走高速模式。",
    "avoid_limit_line": "好的，已开启避开限行。",
    "cancel_avoid_limit_line": "好的，已关闭避开限行。",
    "open_avoid_fee": "好的，已开启避免收费。",
    "cancel_avoid_fee": "好的，已关闭避免收费。",
    # Position query templates
    "ask_where_am_i": "{address}，位于{city}{district}。",
    # Map templates
    "nav_zoom_in": "好的，地图已放大。",
    "nav_zoom_out": "好的，地图已缩小。",
    "set_3d_map": "好的，已切换到3D视图。",
    "set_2d_map": "好的，已切换到2D视图。",
    "set_north_up": "好的，已切换到北朝上模式。",
    "set_head_up": "好的，已切换到车头朝上模式。",
    "back_to_center": "好的，已回到当前位置。",
    "view_small_map": "好的，小地图已打开。",
    "close_small_map": "好的，小地图已关闭。",
    "open_map_setting": "好的，地图设置已打开。",
    "close_map_setting": "好的，地图设置已关闭。",
    "change_nav_sign": "好的，已切换导航标志样式。",
    # Safety & guidance templates
    "open_electronic_eye": "好的，电子眼已开启。",
    "close_electronic_eye": "好的，电子眼已关闭。",
    "open_cruise_information": "好的，路况信息已开启。",
    "close_cruise_information": "好的，路况信息已关闭。",
    "front_line_detail": "好的，{message}",
    # Broadcast templates
    "open_nav_broadcast": "好的，导航播报已开启。",
    "close_nav_broadcast": "好的，导航播报已关闭。",
    "replay_broadcast": "{message}",
    "slow_broadcast_speed": "好的，已放慢播报速度。",
    "accelerate_broadcast_speed": "好的，已加速播报速度。",
    "open_simple_broadcast": "好的，已开启简洁播报模式。",
    "close_simple_broadcast": "好的，已关闭简洁播报模式。",
    # Commute templates
    "open_commute_nav": "好的，通勤导航已开启。",
    "close_commute_nav": "好的，通勤导航已关闭。",
    # Collection templates
    "open_nav_collections": "好的，收藏夹已打开。",
    "close_nav_collections": "好的，收藏夹已关闭。",
    "nav_to_collection": "好的，正在导航到收藏地址。",
    "collect_target_location": "好的，正在收藏目的地。",

    # AC templates
    "ac_on": "好的，空调已打开。",
    "ac_off": "好的，空调已关闭。",
    "ac_auto": "好的，已开启自动空调模式。",
    "defrost": "好的，已开启除雾功能。",
    "sync_ac": "好的，已开启同步控制。",

    # Media templates
    "play_media": "好的，正在播放。",
    "pause_media": "好的，已暂停。",
    "stop_media": "好的，已停止播放。",
    "next_track": "好的，已切换到下一首。",
    "previous_track": "好的，已切换到上一首。",
    "mute_volume": "好的，已静音。",
    "unmute_volume": "好的，已取消静音。",

    # Light templates
    "lights_on": "好的，灯光已打开。",
    "lights_off": "好的，灯光已关闭。",

    # Phone templates
    "make_call": "好的，正在为您拨打 {number}。",
    "end_call": "好的，已挂断电话。",
    "answer_call": "好的，已接听电话。",
    "reject_call": "好的，已拒绝来电。",

    # Weather templates
    "get_weather": "好的，当前天气是 {weather}。",
    #"get_forecast": "好的，明天天气是 {weather}。",
}

# Mapping from tool name to variable names needed for response formatting
# These variable names correspond to keys in the tool result dict
# Used in answer_builder.py
TOOL_VARIABLE_MAPPING: dict[str, list[str]] = {
    # Navigation templates
    "go_poi": ["destination", "address", "distance_meters"],
    "set_frequent_location": ["message", "name", "address"],
    "collect_location": ["name", "longitude", "latitude"],
    "open_nav": [],
    "close_nav": [],
    "go_home": ["destination", "destination_address", "distance", "duration", "message"],
    "go_company": ["destination", "destination_address", "distance", "duration", "message"],
    "flush_route": [],
    "change_route": [],
    "open_ar_nav": [],
    "close_ar_nav": [],
    # Group Travel templates
    "join_group": [],
    "build_group": ["invite_code"],
    "quit_group": [],
    "open_group": [],
    "go_meeting_place": [],
    "ask_meeting_place": [],
    # Traffic templates
    "check_area_traffic": ["context_name", "traffic_status", "description"],
    "check_route_traffic": ["context_name", "distance_km", "estimated_time_minutes"],
    "check_city_traffic_overview": ["context_name", "traffic_status", "description"],
    "home_condition": ["context_name", "destination", "distance_km", "estimated_time_minutes", "traffic_lights", "strategy", "message"],
    "company_condition": ["context_name", "destination", "distance_km", "estimated_time_minutes", "traffic_lights", "strategy", "message"],
    # Route preferences templates
    "switch_main_route": [],
    "switch_side_route": [],
    "speed_fast": [],
    "cancel_speed_fast": [],
    "highway_first": [],
    "smart_recommend": [],
    "cancel_smart_recommend": [],
    "main_route_first": [],
    "cancel_main_first": [],
    "avoid_congestion": [],
    "cancel_avoid_congestion": [],
    "avoid_high_way": [],
    "cancel_avoid_high_way": [],
    "avoid_limit_line": [],
    "cancel_avoid_limit_line": [],
    "open_avoid_fee": [],
    "cancel_avoid_fee": [],
    # Position query templates
    "ask_where_am_i": ["address", "city", "district", "location"],
    # Map templates
    "nav_zoom_in": [],
    "nav_zoom_out": [],
    "set_3d_map": [],
    "set_2d_map": [],
    "set_north_up": [],
    "set_head_up": [],
    "back_to_center": [],
    "view_small_map": [],
    "close_small_map": [],
    "open_map_setting": [],
    "close_map_setting": [],
    "change_nav_sign": [],
    # Safety & guidance templates
    "open_electronic_eye": [],
    "close_electronic_eye": [],
    "open_cruise_information": [],
    "close_cruise_information": [],
    "front_line_detail": ["message"],
    # Broadcast templates
    "open_nav_broadcast": [],
    "close_nav_broadcast": [],
    "replay_broadcast": ["message"],
    "slow_broadcast_speed": [],
    "accelerate_broadcast_speed": [],
    "open_simple_broadcast": [],
    "close_simple_broadcast": [],
    # Commute templates
    "open_commute_nav": [],
    "close_commute_nav": [],
    # Collection templates
    "open_nav_collections": [],
    "close_nav_collections": [],
    "nav_to_collection": [],
    "collect_target_location": [],

    # AC templates
    "ac_on": [],
    "ac_off": [],
    "ac_auto": [],
    "defrost": [],
    "sync_ac": [],

    # Media templates
    "play_media": [],
    "pause_media": [],
    "stop_media": [],
    "next_track": [],
    "previous_track": [],
    "mute_volume": [],
    "unmute_volume": [],

    # Light templates
    "lights_on": [],
    "lights_off": [],

    # Phone templates
    "make_call": ["number"],
    "end_call": [],
    "answer_call": [],
    "reject_call": [],

    # Weather templates
    "get_weather": ["weather"],
    #"get_forecast": ["weather"],
}

# Default server URLs for consolidated MCP servers
# Keys match server names from mapping.SERVER_TO_TOOLS

DEFAULT_SERVER_URLS: dict[str, str] = {
    # port 8001: Navigation + Map + Group Travel
    "nav_server": "http://localhost:8001/mcp",
    # port 8002: Vehicle Control
    "vehicle_server": "http://localhost:8002/mcp",
    # port 8003: Air Conditioning
    "ac_server": "http://localhost:8003/mcp",
    # port 8004: Media + Radio + Music
    "media_server": "http://localhost:8004/mcp",
    # port 8005: Phone + Messages + Device Connections
    "phone_server": "http://localhost:8005/mcp",
    # port 8006: Calendar
    "calendar_server": "http://localhost:8006/mcp",
    # port 8007: Weather
    "weather_server": "http://localhost:8007/mcp",
    # port 8008: Windows + Lights + Seats
    "interior_server": "http://localhost:8008/mcp",
    # port 8009: HUD
    "hud_server": "http://localhost:8009/mcp",
    # port 8010: System Settings + App Management + UI Interaction
    "system_server": "http://localhost:8010/mcp",
    # port 8011: WiFi + Bluetooth
    "wireless_server": "http://localhost:8011/mcp",
    # port 8012: Cameras + Dashcam
    "camera_server": "http://localhost:8012/mcp",
    # port 8013: UI Interaction
    "interaction_server": "http://localhost:8013/mcp",
    # port 8014: App Management (standalone)
    "app_server": "http://localhost:8014/mcp",
}

# Mapping from agents to their MCP servers
# This determines which servers to connect based on SERVER_USE
AGENT_TO_SERVER: dict[str, str] = {
    "navigation-agent": "nav_server",
    "vehicle-control-agent": "vehicle_server",
    "hvac-agent": "ac_server",
    "media-agent": "media_server",
    "phone-agent": "phone_server",
    "calendar-agent": "calendar_server",
    "weather-life-agent": "weather_server",
    "seat-agent": "interior_server",
    "ambient-light-agent": "interior_server",
    "hud-agent": "hud_server",
    "system-settings-agent": "system_server",
    "wireless-agent": "wireless_server",
    "camera-agent": "camera_server",
    "app-agent": "app_server",
}

SERVER_USE = {
    "hvac-agent": False,
    "navigation-agent": True,
    "media-agent": False,
    "seat-agent": False,
    "ambient-light-agent": False,
    "vehicle-control-agent": False,
    "phone-agent": False,
    "weather-life-agent": False,
    "user-profile-agent": False,
    "system-settings-agent": False,
    "car-butler-agent": False,
    "group-travel-agent": False,
}

# Tools that require metadata (vehicle_id, gps_location, etc.)
# Format: server_name -> tool_name -> requires_metadata (bool)
TOOL_METADATA_REQUIREMENTS: dict[str, dict[str, bool]] = {
    "nav_server": {
        # Navigation tools that need vehicle_id for GPS location
        "go_poi": True,
        "set_frequent_location": True,
        "collect_location": True,
        "check_frequent_location": True,
        "delete_frequent_location": True,
        "list_collected_locations": True,
        "delete_collected_locations": True,
        "ask_where_am_i": True,
        "check_area_traffic": True,
        "check_route_traffic": True,
        # Navigation control tools
        "open_nav": False,
        "close_nav": False,
        "go_home": True,
        "go_company": True,
        "add_via": False,
        "delete_via": False,
        "flush_route": False,
        "change_route": False,
        "get_route_information": False,
        "open_full_map": False,
        "close_full_map": False,
        # Route Preferences
        "switch_main_route": False,
        "switch_side_route": False,
        "speed_fast": False,
        "cancel_speed_fast": False,
        "highway_first": False,
        "smart_recommend": False,
        "cancel_smart_recommend": False,
        "main_route_first": False,
        "cancel_main_first": False,
        # Traffic Avoidance
        "avoid_congestion": False,
        "cancel_avoid_congestion": False,
        "avoid_high_way": False,
        "cancel_avoid_high_way": False,
        "avoid_limit_line": False,
        "cancel_avoid_limit_line": False,
        "open_avoid_fee": False,
        "cancel_avoid_fee": False,
        # Traffic Info
        "home_condition": False,
        "company_condition": False,
        "check_city_traffic_overview": False,
        "open_electronic_eye": False,
        "close_electronic_eye": False,
        "open_cruise_information": False,
        "close_cruise_information": False,
        # Map
        "nav_zoom_in": False,
        "nav_zoom_out": False,
        "set_3d_map": False,
        "set_2d_map": False,
        "set_north_up": False,
        "set_head_up": False,
        "back_to_center": False,
        "view_small_map": False,
        "close_small_map": False,
        # AR
        "open_ar_nav": False,
        "close_ar_nav": False,
        "front_line_detail": False,
        # Broadcast
        "open_nav_broadcast": False,
        "close_nav_broadcast": False,
        "replay_broadcast": False,
        "slow_broadcast_speed": False,
        "accelerate_broadcast_speed": False,
        "open_simple_broadcast": False,
        "close_simple_broadcast": False,
        # Commute
        "open_commute_nav": False,
        "close_commute_nav": False,
        # Collections
        "open_nav_collections": False,
        "close_nav_collections": False,
        "nav_to_collection": False,
        "collect_target_location": False,
        # Position Query & Settings
        "open_map_setting": False,
        "close_map_setting": False,
        "change_nav_sign": False,
        # Group Travel
        "join_group": False,
        "build_group": False,
        "quit_group": False,
        "open_group": False,
        "ask_meeting_place": False,
        "go_meeting_place": False,
        "group_member_location": False,
    },
    "vehicle_server": {
        "get_vehicle_speed": False,
        "get_fuel_level": False,
        "get_battery_status": False,
        "lock_doors": False,
        "unlock_doors": False,
        "start_engine": False,
        "stop_engine": False,
        "honk_horn": False,
        "flash_lights": False,
    },
    "ac_server": {
        "ac_on": False,
        "ac_off": False,
        "set_temperature": False,
        "set_fan_speed": False,
        "set_ac_mode": False,
        "ac_auto": False,
        "defrost": False,
        "sync_ac": False,
    },
    "media_server": {
        "play_media": False,
        "pause_media": False,
        "stop_media": False,
        "next_track": False,
        "previous_track": False,
        "set_volume": False,
        "mute_volume": False,
        "unmute_volume": False,
        "search_music": False,
        "play_music": False,
        "play_playlist": False,
        "like_song": False,
        "tune_radio": False,
        "scan_radio": False,
        "save_radio_station": False,
        "preset_radio": False,
        "radio_on": False,
        "radio_off": False,
    },
    "phone_server": {
        "make_call": False,
        "dial_contact": False,
        "answer_call": False,
        "reject_call": False,
        "end_call": False,
        "recent_calls": False,
        "missed_calls": False,
        "send_message": False,
        "read_messages": False,
        "unread_messages": False,
        "delete_message": False,
        "reply_message": False,
        "bluetooth_on": False,
        "bluetooth_off": False,
        "wifi_on": False,
        "wifi_off": False,
        "connect_bluetooth": False,
        "disconnect_bluetooth": False,
    },
    "calendar_server": {
        "add_event": False,
        "view_calendar": False,
        "delete_event": False,
        "update_event": False,
        "today_events": False,
    },
    "weather_server": {
        "get_weather": False,
        "get_forecast": False,
        "weather_alert": False,
    },
    "interior_server": {
        "open_window": False,
        "close_window": False,
        "window_up": False,
        "window_down": False,
        "window_all_up": False,
        "window_all_down": False,
        "set_interior_lights": False,
        "set_headlights": False,
        "lights_on": False,
        "lights_off": False,
        "set_reading_light": False,
        "adjust_seat": False,
        "seat_position": False,
        "seat_heating": False,
        "seat_ventilation": False,
        "seat_massage": False,
        "recline_seat": False,
        "seat_memory": False,
    },
    "hud_server": {
        "hud_on": False,
        "hud_off": False,
        "hud_brightness": False,
        "hud_mode": False,
    },
    "system_server": {
        "system_info": False,
        "system_settings": False,
        "language_setting": False,
        "display_setting": False,
        "sound_setting": False,
        "reset_settings": False,
        "app_list": False,
        "app_install": False,
        "app_uninstall": False,
        "app_update": False,
    },
    "wireless_server": {
        "wifi_on_wireless": False,
        "wifi_off_wireless": False,
        "bluetooth_on_wireless": False,
        "bluetooth_off_wireless": False,
        "connect_bluetooth_wireless": False,
        "disconnect_bluetooth_wireless": False,
    },
    "camera_server": {
        "open_camera": False,
        "close_camera": False,
        "screenshot": False,
        "record_video": False,
        "dashcam_view": False,
    },
    "interaction_server": {
        "screenshot_screen": False,
        "show_notification": False,
        "dismiss_notification": False,
        "open_app_interaction": False,
        "close_app_interaction": False,
    },
    "app_server": {
        "app_list_app": False,
        "app_install_app": False,
        "app_uninstall_app": False,
        "app_update_app": False,
    },
}
