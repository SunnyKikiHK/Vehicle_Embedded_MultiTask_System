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
    "interaction-control-agent": "Interaction Control Agent",
    "info-query-agent": "Info Query Agent",
}

# Tool result templates for common operations
TOOL_RESPONSE_TEMPLATES: dict[str, str] = {
    # Navigation templates
    "go_poi": "好的，正在为您导航到 {destination}，地址是 {address}",
    "open_nav": "好的，导航已打开",
    "close_nav": "好的，导航已关闭",
    "go_home": "好的，正在为您导航回家",
    "go_company": "好的，正在为您导航到公司",
    "nav_set_home": "好的，已设置 {name} 为家庭地址",
    "nav_set_company": "好的，已设置 {name} 为公司地址",
    "flush_route": "好的，路线已重新规划",
    "change_route": "好的，已切换到备选路线",
    "open_ar_nav": "好的，AR导航已开启",
    "close_ar_nav": "好的，AR导航已关闭",
    "join_group": "好的，已加入组队",
    "build_group": "好的，已创建车队，邀请码是 {invite_code}",

    # Map templates
    "nav_zoom_in": "好的，地图已放大",
    "nav_zoom_out": "好的，地图已缩小",
    "set_3d_map": "好的，已切换到3D视图",
    "set_2d_map": "好的，已切换到2D视图",
    "set_north_up": "好的，已切换到北朝上模式",
    "set_head_up": "好的，已切换到车头朝上模式",
    "back_to_center": "好的，已回到当前位置",
    "view_small_map": "好的，小地图已打开",
    "close_small_map": "好的，小地图已关闭",

    # AC templates
    "ac_on": "好的，空调已打开",
    "ac_off": "好的，空调已关闭",
    "ac_auto": "好的，已开启自动空调模式",
    "defrost": "好的，已开启除雾功能",
    "sync_ac": "好的，已开启同步控制",

    # Media templates
    "play_media": "好的，正在播放",
    "pause_media": "好的，已暂停",
    "stop_media": "好的，已停止播放",
    "next_track": "好的，已切换到下一首",
    "previous_track": "好的，已切换到上一首",
    "mute_volume": "好的，已静音",
    "unmute_volume": "好的，已取消静音",

    # Light templates
    "lights_on": "好的，灯光已打开",
    "lights_off": "好的，灯光已关闭",

    # Phone templates
    "make_call": "好的，正在为您拨打 {number}",
    "end_call": "好的，已挂断电话",
    "answer_call": "好的，已接听电话",
    "reject_call": "好的，已拒绝来电",

    # Weather templates
    "get_weather": "好的，当前天气是 {weather}",
    "get_forecast": "好的，明天天气是 {weather}",
}

# Default server URLs for consolidated MCP servers
# Each server may handle multiple logical domains (e.g., nav_server handles nav + map)
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
    # port 8013: UI Interaction (legacy, merged into system_server)
    "interaction_server": "http://localhost:8013/mcp",
    # port 8014: App Management (standalone)
    "app_server": "http://localhost:8014/mcp",
}

# Server port mapping for reference
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
