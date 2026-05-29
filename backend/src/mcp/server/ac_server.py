#!/usr/bin/env python
"""AC Server - MCP Implementation for HVAC (Climate Control)

This server handles air conditioning, heating, defrosting, fan control,
and air quality systems.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ac_server")


#  Power & Mode Control 

@mcp.tool()
def ac_on(mode: Optional[str] = None) -> Dict[str, Any]:
    """打开空调/AC - Turn on AC"""
    if mode == "max_cool":
        return {
            "status": "success",
            "action": "ac_on",
            "mode": "max_cooling",
            "temperature": 16,
            "fan_speed": 7,
            "message": "正在为您快速降温"
        }
    elif mode == "max_heat":
        return {
            "status": "success",
            "action": "ac_on",
            "mode": "max_heating",
            "temperature": 30,
            "fan_speed": 7,
            "message": "正在为您快速升温"
        }
    elif mode == "external":
        return {
            "status": "success",
            "action": "ac_on",
            "mode": "external_circulation",
            "message": "已切换到外循环模式"
        }
    return {
        "status": "success",
        "action": "ac_on",
        "message": "空调已开启"
    }


@mcp.tool()
def ac_off() -> Dict[str, Any]:
    """关闭空调/AC - Turn off AC"""
    return {
        "status": "success",
        "action": "ac_off",
        "message": "空调已关闭"
    }


@mcp.tool()
def ac_auto() -> Dict[str, Any]:
    """空调自动模式 - Enable auto climate control"""
    return {
        "status": "success",
        "action": "ac_auto",
        "mode": "auto",
        "message": "空调已开启自动模式"
    }


@mcp.tool()
def sync_ac(mode: str = "sync") -> Dict[str, Any]:
    """空调同步模式 - Sync/unsyc all zones"""
    if mode == "sync":
        return {
            "status": "success",
            "action": "sync_on",
            "message": "已开启同步模式，所有区域温度一致"
        }
    return {
        "status": "success",
        "action": "sync_off",
        "message": "已关闭同步模式，各区域独立控制"
    }


@mcp.tool()
def set_ac_mode(mode: Optional[str] = None, direction: Optional[str] = None) -> Dict[str, Any]:
    """设置空调模式/风向 - Set AC mode or airflow direction"""
    mode_map = {
        "cooling": "制冷模式",
        "heating": "制热模式",
        "off": "已关闭",
        "auto": "自动模式",
        "fan_only": "送风模式",
        "defog": "除雾模式",
        "defrost": "除霜模式",
    }
    direction_map = {
        "上": "面部出风",
        "下": "脚部出风",
        "前": "前风挡出风",
        "后": "后风挡出风",
        "auto": "自动风向",
        "manual": "手动风向",
    }
    
    message = "空调模式已设置"
    if mode:
        message = f"已切换到{mode_map.get(mode, mode)}"
    if direction:
        message = f"风向已调整为{direction_map.get(direction, direction)}"
    
    return {
        "status": "success",
        "action": "set_mode",
        "mode": mode,
        "direction": direction,
        "message": message
    }


#  Temperature Control 

@mcp.tool()
def set_temperature(temperature: Optional[int] = None, direction: Optional[str] = None) -> Dict[str, Any]:
    """设置温度 - Set temperature or adjust relative"""
    if direction == "up":
        return {
            "status": "success",
            "action": "temp_increase",
            "direction": "up",
            "message": "温度已调高"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "temp_decrease",
            "direction": "down",
            "message": "温度已调低"
        }
    return {
        "status": "success",
        "action": "set_temperature",
        "temperature": temperature or 24,
        "message": f"温度已设置为{temperature or 24}度"
    }


#  Fan Speed Control 

@mcp.tool()
def set_fan_speed(level: Optional[int] = None, direction: Optional[str] = None) -> Dict[str, Any]:
    """设置风力 - Set fan speed or adjust relative"""
    if direction == "up":
        return {
            "status": "success",
            "action": "fan_increase",
            "direction": "up",
            "message": "风力已调高"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "fan_decrease",
            "direction": "down",
            "message": "风力已调低"
        }
    return {
        "status": "success",
        "action": "set_fan_speed",
        "level": level or 3,
        "message": f"风力已设置为{level or 3}档"
    }


#  Defrost 

@mcp.tool()
def defrost(mode: str = "defog") -> Dict[str, Any]:
    """除雾/除霜 - Enable defog/defrost"""
    if mode == "defog":
        return {
            "status": "success",
            "action": "defog",
            "mode": "defog",
            "message": "已开启除雾模式"
        }
    elif mode == "defrost":
        return {
            "status": "success",
            "action": "defrost",
            "mode": "defrost",
            "message": "已开启除霜模式"
        }
    return {
        "status": "success",
        "action": "defrost_off",
        "mode": "off",
        "message": "除雾/除霜已关闭"
    }


if __name__ == "__main__":
    mcp.run()
