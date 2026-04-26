"""Shared Slot Schema — normalized slot types across all agents."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

_SHARED_SLOT_SCHEMA: SharedSlotSchema | None = None


def get_shared_slot_schema() -> SharedSlotSchema:
    """Lazy singleton: return the cached SharedSlotSchema instance."""
    global _SHARED_SLOT_SCHEMA
    if _SHARED_SLOT_SCHEMA is None:
        _SHARED_SLOT_SCHEMA = SharedSlotSchema()
    return _SHARED_SLOT_SCHEMA


SHARED_SLOT_SCHEMA = get_shared_slot_schema



# Position / Zone
class Position(str, Enum):
    """Vehicle seat or zone position."""
    DRIVER = "主驾"
    PASSENGER = "副驾"
    REAR_LEFT = "后排左侧"
    REAR_RIGHT = "后排右侧"
    REAR = "后排"
    FRONT = "前排"
    ALL = "全部"
    BACK_SEAT = "后座"
    PASSENGER_REAR = "副驾后"
    DRIVER_REAR = "主驾后"



# Ratio / Relative adjustment level
class Ratio(str, Enum):
    HIGH = "高"
    MID = "中"
    LOW = "低"
    HIGHEST = "最高"
    LOWEST = "最低"
    HIGH_BIT = "高一点"
    LOW_BIT = "低一点"
    HIGHER = "再高"
    LOWER = "再低"
    SLIGHTLY = "一点"
    SOMEWHAT = "一些"
    A_LOT = "很多"
    SLIGHTLY_MORE = "稍微"
    LARGE = "大幅"
    SMALL = "小幅度"



# Extreme value flag
class Extreme(str, Enum):
    MAX = "最高"
    MIN = "最低"
    MAX_VAL = "最大"
    MIN_VAL = "最小"
    HOTTEST = "最热"
    COLDEST = "最冷"
    STRONGEST = "最强"
    WEAKEST = "最弱"



# Direction
class Direction(str, Enum):
    UP = "上"
    DOWN = "下"
    LEFT = "左"
    RIGHT = "右"
    FORWARD = "前"
    BACKWARD = "后"
    UP_LEFT = "左上"
    UP_RIGHT = "右上"
    DOWN_LEFT = "左下"
    DOWN_RIGHT = "右下"
    FORWARD_BACK = "前后"
    UP_DOWN = "上下"
    LEFT_RIGHT = "左右"



# Ambient Light
class LightColor(str, Enum):
    RED = "红"
    GREEN = "绿"
    BLUE = "蓝"
    YELLOW = "黄"
    PURPLE = "紫"
    ORANGE = "橙"
    PINK = "粉"
    WHITE = "白"
    WARM_WHITE = "暖白"
    COOL_WHITE = "冷白"
    CYAN = "青色"
    BROWN = "棕色"
    CUSTOM = "自定义"


class LightTheme(str, Enum):
    ROMANTIC = "浪漫"
    PASSION = "激情"
    COOL = "清凉"
    WARM = "温暖"
    TECH = "科技"
    NATURE = "自然"
    STARS = "星辰"
    NEON = "霓虹"
    SUNSET = "日落"
    FOREST = "森林"
    OCEAN = "海洋"



# Camera
class CameraView(str, Enum):
    FRONT = "前视"
    BACK = "后视"
    LEFT = "左视"
    RIGHT = "右视"
    THREE_D = "3D"
    PANORAMIC = "全景"
    TOP_DOWN = "俯视"



# Driving Mode
class DrivingMode(str, Enum):
    ECO = "经济"
    SPORT = "运动"
    COMFORT = "舒适"
    STANDARD = "标准"
    SNOW = "雪地"
    OFF_ROAD = "越野"
    ENERGY_SAVING = "节能"
    CUSTOM = "个性"



# Media
class MediaSource(str, Enum):
    BLUETOOTH = "蓝牙"
    USB = "USB"
    ONLINE = "在线"
    LOCAL = "本地"
    FM = "FM"
    AM = "AM"
    AUX = "AUX"
    SD_CARD = "SD卡"
    WIFI = "WiFi"
    MUSIC = "音乐"
    RADIO = "广播"


class SoundSource(str, Enum):
    MEDIA = "媒体"
    NAVIGATION = "导航"
    PHONE = "通话"
    VOICE_ASSISTANT = "语音助手"
    ALARM = "警报"
    TONE = "提示音"
    AC = "空调"
    RADIO = "广播"
    MUSIC = "音乐"
    ALL = "全部"



# Weather / Life
class DateSpec(str, Enum):
    TODAY = "今天"
    TOMORROW = "明天"
    DAY_AFTER = "后天"
    TWO_DAYS_AFTER = "大后天"
    YESTERDAY = "昨天"
    TWO_DAYS_AGO = "前天"
    THIS_WEEK = "本周"
    NEXT_WEEK = "下周"
    WEEKEND = "周末"
    WORKDAY = "工作日"


class WeatherCondition(str, Enum):
    SUNNY = "晴"
    CLOUDY = "阴"
    OVERCAST = "多云"
    LIGHT_RAIN = "小雨"
    MED_RAIN = "中雨"
    HEAVY_RAIN = "大雨"
    TORRENTIAL = "暴雨"
    LIGHT_SNOW = "小雪"
    MED_SNOW = "中雪"
    HEAVY_SNOW = "大雪"
    SNOWSTORM = "暴雪"
    FOG = "雾"
    HAZE = "霾"
    SANDSTORM = "沙尘"
    GALE = "大风"


class AirQuality(str, Enum):
    EXCELLENT = "优"
    GOOD = "良"
    LIGHT = "轻度污染"
    MEDIUM = "中度污染"
    HEAVY = "重度污染"
    SEVERE = "严重污染"


class DressingType(str, Enum):
    LIGHT_JACKET = "薄外套"
    HEAVY_JACKET = "厚外套"
    T_SHIRT = "T恤"
    SHIRT = "衬衫"
    SWEATER = "毛衣"
    COAT = "大衣"
    DOWN_JACKET = "羽绒服"
    SHORTS = "短裤"
    PANTS = "长裤"
    SKIRT = "裙子"



# Phone
class PhoneLabel(str, Enum):
    MOBILE = "手机"
    MOBILE_ALT = "移动"
    WORK = "工作"
    COMPANY = "公司"
    HOME = "家庭"
    RESIDENCE = "住宅"
    BUSINESS = "商务"


class EmergencyType(str, Enum):
    POLICE = "110"
    AMBULANCE = "120"
    FIRE = "119"
    TRAFFIC = "122"
    POLICE_CN = "急救"
    ALARM_CN = "报警"
    FIRE_CN = "火警"



# System Settings
class Scene(str, Enum):
    GO_HOME = "回家"
    LEAVE_HOME = "离家"
    TO_WORK = "上班"
    OFF_WORK = "下班"
    CAMPING = "露营"
    ROMANTIC = "浪漫"
    REST = "休息"
    KIDS = "儿童"
    MEETING = "会议"
    DRIVING = "驾驶"
    RAINY = "雨天"
    SNOWY = "雪天"


class DesktopStyle(str, Enum):
    CLASSIC = "经典"
    SIMPLE = "简洁"
    CARD = "卡片"
    LIST = "列表"
    CUSTOM = "自定义"


class SystemMode(str, Enum):
    DAY = "白天"
    NIGHT = "夜间"
    AUTO = "自动"
    DARK = "深色"
    LIGHT = "浅色"



# Music / Media Search
class MusicGenre(str, Enum):
    POP = "流行"
    ROCK = "摇滚"
    CLASSICAL = "古典"
    JAZZ = "爵士"
    ELECTRONIC = "电子"
    FOLK = "民谣"
    HIPHOP = "嘻哈"
    RNB = "R&B"
    EASY_LISTENING = "轻音乐"
    DANCE = "舞曲"


class MusicChart(str, Enum):
    HOT = "热歌榜"
    NEW = "新歌榜"
    RISING = "飙升榜"
    ORIGINAL = "原创榜"
    SALES = "销量榜"


class MusicMood(str, Enum):
    CHEERFUL = "欢快"
    LYRICAL = "抒情"
    SAD = "悲伤"
    ROMANTIC = "浪漫"
    PASSIONATE = "激情"
    RELAXED = "放松"
    EXCITED = "兴奋"
    CALM = "安静"


class MusicScene(str, Enum):
    DRIVING = "开车"
    WORKING = "工作"
    SPORTS = "运动"
    SLEEPING = "睡前"
    MORNING = "早晨"
    NIGHT = "夜晚"
    PARTY = "Party"


class MusicLanguage(str, Enum):
    CHINESE = "中文"
    ENGLISH = "英文"
    JAPANESE = "日文"
    KOREAN = "韩文"
    CANTONESE = "粤语"
    MINNAN = "闽南语"
    OTHER = "其他"


class MusicAge(str, Enum):
    SEVENTIES = "70年代"
    EIGHTIES = "80年代"
    NINETIES = "90年代"
    TWO_THOUSAND = "00后"
    TWO_THOUSAND_TEN = "10后"
    OLD = "老歌"
    NEW = "新歌"


class AudioQuality(str, Enum):
    STANDARD = "标准"
    HQ = "HQ"
    SQ = "SQ"
    HIFI = "Hi-Fi"
    LOSSLESS = "无损"



# Car Health
class TireStatus(str, Enum):
    NORMAL = "正常"
    LOW = "偏低"
    HIGH = "过高"
    ABNORMAL = "异常"


class FuelStatus(str, Enum):
    SUFFICIENT = "充足"
    LOW = "偏低"
    NEED_REFUEL = "需加油"
    EMPTY = "耗尽"


class MaintenanceStatus(str, Enum):
    NORMAL = "正常"
    DUE = "到期"
    OVERDUE = "过期"
    REMINDER = "提醒"



# Slot Value Resolution
# Maps Ratio descriptors to numeric step offsets for increment/decrement
RATIO_TO_STEP: dict[Ratio, int] = {
    Ratio.HIGH: 3,
    Ratio.MID: 0,
    Ratio.LOW: -3,
    Ratio.HIGHEST: 99,   # sentinel for "set to max"
    Ratio.LOWEST: -99,    # sentinel for "set to min"
    Ratio.HIGH_BIT: 1,
    Ratio.LOW_BIT: -1,
    Ratio.HIGHER: 2,
    Ratio.LOWER: -2,
    Ratio.SLIGHTLY: 1,
    Ratio.SOMEWHAT: 2,
    Ratio.A_LOT: 5,
    Ratio.SLIGHTLY_MORE: 1,
    Ratio.LARGE: 5,
    Ratio.SMALL: 2,
}


@dataclass
class SlotValue:
    """
    Normalized slot value with metadata.
    
    It tracks both the raw value (as spoken/entered by the user) and a resolved 
    value (after normalization or transformation). 
    The agent, intent, and confidence fields attach metadata 
    about where and how the slot was extracted.
    """

    key: str
    raw_value: Any
    resolved_value: Any = None
    agent: str | None = None
    intent: str | None = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if self.resolved_value is None:
            self.resolved_value = self.raw_value


@dataclass
class SlotContext:
    """
    A container for the full context of one conversation turn,
    persisted to Redis for cross-turn state.
    """

    agent: str
    intent: str
    slots: dict[str, SlotValue] = field(default_factory=dict)
    raw_query: str = ""

    def to_redis_value(self) -> str:
        parts = [
            self.agent,
            self.intent,
            ",".join(f"{k}={v.resolved_value}" for k, v in self.slots.items()),
            self.raw_query,
        ]
        return "#".join(parts)

    @classmethod
    def from_redis_value(cls, value: str) -> SlotContext:
        parts = value.split("#", 3)
        agent, intent, slots_str, raw_query = (
            parts + ["", "", ""]
        )[:4] # [:4] guard with parts + ["", "", ""] handles the edge case where fewer than 4 #-delimited fields are present.
        slots: dict[str, SlotValue] = {}
        for part in slots_str.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                slots[k] = SlotValue(key=k, raw_value=v, resolved_value=v) # raw_value is useless here
        return cls(agent=agent, intent=intent, slots=slots, raw_query=raw_query)



# Main Schema Loader
class SharedSlotSchema:
    """Loader and accessor for the shared slot schema definition."""

    def __init__(self, schema_path: str | Path | None = None) -> None:
        if schema_path is None:
            schema_path = Path(__file__).parent / "shared_slot_schema.json"
        with open(schema_path, encoding="utf-8") as f:
            self._data = json.load(f)

    @property
    def slot_definitions(self) -> dict[str, Any]:
        return self._data["slot_definitions"]

    @property
    def agent_coverage(self) -> dict[str, list[str]]:
        return self._data["agent_slot_coverage"]

    @property
    def shared_types(self) -> dict[str, Any]:
        return self._data["shared_slot_types"]

    @property
    def agent_definitions(self) -> dict[str, Any]:
        return self._data["agent_definitions"]

    def get_slot_definition(self, slot_type: str) -> dict[str, Any] | None:
        return self.slot_definitions.get(slot_type)

    def get_slot_enum(self, slot_type: str) -> list[str]:
        """Returns allowed values for a slot type. Returns empty list for open-type slots (no enum)."""
        defn = self.get_slot_definition(slot_type)
        if defn is None:
            return []
        return defn.get("enum", [])

    def is_valid_slot_value(self, slot_type: str, value: str) -> bool:
        """Check whether a value is valid for the given slot type."""
        allowed = self.get_slot_enum(slot_type)
        if not allowed: # accept open type
            return True
        return value in allowed

    def agents_for_slot(self, slot_type: str) -> list[str]:
        """Return list of agents that use a given slot type."""
        return [
            agent
            for agent, slots in self.agent_coverage.items()
            if slot_type in slots
        ]

    def slots_for_agent(self, agent: str) -> list[str]:
        """Return list of slot types used by a given agent."""
        return self.agent_coverage.get(agent, [])

    def resolve_ratio(self, ratio: str) -> int:
        """Converts a Chinese ratio string like "高" to its numeric step offset (+3), using the RATIO_TO_STEP dict defined earlier"""
        try:
            return RATIO_TO_STEP[Ratio(ratio)]
        except (ValueError, KeyError):
            return 0

    def normalize_time(self, time_str: str) -> int | None:
        """
        Parse a natural-language time string into seconds.

        Examples:
            "5分钟"  → 300
            "1小时"  → 3600
            "30秒"  → 30
        """
        match = re.match(r"(\d+)\s*(秒|分钟|分|时|小时|小时半)", time_str)
        if not match:
            return None
        num, unit = int(match.group(1)), match.group(2)
        if unit in ("秒",):
            return num
        if unit in ("分钟", "分"):
            return num * 60
        if unit in ("时", "小时"):
            return num * 3600
        if unit == "小时半":
            return num * 3600 + 1800
        return None

    def resolve_date(self, date_spec: str) -> str | None:
        """Map a date specifier to a concrete ISO date string (relative to today)."""
        from datetime import date, timedelta

        today = date.today()
        mapping: dict[str, int] = {
            DateSpec.TODAY.value: 0,
            DateSpec.TOMORROW.value: 1,
            DateSpec.DAY_AFTER.value: 2,
            DateSpec.TWO_DAYS_AFTER.value: 3,
            DateSpec.YESTERDAY.value: -1,
            DateSpec.TWO_DAYS_AGO.value: -2,
            DateSpec.THIS_WEEK.value: 0,
            DateSpec.NEXT_WEEK.value: 7,
        }
        offset = mapping.get(date_spec)
        if offset is None:
            return None
        return (today + timedelta(days=offset)).isoformat()

if __name__ == "__main__":
    import sys

    print("SharedSlotSchema self-test\n")

    schema = SharedSlotSchema()
    passed = 0
    failed = 0

    def check(label: str, condition: bool) -> None:
        global passed, failed
        status = "PASS" if condition else "FAIL"
        print(f"  [{status}] {label}")
        if condition:
            passed += 1
        else:
            failed += 1

    #  Schema loading 
    print("\n[Schema loading]")
    check("slot_definitions not empty", len(schema.slot_definitions) > 0)
    check("Position has enum", len(schema.get_slot_enum("Position")) > 0)
    check("Number has no enum (open type)", schema.get_slot_enum("Number") == [])

    #  Enum lookup 
    print("\n[Enum lookup]")
    pos_enum = schema.get_slot_enum("Position")
    check("Position enum contains 主驾", "主驾" in pos_enum)
    check("Position enum contains 副驾", "副驾" in pos_enum)
    check("Unknown slot returns empty list", schema.get_slot_enum("FakeSlot") == [])

    #  Slot validation 
    print("\n[Slot validation]")
    check("Valid Position value passes", schema.is_valid_slot_value("Position", "主驾"))
    check("Invalid Position value fails", not schema.is_valid_slot_value("Position", "幽灵座位"))
    check("Open-type Number always passes", schema.is_valid_slot_value("Number", "999"))
    check("Unknown slot type always passes", schema.is_valid_slot_value("FakeSlot", "任意值"))

    #  SlotContext creation & Redis round-trip 
    print("\n[SlotContext serialization]")
    ctx = SlotContext(
        agent="HVAC Agent",
        intent="调节温度",
        slots={"Temperature": SlotValue(key="Temperature", raw_value="好热", resolved_value="22")},
        raw_query="太热了，调到22度",
    )
    redis_str = ctx.to_redis_value()
    check("Redis string contains agent", "HVAC Agent" in redis_str)
    check("Redis string contains resolved value", "22" in redis_str)
    check("Redis string uses # delimiter", "#" in redis_str)

    ctx2 = SlotContext.from_redis_value(redis_str)
    check("Round-trip: agent preserved", ctx2.agent == "HVAC Agent")
    check("Round-trip: intent preserved", ctx2.intent == "调节温度")
    check("Round-trip: slots preserved", "Temperature" in ctx2.slots)
    check("Round-trip: resolved_value preserved", ctx2.slots["Temperature"].resolved_value == "22")
    check("Round-trip: raw_value == resolved_value (limitation)", ctx2.slots["Temperature"].raw_value == "22")
    check("Round-trip: raw_query preserved", ctx2.raw_query == "太热了，调到22度")

    #  Malformed Redis string 
    print("\n[Malformed input handling]")
    ctx3 = SlotContext.from_redis_value("only_one_field")
    check("Short string: agent populated", ctx3.agent == "only_one_field")
    check("Short string: intent empty", ctx3.intent == "")
    check("Short string: slots empty", ctx3.slots == {})

    #  Agent coverage
    print("\n[Agent coverage]")
    hvac_slots = schema.slots_for_agent("HVAC Agent")
    check("HVAC Agent has slots", len(hvac_slots) > 0)
    check("HVAC Agent uses Temperature slot", "Temperature" in hvac_slots)
    agents_for_temp = schema.agents_for_slot("Temperature")
    check("Temperature slot used by at least one agent", len(agents_for_temp) > 0)

    #  Agent definitions
    print("\n[Agent definitions]")
    agent_defs = schema.agent_definitions
    check("agent_definitions not empty", len(agent_defs) > 0)
    check("agent_definitions has Navigation Agent", "Navigation Agent" in agent_defs)
    check("Navigation Agent has duty", "duty" in agent_defs["Navigation Agent"])
    check("Navigation Agent has keywords", "keywords" in agent_defs["Navigation Agent"])
    check("Navigation Agent has 14 agents", len(agent_defs) == 14)

    #  Date resolution 
    print("\n[Date resolution]")
    date_today = schema.resolve_date("今天")
    check("resolve_date('今天') returns ISO date", date_today is not None and len(date_today) == 10)
    check("resolve_date('无效日期') returns None", schema.resolve_date("无效日期") is None)

    #  Time resolution 
    print("\n[Time resolution]")
    sec = schema.resolve_duration("半小时")
    check("resolve_duration('半小时') == 1800s", sec == 1800)
    sec2 = schema.resolve_duration("一个半小时")
    check("resolve_duration('一个半小时') == 5400s", sec2 == 5400)
    check("resolve_duration('无效时间') == None", schema.resolve_duration("无效时间") is None)

    #  Summary 
    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*40}")
    sys.exit(0 if failed == 0 else 1)
