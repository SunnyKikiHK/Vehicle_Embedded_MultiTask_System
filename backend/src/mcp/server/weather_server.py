#!/usr/bin/env python
"""Weather Server - MCP Implementation for Weather & Life Information

This server handles weather queries, life advisory, fuel prices, and license plate restrictions.
"""
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_server")


@mcp.tool()
def get_weather(location: Optional[str] = None, date: Optional[str] = None,
                advisory: Optional[str] = None, type: Optional[str] = None) -> Dict[str, Any]:
    """获取天气 - Get weather, advisories, or date/time info"""
    
    # Date/time queries
    if type == "weekday":
        return {
            "status": "success",
            "type": "weekday",
            "weekday": "星期日",
            "message": "今天是星期日"
        }
    elif type == "date":
        return {
            "status": "success",
            "type": "date",
            "date": "2026-05-03",
            "message": "今天是2026年5月3日"
        }
    elif type == "oil_price":
        return {
            "status": "success",
            "type": "oil_price",
            "price_92": 7.85,
            "price_95": 8.35,
            "price_0": 7.55,
            "message": "今日油价：92号7.85元/升，95号8.35元/升"
        }
    elif type == "restriction":
        return {
            "status": "success",
            "type": "restriction",
            "city": location,
            "plate": date,
            "restricted": False,
            "message": "明天不限行"
        }
    elif type == "restriction_check":
        return {
            "status": "success",
            "type": "restriction_check",
            "restricted": False,
            "message": "今日不限行"
        }
    elif type == "air_quality":
        return {
            "status": "success",
            "type": "air_quality",
            "location": location or "北京",
            "aqi": 68,
            "grade": "良",
            "pm25": 45,
            "pm10": 78,
            "message": "当前空气质量为良，PM2.5指数为45"
        }
    elif type == "humidity":
        return {
            "status": "success",
            "type": "humidity",
            "location": location or "北京",
            "humidity": 55,
            "feeling": "舒适",
            "message": "当前相对湿度为55%，体感舒适"
        }
    elif type == "data_remaining":
        return {
            "status": "success",
            "type": "data_remaining",
            "remaining": 3.5,
            "unit": "GB",
            "expires": "15天后",
            "message": "本月还有3.5GB流量"
        }
    
    # Weather advisories
    if advisory == "clothing":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "clothing",
            "location": location or "当前地区",
            "temperature": 25,
            "advice": "建议穿薄外套，早晚温差大，可以带件披肩",
            "message": "25度，建议穿薄外套"
        }
    elif advisory == "car_wash":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "car_wash",
            "location": location or "当前地区",
            "suitable": True,
            "reason": "明天预报晴朗，适合洗车",
            "message": "明天适合洗车，天气晴朗"
        }
    elif advisory == "uv_index":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "uv_index",
            "location": location or "当前地区",
            "uv_index": 6,
            "level": "较强",
            "advice": "建议涂抹防晒霜",
            "message": "紫外线指数为6，属于较强"
        }
    elif advisory == "allergy":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "allergy",
            "location": location or "当前地区",
            "risk": "较高",
            "reason": "花粉浓度较高",
            "advice": "建议戴口罩",
            "message": "今天花粉浓度较高，建议戴口罩"
        }
    elif advisory == "fishing":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "fishing",
            "location": location or "当前地区",
            "suitable": True,
            "reason": "天气晴朗，微风",
            "message": "今天适合钓鱼"
        }
    elif advisory == "sport":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "sport",
            "location": location or "当前地区",
            "suitable": True,
            "reason": "温度适宜",
            "message": "今天适合户外运动"
        }
    elif advisory == "travel":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "travel",
            "location": location or "当前地区",
            "suitable": True,
            "message": "今天适合出行"
        }
    elif advisory == "transport":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "transport",
            "location": location or "当前地区",
            "message": "交通状况良好"
        }
    elif advisory == "feels_like":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "feels_like",
            "location": location or "当前地区",
            "temperature": 25,
            "feels_like": 27,
            "message": "体感温度为27度"
        }
    elif advisory == "cold_index":
        return {
            "status": "success",
            "type": "weather",
            "advisory": "cold_index",
            "location": location or "当前地区",
            "risk": "低",
            "message": "感冒风险较低"
        }
    
    # Default weather query
    return {
        "status": "success",
        "type": "weather",
        "location": location or "北京",
        "weather": "晴",
        "temperature": 25,
        "feels_like": 27,
        "wind": "东南风3级",
        "humidity": "55%",
        "message": f"{location or '北京'}今天晴，25度"
    }


@mcp.tool()
def get_forecast(location: Optional[str] = None, date: Optional[str] = None) -> Dict[str, Any]:
    """获取天气预报 - Get weather forecast"""
    forecasts = [
        {"date": "今天", "weather": "晴", "temperature_high": 28, "temperature_low": 18},
        {"date": "明天", "weather": "多云", "temperature_high": 26, "temperature_low": 17},
        {"date": "后天", "weather": "小雨", "temperature_high": 22, "temperature_low": 15},
    ]
    return {
        "status": "success",
        "type": "forecast",
        "location": location or "北京",
        "forecasts": forecasts,
        "message": f"{location or '北京'}未来三天预报已加载"
    }


@mcp.tool()
def weather_alert(location: Optional[str] = None) -> Dict[str, Any]:
    """获取天气预警 - Get weather alerts"""
    return {
        "status": "success",
        "type": "alert",
        "location": location or "当前地区",
        "alerts": [],
        "message": "当前无天气预警"
    }


if __name__ == "__main__":
    mcp.run()
