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
def open_nav() -> Dict[str, Any]:
    """打开导航 - Open the navigation app"""
    return {
        "status": "success",
        "action": "open_nav",
        "message": "导航已打开"
    }


@mcp.tool()
def close_nav() -> Dict[str, Any]:
    """关闭导航 - Close navigation"""
    return {
        "status": "success",
        "action": "close_nav",
        "message": "导航已关闭"
    }


@mcp.tool()
def go_home() -> Dict[str, Any]:
    """导航回家 - Navigate to saved home address"""
    return {
        "status": "success",
        "action": "go_home",
        "message": "正在导航回家"
    }


@mcp.tool()
def go_company() -> Dict[str, Any]:
    """导航公司 - Navigate to saved company address"""
    return {
        "status": "success",
        "action": "go_company",
        "message": "正在导航到公司"
    }


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
def delete_via() -> Dict[str, Any]:
    """删除途经点 - Remove waypoint"""
    return {
        "status": "success",
        "action": "delete_via",
        "message": "已删除途经点"
    }


@mcp.tool()
def flush_route() -> Dict[str, Any]:
    """重新算路 - Recalculate route"""
    return {
        "status": "success",
        "action": "flush_route",
        "message": "路线已重新规划"
    }


@mcp.tool()
def change_route() -> Dict[str, Any]:
    """切换路线 - Switch to alternate route"""
    return {
        "status": "success",
        "action": "change_route",
        "message": "已切换到备选路线"
    }


@mcp.tool()
def get_route_information() -> Dict[str, Any]:
    """打开路线信息 - Get detailed route info"""
    return {"status": "info", "message": "请开始导航后查看路线详情"}


@mcp.tool()
def open_full_map() -> Dict[str, Any]:
    """打开路线全览 - Show full route overview"""
    return {
        "status": "success",
        "action": "open_full_map",
        "message": "路线全览已打开"
    }


@mcp.tool()
def close_full_map() -> Dict[str, Any]:
    """关闭路线全览 - Hide route overview"""
    return {
        "status": "success",
        "action": "close_full_map",
        "message": "路线全览已关闭"
    }


#  Route Preferences 

@mcp.tool()
def switch_main_route() -> Dict[str, Any]:
    """切换到主路 - Prefer main road"""
    return {
        "status": "success",
        "action": "switch_main_route",
        "message": "已切换到主路优先"
    }


@mcp.tool()
def switch_side_route() -> Dict[str, Any]:
    """切换到辅路 - Prefer side road"""
    return {
        "status": "success",
        "action": "switch_side_route",
        "message": "已切换到辅路优先"
    }


@mcp.tool()
def speed_fast() -> Dict[str, Any]:
    """打开速度最快 - Enable fastest route mode"""
    return {
        "status": "success",
        "action": "speed_fast",
        "message": "已开启速度最快模式"
    }


@mcp.tool()
def cancel_speed_fast() -> Dict[str, Any]:
    """关闭速度最快 - Disable fastest route"""
    return {
        "status": "success",
        "action": "cancel_speed_fast",
        "message": "已关闭速度最快模式"
    }


@mcp.tool()
def highway_first() -> Dict[str, Any]:
    """打开高速优先 - Prefer highways"""
    return {
        "status": "success",
        "action": "highway_first",
        "message": "已开启高速优先"
    }


@mcp.tool()
def smart_recommend() -> Dict[str, Any]:
    """打开智能路线推荐 - Enable smart route recommendation"""
    return {
        "status": "success",
        "action": "smart_recommend",
        "message": "已开启智能路线推荐"
    }


@mcp.tool()
def cancel_smart_recommend() -> Dict[str, Any]:
    """取消智能路线推荐 - Disable smart recommendation"""
    return {
        "status": "success",
        "action": "cancel_smart_recommend",
        "message": "已关闭智能路线推荐"
    }


@mcp.tool()
def main_route_first() -> Dict[str, Any]:
    """打开大路优先 - Prefer main roads"""
    return {
        "status": "success",
        "action": "main_route_first",
        "message": "已开启大路优先"
    }


@mcp.tool()
def cancel_main_first() -> Dict[str, Any]:
    """关闭大路优先 - Cancel main road preference"""
    return {
        "status": "success",
        "action": "cancel_main_first",
        "message": "已关闭大路优先"
    }


#  Traffic Avoidance 

@mcp.tool()
def avoid_congestion() -> Dict[str, Any]:
    """打开躲避拥堵 - Enable congestion avoidance"""
    return {
        "status": "success",
        "action": "avoid_congestion",
        "message": "已开启躲避拥堵"
    }


@mcp.tool()
def cancel_avoid_congestion() -> Dict[str, Any]:
    """关闭躲避拥堵 - Disable congestion avoidance"""
    return {
        "status": "success",
        "action": "cancel_avoid_congestion",
        "message": "已关闭躲避拥堵"
    }


@mcp.tool()
def avoid_high_way() -> Dict[str, Any]:
    """打开不走高速 - Avoid highways"""
    return {
        "status": "success",
        "action": "avoid_high_way",
        "message": "已开启不走高速模式"
    }


@mcp.tool()
def cancel_avoid_high_way() -> Dict[str, Any]:
    """关闭不走高速 - Cancel avoid highway"""
    return {
        "status": "success",
        "action": "cancel_avoid_high_way",
        "message": "已关闭不走高速模式"
    }


@mcp.tool()
def avoid_limit_line() -> Dict[str, Any]:
    """打开避开限行 - Avoid restricted zones"""
    return {
        "status": "success",
        "action": "avoid_limit_line",
        "message": "已开启避开限行"
    }


@mcp.tool()
def cancel_avoid_limit_line() -> Dict[str, Any]:
    """关闭避开限行 - Cancel avoid restricted zones"""
    return {
        "status": "success",
        "action": "cancel_avoid_limit_line",
        "message": "已关闭避开限行"
    }


@mcp.tool()
def open_avoid_fee() -> Dict[str, Any]:
    """打开避免收费 - Enable toll avoidance"""
    return {
        "status": "success",
        "action": "open_avoid_fee",
        "message": "已开启避免收费"
    }


@mcp.tool()
def cancel_avoid_fee() -> Dict[str, Any]:
    """关闭避免收费 - Disable toll avoidance"""
    return {
        "status": "success",
        "action": "cancel_avoid_fee",
        "message": "已关闭避免收费"
    }


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
def open_electronic_eye() -> Dict[str, Any]:
    """打开电子眼 - Show speed cameras"""
    return {
        "status": "success",
        "action": "open_electronic_eye",
        "message": "电子眼已开启"
    }


@mcp.tool()
def close_electronic_eye() -> Dict[str, Any]:
    """关闭电子眼 - Hide speed cameras"""
    return {
        "status": "success",
        "action": "close_electronic_eye",
        "message": "电子眼已关闭"
    }


@mcp.tool()
def open_cruise_information() -> Dict[str, Any]:
    """打开路况信息 - Enable traffic info overlay"""
    return {
        "status": "success",
        "action": "open_cruise_information",
        "message": "路况信息已开启"
    }


@mcp.tool()
def close_cruise_information() -> Dict[str, Any]:
    """关闭路况信息 - Disable traffic info"""
    return {
        "status": "success",
        "action": "close_cruise_information",
        "message": "路况信息已关闭"
    }


#  AR Navigation 

@mcp.tool()
def open_ar_nav() -> Dict[str, Any]:
    """打开AR导航 - Enable AR navigation"""
    return {
        "status": "success",
        "action": "open_ar_nav",
        "message": "AR导航已开启"
    }


@mcp.tool()
def close_ar_nav() -> Dict[str, Any]:
    """关闭AR导航 - Disable AR navigation"""
    return {
        "status": "success",
        "action": "close_ar_nav",
        "message": "AR导航已关闭"
    }


@mcp.tool()
def front_line_detail() -> Dict[str, Any]:
    """前方路线引导 - Show upcoming route guidance"""
    return {
        "status": "success",
        "action": "front_line_detail",
        "message": "前方直行500米，左转进入XX路"
    }


#  Navigation Broadcast 

@mcp.tool()
def open_nav_broadcast() -> Dict[str, Any]:
    """打开导航播报 - Enable navigation TTS"""
    return {
        "status": "success",
        "action": "open_nav_broadcast",
        "message": "导航播报已开启"
    }


@mcp.tool()
def close_nav_broadcast() -> Dict[str, Any]:
    """关闭导航播报 - Disable navigation TTS"""
    return {
        "status": "success",
        "action": "close_nav_broadcast",
        "message": "导航播报已关闭"
    }


@mcp.tool()
def replay_broadcast() -> Dict[str, Any]:
    """重播广播 - Repeat last navigation prompt"""
    return {
        "status": "success",
        "action": "replay_broadcast",
        "message": "前方直行500米，左转"
    }


@mcp.tool()
def slow_broadcast_speed() -> Dict[str, Any]:
    """放慢播报 - Slow down TTS speed"""
    return {
        "status": "success",
        "action": "slow_broadcast_speed",
        "message": "已放慢播报速度"
    }


@mcp.tool()
def accelerate_broadcast_speed() -> Dict[str, Any]:
    """加速播报 - Speed up TTS"""
    return {
        "status": "success",
        "action": "accelerate_broadcast_speed",
        "message": "已加速播报速度"
    }


@mcp.tool()
def open_simple_broadcast() -> Dict[str, Any]:
    """打开简洁播报 - Enable concise prompts"""
    return {
        "status": "success",
        "action": "open_simple_broadcast",
        "message": "已开启简洁播报模式"
    }


@mcp.tool()
def close_simple_broadcast() -> Dict[str, Any]:
    """关闭简洁播报 - Disable concise prompts"""
    return {
        "status": "success",
        "action": "close_simple_broadcast",
        "message": "已关闭简洁播报模式"
    }


#  Commute Navigation 

@mcp.tool()
def open_commute_nav() -> Dict[str, Any]:
    """打开通勤导航 - Enable commute navigation"""
    return {
        "status": "success",
        "action": "open_commute_nav",
        "message": "通勤导航已开启"
    }


@mcp.tool()
def close_commute_nav() -> Dict[str, Any]:
    """关闭通勤导航 - Disable commute navigation"""
    return {
        "status": "success",
        "action": "close_commute_nav",
        "message": "通勤导航已关闭"
    }


#  Collections 

@mcp.tool()
def open_nav_collections() -> Dict[str, Any]:
    """打开导航收藏夹 - Open saved locations"""
    return {
        "status": "success",
        "action": "open_nav_collections",
        "message": "收藏夹已打开"
    }


@mcp.tool()
def close_nav_collections() -> Dict[str, Any]:
    """关闭导航收藏夹 - Close saved locations"""
    return {
        "status": "success",
        "action": "close_nav_collections",
        "message": "收藏夹已关闭"
    }


@mcp.tool()
def nav_to_collection() -> Dict[str, Any]:
    """去收藏地址 - Navigate to saved location"""
    return {
        "status": "info",
        "action": "nav_to_collection",
        "message": "请选择要导航的收藏地址"
    }


@mcp.tool()
def collect_target_location() -> Dict[str, Any]:
    """收藏目的地 - Save destination"""
    return {
        "status": "info",
        "action": "collect_target_location",
        "message": "请先开始导航再收藏目的地"
    }


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
def open_map_setting() -> Dict[str, Any]:
    """打开地图设置 - Open map settings"""
    return {
        "status": "success",
        "action": "open_map_setting",
        "message": "地图设置已打开"
    }


@mcp.tool()
def close_map_setting() -> Dict[str, Any]:
    """关闭地图设置 - Close map settings"""
    return {
        "status": "success",
        "action": "close_map_setting",
        "message": "地图设置已关闭"
    }


@mcp.tool()
def change_nav_sign() -> Dict[str, Any]:
    """切换导航标志 - Change navigation sign style"""
    return {
        "status": "success",
        "action": "change_nav_sign",
        "message": "已切换导航标志样式"
    }


#  Group Travel 

@mcp.tool()
def join_group() -> Dict[str, Any]:
    """加入组队 - Join a travel group"""
    return {
        "status": "info",
        "action": "join_group",
        "message": "请提供组队邀请码"
    }


@mcp.tool()
def build_group() -> Dict[str, Any]:
    """创建组队 - Create a new group"""
    return {
        "status": "success",
        "action": "build_group",
        "message": "车队已创建",
        "invite_code": "ABC123"
    }


@mcp.tool()
def quit_group() -> Dict[str, Any]:
    """退出组队 - Leave current group"""
    return {
        "status": "success",
        "action": "quit_group",
        "message": "已退出车队"
    }


@mcp.tool()
def open_group() -> Dict[str, Any]:
    """打开组队 - Open group travel interface"""
    return {
        "status": "success",
        "action": "open_group",
        "message": "组队界面已打开"
    }


@mcp.tool()
def ask_meeting_place() -> Dict[str, Any]:
    """设置集结地 - Query group meetup location"""
    return {
        "status": "info",
        "action": "ask_meeting_place",
        "message": "请设置集结地点"
    }


@mcp.tool()
def go_meeting_place() -> Dict[str, Any]:
    """去汇合地点 - Navigate to meetup point"""
    return {
        "status": "success",
        "action": "go_meeting_place",
        "message": "正在导航到汇合地点"
    }


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
