"""Tests for Navigation Server MCP - Amap API Integration Tests

Tests all navigation tools that interact with the Amap API.
Tests verify that functions return valid responses without checking specific values.
"""
import os
import sys
import logging
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.constants import NAV_TEST_LOG_PATH

from src.mcp.server.nav_server import (
    mcp,
    go_poi,
    set_frequent_location,
    collect_location,
    ask_where_am_i,
    check_area_traffic,
    check_route_traffic,
    check_city_traffic_overview,
    open_nav,
    close_nav,
    go_home,
    go_company,
    add_via,
    delete_via,
    flush_route,
    change_route,
    get_route_information,
    open_full_map,
    close_full_map,
    switch_main_route,
    switch_side_route,
    speed_fast,
    cancel_speed_fast,
    highway_first,
    smart_recommend,
    cancel_smart_recommend,
    main_route_first,
    cancel_main_first,
    avoid_congestion,
    cancel_avoid_congestion,
    avoid_high_way,
    cancel_avoid_high_way,
    avoid_limit_line,
    cancel_avoid_limit_line,
    open_avoid_fee,
    cancel_avoid_fee,
    home_condition,
    company_condition,
    open_electronic_eye,
    close_electronic_eye,
    open_cruise_information,
    close_cruise_information,
    open_ar_nav,
    close_ar_nav,
    front_line_detail,
    open_nav_broadcast,
    close_nav_broadcast,
    replay_broadcast,
    slow_broadcast_speed,
    accelerate_broadcast_speed,
    open_simple_broadcast,
    close_simple_broadcast,
    open_commute_nav,
    close_commute_nav,
    open_nav_collections,
    close_nav_collections,
    nav_to_collection,
    collect_target_location,
    open_map_setting,
    close_map_setting,
    change_nav_sign,
    join_group,
    build_group,
    quit_group,
    open_group,
    ask_meeting_place,
    go_meeting_place,
    group_member_location,
)

# Configure test logger
test_logger = logging.getLogger("nav_test")
test_logger.setLevel(logging.INFO)
test_logger.handlers.clear()

file_handler = logging.FileHandler(NAV_TEST_LOG_PATH, mode='a')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
))

test_logger.addHandler(file_handler)
test_logger.addHandler(console_handler)

test_logger.info("=" * 70)
test_logger.info(f"AMap Test Suite Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
test_logger.info("=" * 70)

os.environ["AMAP_API_KEY"] = "test_api_key_12345"
os.environ["AMAP_BASE_URL"] = "https://restapi.amap.com/v3"
os.environ["VEHICLE_GPS"] = "116.473168,39.993015"


# Test Fixtures - Based on actual Amap API response format

@pytest.fixture
def mock_poi_search_result():
    """Mock POI search result - matches actual Amap place/text API response.
    
    Key fields:
    - status: "1" = success
    - count: string number
    - pois: array with location, name, address, etc.
    - Note: distance can be [] (empty array) or a string
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "count": "1",
        "pois": [
            {
                "id": "B001234567",
                "name": "测试地点",
                "type": "地名地址信息;普通地名;地标",
                "typecode": "190102",
                "location": "116.397128,39.916527",
                "address": "北京市东城区测试路1号",
                "tel": [],
                "pname": "北京市",
                "cityname": "北京市",
                "adname": "东城区",
                "biz_type": [],
                "distance": "500",
                "biz_ext": {
                    "rating": [],
                    "cost": [],
                    "open_time": []
                }
            }
        ]
    }


@pytest.fixture
def mock_poi_search_result_empty_distance():
    """Mock POI search result with empty distance array (actual API format).
    
    Actual Amap API returns distance as [] when not available.
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "count": "1",
        "pois": [
            {
                "id": "B001234567",
                "name": "测试地点",
                "type": "地名地址信息;普通地名;地标",
                "typecode": "190102",
                "location": "116.397128,39.916527",
                "address": "北京市东城区测试路1号",
                "tel": [],
                "pname": "北京市",
                "cityname": "北京市",
                "adname": "东城区",
                "biz_type": [],
                "distance": [],
                "biz_ext": {
                    "rating": [],
                    "cost": [],
                    "open_time": []
                }
            }
        ]
    }


@pytest.fixture
def mock_regeo_result():
    """Mock reverse geocoding result - matches actual Amap geocode/regeo API.
    
    Key fields:
    - regeocode.formatted_address: full address string
    - regeocode.addressComponent: province, city, district, etc.
    - Note: city can be [] (empty array) for direct municipality cities like Beijing
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "regeocode": {
            "formatted_address": "北京市朝阳区望京街道方恒国际中心A座",
            "addressComponent": {
                "province": "北京市",
                "city": [],
                "citycode": "010",
                "adcode": "110105",
                "district": "朝阳区",
                "township": "望京街道",
                "streetNumber": {
                    "street": "阜荣街",
                    "number": "6号",
                    "location": "116.480852,39.989477",
                    "direction": "西北",
                    "distance": "7.84801"
                }
            }
        }
    }


@pytest.fixture
def mock_regeo_result_with_city():
    """Mock reverse geocoding result for non-municipality cities.
    
    For cities outside direct municipalities, city is a string array.
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "regeocode": {
            "formatted_address": "上海市浦东新区陆家嘴街道",
            "addressComponent": {
                "province": "上海市",
                "city": ["上海市"],
                "citycode": "021",
                "adcode": "310115",
                "district": "浦东新区",
                "township": "陆家嘴街道"
            }
        }
    }


@pytest.fixture
def mock_traffic_circle_result():
    """Mock traffic circle result - matches actual Amap traffic/status/circle API.
    
    Key fields:
    - trafficinfo.evaluation.expedite/congested/blocked: percentage strings like "86.96%"
    - trafficinfo.evaluation.status: "0"=未知, "1"=畅通, "2"=缓行, "3"=拥堵, "4"=严重拥堵
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "trafficinfo": {
            "description": "该区域道路基本畅通",
            "evaluation": {
                "expedite": "86.96%",
                "congested": "10.87%",
                "blocked": "2.17%",
                "unknown": "0.00%",
                "status": "2",
                "description": "轻度拥堵"
            }
        }
    }


@pytest.fixture
def mock_traffic_rectangle_result():
    """Mock traffic rectangle result - matches actual Amap traffic/status/rectangle API.
    
    Same structure as circle, used for city-wide traffic.
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "trafficinfo": {
            "description": "该区域道路畅通",
            "evaluation": {
                "expedite": "76.52%",
                "congested": "10.61%",
                "blocked": "9.85%",
                "unknown": "3.02%",
                "status": "1",
                "description": "畅通"
            }
        }
    }


@pytest.fixture
def mock_driving_route_result():
    """Mock driving route result - matches actual Amap direction/driving API.
    
    Key fields:
    - route.origin/destination: coordinates
    - route.paths[0].distance: meters (string)
    - route.paths[0].duration: seconds (string)
    - route.paths[0].traffic_lights: count (string)
    - route.paths[0].strategy: routing strategy name
    """
    return {
        "status": "1",
        "info": "OK",
        "infocode": "10000",
        "count": "1",
        "route": {
            "origin": "116.473168,39.993015",
            "destination": "116.481028,39.989049",
            "taxi_cost": "13",
            "paths": [
                {
                    "distance": "1484",
                    "duration": "467",
                    "strategy": "速度最快",
                    "tolls": "0",
                    "toll_distance": "0",
                    "restriction": "0",
                    "traffic_lights": "4",
                    "steps": [
                        {
                            "instruction": "向西北行驶30米左转",
                            "orientation": "西北",
                            "distance": "30",
                            "tolls": "0",
                            "duration": "16",
                            "polyline": "116.473221,39.993062;116.473214,39.993066;116.472957,39.993243",
                            "action": "左转",
                            "tmcs": [
                                {
                                    "lcode": [],
                                    "distance": "1",
                                    "status": "未知",
                                    "polyline": "116.473221,39.993062;116.473214,39.993066"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }



# POI Search Tests


class TestGoPoi:
    """Tests for go_poi."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_city_search(self, mock_request, mock_poi_search_result):
        """Test city-level POI search returns valid response."""
        mock_request.return_value = mock_poi_search_result
        result = go_poi(poi="测试地点", search_mode="city", city="北京")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_nearby_search(self, mock_request, mock_poi_search_result):
        """Test nearby POI search returns valid response."""
        mock_request.return_value = mock_poi_search_result
        result = go_poi(poi="加油站", search_mode="nearby")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_search_with_type(self, mock_request, mock_poi_search_result):
        """Test POI search with type filter."""
        mock_request.return_value = mock_poi_search_result
        result = go_poi(poi="充电", search_mode="nearby", poi_type="充电桩")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_search_not_found(self, mock_request):
        """Test POI search when not found."""
        mock_request.return_value = {"status": "1", "pois": []}
        result = go_poi(poi="不存在的地点", search_mode="city", city="北京")
        assert result is not None
        assert result.get("status") == "fail"

    @patch("src.mcp.server.nav_server.amap_request")
    def test_search_empty_distance(self, mock_request, mock_poi_search_result_empty_distance):
        """Test POI search with empty distance array (actual API format)."""
        mock_request.return_value = mock_poi_search_result_empty_distance
        result = go_poi(poi="测试", search_mode="city", city="北京")
        assert result is not None
        assert "status" in result



# Frequent Location Tests


class TestSetFrequentLocation:
    """Tests for set_frequent_location."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_set_home_with_poi(self, mock_request, mock_poi_search_result):
        """Test setting home with POI."""
        mock_request.return_value = mock_poi_search_result
        result = set_frequent_location(location_type="home", poi="望京SOHO")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_set_company_with_poi(self, mock_request, mock_poi_search_result):
        """Test setting company with POI."""
        mock_request.return_value = mock_poi_search_result
        result = set_frequent_location(location_type="company", poi="国贸大厦")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_set_home_with_gps(self, mock_request, mock_regeo_result):
        """Test setting home with current GPS."""
        mock_request.return_value = mock_regeo_result
        result = set_frequent_location(location_type="home")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_set_company_with_gps(self, mock_request, mock_regeo_result):
        """Test setting company with current GPS."""
        mock_request.return_value = mock_regeo_result
        result = set_frequent_location(location_type="company")
        assert result is not None
        assert "status" in result

    def test_invalid_location_type(self):
        """Test invalid location type."""
        result = set_frequent_location(location_type="invalid")
        assert result is not None
        assert result.get("status") == "fail"



# Location Collection Tests - Signature: collect_location(poi)


class TestCollectLocation:
    """Tests for collect_location."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_collect_with_poi(self, mock_request, mock_poi_search_result):
        """Test collecting location with POI name."""
        mock_request.return_value = mock_poi_search_result
        result = collect_location(poi="望京SOHO")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_collect_with_current_gps(self, mock_request, mock_regeo_result):
        """Test collecting current GPS location."""
        mock_request.return_value = mock_regeo_result
        result = collect_location()
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_collect_poi_not_found(self, mock_request):
        """Test collecting when POI not found."""
        mock_request.return_value = {"status": "1", "pois": []}
        result = collect_location(poi="不存在的地点")
        assert result is not None
        assert result.get("status") == "fail"



# Current Location Tests


class TestAskWhereAmI:
    """Tests for ask_where_am_i."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_get_current_location(self, mock_request, mock_regeo_result):
        """Test getting current location."""
        mock_request.return_value = mock_regeo_result
        result = ask_where_am_i()
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_location_with_city_array(self, mock_request, mock_regeo_result_with_city):
        """Test location with city as array (non-municipality cities)."""
        mock_request.return_value = mock_regeo_result_with_city
        result = ask_where_am_i()
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_location_failure(self, mock_request):
        """Test location failure."""
        mock_request.return_value = {"status": "0"}
        result = ask_where_am_i()
        assert result is not None
        assert result.get("status") == "fail"



# Traffic Area Tests


class TestCheckAreaTraffic:
    """Tests for check_area_traffic."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_area_traffic_with_poi(self, mock_request, mock_traffic_circle_result, mock_poi_search_result):
        """Test traffic around POI."""
        mock_request.side_effect = [mock_poi_search_result, mock_traffic_circle_result]
        result = check_area_traffic(poi="故宫", radius=1000)
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_area_traffic_around_me(self, mock_request, mock_traffic_circle_result):
        """Test traffic around current location."""
        mock_request.return_value = mock_traffic_circle_result
        result = check_area_traffic(radius=500)
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_area_traffic_poi_not_found(self, mock_request):
        """Test traffic when POI not found."""
        mock_request.return_value = {"status": "1", "pois": []}
        result = check_area_traffic(poi="不存在的地点")
        assert result is not None
        assert result.get("status") == "error"



# Route Traffic Tests - destination is required


class TestCheckRouteTraffic:
    """Tests for check_route_traffic."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_route_traffic_with_destination(self, mock_request, mock_driving_route_result, mock_poi_search_result):
        """Test route traffic with destination."""
        mock_request.side_effect = [mock_poi_search_result, mock_driving_route_result]
        result = check_route_traffic(destination="天安门广场")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_route_traffic_with_origin_and_destination(self, mock_request, mock_driving_route_result, mock_poi_search_result):
        """Test route traffic with origin and destination."""
        mock_request.side_effect = [mock_poi_search_result, mock_poi_search_result, mock_driving_route_result]
        result = check_route_traffic(destination="天安门广场", origin="望京SOHO")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_route_traffic_no_destination(self, mock_request):
        """Test route traffic without destination."""
        result = check_route_traffic(destination="")
        assert result is not None
        assert result.get("status") == "error"

    @patch("src.mcp.server.nav_server.amap_request")
    def test_route_traffic_destination_not_found(self, mock_request):
        """Test route when destination not found."""
        mock_request.return_value = {"status": "1", "pois": []}
        result = check_route_traffic(destination="不存在的地点")
        assert result is not None
        assert result.get("status") == "error"



# City Traffic Overview Tests


class TestCheckCityTrafficOverview:
    """Tests for check_city_traffic_overview."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_beijing_traffic(self, mock_request, mock_traffic_rectangle_result):
        """Test Beijing traffic."""
        mock_request.return_value = mock_traffic_rectangle_result
        result = check_city_traffic_overview(city="北京")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_shanghai_traffic(self, mock_request, mock_traffic_rectangle_result):
        """Test Shanghai traffic."""
        mock_request.return_value = mock_traffic_rectangle_result
        result = check_city_traffic_overview(city="上海")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_guangzhou_traffic(self, mock_request, mock_traffic_rectangle_result):
        """Test Guangzhou traffic."""
        mock_request.return_value = mock_traffic_rectangle_result
        result = check_city_traffic_overview(city="广州")
        assert result is not None
        assert "status" in result

    @patch("src.mcp.server.nav_server.amap_request")
    def test_shenzhen_traffic(self, mock_request, mock_traffic_rectangle_result):
        """Test Shenzhen traffic."""
        mock_request.return_value = mock_traffic_rectangle_result
        result = check_city_traffic_overview(city="深圳")
        assert result is not None
        assert "status" in result

    def test_unsupported_city(self):
        """Test unsupported city."""
        result = check_city_traffic_overview(city="不支持的城市")
        assert result is not None
        assert result.get("status") == "error"



# Navigation Control Tests


class TestNavigationControl:
    """Tests for navigation control tools."""

    def test_open_nav(self):
        result = open_nav()
        assert result is not None
        assert "status" in result

    def test_close_nav(self):
        result = close_nav()
        assert result is not None
        assert "status" in result

    def test_go_home(self):
        result = go_home()
        assert result is not None
        assert "status" in result

    def test_go_company(self):
        result = go_company()
        assert result is not None
        assert "status" in result

    def test_add_via(self):
        result = add_via(poi="加油站")
        assert result is not None
        assert "status" in result

    def test_delete_via(self):
        result = delete_via()
        assert result is not None
        assert "status" in result

    def test_flush_route(self):
        result = flush_route()
        assert result is not None
        assert "status" in result

    def test_change_route(self):
        result = change_route()
        assert result is not None
        assert "status" in result

    def test_get_route_information(self):
        result = get_route_information()
        assert result is not None
        assert "status" in result

    def test_open_full_map(self):
        result = open_full_map()
        assert result is not None
        assert "status" in result

    def test_close_full_map(self):
        result = close_full_map()
        assert result is not None
        assert "status" in result



# Route Preference Tests


class TestRoutePreferences:
    """Tests for route preference tools."""

    def test_switch_main_route(self):
        result = switch_main_route()
        assert result is not None
        assert "status" in result

    def test_switch_side_route(self):
        result = switch_side_route()
        assert result is not None
        assert "status" in result

    def test_speed_fast(self):
        result = speed_fast()
        assert result is not None
        assert "status" in result

    def test_cancel_speed_fast(self):
        result = cancel_speed_fast()
        assert result is not None
        assert "status" in result

    def test_highway_first(self):
        result = highway_first()
        assert result is not None
        assert "status" in result

    def test_smart_recommend(self):
        result = smart_recommend()
        assert result is not None
        assert "status" in result

    def test_cancel_smart_recommend(self):
        result = cancel_smart_recommend()
        assert result is not None
        assert "status" in result

    def test_main_route_first(self):
        result = main_route_first()
        assert result is not None
        assert "status" in result

    def test_cancel_main_first(self):
        result = cancel_main_first()
        assert result is not None
        assert "status" in result



# Traffic Avoidance Tests


class TestTrafficAvoidance:
    """Tests for traffic avoidance tools."""

    def test_avoid_congestion(self):
        result = avoid_congestion()
        assert result is not None
        assert "status" in result

    def test_cancel_avoid_congestion(self):
        result = cancel_avoid_congestion()
        assert result is not None
        assert "status" in result

    def test_avoid_high_way(self):
        result = avoid_high_way()
        assert result is not None
        assert "status" in result

    def test_cancel_avoid_high_way(self):
        result = cancel_avoid_high_way()
        assert result is not None
        assert "status" in result

    def test_avoid_limit_line(self):
        result = avoid_limit_line()
        assert result is not None
        assert "status" in result

    def test_cancel_avoid_limit_line(self):
        result = cancel_avoid_limit_line()
        assert result is not None
        assert "status" in result

    def test_open_avoid_fee(self):
        result = open_avoid_fee()
        assert result is not None
        assert "status" in result

    def test_cancel_avoid_fee(self):
        result = cancel_avoid_fee()
        assert result is not None
        assert "status" in result



# Traffic Information Tests


class TestTrafficInformation:
    """Tests for traffic information tools."""

    def test_home_condition(self):
        result = home_condition()
        assert result is not None
        assert "status" in result

    def test_company_condition(self):
        result = company_condition()
        assert result is not None
        assert "status" in result

    def test_open_electronic_eye(self):
        result = open_electronic_eye()
        assert result is not None
        assert "status" in result

    def test_close_electronic_eye(self):
        result = close_electronic_eye()
        assert result is not None
        assert "status" in result

    def test_open_cruise_information(self):
        result = open_cruise_information()
        assert result is not None
        assert "status" in result

    def test_close_cruise_information(self):
        result = close_cruise_information()
        assert result is not None
        assert "status" in result



# AR Navigation Tests


class TestARNavigation:
    """Tests for AR navigation tools."""

    def test_open_ar_nav(self):
        result = open_ar_nav()
        assert result is not None
        assert "status" in result

    def test_close_ar_nav(self):
        result = close_ar_nav()
        assert result is not None
        assert "status" in result

    def test_front_line_detail(self):
        result = front_line_detail()
        assert result is not None
        assert "status" in result



# Navigation Broadcast Tests


class TestNavBroadcast:
    """Tests for navigation TTS tools."""

    def test_open_nav_broadcast(self):
        result = open_nav_broadcast()
        assert result is not None
        assert "status" in result

    def test_close_nav_broadcast(self):
        result = close_nav_broadcast()
        assert result is not None
        assert "status" in result

    def test_replay_broadcast(self):
        result = replay_broadcast()
        assert result is not None
        assert "status" in result

    def test_slow_broadcast_speed(self):
        result = slow_broadcast_speed()
        assert result is not None
        assert "status" in result

    def test_accelerate_broadcast_speed(self):
        result = accelerate_broadcast_speed()
        assert result is not None
        assert "status" in result

    def test_open_simple_broadcast(self):
        result = open_simple_broadcast()
        assert result is not None
        assert "status" in result

    def test_close_simple_broadcast(self):
        result = close_simple_broadcast()
        assert result is not None
        assert "status" in result



# Commute Navigation Tests


class TestCommuteNavigation:
    """Tests for commute navigation tools."""

    def test_open_commute_nav(self):
        result = open_commute_nav()
        assert result is not None
        assert "status" in result

    def test_close_commute_nav(self):
        result = close_commute_nav()
        assert result is not None
        assert "status" in result



# Collections Tests


class TestCollections:
    """Tests for collection tools."""

    def test_open_nav_collections(self):
        result = open_nav_collections()
        assert result is not None
        assert "status" in result

    def test_close_nav_collections(self):
        result = close_nav_collections()
        assert result is not None
        assert "status" in result

    def test_nav_to_collection(self):
        result = nav_to_collection()
        assert result is not None
        assert "status" in result

    def test_collect_target_location(self):
        result = collect_target_location()
        assert result is not None
        assert "status" in result



# Map Settings Tests


class TestMapSettings:
    """Tests for map setting tools."""

    def test_open_map_setting(self):
        result = open_map_setting()
        assert result is not None
        assert "status" in result

    def test_close_map_setting(self):
        result = close_map_setting()
        assert result is not None
        assert "status" in result

    def test_change_nav_sign(self):
        result = change_nav_sign()
        assert result is not None
        assert "status" in result



# Group Travel Tests


class TestGroupTravel:
    """Tests for group travel tools."""

    def test_join_group(self):
        result = join_group()
        assert result is not None
        assert "status" in result

    def test_build_group(self):
        result = build_group()
        assert result is not None
        assert "status" in result

    def test_quit_group(self):
        result = quit_group()
        assert result is not None
        assert "status" in result

    def test_open_group(self):
        result = open_group()
        assert result is not None
        assert "status" in result

    def test_ask_meeting_place(self):
        result = ask_meeting_place()
        assert result is not None
        assert "status" in result

    def test_go_meeting_place(self):
        result = go_meeting_place()
        assert result is not None
        assert "status" in result

    def test_group_member_location(self):
        result = group_member_location()
        assert result is not None
        assert "status" in result



# Integration Tests


class TestIntegration:
    """Integration tests for multi-step workflows."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_full_navigation_workflow(self, mock_request, mock_poi_search_result, mock_driving_route_result):
        """Test complete navigation workflow."""
        mock_request.side_effect = [mock_poi_search_result, mock_poi_search_result, mock_driving_route_result]
        
        poi_result = go_poi(poi="天安门", search_mode="city", city="北京")
        assert poi_result is not None
        
        route_result = check_route_traffic(destination="天安门广场")
        assert route_result is not None
        
        nav_result = open_nav()
        assert nav_result is not None

    @patch("src.mcp.server.nav_server.amap_request")
    def test_collect_and_navigate_workflow(self, mock_request, mock_poi_search_result, mock_regeo_result):
        """Test collect location and navigate workflow."""
        mock_request.side_effect = [mock_poi_search_result, mock_regeo_result]
        
        collect_result = collect_location(poi="望京SOHO")
        assert collect_result is not None
        
        location_result = ask_where_am_i()
        assert location_result is not None



# Edge Cases Tests


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @patch("src.mcp.server.nav_server.amap_request")
    def test_api_key_not_configured(self, mock_request):
        """Test behavior when API key not configured."""
        with patch.dict(os.environ, {"AMAP_API_KEY": ""}):
            from src.mcp.server import nav_server
            nav_server.AMAP_API_KEY = None
            result = go_poi(poi="测试", search_mode="city")
            assert result is not None

    @patch("src.mcp.server.nav_server.amap_request")
    def test_empty_response(self, mock_request):
        """Test empty response handling."""
        mock_request.return_value = {}
        result = ask_where_am_i()
        assert result is not None

    def test_vehicle_gps_fallback(self):
        """Test GPS fallback when env not set."""
        with patch.dict(os.environ, {"VEHICLE_GPS": ""}):
            from src.mcp.server import nav_server
            nav_server.AMAP_API_KEY = "test_key"
            nav_server.AMAP_BASE_URL = "https://restapi.amap.com/v3"

            with patch.object(nav_server, "amap_request") as mock_request:
                mock_request.return_value = {
                    "status": "1",
                    "regeocode": {
                        "formatted_address": "北京市朝阳区",
                        "addressComponent": {
                            "province": "北京市",
                            "city": [],
                            "district": "朝阳区"
                        }
                    }
                }
                result = ask_where_am_i()
                assert result is not None
                assert "status" in result


if __name__ == "__main__":
    import datetime

    test_logger.info("=" * 70)
    test_logger.info("Starting AMap Test Suite Execution")
    test_logger.info("=" * 70)

    start_time = datetime.datetime.now()

    class TestResultPlugin:
        def __init__(self):
            self.passed = []
            self.failed = []
            self.skipped = []

        def pytest_runtest_logreport(self, report):
            if report.when == "call":
                test_name = report.nodeid.split("::")[-1]
                class_name = report.nodeid.split("::")[-2] if "::" in report.nodeid else ""
                full_name = f"[{class_name}] {test_name}"

                if report.passed:
                    self.passed.append(full_name)
                elif report.failed:
                    self.failed.append(full_name)
                elif report.skipped:
                    self.skipped.append(full_name)

        def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
            elapsed = datetime.datetime.now() - start_time
            test_logger.info("=" * 70)
            test_logger.info("AMap Test Suite Results Summary")
            test_logger.info("=" * 70)
            test_logger.info(f"Total tests: {len(self.passed) + len(self.failed) + len(self.skipped)}")
            test_logger.info(f"Passed: {len(self.passed)}")
            test_logger.info(f"Failed: {len(self.failed)}")
            test_logger.info(f"Skipped: {len(self.skipped)}")
            test_logger.info(f"Execution time: {elapsed}")

            if self.passed:
                test_logger.info("-" * 50)
                test_logger.info("PASSED:")
                for test in self.passed:
                    test_logger.info(f"  [OK] {test}")

            if self.failed:
                test_logger.error("-" * 50)
                test_logger.error("FAILED:")
                for test in self.failed:
                    test_logger.error(f"  [FAIL] {test}")

            test_logger.info("=" * 70)
            test_logger.info(f"Completed - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            test_logger.info("=" * 70)

    exit_code = pytest.main([__file__, "-v", "--tb=short", "-p", "no:cacheprovider"], plugins=[TestResultPlugin()])
    test_logger.info(f"Pytest exit code: {exit_code}")
    sys.exit(exit_code)
