#!/usr/bin/env python
"""Navigation Server - MCP Implementation for Navigation & Routing

This server handles navigation operations including route planning, POI search, 
traffic conditions, and route preferences. Uses Amap (Gaode) API for location services.
Based on navigation-agent and group-travel-agent intents from AGENT_DESIGN_PROPOSAL.md
"""
import os
import httpx
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nav_server")

AMAP_API_KEY = os.environ.get("AMAP_API_KEY", None)
AMAP_BASE_URL = os.environ.get("AMAP_BASE_URL", None)

HEADERS = {"User-Agent": "VehicleNavigation/1.0"}


def amap_request(endpoint: str, params: Dict[str, Any]) -> Dict:
    """Make request to Amap API"""
    params["key"] = AMAP_API_KEY
    try:
        response = httpx.get(
            f"{AMAP_BASE_URL}/{endpoint}",
            params=params,
            headers=HEADERS,
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"info": str(e), "status": "0"}


#  Route Planning 

@mcp.tool()
def go_poi(poi: str, city: Optional[str] = None, index: int = 1) -> Dict[str, Any]:
    """导航搜索 - Search and navigate to a POI"""
    if city:
        result = amap_request("place/text", {"keywords": poi, "city": city, "types": "风景名胜|机场|火车站"})
    else:
        result = amap_request("place/text", {"keywords": poi, "types": "风景名胜|机场|火车站"})
    
    if result.get("pois") and len(result["pois"]) >= index:
        selected = result["pois"][index - 1]
        return {
            "status": "success",
            "destination": selected.get("name"),
            "location": selected.get("location"),
            "address": selected.get("address"),
            "tel": selected.get("tel"),
            "distance": selected.get("distance")
        }
    return {"status": "error", "message": f"未找到{poi}相关地点"}


@mcp.tool()
def open_nav() -> str:
    """打开导航 - Open the navigation app"""
    return "导航已打开"


@mcp.tool()
def close_nav() -> str:
    """关闭导航 - Close navigation"""
    return "导航已关闭"


@mcp.tool()
def go_home() -> str:
    """导航回家 - Navigate to saved home address"""
    return "正在导航回家"


@mcp.tool()
def go_company() -> str:
    """导航公司 - Navigate to saved company address"""
    return "正在导航到公司"


@mcp.tool()
def nav_set_home(poi: Optional[str] = None, index: int = 1) -> Dict[str, Any]:
    """设置家地址 - Set or update home address"""
    if poi:
        result = amap_request("place/text", {"keywords": poi})
        if result.get("pois"):
            selected = result["pois"][index - 1]
            return {
                "status": "success",
                "type": "home",
                "name": selected.get("name"),
                "location": selected.get("location"),
                "address": selected.get("address")
            }
    return {"status": "success", "type": "home", "name": "当前位置", "address": "当前GPS位置"}


@mcp.tool()
def nav_set_company(poi: Optional[str] = None, index: int = 1) -> Dict[str, Any]:
    """设置公司地址 - Set or update company address"""
    if poi:
        result = amap_request("place/text", {"keywords": poi})
        if result.get("pois"):
            selected = result["pois"][index - 1]
            return {
                "status": "success",
                "type": "company",
                "name": selected.get("name"),
                "location": selected.get("location"),
                "address": selected.get("address")
            }
    return {"status": "success", "type": "company", "name": "当前位置", "address": "当前GPS位置"}


@mcp.tool()
def add_via(poi: str, via_index: int = 1) -> Dict[str, Any]:
    """添加途经点 - Add waypoint to route"""
    result = amap_request("place/text", {"keywords": poi})
    if result.get("pois"):
        selected = result["pois"][via_index - 1]
        return {
            "status": "success",
            "via_location": selected.get("name"),
            "location": selected.get("location"),
            "address": selected.get("address")
        }
    return {"status": "error", "message": f"未找到途经点: {poi}"}


@mcp.tool()
def delete_via() -> str:
    """删除途经点 - Remove waypoint"""
    return "已删除途经点"


@mcp.tool()
def flush_route() -> str:
    """重新算路 - Recalculate route"""
    return "路线已重新规划"


@mcp.tool()
def change_route() -> str:
    """切换路线 - Switch to alternate route"""
    return "已切换到备选路线"


@mcp.tool()
def get_route_information() -> Dict[str, Any]:
    """打开路线信息 - Get detailed route info"""
    return {"status": "info", "message": "请开始导航后查看路线详情"}


@mcp.tool()
def open_full_map() -> str:
    """打开路线全览 - Show full route overview"""
    return "路线全览已打开"


@mcp.tool()
def close_full_map() -> str:
    """关闭路线全览 - Hide route overview"""
    return "路线全览已关闭"


#  Route Preferences 

@mcp.tool()
def switch_main_route() -> str:
    """切换到主路 - Prefer main road"""
    return "已切换到主路优先"


@mcp.tool()
def switch_side_route() -> str:
    """切换到辅路 - Prefer side road"""
    return "已切换到辅路优先"


@mcp.tool()
def speed_fast() -> str:
    """打开速度最快 - Enable fastest route mode"""
    return "已开启速度最快模式"


@mcp.tool()
def cancel_speed_fast() -> str:
    """关闭速度最快 - Disable fastest route"""
    return "已关闭速度最快模式"


@mcp.tool()
def highway_first() -> str:
    """打开高速优先 - Prefer highways"""
    return "已开启高速优先"


@mcp.tool()
def smart_recommend() -> str:
    """打开智能路线推荐 - Enable smart route recommendation"""
    return "已开启智能路线推荐"


@mcp.tool()
def cancel_smart_recommend() -> str:
    """取消智能路线推荐 - Disable smart recommendation"""
    return "已关闭智能路线推荐"


@mcp.tool()
def main_route_first() -> str:
    """打开大路优先 - Prefer main roads"""
    return "已开启大路优先"


@mcp.tool()
def cancel_main_first() -> str:
    """关闭大路优先 - Cancel main road preference"""
    return "已关闭大路优先"


#  Traffic Avoidance 

@mcp.tool()
def avoid_congestion() -> str:
    """打开躲避拥堵 - Enable congestion avoidance"""
    return "已开启躲避拥堵"


@mcp.tool()
def cancel_avoid_congestion() -> str:
    """关闭躲避拥堵 - Disable congestion avoidance"""
    return "已关闭躲避拥堵"


@mcp.tool()
def avoid_high_way() -> str:
    """打开不走高速 - Avoid highways"""
    return "已开启不走高速模式"


@mcp.tool()
def cancel_avoid_high_way() -> str:
    """关闭不走高速 - Cancel avoid highway"""
    return "已关闭不走高速模式"


@mcp.tool()
def avoid_limit_line() -> str:
    """打开避开限行 - Avoid restricted zones"""
    return "已开启避开限行"


@mcp.tool()
def cancel_avoid_limit_line() -> str:
    """关闭避开限行 - Cancel avoid restricted zones"""
    return "已关闭避开限行"


@mcp.tool()
def open_avoid_fee() -> str:
    """打开避免收费 - Enable toll avoidance"""
    return "已开启避免收费"


@mcp.tool()
def cancel_avoid_fee() -> str:
    """关闭避免收费 - Disable toll avoidance"""
    return "已关闭避免收费"


#  Traffic Information 

@mcp.tool()
def home_condition() -> Dict[str, Any]:
    """家路况 - Check traffic on route home"""
    return {"status": "info", "message": "请先设置家地址后查询路况"}


@mcp.tool()
def company_condition() -> Dict[str, Any]:
    """公司路况 - Check traffic on route to company"""
    return {"status": "info", "message": "请先设置公司地址后查询路况"}


@mcp.tool()
def poi_condition(poi: str, city: Optional[str] = None) -> Dict[str, Any]:
    """POI路况 - Check traffic at a specific POI"""
    place_result = amap_request("place/text", {"keywords": poi})
    if not place_result.get("pois"):
        return {"status": "error", "message": f"未找到{poi}"}

    selected = place_result["pois"][0]
    name = selected.get("name", "")
    location = selected.get("location", "")
    search_city = city or selected.get("cityname", "北京")

    traffic_result = amap_request(
        "traffic/status/road",
        {"name": name, "city": search_city, "level": "3", "extensions": "all"}
    )

    if traffic_result.get("status") != "1":
        return {
            "status": "error",
            "message": traffic_result.get("info", "API调用失败"),
            "infocode": traffic_result.get("infocode")
        }

    if not traffic_result.get("trafficinfo"):
        return {
            "status": "error",
            "message": "未获取到路况信息",
            "poi": name
        }

    ti = traffic_result["trafficinfo"]
    eval_data = ti.get("evaluation") or {}
    road = ti.get("roads")
    status_map = {"0": "未知", "1": "畅通", "2": "缓行", "3": "拥堵", "4": "严重拥堵"}

    return {
        "status": "success",
        "poi": name,
        "location": location,
        "traffic_status": status_map.get(eval_data.get("status", "1"), "畅通"),
        "description": eval_data.get("description"),
        "expedite": eval_data.get("expedite"),
        "congested": eval_data.get("congested"),
        "blocked": eval_data.get("blocked"),
        "road": {
            "name": road.get("name") if road else None,
            "status": status_map.get(road.get("status", "1") if road else "1", "畅通"),
            "speed": road.get("speed") if road else None,
            "direction": road.get("direction") if road else None,
            "polyline": road.get("polyline") if road else None
        } if road else None
    }


@mcp.tool()
def ahead_condition(poi: Optional[str] = None) -> Dict[str, Any]:
    """查看沿途路况 - Check traffic along the route"""
    if not poi:
        return {"status": "error", "message": "请提供具体地点查询沿途路况"}

    place_result = amap_request("place/text", {"keywords": poi})
    if not place_result.get("pois"):
        return {"status": "error", "message": f"未找到地点{poi}"}

    selected = place_result["pois"][0]
    name = selected.get("name", "")
    search_city = selected.get("cityname", "北京")

    traffic_result = amap_request(
        "traffic/status/road",
        {"name": name, "city": search_city, "level": "3", "extensions": "all"}
    )

    if traffic_result.get("status") != "1":
        return {
            "status": "error",
            "message": traffic_result.get("info", "API调用失败"),
            "infocode": traffic_result.get("infocode")
        }

    if not traffic_result.get("trafficinfo"):
        return {
            "status": "error",
            "message": "未获取到路况信息",
            "poi": name
        }

    ti = traffic_result["trafficinfo"]
    eval_data = ti.get("evaluation") or {}
    road = ti.get("roads")
    status_map = {"0": "未知", "1": "畅通", "2": "缓行", "3": "拥堵", "4": "严重拥堵"}

    return {
        "status": "success",
        "poi": name,
        "traffic_status": status_map.get(eval_data.get("status", "1"), "畅通"),
        "description": eval_data.get("description"),
        "expedite": eval_data.get("expedite"),
        "congested": eval_data.get("congested"),
        "blocked": eval_data.get("blocked"),
        "road": {
            "name": road.get("name") if road else None,
            "status": status_map.get(road.get("status", "1") if road else "1", "畅通"),
            "speed": road.get("speed") if road else None,
            "direction": road.get("direction") if road else None,
            "polyline": road.get("polyline") if road else None
        } if road else None
    }


@mcp.tool()
def target_condition() -> Dict[str, Any]:
    """目的地路况 - Check traffic at destination"""
    return {"status": "info", "message": "请开始导航后查询目的地路况"}


@mcp.tool()
def traffic_incidents(city: Optional[str] = None) -> Dict[str, Any]:
    """查看交通事件 - View traffic incidents"""
    result = amap_request(
        "traffic/status/road",
        {"city": city or "北京", "level": "3", "extensions": "all"}
    )

    if result.get("status") != "1":
        return {
            "status": "error",
            "message": result.get("info", "API调用失败"),
            "infocode": result.get("infocode")
        }

    if not result.get("trafficinfo"):
        return {"status": "error", "message": "未获取到交通态势信息"}

    ti = result["trafficinfo"]
    eval_data = ti.get("evaluation") or {}
    road = ti.get("roads")
    status_map = {"0": "未知", "1": "畅通", "2": "缓行", "3": "拥堵", "4": "严重拥堵"}

    return {
        "status": "success",
        "description": eval_data.get("description"),
        "expedite": eval_data.get("expedite"),
        "congested": eval_data.get("congested"),
        "blocked": eval_data.get("blocked"),
        "traffic_status": status_map.get(eval_data.get("status", "0"), "未知"),
        "road": {
            "name": road.get("name") if road else None,
            "status": status_map.get(road.get("status", "0") if road else "0", "未知"),
            "speed": road.get("speed") if road else None,
            "direction": road.get("direction") if road else None,
            "angle": road.get("angle") if road else None,
            "polyline": road.get("polyline") if road else None
        } if road else None
    }


@mcp.tool()
def open_electronic_eye() -> str:
    """打开电子眼 - Show speed cameras"""
    return "电子眼已开启"


@mcp.tool()
def close_electronic_eye() -> str:
    """关闭电子眼 - Hide speed cameras"""
    return "电子眼已关闭"


@mcp.tool()
def open_cruise_information() -> str:
    """打开路况信息 - Enable traffic info overlay"""
    return "路况信息已开启"


@mcp.tool()
def close_cruise_information() -> str:
    """关闭路况信息 - Disable traffic info"""
    return "路况信息已关闭"


#  AR Navigation 

@mcp.tool()
def open_ar_nav() -> str:
    """打开AR导航 - Enable AR navigation"""
    return "AR导航已开启"


@mcp.tool()
def close_ar_nav() -> str:
    """关闭AR导航 - Disable AR navigation"""
    return "AR导航已关闭"


@mcp.tool()
def front_line_detail() -> str:
    """前方路线引导 - Show upcoming route guidance"""
    return "前方直行500米，左转进入XX路"


#  Navigation Broadcast 

@mcp.tool()
def open_nav_broadcast() -> str:
    """打开导航播报 - Enable navigation TTS"""
    return "导航播报已开启"


@mcp.tool()
def close_nav_broadcast() -> str:
    """关闭导航播报 - Disable navigation TTS"""
    return "导航播报已关闭"


@mcp.tool()
def replay_broadcast() -> str:
    """重播广播 - Repeat last navigation prompt"""
    return "前方直行500米，左转"


@mcp.tool()
def slow_broadcast_speed() -> str:
    """放慢播报 - Slow down TTS speed"""
    return "已放慢播报速度"


@mcp.tool()
def accelerate_broadcast_speed() -> str:
    """加速播报 - Speed up TTS"""
    return "已加速播报速度"


@mcp.tool()
def open_simple_broadcast() -> str:
    """打开简洁播报 - Enable concise prompts"""
    return "已开启简洁播报模式"


@mcp.tool()
def close_simple_broadcast() -> str:
    """关闭简洁播报 - Disable concise prompts"""
    return "已关闭简洁播报模式"


#  Commute Navigation 

@mcp.tool()
def open_commute_nav() -> str:
    """打开通勤导航 - Enable commute navigation"""
    return "通勤导航已开启"


@mcp.tool()
def close_commute_nav() -> str:
    """关闭通勤导航 - Disable commute navigation"""
    return "通勤导航已关闭"


#  Collections 

@mcp.tool()
def open_nav_collections() -> str:
    """打开导航收藏夹 - Open saved locations"""
    return "收藏夹已打开"


@mcp.tool()
def close_nav_collections() -> str:
    """关闭导航收藏夹 - Close saved locations"""
    return "收藏夹已关闭"


@mcp.tool()
def nav_to_collection() -> str:
    """去收藏地址 - Navigate to saved location"""
    return "请选择要导航的收藏地址"


@mcp.tool()
def collect_target_location() -> str:
    """收藏目的地 - Save destination"""
    return "请先开始导航再收藏目的地"


@mcp.tool()
def collect_current_location() -> Dict[str, Any]:
    """收藏当前地址 - Save current location"""
    result = amap_request("config/view", {"extensions": "base"})
    if result.get("regeocode"):
        return {
            "status": "success",
            "name": "当前位置",
            "address": result["regeocode"].get("formatted_address")
        }
    return {"status": "success", "name": "当前位置"}


#  Map Settings 

@mcp.tool()
def ask_where() -> Dict[str, Any]:
    """当前位置查询 - Query current GPS location"""
    result = amap_request("config/view", {"extensions": "base"})
    if result.get("regeocode"):
        return {
            "status": "success",
            "address": result["regeocode"].get("formatted_address"),
            "province": result["regeocode"].get("addressComponent", {}).get("province"),
            "city": result["regeocode"].get("addressComponent", {}).get("city"),
            "district": result["regeocode"].get("addressComponent", {}).get("district")
        }
    return {"status": "error", "message": "正在获取位置..."}


@mcp.tool()
def open_map_setting() -> str:
    """打开地图设置 - Open map settings"""
    return "地图设置已打开"


@mcp.tool()
def close_map_setting() -> str:
    """关闭地图设置 - Close map settings"""
    return "地图设置已关闭"


@mcp.tool()
def change_nav_sign() -> str:
    """切换导航标志 - Change navigation sign style"""
    return "已切换导航标志样式"


#  Group Travel 

@mcp.tool()
def join_group() -> str:
    """加入组队 - Join a travel group"""
    return "请提供组队邀请码"


@mcp.tool()
def build_group() -> Dict[str, Any]:
    """创建组队 - Create a new group"""
    return {"status": "success", "message": "车队已创建", "invite_code": "ABC123"}


@mcp.tool()
def quit_group() -> str:
    """退出组队 - Leave current group"""
    return "已退出车队"


@mcp.tool()
def open_group() -> str:
    """打开组队 - Open group travel interface"""
    return "组队界面已打开"


@mcp.tool()
def ask_meeting_place() -> str:
    """设置集结地 - Query group meetup location"""
    return "请设置集结地点"


@mcp.tool()
def go_meeting_place() -> str:
    """去汇合地点 - Navigate to meetup point"""
    return "正在导航到汇合地点"


@mcp.tool()
def group_member_location() -> Dict[str, Any]:
    """查看成员位置 - View locations of group members"""
    return {
        "status": "success",
        "members": [
            {"name": "张三", "distance": "3公里", "direction": "前方"},
            {"name": "李四", "distance": "5公里", "direction": "左后方"}
        ]
    }


if __name__ == "__main__":
    mcp.run()
