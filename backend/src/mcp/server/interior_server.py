#!/usr/bin/env python
"""Interior Server - MCP Implementation for Windows, Lights & Seats

This server handles window control, ambient lights, seat adjustments,
steering wheel, and rearview mirrors.
"""
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("interior_server")


#  Window Control 

@mcp.tool()
def open_window(position: str = "全部") -> Dict[str, Any]:
    """打开车窗 - Open car windows"""
    return {
        "status": "success",
        "action": "window_open",
        "position": position,
        "message": f"{position}车窗已打开"
    }


@mcp.tool()
def close_window(position: str = "全部") -> Dict[str, Any]:
    """关闭车窗 - Close car windows"""
    return {
        "status": "success",
        "action": "window_close",
        "position": position,
        "message": f"{position}车窗已关闭"
    }


@mcp.tool()
def window_up(position: str = "全部") -> Dict[str, Any]:
    """车窗上升 - Raise windows"""
    return {
        "status": "success",
        "action": "window_up",
        "position": position,
        "message": f"{position}车窗已升起"
    }


@mcp.tool()
def window_down(position: str = "全部", level: Optional[int] = None) -> Dict[str, Any]:
    """车窗下降 - Lower windows"""
    return {
        "status": "success",
        "action": "window_down",
        "position": position,
        "level": level,
        "message": f"{position}车窗已降下"
    }


@mcp.tool()
def window_all_up() -> Dict[str, Any]:
    """所有车窗上升 - Raise all windows"""
    return {
        "status": "success",
        "action": "window_all_up",
        "message": "所有车窗已升起"
    }


@mcp.tool()
def window_all_down() -> Dict[str, Any]:
    """所有车窗下降 - Lower all windows"""
    return {
        "status": "success",
        "action": "window_all_down",
        "message": "所有车窗已降下"
    }


#  Ambient Lights 

@mcp.tool()
def set_interior_lights(switch: Optional[str] = None, color: Optional[str] = None,
                         theme: Optional[str] = None, level: Optional[int] = None,
                         target: Optional[str] = None, direction: Optional[str] = None,
                         mode: Optional[str] = None) -> Dict[str, Any]:
    """设置氛围灯 - Set ambient lights, dashboard, screen brightness"""
    if switch == "on":
        return {
            "status": "success",
            "action": "lights_on",
            "message": "氛围灯已开启"
        }
    elif switch == "off":
        return {
            "status": "success",
            "action": "lights_off",
            "message": "氛围灯已关闭"
        }
    elif color:
        return {
            "status": "success",
            "action": "set_color",
            "color": color,
            "message": f"氛围灯已切换到{color}"
        }
    elif theme:
        return {
            "status": "success",
            "action": "set_theme",
            "theme": theme,
            "message": f"氛围灯主题已切换到{theme}"
        }
    elif level is not None:
        target_msg = f"{target}亮度" if target else "亮度"
        dir_msg = "已调高" if direction == "up" else "已调低" if direction == "down" else ""
        return {
            "status": "success",
            "action": "set_brightness",
            "target": target,
            "level": level,
            "direction": direction,
            "message": f"{target_msg}已设置为{level}%"
        }
    elif mode:
        return {
            "status": "success",
            "action": "set_mode",
            "mode": mode,
            "message": f"氛围灯已切换到{mode}模式"
        }
    
    return {
        "status": "success",
        "message": "氛围灯设置已更新"
    }


@mcp.tool()
def set_headlights(mode: str = "on") -> Dict[str, Any]:
    """设置大灯 - Set headlights"""
    mode_map = {
        "on": "大灯已开启",
        "off": "大灯已关闭",
        "low_beam": "近光灯已开启",
        "high_beam": "远光灯已开启",
        "fog_on": "雾灯已开启",
        "fog_off": "雾灯已关闭",
        "auto": "大灯已设置为自动模式",
    }
    return {
        "status": "success",
        "action": "set_headlights",
        "mode": mode,
        "message": mode_map.get(mode, f"大灯已设置为{mode}")
    }


@mcp.tool()
def lights_on() -> Dict[str, Any]:
    """打开车内灯 - Turn on interior lights"""
    return {
        "status": "success",
        "action": "lights_on",
        "message": "车内灯已开启"
    }


@mcp.tool()
def lights_off() -> Dict[str, Any]:
    """关闭车内灯 - Turn off interior lights"""
    return {
        "status": "success",
        "action": "lights_off",
        "message": "车内灯已关闭"
    }


@mcp.tool()
def set_reading_light(switch: str = "on") -> Dict[str, Any]:
    """设置阅读灯 - Set reading light"""
    if switch == "on":
        return {
            "status": "success",
            "action": "reading_light_on",
            "message": "阅读灯已开启"
        }
    return {
        "status": "success",
        "action": "reading_light_off",
        "message": "阅读灯已关闭"
    }


#  Seat Control 

@mcp.tool()
def adjust_seat(direction: Optional[str] = None, position: str = "主驾",
                target: Optional[str] = None, action: Optional[str] = None) -> Dict[str, Any]:
    """调节座椅 - Adjust seat position or mirrors"""
    if target == "mirror":
        if action == "fold":
            return {
                "status": "success",
                "action": "mirror_fold",
                "message": "后视镜已折叠"
            }
        elif action == "unfold":
            return {
                "status": "success",
                "action": "mirror_unfold",
                "message": "后视镜已展开"
            }
    
    if direction == "forward":
        return {
            "status": "success",
            "action": "seat_forward",
            "position": position,
            "message": f"{position}座椅已向前调整"
        }
    elif direction == "backward":
        return {
            "status": "success",
            "action": "seat_backward",
            "position": position,
            "message": f"{position}座椅已向后调整"
        }
    elif direction == "up":
        return {
            "status": "success",
            "action": "seat_up",
            "position": position,
            "message": f"{position}座椅已向上调整"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "seat_down",
            "position": position,
            "message": f"{position}座椅已向下调整"
        }
    
    return {
        "status": "success",
        "message": f"{position}座椅位置已调整"
    }


@mcp.tool()
def seat_position(position: str = "主驾") -> Dict[str, Any]:
    """获取座椅位置 - Get seat position"""
    return {
        "status": "success",
        "position": position,
        "memory": 1,
        "message": f"{position}座椅位置已保存"
    }


@mcp.tool()
def seat_heating(switch: Optional[str] = None, position: str = "主驾",
                 level: Optional[int] = None, direction: Optional[str] = None,
                 target: Optional[str] = None) -> Dict[str, Any]:
    """座椅加热/方向盘加热 - Seat heating or steering wheel heating"""
    if target == "steering_wheel":
        if switch == "on":
            return {
                "status": "success",
                "action": "steering_heat_on",
                "message": "方向盘加热已开启"
            }
        elif switch == "off":
            return {
                "status": "success",
                "action": "steering_heat_off",
                "message": "方向盘加热已关闭"
            }
        return {
            "status": "success",
            "action": "steering_heat",
            "level": level,
            "message": "方向盘加热已设置"
        }
    elif target == "mirror":
        if switch == "on":
            return {
                "status": "success",
                "action": "mirror_heat_on",
                "message": "后视镜加热已开启"
            }
        return {
            "status": "success",
            "action": "mirror_heat_off",
            "message": "后视镜加热已关闭"
        }
    
    if switch == "on":
        return {
            "status": "success",
            "action": "seat_heat_on",
            "position": position,
            "level": level or 2,
            "message": f"{position}座椅加热已开启"
        }
    elif switch == "off":
        return {
            "status": "success",
            "action": "seat_heat_off",
            "position": position,
            "message": f"{position}座椅加热已关闭"
        }
    elif direction == "up":
        return {
            "status": "success",
            "action": "seat_heat_up",
            "position": position,
            "message": f"{position}座椅温度已调高"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "seat_heat_down",
            "position": position,
            "message": f"{position}座椅温度已调低"
        }
    
    return {
        "status": "success",
        "action": "seat_heat",
        "position": position,
        "level": level,
        "message": f"{position}座椅温度已设置"
    }


@mcp.tool()
def seat_ventilation(switch: Optional[str] = None, position: str = "主驾",
                      level: Optional[int] = None, direction: Optional[str] = None) -> Dict[str, Any]:
    """座椅通风 - Seat ventilation"""
    if switch == "on":
        return {
            "status": "success",
            "action": "seat_vent_on",
            "position": position,
            "level": level or 2,
            "message": f"{position}座椅通风已开启"
        }
    elif switch == "off":
        return {
            "status": "success",
            "action": "seat_vent_off",
            "position": position,
            "message": f"{position}座椅通风已关闭"
        }
    elif direction == "up":
        return {
            "status": "success",
            "action": "seat_vent_up",
            "position": position,
            "message": f"{position}座椅通风已调高"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "seat_vent_down",
            "position": position,
            "message": f"{position}座椅通风已调低"
        }
    
    return {
        "status": "success",
        "action": "seat_vent",
        "position": position,
        "level": level,
        "message": f"{position}座椅通风已设置"
    }


@mcp.tool()
def seat_massage(switch: Optional[str] = None, position: str = "主驾",
                level: Optional[int] = None, direction: Optional[str] = None) -> Dict[str, Any]:
    """座椅按摩 - Seat massage"""
    if switch == "on":
        return {
            "status": "success",
            "action": "seat_massage_on",
            "position": position,
            "level": level or 2,
            "message": f"{position}座椅按摩已开启"
        }
    elif switch == "off":
        return {
            "status": "success",
            "action": "seat_massage_off",
            "position": position,
            "message": f"{position}座椅按摩已关闭"
        }
    elif direction == "up":
        return {
            "status": "success",
            "action": "seat_massage_up",
            "position": position,
            "message": f"{position}座椅按摩强度已调高"
        }
    elif direction == "down":
        return {
            "status": "success",
            "action": "seat_massage_down",
            "position": position,
            "message": f"{position}座椅按摩强度已调低"
        }
    
    return {
        "status": "success",
        "action": "seat_massage",
        "position": position,
        "level": level,
        "message": f"{position}座椅按摩已设置"
    }


@mcp.tool()
def recline_seat(position: str = "主驾", direction: str = "back") -> Dict[str, Any]:
    """倾斜座椅 - Recline seat"""
    return {
        "status": "success",
        "action": "seat_recline",
        "position": position,
        "direction": direction,
        "message": f"{position}座椅靠背已{direction}"
    }


@mcp.tool()
def seat_memory(position: str = "主驾", memory_slot: int = 1) -> Dict[str, Any]:
    """座椅记忆 - Seat memory"""
    return {
        "status": "success",
        "action": "seat_memory",
        "position": position,
        "slot": memory_slot,
        "message": f"{position}座椅已保存到记忆{memory_slot}"
    }


if __name__ == "__main__":
    mcp.run()
