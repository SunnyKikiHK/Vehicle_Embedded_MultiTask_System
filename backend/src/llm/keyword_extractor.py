"""Fast keyword extractor for query optimization.

This module provides lightweight keyword extraction without LLM calls,
significantly reducing latency for classifier and router stages.
"""

import re
from typing import TypedDict

from src.constants import SERVER_USE


class ClassifierKeywords(TypedDict):
    """Keywords for classifier."""
    is_chat_pattern: bool
    is_meaningless_pattern: bool
    has_task_intent: bool


class RouterKeywords(TypedDict):
    """Keywords for router."""
    matched_domains: list[str]
    primary_domain: str | None


# Domain keywords mapped to agent names (no conversion needed)
DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "navigation-agent": ["导航", "加油站", "停车场", "餐馆", "餐厅", "酒店", "银行", "医院", "商场", "超市", "景点", "地址", "附近", "搜索", "终点", "路径"],
    "hvac-agent": ["空调", "温度", "冷气", "暖气", "热", "冷", "风速", "风力", "除雾", "除霜", "度", "外循环", "内循环", "auto"],
    "media-agent": ["播放", "音乐", "歌曲", "暂停", "停止", "下一首", "上一首", "音量", "静音", "收音机", "蓝牙", "切歌"],
    "phone-agent": ["打电话", "拨号", "发消息", "短信", "微信", "呼叫", "接听", "挂断", "免提"],
    "seat-agent": ["座椅", "按摩", "通风", "加热", "靠背", "腰托", "腿托"],
    "ambient-light-agent": ["氛围灯", "灯光", "颜色", "车灯", "阅读灯", "蓝色", "红色", "绿色"],
    "weather-life-agent": ["天气", "气温", "下雨", "晴天", "湿度", "风力", "空气质量", "PM2.5"],
    "system-settings-agent": ["设置", "音量", "屏幕", "显示", "亮度", "语言", "模式", "主题"],
    "car-butler-agent": ["保养", "维修", "年检", "保险", "油耗", "里程", "故障", "警示", "电瓶", "轮胎", "刹车"],
    "user-profile-agent": ["个人信息", "头像", "昵称", "账户", "登录", "注册", "资料"],
}

# Task intent keywords for classifier (concise)
TASK_INTENT_KEYWORDS: list[str] = ["打开", "关闭", "开启", "关掉", "启动", "停止", "暂停", "继续", "设置", "调节", "调高", "调低", "播放", "搜索", "查询", "导航", "拨打", "发送", "呼叫", "帮我", "给", "把", "请"]

# Chill chat patterns (concise)
CHAT_PATTERNS: list[re.Pattern] = [
    re.compile(r"你是谁"),
    re.compile(r"讲.*故事"),
    re.compile(r"讲.*笑话"),
    re.compile(r"翻译"),
    re.compile(r"推荐"),
    re.compile(r"介绍"),
    re.compile(r"唱歌"),
]

# Meaningless patterns (Chinese)
MEANINGLESS_PATTERNS: list[re.Pattern] = [
    re.compile(r"^[呃啊哦嗯哈嘻嗨呀嘛哈啰]+$"),
    re.compile(r"^.{1,2}$"),
    re.compile(r"^[0-9]+$"),
    re.compile(r"^[\s\W]+$"),
    re.compile(r"^[a-z]+$", re.I),
]


def extract_classifier_keywords(query: str) -> ClassifierKeywords:
    """
    Extract keywords for classification decision.

    This is a lightweight operation that runs in O(n) time with no external calls.

    Args:
        query: The user query to analyze.

    Returns:
        ClassifierKeywords with classification hints.
    """
    # Check meaningless patterns first
    is_meaningless_pattern = any(pattern.search(query) for pattern in MEANINGLESS_PATTERNS)

    # Check chat patterns
    is_chat_pattern = any(pattern.search(query) for pattern in CHAT_PATTERNS)

    # Check for task intent keywords
    has_task_intent = any(kw in query for kw in TASK_INTENT_KEYWORDS)

    return ClassifierKeywords(
        is_chat_pattern=is_chat_pattern,
        is_meaningless_pattern=is_meaningless_pattern,
        has_task_intent=has_task_intent
    )


def extract_router_keywords(query: str, enabled_only: bool = False) -> RouterKeywords:
    """
    Extract keywords for routing decision.

    This is a lightweight operation that runs in O(n) time with no external calls.

    Args:
        query: The user query to analyze.
        enabled_only: If True, only consider agents enabled in SERVER_USE.

    Returns:
        RouterKeywords with agent hints.
    """
    matched_agents: list[str] = []
    agent_scores: dict[str, int] = {}

    domain_keywords = {
        agent: keywords
        for agent, keywords in DOMAIN_KEYWORDS.items()
        if not enabled_only or SERVER_USE.get(agent, False)
    }

    for agent, keywords in domain_keywords.items():
        score = 0
        for kw in keywords:
            if kw in query:
                score += 1
                if agent not in matched_agents:
                    matched_agents.append(agent)
        if score > 0:
            agent_scores[agent] = score

    # Determine primary agent (highest score)
    primary_agent = None
    if agent_scores:
        primary_agent = max(agent_scores, key=agent_scores.get)

    return RouterKeywords(
        matched_domains=matched_agents,
        primary_domain=primary_agent
    )


def fast_classify(query: str) -> tuple[str, float, ClassifierKeywords]:
    """
    Fast classification based purely on keyword matching.

    Args:
        query: The user query.

    Returns:
        Tuple of (query_type, confidence, classifier_keywords).
    """
    keywords = extract_classifier_keywords(query)

    # Check meaningless first
    if keywords["is_meaningless_pattern"]:
        return "meaningless", 0.95, keywords

    # Check chill chat patterns (without domain hints = definitely chat)
    if keywords["is_chat_pattern"] and not keywords["has_task_intent"]:
        return "chill_chat", 0.90, keywords

    # Has task intent = likely task-specific
    if keywords["has_task_intent"]:
        return "task_specific", 0.75, keywords

    # No clear indicators
    return "task_specific", 0.4, keywords


def fast_route(query: str) -> tuple[str | None, float]:
    """
    Fast routing based purely on keyword matching.

    Args:
        query: The user query.

    Returns:
        Tuple of (target_agent or None, confidence).
    """
    keywords = extract_router_keywords(query, enabled_only=True)

    if not keywords["primary_domain"]:
        return None, 0.0

    # primary_domain now directly contains agent name
    agent = keywords["primary_domain"]

    # Confidence based on number of matched domains
    num_matches = len(keywords["matched_domains"])
    if num_matches >= 3:
        confidence = 0.85
    elif num_matches >= 1:
        confidence = 0.80
    else:
        confidence = 0.50

    return agent, confidence


if __name__ == "__main__":
    # Test the keyword extractor
    test_queries = [
        "帮我导航到最近的加油站",
        "把空调调到24度",
        "播放周杰伦的晴天",
        "今天心情不太好",
        "asdfghjkl",
        "你好吗",
        "打开车窗",
        "附近有什么餐厅",
        "搜索附近的停车场",
        "把温度调低一点",
        "放首歌听听",
        "嗯嗯啊啊",
    ]

    print("Keyword Extractor Test\n" + "=" * 50)

    for query in test_queries:
        print(f"\nQuery: {query}")

        # Classifier keywords
        clf_kw = extract_classifier_keywords(query)
        print(f"  [Classifier] chat={clf_kw['is_chat_pattern']}, "
              f"meaningless={clf_kw['is_meaningless_pattern']}, "
              f"task={clf_kw['has_task_intent']}")

        fast_type, fast_conf = fast_classify(query)
        print(f"  [Fast Classify] {fast_type} ({fast_conf:.2f})")

        # Router keywords
        rtr_kw = extract_router_keywords(query)
        print(f"  [Router] agents={rtr_kw['matched_domains']}, "
              f"primary={rtr_kw['primary_domain']}")

        fast_agent, route_conf = fast_route(query)
        print(f"  [Fast Route] {fast_agent} ({route_conf:.2f})")
