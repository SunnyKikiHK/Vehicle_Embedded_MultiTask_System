"""
Tool to Server Mapping for MCP (Model Context Protocol)

This module provides a centralized mapping of all available tools to their
respective MCP servers. Each server is a consolidated MCP server that handles
multiple logical domains on a single port.

Server Consolidation:
- port 8001: nav_server (nav + map + group travel)
- port 8002: vehicle_server (vehicle control)
- port 8003: ac_server (HVAC/climate)
- port 8004: media_server (media + radio + music)
- port 8005: phone_server (phone + messages)
- port 8006: calendar_server (calendar)
- port 8007: weather_server (weather + life info)
- port 8008: interior_server (windows + lights + seats)
- port 8009: hud_server (HUD display)
- port 8010: system_server (system settings + apps)
- port 8011: wireless_server (WiFi + Bluetooth)
- port 8012: camera_server (cameras + dashcam)
- port 8013: interaction_server (UI interactions)
- port 8014: app_server (app management)
"""

from typing import Dict, List, Optional

TOOL_TO_SERVER: Dict[str, str] = {
    #  NAV_SERVER (port 8001) 
    # Navigation tools
    "go_poi": "nav_server",
    "set_frequent_location": "nav_server",
    "collect_location": "nav_server",
    "check_frequent_location": "nav_server",
    "delete_frequent_location": "nav_server",
    "list_collected_locations": "nav_server",
    "delete_collected_locations": "nav_server",
    "open_nav": "nav_server",
    "close_nav": "nav_server",
    "go_home": "nav_server",
    "go_company": "nav_server",
    "add_via": "nav_server",
    "delete_via": "nav_server",
    "flush_route": "nav_server",
    "change_route": "nav_server",
    "get_route_information": "nav_server",
    "open_full_map": "nav_server",
    "close_full_map": "nav_server",
    # Route Preferences
    "switch_main_route": "nav_server",
    "switch_side_route": "nav_server",
    "speed_fast": "nav_server",
    "cancel_speed_fast": "nav_server",
    "highway_first": "nav_server",
    "smart_recommend": "nav_server",
    "cancel_smart_recommend": "nav_server",
    "main_route_first": "nav_server",
    "cancel_main_first": "nav_server",
    # Traffic Avoidance
    "avoid_congestion": "nav_server",
    "cancel_avoid_congestion": "nav_server",
    "avoid_high_way": "nav_server",
    "cancel_avoid_high_way": "nav_server",
    "avoid_limit_line": "nav_server",
    "cancel_avoid_limit_line": "nav_server",
    "open_avoid_fee": "nav_server",
    "cancel_avoid_fee": "nav_server",
    # Traffic Information
    "home_condition": "nav_server",
    "company_condition": "nav_server",
    "check_area_traffic": "nav_server",
    "check_route_traffic": "nav_server",
    "check_city_traffic_overview": "nav_server",
    "open_electronic_eye": "nav_server",
    "close_electronic_eye": "nav_server",
    "open_cruise_information": "nav_server",
    "close_cruise_information": "nav_server",
    # Map tools (from map_server)
    "nav_zoom_in": "nav_server",
    "nav_zoom_out": "nav_server",
    "set_3d_map": "nav_server",
    "set_2d_map": "nav_server",
    "set_north_up": "nav_server",
    "set_head_up": "nav_server",
    "back_to_center": "nav_server",
    "view_small_map": "nav_server",
    "close_small_map": "nav_server",
    # AR Navigation
    "open_ar_nav": "nav_server",
    "close_ar_nav": "nav_server",
    "front_line_detail": "nav_server",
    # Navigation Broadcast
    "open_nav_broadcast": "nav_server",
    "close_nav_broadcast": "nav_server",
    "replay_broadcast": "nav_server",
    "slow_broadcast_speed": "nav_server",
    "accelerate_broadcast_speed": "nav_server",
    "open_simple_broadcast": "nav_server",
    "close_simple_broadcast": "nav_server",
    # Commute Navigation
    "open_commute_nav": "nav_server",
    "close_commute_nav": "nav_server",
    # Collections
    "open_nav_collections": "nav_server",
    "close_nav_collections": "nav_server",
    "nav_to_collection": "nav_server",
    "collect_target_location": "nav_server",
    "collect_location": "nav_server",
    # Position Query
    "ask_where_am_i": "nav_server",
    "open_map_setting": "nav_server",
    "close_map_setting": "nav_server",
    "change_nav_sign": "nav_server",
    # Group Travel
    "join_group": "nav_server",
    "build_group": "nav_server",
    "quit_group": "nav_server",
    "open_group": "nav_server",
    "ask_meeting_place": "nav_server",
    "go_meeting_place": "nav_server",
    "group_member_location": "nav_server",

    #  VEHICLE_SERVER (port 8002) 
    "get_vehicle_speed": "vehicle_server",
    "get_fuel_level": "vehicle_server",
    "get_battery_status": "vehicle_server",
    "lock_doors": "vehicle_server",
    "unlock_doors": "vehicle_server",
    "start_engine": "vehicle_server",
    "stop_engine": "vehicle_server",
    "honk_horn": "vehicle_server",
    "flash_lights": "vehicle_server",

    #  AC_SERVER (port 8003) 
    "ac_on": "ac_server",
    "ac_off": "ac_server",
    "set_temperature": "ac_server",
    "set_fan_speed": "ac_server",
    "set_ac_mode": "ac_server",
    "ac_auto": "ac_server",
    "defrost": "ac_server",
    "sync_ac": "ac_server",

    #  MEDIA_SERVER (port 8004) 
    # Media playback
    "play_media": "media_server",
    "pause_media": "media_server",
    "stop_media": "media_server",
    "next_track": "media_server",
    "previous_track": "media_server",
    # Volume
    "set_volume": "media_server",
    "mute_volume": "media_server",
    "unmute_volume": "media_server",
    # Music
    "search_music": "media_server",
    "play_music": "media_server",
    "play_playlist": "media_server",
    "like_song": "media_server",
    # Radio
    "tune_radio": "media_server",
    "scan_radio": "media_server",
    "save_radio_station": "media_server",
    "preset_radio": "media_server",
    "radio_on": "media_server",
    "radio_off": "media_server",

    #  PHONE_SERVER (port 8005) 
    "make_call": "phone_server",
    "dial_contact": "phone_server",
    "answer_call": "phone_server",
    "reject_call": "phone_server",
    "end_call": "phone_server",
    "recent_calls": "phone_server",
    "missed_calls": "phone_server",
    # Messages
    "send_message": "phone_server",
    "read_messages": "phone_server",
    "unread_messages": "phone_server",
    "delete_message": "phone_server",
    "reply_message": "phone_server",
    # Device Connections
    "bluetooth_on": "phone_server",
    "bluetooth_off": "phone_server",
    "wifi_on": "phone_server",
    "wifi_off": "phone_server",
    "connect_bluetooth": "phone_server",
    "disconnect_bluetooth": "phone_server",

    #  CALENDAR_SERVER (port 8006) 
    "add_event": "calendar_server",
    "view_calendar": "calendar_server",
    "delete_event": "calendar_server",
    "update_event": "calendar_server",
    "today_events": "calendar_server",

    #  WEATHER_SERVER (port 8007) 
    "get_weather": "weather_server",
    "get_forecast": "weather_server",
    "weather_alert": "weather_server",

    #  INTERIOR_SERVER (port 8008) 
    # Windows
    "open_window": "interior_server",
    "close_window": "interior_server",
    "window_up": "interior_server",
    "window_down": "interior_server",
    "window_all_up": "interior_server",
    "window_all_down": "interior_server",
    # Lights
    "set_interior_lights": "interior_server",
    "set_headlights": "interior_server",
    "lights_on": "interior_server",
    "lights_off": "interior_server",
    "set_reading_light": "interior_server",
    # Seats
    "adjust_seat": "interior_server",
    "seat_position": "interior_server",
    "seat_heating": "interior_server",
    "seat_ventilation": "interior_server",
    "seat_massage": "interior_server",
    "recline_seat": "interior_server",
    "seat_memory": "interior_server",

    #  HUD_SERVER (port 8009) 
    "hud_on": "hud_server",
    "hud_off": "hud_server",
    "hud_brightness": "hud_server",
    "hud_mode": "hud_server",

    #  SYSTEM_SERVER (port 8010) 
    "system_info": "system_server",
    "system_settings": "system_server",
    "language_setting": "system_server",
    "display_setting": "system_server",
    "sound_setting": "system_server",
    "reset_settings": "system_server",
    # App management
    "app_list": "system_server",
    "app_install": "system_server",
    "app_uninstall": "system_server",
    "app_update": "system_server",

    #  WIRELESS_SERVER (port 8011) 
    "wifi_on_wireless": "wireless_server",
    "wifi_off_wireless": "wireless_server",
    "bluetooth_on_wireless": "wireless_server",
    "bluetooth_off_wireless": "wireless_server",
    "connect_bluetooth_wireless": "wireless_server",
    "disconnect_bluetooth_wireless": "wireless_server",

    #  CAMERA_SERVER (port 8012) 
    "open_camera": "camera_server",
    "close_camera": "camera_server",
    "screenshot": "camera_server",
    "record_video": "camera_server",
    "dashcam_view": "camera_server",

    #  INTERACTION_SERVER (port 8013) 
    "screenshot_screen": "interaction_server",
    "show_notification": "interaction_server",
    "dismiss_notification": "interaction_server",
    "open_app_interaction": "interaction_server",
    "close_app_interaction": "interaction_server",

    #  APP_SERVER (port 8014) 
    "app_list_app": "app_server",
    "app_install_app": "app_server",
    "app_uninstall_app": "app_server",
    "app_update_app": "app_server",
}


SERVER_TO_TOOLS: Dict[str, List[str]] = {
    "nav_server": [
        # Navigation
        "go_poi", "set_frequent_location", "collect_location",
        "check_frequent_location", "delete_frequent_location",
        "list_collected_locations", "delete_collected_locations",
        "open_nav", "close_nav",
        "go_home", "go_company", "add_via", "delete_via",
        "flush_route", "change_route", "get_route_information",
        "open_full_map", "close_full_map",
        # Route Preferences
        "switch_main_route", "switch_side_route", "speed_fast", "cancel_speed_fast",
        "highway_first", "smart_recommend", "cancel_smart_recommend",
        "main_route_first", "cancel_main_first",
        # Traffic Avoidance
        "avoid_congestion", "cancel_avoid_congestion", "avoid_high_way", "cancel_avoid_high_way",
        "avoid_limit_line", "cancel_avoid_limit_line", "open_avoid_fee", "cancel_avoid_fee",
        # Traffic Info
        "home_condition", "company_condition", "check_area_traffic",
        "check_route_traffic", "check_city_traffic_overview",
        "open_electronic_eye", "close_electronic_eye",
        "open_cruise_information", "close_cruise_information",
        # Map
        "nav_zoom_in", "nav_zoom_out",
        "set_3d_map", "set_2d_map", "set_north_up", "set_head_up",
        "back_to_center", "view_small_map", "close_small_map",
        # AR
        "open_ar_nav", "close_ar_nav", "front_line_detail",
        # Broadcast
        "open_nav_broadcast", "close_nav_broadcast", "replay_broadcast",
        "slow_broadcast_speed", "accelerate_broadcast_speed",
        "open_simple_broadcast", "close_simple_broadcast",
        # Commute
        "open_commute_nav", "close_commute_nav",
        # Collections
        "open_nav_collections", "close_nav_collections", "nav_to_collection",
        "collect_target_location", "collect_location",
        # Position Query & Settings
        "ask_where_am_i", "open_map_setting", "close_map_setting", "change_nav_sign",
        # Group Travel
        "join_group", "build_group", "quit_group", "open_group",
        "ask_meeting_place", "go_meeting_place", "group_member_location",
    ],
    "vehicle_server": [
        "get_vehicle_speed", "get_fuel_level", "get_battery_status",
        "lock_doors", "unlock_doors", "start_engine", "stop_engine",
        "honk_horn", "flash_lights",
    ],
    "ac_server": [
        "ac_on", "ac_off", "set_temperature", "set_fan_speed", "set_ac_mode",
        "ac_auto", "defrost", "sync_ac",
    ],
    "media_server": [
        "play_media", "pause_media", "stop_media", "next_track", "previous_track",
        "set_volume", "mute_volume", "unmute_volume",
        "search_music", "play_music", "play_playlist", "like_song",
        "tune_radio", "scan_radio", "save_radio_station", "preset_radio",
        "radio_on", "radio_off",
    ],
    "phone_server": [
        "make_call", "dial_contact", "answer_call", "reject_call", "end_call",
        "recent_calls", "missed_calls",
        "send_message", "read_messages", "unread_messages", "delete_message", "reply_message",
        "bluetooth_on", "bluetooth_off", "wifi_on", "wifi_off",
        "connect_bluetooth", "disconnect_bluetooth",
    ],
    "calendar_server": [
        "add_event", "view_calendar", "delete_event", "update_event", "today_events",
    ],
    "weather_server": [
        "get_weather", "get_forecast", "weather_alert",
    ],
    "interior_server": [
        "open_window", "close_window", "window_up", "window_down",
        "window_all_up", "window_all_down",
        "set_interior_lights", "set_headlights", "lights_on", "lights_off",
        "set_reading_light",
        "adjust_seat", "seat_position", "seat_heating", "seat_ventilation",
        "seat_massage", "recline_seat", "seat_memory",
    ],
    "hud_server": [
        "hud_on", "hud_off", "hud_brightness", "hud_mode",
    ],
    "system_server": [
        "system_info", "system_settings", "language_setting", "display_setting",
        "sound_setting", "reset_settings",
        "app_list", "app_install", "app_uninstall", "app_update",
    ],
    "wireless_server": [
        "wifi_on_wireless", "wifi_off_wireless",
        "bluetooth_on_wireless", "bluetooth_off_wireless",
        "connect_bluetooth_wireless", "disconnect_bluetooth_wireless",
    ],
    "camera_server": [
        "open_camera", "close_camera", "screenshot", "record_video", "dashcam_view",
    ],
    "interaction_server": [
        "screenshot_screen", "show_notification", "dismiss_notification",
        "open_app_interaction", "close_app_interaction",
    ],
    "app_server": [
        "app_list_app", "app_install_app", "app_uninstall_app", "app_update_app",
    ],
}


def get_server_for_tool(tool_name: str) -> Optional[str]:
    """Get the server name for a given tool."""
    return TOOL_TO_SERVER.get(tool_name)


def get_tools_for_server(server_name: str) -> List[str]:
    """Get all tools available on a given server."""
    return SERVER_TO_TOOLS.get(server_name, [])


def get_all_servers() -> List[str]:
    """Get list of all available servers."""
    return list(SERVER_TO_TOOLS.keys())


def get_all_tools() -> List[str]:
    """Get list of all available tools."""
    return list(TOOL_TO_SERVER.keys())


SERVER_DESCRIPTIONS: dict[str, str] = {
    "nav_server": "导航服务器 (port 8001) - 路线规划、POI搜索、交通信息、地图显示、组队出行",
    "vehicle_server": "车辆控制服务器 (port 8002) - 车门、车灯、引擎等车辆控制",
    "ac_server": "空调服务器 (port 8003) - 温度、风速、模式等空调控制",
    "media_server": "媒体服务器 (port 8004) - 音视频播放、电台、音量控制",
    "phone_server": "电话服务器 (port 8005) - 通话、联系人、消息、蓝牙WiFi",
    "calendar_server": "日历服务器 (port 8006) - 日程和提醒管理",
    "weather_server": "天气服务器 (port 8007) - 天气查询和生活信息",
    "interior_server": "内饰服务器 (port 8008) - 车窗、氛围灯、座椅调节",
    "hud_server": "HUD服务器 (port 8009) - 平视显示器控制",
    "system_server": "系统服务器 (port 8010) - 系统设置和应用管理",
    "wireless_server": "无线服务器 (port 8011) - WiFi和蓝牙连接",
    "camera_server": "摄像头服务器 (port 8012) - 行车记录仪和全景影像",
    "interaction_server": "交互服务器 (port 8013) - UI交互操作",
    "app_server": "应用服务器 (port 8014) - 应用安装和管理",
}


def get_server_description(server_name: str) -> str:
    return SERVER_DESCRIPTIONS.get(server_name)


# Port mapping for reference
SERVER_PORTS: dict[str, int] = {
    "nav_server": 8001,
    "vehicle_server": 8002,
    "ac_server": 8003,
    "media_server": 8004,
    "phone_server": 8005,
    "calendar_server": 8006,
    "weather_server": 8007,
    "interior_server": 8008,
    "hud_server": 8009,
    "system_server": 8010,
    "wireless_server": 8011,
    "camera_server": 8012,
    "interaction_server": 8013,
    "app_server": 8014,
}
