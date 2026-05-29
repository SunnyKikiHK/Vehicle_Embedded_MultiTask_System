#!/usr/bin/env python
"""Navigation Server - MCP Implementation for Navigation & Routing

This server handles navigation operations including route planning, POI search,
traffic conditions, and route preferences. Uses Amap (Gaode) API for location services.
Based on navigation-agent and group-travel-agent intents from AGENT_DESIGN_PROPOSAL.md
"""
import os
import httpx
import logging
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

from src.db.redis_client import RedisClient
from src.db.postgres_client import FrequentLocationStore, CollectedLocationStore
from src.context.location_provider import init_location_provider

logger = logging.getLogger(__name__)

mcp = FastMCP("nav_server", host="0.0.0.0", port=8001)

AMAP_API_KEY = os.environ.get("AMAP_API_KEY", None)
AMAP_BASE_URL = os.environ.get("AMAP_BASE_URL", None)

HEADERS = {"User-Agent": "VehicleNavigation/1.0"}

# Global location provider instance (initialized lazily)
_location_provider = None

# PostgreSQL configuration
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)

# Global store instances - initialized lazily like Redis
_frequent_store: FrequentLocationStore | None = None
_collected_store: CollectedLocationStore | None = None


def _create_stores():
    """Create store instances with connection info (without initializing pools)."""
    global _frequent_store, _collected_store
    if _frequent_store is None:
        _frequent_store = FrequentLocationStore(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
    if _collected_store is None:
        _collected_store = CollectedLocationStore(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )


async def _ensure_stores_initialized():
    """Lazily initialize store instances and pools (like Redis pattern)."""
    global _frequent_store, _collected_store
    _create_stores()
    
    if FrequentLocationStore._pool is None:
        await FrequentLocationStore.init_pool(_frequent_store)
        logger.info("[nav_server] FrequentLocationStore pool initialized")
    if CollectedLocationStore._pool is None:
        await CollectedLocationStore.init_pool(_collected_store)
        logger.info("[nav_server] CollectedLocationStore pool initialized")


def _init_location_provider():
    """Initialize location provider with Redis client if available."""
    global _location_provider
    if _location_provider is not None:
        return _location_provider
    
    try:  
        redis_client = RedisClient(host="localhost", port=6379)
        _location_provider = init_location_provider(redis_client)
        logger.info("[nav_server] LocationProvider initialized with Redis")
        return _location_provider
    except Exception as e:
        logger.warning(f"[nav_server] Failed to initialize LocationProvider: {e}")
        return None


async def _get_location_async(vehicle_id: str) -> Optional[Dict[str, Any]]:
    """Get vehicle location from Redis-based LocationProvider (async)."""
    provider = _init_location_provider()
    if provider is None:
        return None
    try:
        return await provider.get_current_location(vehicle_id)
    except Exception as e:
        logger.warning(f"[nav_server] Failed to get location from provider: {e}")
        return None


async def get_current_vehicle_location(vehicle_id: Optional[str] = None) -> str:
    """
    Async version of get_current_vehicle_location.
    
    Args:
        vehicle_id: Optional vehicle identifier.
    
    Returns:
        - "no_id": When vehicle_id is not provided
        - "no_location": When no GPS location is available
        - "lng,lat": Valid coordinates string (e.g., "116.473168,39.993015")
    """
    # Try to get from environment variable first
    env_location = os.environ.get("VEHICLE_GPS")
    if env_location:
        return env_location
    
    # Check if vehicle_id is provided
    if vehicle_id is None:
        return "no_id"
    
    # Try to get from LocationProvider
    try:
        location = await _get_location_async(vehicle_id)
        if location:
            return f"{location.longitude},{location.latitude}"
    except Exception as e:
        logger.debug(f"[nav_server] Could not get location from provider: {e}")
    
    # No location available
    return "no_location"



async def amap_request(endpoint: str, params: Dict[str, Any]) -> Dict:
    if not AMAP_API_KEY:
        return {"status": "0", "info": "AMAP_API_KEY not configured"}
    params["key"] = AMAP_API_KEY
    params["output"] = "json"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{AMAP_BASE_URL}/{endpoint}", params=params, headers=HEADERS, timeout=10)
            return r.json()
    except Exception as e:
        return {"status": "0", "info": f"Network error: {str(e)}"}


#  Route Planning 
@mcp.tool()
async def go_poi(
    poi: str,
    search_mode: str = "city",
    radius: int = 5000,
    city: Optional[str] = None,
    poi_type: Optional[str] = None,
    index: int = 1,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Search and navigate to a Point of Interest (POI).
    
    Args:
        poi: The clean name/keyword of the place (e.g., "加油站", "故宫").
             NEVER include spatial words like "附近的" or "最近的" here.
        search_mode: 
            - "nearby": Use when user says "nearest", "closest", "around me" (附近的, 最近的).
            - "city": Use when user specifies a city or a specific famous landmark.
        radius: Search radius in meters (default 5000m).
        city: City name (e.g., "北京"). Required if search_mode is "city" and POI is not unique.
        poi_type: Category filter (e.g., "加油站", "充电桩", "停车场").
        index: Which result to select (1-based, default 1).
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if search_mode == "nearby":
        current_location = await get_current_vehicle_location(vehicle_id)
        if current_location == "no_id":
            return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
        if current_location == "no_location":
            return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}
        endpoint = "place/around"
        params: Dict[str, Any] = {
            "keywords": poi,
            "location": current_location,
            "radius": 5000,
            "sortrule": "distance"
        }
    else:
        endpoint = "place/text"
        params = {"keywords": poi, "city": city or "全国"}

    if poi_type:
        params["types"] = poi_type

    result = await amap_request(endpoint, params)

    if result.get("status") == "1" and result.get("pois") and len(result["pois"]) >= index:
        selected = result["pois"][index - 1]

        distance_str = selected.get("distance", [])
        distance = distance_str[0] if isinstance(distance_str, list) and len(distance_str) > 0 else None

        return {
            "status": "success",
            "destination": selected.get("name"),
            "location": selected.get("location"),
            "address": selected.get("address"),
            "distance_meters": distance,
            "api_used": endpoint
        }

    return {"status": "fail", "message": f"未找到与 '{poi}' 相关的地点"}


@mcp.tool()
async def set_frequent_location(location_type: str, poi: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Set or update Home or Company address.
    
    Args:
        location_type: Must be either "home" (家) or "company" (公司).
        poi: Address/POI name (e.g., "望京SOHO"). If omitted, uses current vehicle GPS location. Do not input poi if user does not mention origin.
        metadata: Internal context data (auto-populated by the system).
    """
    if location_type not in ["home", "company"]:
        return {"status": "fail", "message": "location_type 必须是 'home' 或 'company'"}

    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    longitude = None
    latitude = None
    name = None
    address = None

    if poi:
        # Search for POI
        result = await amap_request("place/text", {"keywords": poi})
        if result.get("status") == "1" and result.get("pois"):
            selected = result["pois"][0]
            loc_str = selected.get("location", "")
            if loc_str:
                try:
                    longitude, latitude = map(float, loc_str.split(","))
                except:
                    pass
            name = selected.get("name")
            address = selected.get("address", "")
        else:
            return {"status": "fail", "message": f"未找到地点: {poi}"}
    else:
        # Use current GPS location
        current_loc = await get_current_vehicle_location(vehicle_id)
        if current_loc == "no_id":
            return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
        if current_loc == "no_location":
            return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}

        try:
            longitude, latitude = map(float, current_loc.split(","))
        except:
            return {"status": "fail", "message": "GPS坐标解析失败"}

        regeo = await amap_request("geocode/regeo", {"location": current_loc})
        address = regeo.get("regeocode", {}).get("formatted_address", "当前GPS位置")
        name = "当前位置"

    # Save to PostgreSQL 
    await _ensure_stores_initialized()
    success, err_msg = await _frequent_store.save(
        vehicle_id=vehicle_id,
        location_type=location_type,
        name=name,
        address=address,
        longitude=longitude,
        latitude=latitude
    )

    if not success:
        return {"status": "fail", "message": f"保存失败: {err_msg}"}

    return {
        "status": "success",
        "type": location_type,
        "name": name,
        "address": address,
        "location": f"{longitude},{latitude}" if longitude and latitude else None,
        "message": f"已将{'家' if location_type == 'home' else '公司'}地址设置为{name}"
    }

@mcp.tool()
async def collect_location(poi: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Save current location or a specific POI to favorites (收藏地址).
    
    Args:
        poi: Name or address of the place to collect (e.g., "望京SOHO", "故宫").
             If omitted, automatically uses current vehicle GPS location. Do not input poi if user does not mention poi.
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    longitude = None
    latitude = None
    name = None
    address = ""

    # Case 1: POI provided -> use place/text search
    if poi:
        search_result = await amap_request("place/text", {"keywords": poi})
        if not (search_result.get("status") == "1" and search_result.get("pois")):
            return {"status": "fail", "message": f"未找到地点: {poi}"}
        
        selected_poi = search_result["pois"][0]
        loc_str = selected_poi.get("location", "")
        if not loc_str:
            return {"status": "fail", "message": "地点坐标异常，无法收藏"}
        
        try:
            longitude, latitude = map(float, loc_str.split(","))
        except:
            return {"status": "fail", "message": "坐标解析失败"}
        
        name = selected_poi.get("name", "未知地点")
        address = selected_poi.get("address", "")

    # Case 2: No POI -> use current GPS
    else:
        loc_str = await get_current_vehicle_location(vehicle_id)
        if loc_str == "no_id":
            return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
        if loc_str == "no_location":
            return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}
        
        try:
            longitude, latitude = map(float, loc_str.split(","))
        except:
            return {"status": "fail", "message": "GPS坐标解析失败"}

        result = await amap_request("geocode/regeo", {"location": loc_str})
        if result.get("status") == "1" and result.get("regeocode"):
            rc = result["regeocode"]
            name = rc.get("formatted_address", "未知地点")
        else:
            name = "未知地点"

    # Save to PostgreSQL 
    await _ensure_stores_initialized()
    success, err_msg = await _collected_store.save(
        vehicle_id=vehicle_id,
        name=name,
        address=address,
        longitude=longitude,
        latitude=latitude
    )

    if not success:
        return {"status": "fail", "message": f"保存收藏地点失败: {err_msg}"}

    return {
        "status": "success",
        "name": name,
        "address": address,
        "longitude": longitude,
        "latitude": latitude,
        "message": f"已收藏地点: {name}"
    }



# New Tools for Frequent & Collected Locations
@mcp.tool()
async def check_frequent_location(location_type: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Check frequent location information (home or company).
    
    Args:
        location_type: Optional. Either "home" or "company". If omitted, returns all frequent locations.
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    await _ensure_stores_initialized()

    if location_type:
        if location_type not in ["home", "company"]:
            return {"status": "fail", "message": "location_type 必须是 'home' 或 'company'"}
        
        result, err_msg = await _frequent_store.get(vehicle_id, location_type)
        if err_msg:
            return {"status": "error", "message": f"查询失败: {err_msg}"}
        if result:
            return {
                "status": "success",
                "type": result["location_type"],
                "name": result["name"],
                "address": result["address"],
                "location": f"{result['longitude']},{result['latitude']}" if result.get("longitude") and result.get("latitude") else None,
                "updated_at": str(result.get("updated_at", ""))
            }
        return {
            "status": "success",
            "type": location_type,
            "message": f"尚未设置{'家' if location_type == 'home' else '公司'}地址"
        }
    else:
        # Return all frequent locations
        results, err_msg = await _frequent_store.get_all(vehicle_id)
        if err_msg:
            return {"status": "error", "message": f"查询失败: {err_msg}"}
        locations = []
        for r in results:
            locations.append({
                "type": r["location_type"],
                "name": r["name"],
                "address": r["address"],
                "location": f"{r['longitude']},{r['latitude']}" if r.get("longitude") and r.get("latitude") else None,
                "updated_at": str(r.get("updated_at", ""))
            })
        
        if not locations:
            return {"status": "success", "locations": [], "message": "尚未设置任何常用地址"}
        
        return {"status": "success", "locations": locations}


@mcp.tool()
async def delete_frequent_location(location_type: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Delete a frequent location (home or company).
    
    Args:
        location_type: Must be either "home" (家) or "company" (公司).
        metadata: Internal context data (auto-populated by the system).
    """
    if location_type not in ["home", "company"]:
        return {"status": "fail", "message": "location_type 必须是 'home' 或 'company'"}
    
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    await _ensure_stores_initialized()
    success, err_msg = await _frequent_store.delete(vehicle_id, location_type)
    if not success:
        return {"status": "fail", "message": f"删除失败: {err_msg}"}
    return {
        "status": "success",
        "message": f"已删除{'家' if location_type == 'home' else '公司'}地址"
    }


@mcp.tool()
async def list_collected_locations(metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """List all collected/favorite locations (收藏地址列表).
    
    Args:
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    await _ensure_stores_initialized()
    results, err_msg = await _collected_store.get_all(vehicle_id)
    if err_msg:
        return {"status": "error", "message": f"查询失败: {err_msg}"}
    locations = []
    for r in results:
        locations.append({
            "id": r["id"],
            "name": r["name"],
            "address": r["address"],
            "location": f"{r['longitude']},{r['latitude']}" if r.get("longitude") and r.get("latitude") else None,
            "created_at": str(r.get("created_at", ""))
        })
    
    if not locations:
        return {"status": "success", "locations": [], "message": "暂无收藏地址"}
    
    return {"status": "success", "locations": locations, "count": len(locations)}


@mcp.tool()
async def delete_collected_locations(location_id: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Delete collected/favorite locations.
    
    Args:
        location_id: Optional. Specific location ID to delete. If omitted, deletes ALL collected locations.
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    if not vehicle_id:
        return {"status": "error", "message": "无法获取车辆标识"}

    await _ensure_stores_initialized()
    if location_id:
        # Delete specific location
        success, err_msg = await _collected_store.delete(location_id)
        if not success:
            return {"status": "fail", "message": f"删除失败: {err_msg}"}
        return {"status": "success", "message": f"已删除收藏地点 (ID: {location_id})"}
    else:
        # Delete all collected locations
        success, err_msg = await _collected_store.delete_all(vehicle_id)
        if not success:
            return {"status": "fail", "message": f"删除失败: {err_msg}"}
        return {"status": "success", "message": "已删除所有收藏地点"}

@mcp.tool()
async def ask_where_am_i(metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Query current vehicle GPS location (我在哪 / 当前位置).
    Use this when the user asks "Where are we?", "What is my current location?", or "我在哪".
    No parameters required; automatically reads vehicle GPS.
    
    Args:
        metadata: Internal context data (auto-populated by the system).
    """
    vehicle_id = metadata.get("vehicle_id") if metadata else None
    loc_str = await get_current_vehicle_location(vehicle_id)
    
    if loc_str == "no_id":
        return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
    if loc_str == "no_location":
        return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}
    
    result = await amap_request("geocode/regeo", {"location": loc_str})
    
    if result.get("status") == "1" and result.get("regeocode"):
        rc = result["regeocode"]
        return {
            "status": "success",
            "address": rc.get("formatted_address"),
            "province": rc.get("addressComponent", {}).get("province"),
            "city": rc.get("addressComponent", {}).get("city"),
            "district": rc.get("addressComponent", {}).get("district"),
            "location": loc_str
        }
    return {"status": "fail", "message": "GPS定位失败或逆地理编码失败"}

@mcp.tool()
async def check_area_traffic(poi: Optional[str] = None, radius: int = 1000, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Check traffic congestion AROUND a specific POI or current location (周边路况).
    
    Use when user asks: 
    - "How is the traffic near [Place]?" / "[Place]附近堵不堵？" -> Provide poi argument.
    - "Is it congested around me?" / "附近堵不堵？" / "当前路况" -> Omit poi argument (uses car GPS).
    
    Args:
        poi: Name of the POI or area (e.g., "故宫", "国贸"). If omitted, automatically uses current vehicle GPS location. Do not input poi if user does not mention origin.
        radius: Search radius in meters (default 1000m).
        metadata: Internal context data (auto-populated by the system).
    """
    context_name = ""
    location = ""
    vehicle_id = metadata.get("vehicle_id") if metadata else None

    # 1. Determine target location: POI search vs Current GPS
    if poi:
        place_result = await amap_request("place/text", {"keywords": poi})
        if not (place_result.get("status") == "1" and place_result.get("pois")):
            return {"status": "error", "message": f"未找到地点: {poi}"}
        
        selected = place_result["pois"][0]
        location = selected.get("location")
        context_name = selected.get("name", poi)
    else:
        # Fallback to current vehicle GPS for "around me" queries
        location = await get_current_vehicle_location(vehicle_id)
        if location == "no_id":
            return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
        if location == "no_location":
            return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}
        context_name = "当前位置周边"

    if not location:
        return {"status": "error", "message": "无法确定查询位置，请提供POI名称或确保GPS已开启"}

    # 2. Use Circle API to check area traffic
    traffic_result = await amap_request(
        "traffic/status/circle",
        {"location": location, "radius": radius}
    )

    return _parse_traffic_evaluation(traffic_result, context_name=context_name)


@mcp.tool()
async def check_route_traffic(
    destination: str,
    origin: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Check traffic conditions ALONG a driving route (沿途路况 / 路线拥堵情况).
    Use when user asks: "Is the road to [Destination] jammed?" or "去[目的地]的路上堵吗？"

    Args:
        destination: Destination POI name (e.g., "望京SOHO", "故宫"). ONLY POI name allowed.
        origin: Starting point POI name. If omitted, uses current vehicle GPS. Do not input origin if user does not mention origin.
        metadata: Internal context data (auto-populated by the system).
    """
    if not destination:
        return {"status": "error", "message": "必须提供目的地 (destination)"}

    vehicle_id = metadata.get("vehicle_id") if metadata else None

    # Resolve ORIGIN (ONLY POI name OR current GPS)
    if origin is None:
        # No origin → use current vehicle GPS
        origin_loc = await get_current_vehicle_location(vehicle_id)
        if origin_loc == "no_id":
            return {"status": "error", "message": "系统错误：无法获取车辆标识，请检查车辆连接状态"}
        if origin_loc == "no_location":
            return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启并发送位置信息"}
    else:
        # Origin IS A POI → resolve to coordinates
        origin_search = await amap_request("place/text", {"keywords": origin})
        if not (origin_search.get("status") == "1" and origin_search.get("pois")):
            return {"status": "error", "message": f"未找到起点: {origin}"}
        origin_loc = origin_search["pois"][0].get("location")
        if not origin_loc:
            return {"status": "error", "message": f"起点 {origin} 坐标异常"}

    # Resolve DESTINATION ,ONLY POI name
    dest_search = await amap_request("place/text", {"keywords": destination})
    if not (dest_search.get("status") == "1" and dest_search.get("pois")):
        return {"status": "error", "message": f"未找到目的地: {destination}"}
    
    dest_loc = dest_search["pois"][0].get("location")
    dest_name = dest_search["pois"][0].get("name", destination)
    
    if not dest_loc:
        return {"status": "error", "message": f"目的地 {destination} 坐标异常"}

    # Get driving route & traffic
    route_result = await amap_request(
        "direction/driving",
        {"origin": origin_loc, "destination": dest_loc, "strategy": 0}
    )

    if route_result.get("status") == "1" and route_result.get("route", {}).get("paths"):
        path = route_result["route"]["paths"][0]
        distance_km = round(int(path.get("distance", 0)) / 1000, 1)
        duration_min = round(int(path.get("duration", 0)) / 60, 1)

        return {
            "status": "success",
            "context_name": f"去 {dest_name} 的路线",
            "distance_km": distance_km,
            "estimated_time_minutes": duration_min,
            "traffic_lights": path.get("traffic_lights", 0),
            "strategy": "躲避拥堵" if path.get("strategy") else "默认",
            "message": f"全程 {distance_km} 公里，预计行驶 {duration_min} 分钟。"
        }

    return {"status": "error", "message": "路线规划失败，无法获取沿途路况"}

@mcp.tool()
async def check_city_traffic_overview(city: str = "北京") -> Dict[str, Any]:
    """Get traffic congestion overview for a city's **major central region** (市中心核心区域路况/交通态势).
    Use when user asks: "How is the traffic in Beijing now?" or "北京现在堵不堵？"
    Note: This API only supports a **rectangle ≤10km diagonal**; true incidents (crashes/construction) require paid enterprise license.
    This tool returns congestion evaluation for the **city center / central business area**, not the whole city.

    Args:
        city: City name (e.g., "北京", "上海", "广州", "深圳").
    """
    # Major central regions (rectangle diagonal ≤10km)
    city_rectangles = {
        "北京": "116.38,39.90;116.42,39.93",
        "上海": "121.45,31.20;121.49,31.23",
        "广州": "113.28,23.10;113.32,23.13",
        "深圳": "114.08,22.52;114.12,22.55"
    }

    rectangle = city_rectangles.get(city)
    if not rectangle:
        return {
            "status": "error",
            "message": f"暂不支持 {city} 的核心区域路况查询，请尝试查询具体地点周边路况。"
        }

    result = await amap_request(
        "traffic/status/rectangle",
        {"rectangle": rectangle, "level": 5}
    )

    return _parse_traffic_evaluation(result, context_name=f"{city}核心区域")


def _parse_traffic_evaluation(traffic_result: Dict, context_name: str = "") -> Dict[str, Any]:
    """Helper to parse Amap traffic evaluation data."""
    if traffic_result.get("status") != "1":
        return {
            "status": "error",
            "message": traffic_result.get("info", "路况API调用失败"),
            "infocode": traffic_result.get("infocode")
        }

    ti = traffic_result.get("trafficinfo", {})
    eval_data = ti.get("evaluation", {})
    
    if not eval_data:
        return {"status": "success", "context_name": context_name, "message": "该区域当前无拥堵数据，路况良好。"}

    status_map = {"0": "未知", "1": "畅通", "2": "缓行", "3": "拥堵", "4": "严重拥堵"}
    
    return {
        "status": "success",
        "context_name": context_name,
        "traffic_status": status_map.get(str(eval_data.get("status", "1")), "畅通"),
        "description": eval_data.get("description", ""),
        "expedite_ratio": eval_data.get("expedite"),  # 畅通比例
        "congested_ratio": eval_data.get("congested"),# 拥堵比例
        "blocked_ratio": eval_data.get("blocked")     # 严重拥堵比例
    }

@mcp.tool()
async def open_nav() -> Dict[str, Any]:
    """打开导航 - Open the navigation app"""
    return {
        "status": "success",
        "action": "open_nav",
        "message": "导航已打开"
    }


@mcp.tool()
async def close_nav() -> Dict[str, Any]:
    """关闭导航 - Close navigation"""
    return {
        "status": "success",
        "action": "close_nav",
        "message": "导航已关闭"
    }


@mcp.tool()
async def go_home() -> Dict[str, Any]:
    """导航回家 - Navigate to saved home address
    
    Gets the saved home location from database and calculates navigation route.
    """
    vehicle_id = None
    current_loc = await get_current_vehicle_location(vehicle_id)
    
    if current_loc == "no_id":
        return {"status": "error", "message": "无法获取车辆标识"}
    if current_loc == "no_location":
        return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启"}
    
    await _ensure_stores_initialized()
    home, err_msg = await _frequent_store.get(vehicle_id, "home")
    if err_msg:
        return {"status": "error", "message": f"查询失败: {err_msg}"}
    if not home:
        return {"status": "error", "message": "尚未设置家地址，请先设置"}
    
    home_lng = home.get("longitude")
    home_lat = home.get("latitude")
    if not home_lng or not home_lat:
        return {"status": "error", "message": "家地址缺少坐标信息，请重新设置"}
    
    # Get driving route
    route_result = await amap_request(
        "direction/driving",
        {"origin": current_loc, "destination": f"{home_lng},{home_lat}", "strategy": 0}
    )
    
    if route_result.get("status") != "1" or not route_result.get("route"):
        return {
            "status": "error",
            "action": "go_home",
            "destination": home.get("name", "家"),
            "destination_address": home.get("address"),
            "message": "路线规划失败，请检查网络或稍后重试"
        }
    
    route = route_result["route"]
    paths = route.get("paths", [])
    if paths:
        path = paths[0]
        return {
            "status": "success",
            "action": "go_home",
            "destination": home.get("name", "家"),
            "destination_address": home.get("address"),
            "distance": path.get("distance", ""),
            "duration": path.get("duration", ""),
            "strategy": "速度优先",
            "message": f"正在导航回家，距离{path.get('distance', '')}，预计{path.get('duration', '')}"
        }
    
    return {
        "status": "success",
        "action": "go_home",
        "destination": home.get("name", "家"),
        "destination_address": home.get("address"),
        "message": "正在导航回家"
    }


@mcp.tool()
async def go_company() -> Dict[str, Any]:
    """导航到公司 - Navigate to saved company address
    
    Gets the saved company location from database and calculates navigation route.
    """
    vehicle_id = None
    current_loc = await get_current_vehicle_location(vehicle_id)
    
    if current_loc == "no_id":
        return {"status": "error", "message": "无法获取车辆标识"}
    if current_loc == "no_location":
        return {"status": "error", "message": "无法获取当前位置，请确保GPS已开启"}
    
    await _ensure_stores_initialized()
    company, err_msg = await _frequent_store.get(vehicle_id, "company")
    if err_msg:
        return {"status": "error", "message": f"查询失败: {err_msg}"}
    if not company:
        return {"status": "error", "message": "尚未设置公司地址，请先设置"}
    
    company_lng = company.get("longitude")
    company_lat = company.get("latitude")
    if not company_lng or not company_lat:
        return {"status": "error", "message": "公司地址缺少坐标信息，请重新设置"}
    
    # Get driving route
    route_result = await amap_request(
        "direction/driving",
        {"origin": current_loc, "destination": f"{company_lng},{company_lat}", "strategy": 0}
    )
    
    if route_result.get("status") != "1" or not route_result.get("route"):
        return {
            "status": "error",
            "action": "go_company",
            "destination": company.get("name", "公司"),
            "destination_address": company.get("address"),
            "message": "路线规划失败，请检查网络或稍后重试"
        }
    
    route = route_result["route"]
    paths = route.get("paths", [])
    if paths:
        path = paths[0]
        return {
            "status": "success",
            "action": "go_company",
            "destination": company.get("name", "公司"),
            "destination_address": company.get("address"),
            "distance": path.get("distance", ""),
            "duration": path.get("duration", ""),
            "strategy": "速度优先",
            "message": f"正在导航到公司，距离{path.get('distance', '')}，预计{path.get('duration', '')}"
        }
    
    return {
        "status": "success",
        "action": "go_company",
        "destination": company.get("name", "公司"),
        "destination_address": company.get("address"),
        "message": "正在导航到公司"
    }

@mcp.tool()
async def add_via(poi: str, via_index: int = 1) -> Dict[str, Any]:
    """添加途经点 - Add waypoint to route"""
    return {"status": "error", "message": f"未找到途经点: {poi}"}


@mcp.tool()
async def delete_via() -> Dict[str, Any]:
    """删除途经点 - Remove waypoint"""
    return {
        "status": "success",
        "action": "delete_via",
        "message": "已删除途经点"
    }


@mcp.tool()
async def flush_route() -> Dict[str, Any]:
    """重新算路 - Recalculate route"""
    return {
        "status": "success",
        "action": "flush_route",
        "message": "路线已重新规划"
    }


@mcp.tool()
async def change_route() -> Dict[str, Any]:
    """切换路线 - Switch to alternate route"""
    return {
        "status": "success",
        "action": "change_route",
        "message": "已切换到备选路线"
    }


@mcp.tool()
async def get_route_information() -> Dict[str, Any]:
    """打开路线信息 - Get detailed route info"""
    return {"status": "info", "message": "请开始导航后查看路线详情"}


@mcp.tool()
async def open_full_map() -> Dict[str, Any]:
    """打开路线全览 - Show full route overview"""
    return {
        "status": "success",
        "action": "open_full_map",
        "message": "路线全览已打开"
    }


@mcp.tool()
async def close_full_map() -> Dict[str, Any]:
    """关闭路线全览 - Hide route overview"""
    return {
        "status": "success",
        "action": "close_full_map",
        "message": "路线全览已关闭"
    }


#  Route Preferences 

@mcp.tool()
async def switch_main_route() -> Dict[str, Any]:
    """切换到主路 - Prefer main road"""
    return {
        "status": "success",
        "action": "switch_main_route",
        "message": "已切换到主路优先"
    }


@mcp.tool()
async def switch_side_route() -> Dict[str, Any]:
    """切换到辅路 - Prefer side road"""
    return {
        "status": "success",
        "action": "switch_side_route",
        "message": "已切换到辅路优先"
    }


@mcp.tool()
async def speed_fast() -> Dict[str, Any]:
    """打开速度最快 - Enable fastest route mode"""
    return {
        "status": "success",
        "action": "speed_fast",
        "message": "已开启速度最快模式"
    }


@mcp.tool()
async def cancel_speed_fast() -> Dict[str, Any]:
    """关闭速度最快 - Disable fastest route"""
    return {
        "status": "success",
        "action": "cancel_speed_fast",
        "message": "已关闭速度最快模式"
    }


@mcp.tool()
async def highway_first() -> Dict[str, Any]:
    """打开高速优先 - Prefer highways"""
    return {
        "status": "success",
        "action": "highway_first",
        "message": "已开启高速优先"
    }


@mcp.tool()
async def smart_recommend() -> Dict[str, Any]:
    """打开智能路线推荐 - Enable smart route recommendation"""
    return {
        "status": "success",
        "action": "smart_recommend",
        "message": "已开启智能路线推荐"
    }


@mcp.tool()
async def cancel_smart_recommend() -> Dict[str, Any]:
    """取消智能路线推荐 - Disable smart recommendation"""
    return {
        "status": "success",
        "action": "cancel_smart_recommend",
        "message": "已关闭智能路线推荐"
    }


@mcp.tool()
async def main_route_first() -> Dict[str, Any]:
    """打开大路优先 - Prefer main roads"""
    return {
        "status": "success",
        "action": "main_route_first",
        "message": "已开启大路优先"
    }


@mcp.tool()
async def cancel_main_first() -> Dict[str, Any]:
    """关闭大路优先 - Cancel main road preference"""
    return {
        "status": "success",
        "action": "cancel_main_first",
        "message": "已关闭大路优先"
    }


#  Traffic Avoidance 

@mcp.tool()
async def avoid_congestion() -> Dict[str, Any]:
    """打开躲避拥堵 - Enable congestion avoidance"""
    return {
        "status": "success",
        "action": "avoid_congestion",
        "message": "已开启躲避拥堵"
    }


@mcp.tool()
async def cancel_avoid_congestion() -> Dict[str, Any]:
    """关闭躲避拥堵 - Disable congestion avoidance"""
    return {
        "status": "success",
        "action": "cancel_avoid_congestion",
        "message": "已关闭躲避拥堵"
    }


@mcp.tool()
async def avoid_high_way() -> Dict[str, Any]:
    """打开不走高速 - Avoid highways"""
    return {
        "status": "success",
        "action": "avoid_high_way",
        "message": "已开启不走高速模式"
    }


@mcp.tool()
async def cancel_avoid_high_way() -> Dict[str, Any]:
    """关闭不走高速 - Cancel avoid highway"""
    return {
        "status": "success",
        "action": "cancel_avoid_high_way",
        "message": "已关闭不走高速模式"
    }


@mcp.tool()
async def avoid_limit_line() -> Dict[str, Any]:
    """打开避开限行 - Avoid restricted zones"""
    return {
        "status": "success",
        "action": "avoid_limit_line",
        "message": "已开启避开限行"
    }


@mcp.tool()
async def cancel_avoid_limit_line() -> Dict[str, Any]:
    """关闭避开限行 - Cancel avoid restricted zones"""
    return {
        "status": "success",
        "action": "cancel_avoid_limit_line",
        "message": "已关闭避开限行"
    }


@mcp.tool()
async def open_avoid_fee() -> Dict[str, Any]:
    """打开避免收费 - Enable toll avoidance"""
    return {
        "status": "success",
        "action": "open_avoid_fee",
        "message": "已开启避免收费"
    }


@mcp.tool()
async def cancel_avoid_fee() -> Dict[str, Any]:
    """关闭避免收费 - Disable toll avoidance"""
    return {
        "status": "success",
        "action": "cancel_avoid_fee",
        "message": "已关闭避免收费"
    }


#  Traffic Information 

@mcp.tool()
async def home_condition() -> Dict[str, Any]:
    """家路况 - Check traffic on route home"""
    return {"status": "info", "message": "请先设置家地址后查询路况"}


@mcp.tool()
async def company_condition() -> Dict[str, Any]:
    """公司路况 - Check traffic on route to company"""
    return {"status": "info", "message": "请先设置公司地址后查询路况"}


@mcp.tool()
async def open_electronic_eye() -> Dict[str, Any]:
    """打开电子眼 - Show speed cameras"""
    return {
        "status": "success",
        "action": "open_electronic_eye",
        "message": "电子眼已开启"
    }


@mcp.tool()
async def close_electronic_eye() -> Dict[str, Any]:
    """关闭电子眼 - Hide speed cameras"""
    return {
        "status": "success",
        "action": "close_electronic_eye",
        "message": "电子眼已关闭"
    }


@mcp.tool()
async def open_cruise_information() -> Dict[str, Any]:
    """打开路况信息 - Enable traffic info overlay"""
    return {
        "status": "success",
        "action": "open_cruise_information",
        "message": "路况信息已开启"
    }


@mcp.tool()
async def close_cruise_information() -> Dict[str, Any]:
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
async def close_nav_collections() -> Dict[str, Any]:
    """关闭导航收藏夹 - Close saved locations"""
    return {
        "status": "success",
        "action": "close_nav_collections",
        "message": "收藏夹已关闭"
    }


@mcp.tool()
async def nav_to_collection() -> Dict[str, Any]:
    """去收藏地址 - Navigate to saved location"""
    return {
        "status": "info",
        "action": "nav_to_collection",
        "message": "请选择要导航的收藏地址"
    }


@mcp.tool()
async def collect_target_location() -> Dict[str, Any]:
    """收藏目的地 - Save destination"""
    return {
        "status": "info",
        "action": "collect_target_location",
        "message": "请先开始导航再收藏目的地"
    }


@mcp.tool()
async def open_map_setting() -> Dict[str, Any]:
    """打开地图设置 - Open map settings"""
    return {
        "status": "success",
        "action": "open_map_setting",
        "message": "地图设置已打开"
    }


@mcp.tool()
async def close_map_setting() -> Dict[str, Any]:
    """关闭地图设置 - Close map settings"""
    return {
        "status": "success",
        "action": "close_map_setting",
        "message": "地图设置已关闭"
    }


@mcp.tool()
async def change_nav_sign() -> Dict[str, Any]:
    """切换导航标志 - Change navigation sign style"""
    return {
        "status": "success",
        "action": "change_nav_sign",
        "message": "已切换导航标志样式"
    }


#  Group Travel 

@mcp.tool()
async def join_group() -> Dict[str, Any]:
    """加入组队 - Join a travel group"""
    return {
        "status": "info",
        "action": "join_group",
        "message": "请提供组队邀请码"
    }


@mcp.tool()
async def build_group() -> Dict[str, Any]:
    """创建组队 - Create a new group"""
    return {
        "status": "success",
        "action": "build_group",
        "message": "车队已创建",
        "invite_code": "ABC123"
    }


@mcp.tool()
async def quit_group() -> Dict[str, Any]:
    """退出组队 - Leave current group"""
    return {
        "status": "success",
        "action": "quit_group",
        "message": "已退出车队"
    }


@mcp.tool()
async def open_group() -> Dict[str, Any]:
    """打开组队 - Open group travel interface"""
    return {
        "status": "success",
        "action": "open_group",
        "message": "组队界面已打开"
    }


@mcp.tool()
async def ask_meeting_place() -> Dict[str, Any]:
    """设置集结地 - Query group meetup location"""
    return {
        "status": "info",
        "action": "ask_meeting_place",
        "message": "请设置集结地点"
    }


@mcp.tool()
async def go_meeting_place() -> Dict[str, Any]:
    """去汇合地点 - Navigate to meetup point"""
    return {
        "status": "success",
        "action": "go_meeting_place",
        "message": "正在导航到汇合地点"
    }


@mcp.tool()
async def group_member_location() -> Dict[str, Any]:
    """查看成员位置 - View locations of group members"""
    return {
        "status": "success",
        "members": [
            {"name": "张三", "distance": "3公里", "direction": "前方"},
            {"name": "李四", "distance": "5公里", "direction": "左后方"}
        ]
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")