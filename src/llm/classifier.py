"""Query classifier using LangChain with structured output to distinguish chill chat from task-specific queries."""

from __future__ import annotations

import logging
from typing import Any, Protocol

from src.prompts import CLASSIFIER_PROMPT
from src.schema.classifier_output import ClassifierOutput, QueryType
from src.agent_schema.shared_slot_schema import SlotContext

logger = logging.getLogger(__name__)


class QueryClassifier:
    """
    Classifies user queries as either 'chill_chat' or 'task_specific' using an LLM.

    This classifier determines whether a query is primarily for:
    - chill_chat: Social, emotional, or entertainment purposes
    - task_specific: Requires specific function execution or tool calls

    Usage:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(ClassifierOutput)
        classifier = QueryClassifier(llm)

        result = classifier.classify("今天心情不太好")
        print(result.query_type)  # QueryType.CHILL_CHAT

        result = classifier.classify("帮我导航到最近的加油站")
        print(result.query_type)  # QueryType.TASK_SPECIFIC
    """

    def __init__(self, structured_llm: Any) -> None:
        """
        Args:
            structured_llm: A LangChain chat model bound with
                `.with_structured_output(ClassifierOutput)`.
        """
        self._llm = structured_llm

    def classify(
        self,
        query: str,
        conversation_history: list[SlotContext] | None = None,
    ) -> ClassifierOutput:
        """
        Classify the query as 1 (chill_chat), 2 (task_specific), or 3 (meaningless).

        Args:
            query: The user query to classify.
            conversation_history: Optional conversation history for context.

        Returns:
            ClassifierOutput with query_type (1/2/3), confidence, and reasoning.
        """
        prompt = self._build_prompt(query, conversation_history)

        try:
            output: ClassifierOutput = self._llm.invoke(prompt)
            return output
        except Exception as exc:
            logger.warning("[QueryClassifier] LLM call failed: %s", exc)
            return ClassifierOutput(
                query_type=QueryType.TASK_SPECIFIC,
                confidence=0.0,
                reasoning="LLM调用失败，默认返回任务指令类型。",
            )

    def is_chill_chat(self, query: str, conversation_history: list[SlotContext] | None = None) -> bool:
        """
        Convenience method to check if query is chill_chat (type 1).

        Args:
            query: The user query to classify.
            conversation_history: Optional conversation history for context.

        Returns:
            True if query_type is 1 (chill_chat), False otherwise.
        """
        result = self.classify(query, conversation_history)
        return result.query_type == QueryType.CHILL_CHAT

    def is_task_specific(self, query: str, conversation_history: list[SlotContext] | None = None) -> bool:
        """
        Convenience method to check if query is task_specific (type 2).

        Args:
            query: The user query to classify.
            conversation_history: Optional conversation history for context.

        Returns:
            True if query_type is 2 (task_specific), False otherwise.
        """
        result = self.classify(query, conversation_history)
        return result.query_type == QueryType.TASK_SPECIFIC

    def is_meaningless(self, query: str, conversation_history: list[SlotContext] | None = None) -> bool:
        """
        Convenience method to check if query is meaningless (type 3).

        Args:
            query: The user query to classify.
            conversation_history: Optional conversation history for context.

        Returns:
            True if query_type is 3 (meaningless), False otherwise.
        """
        result = self.classify(query, conversation_history)
        return result.query_type == QueryType.MEANINGLESS

    def _build_prompt(
        self,
        query: str,
        conversation_history: list[SlotContext] | None,
    ) -> str:
        """Assemble the full prompt from query and history."""
        history_str = self._format_history(conversation_history)

        return CLASSIFIER_PROMPT.format(
            query=query,
            conversation_history=history_str,
        )

    def _format_history(self, contexts: list[SlotContext] | None) -> str:
        """Format conversation history for the prompt."""
        if not contexts:
            return "(无历史记录)"

        lines = []
        for i, ctx in enumerate(contexts, start=1):
            lines.append(f"--- 轮次 {i} ---")
            if ctx.raw_query:
                lines.append(f"用户: {ctx.raw_query}")
            if ctx.agent and ctx.intent:
                lines.append(f"系统: 代理={ctx.agent}, 意图={ctx.intent}")
            lines.append("")

        return "\n".join(lines) if lines else "(无历史记录)"


if __name__ == "__main__":
    print("QueryClassifier self-test\n")

    class MockOutput:
        def __init__(
            self,
            query_type: QueryType,
            confidence: float = 0.9,
            reasoning: str = "",
        ) -> None:
            self.query_type = query_type
            self.confidence = confidence
            self.reasoning = reasoning

    class MockLLM:
        def invoke(self, prompt: str) -> MockOutput:
            # Meaningless keywords
            meaningless_patterns = [
                "asdfghjkl", "呃呃呃", "啊啊啊", "对对对", "嗯嗯嗯",
                "哈哈哈哈", "嘿嘿嘿嘿", "哦哦哦", "啊啊啊啊", "123456",
            ]

            # Chill chat keywords (Chinese & English)
            chill_keywords = [
                # Casual chat
                "心情", "你好", "无聊", "讲个故事", "笑话", "喜欢吃什么",
                "feeling", "hello", "bored", "tell me a story", "joke",
                # Knowledge queries
                "介绍", "百科", "知识", "人物", "歌手", "歌曲",
                "tell me about", "who is",
                # Poetry
                "诗", "词", "古诗", "诗人", "poem", "poet",
                # Math/Unit conversion
                "计算", "等于", "换算", "多少", "calculate", "convert",
                # Translation
                "翻译", "translate",
                # Recommendations
                "推荐", "建议", "recommend", "suggest",
                # Geography/Travel
                "首都", "国家", "城市", "地理", "旅游",
                "capital", "country", "city", "geography", "travel",
            ]

            # Task-specific keywords (Chinese & English)
            task_keywords = [
                "导航", "播放", "空调", "打电话", "打开", "查看", "天气", "车窗",
                "调节", "设置", "关闭", "发送",
                "navigate", "play", "call", "open", "check", "weather", "window",
                "set", "adjust", "close", "send",
            ]

            # Check for meaningless first
            if any(p in prompt for p in meaningless_patterns):
                return MockOutput(
                    query_type=QueryType.MEANINGLESS,
                    confidence=0.98,
                    reasoning="查询内容无明确语义，判定为无意义内容。",
                )

            if any(kw in prompt for kw in chill_keywords):
                return MockOutput(
                    query_type=QueryType.CHILL_CHAT,
                    confidence=0.95,
                    reasoning="查询为闲聊问答或信息获取类型。",
                )
            if any(kw in prompt.lower() for kw in task_keywords):
                return MockOutput(
                    query_type=QueryType.TASK_SPECIFIC,
                    confidence=0.92,
                    reasoning="查询包含明确的车辆控制或任务操作意图。",
                )
            return MockOutput(
                query_type=QueryType.TASK_SPECIFIC,
                confidence=0.7,
                reasoning="未识别到闲聊特征，默认按任务指令处理。",
            )

    # Tests
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

    classifier = QueryClassifier(MockLLM())

    #  Type 1: Chill Chat Tests 

    # Test 1: Casual chat - Chinese
    result1 = classifier.classify("今天心情不太好")
    print("[Type 1 - Chinese casual chat]")
    check("query_type is 1 (chill_chat)", result1.query_type == QueryType.CHILL_CHAT)
    check("confidence is reasonable", 0.0 <= result1.confidence <= 1.0)

    # Test 2: Casual chat - English
    result2 = classifier.classify("Hello there, how are you?")
    print("\n[Type 1 - English casual chat]")
    check("query_type is 1 (chill_chat)", result2.query_type == QueryType.CHILL_CHAT)

    # Test 3: Person introduction - Chinese
    result3 = classifier.classify("介绍一下周杰伦")
    print("\n[Type 1 - Chinese person introduction]")
    check("query_type is 1 (chill_chat)", result3.query_type == QueryType.CHILL_CHAT)

    # Test 4: Poetry - Chinese
    result4 = classifier.classify("床前明月光是谁写的")
    print("\n[Type 1 - Chinese poetry knowledge]")
    check("query_type is 1 (chill_chat)", result4.query_type == QueryType.CHILL_CHAT)

    # Test 5: Math calculation - Chinese
    result5 = classifier.classify("计算256的平方根")
    print("\n[Type 1 - Chinese math calculation]")
    check("query_type is 1 (chill_chat)", result5.query_type == QueryType.CHILL_CHAT)

    # Test 6: Unit conversion - Chinese
    result6 = classifier.classify("1英里等于多少公里")
    print("\n[Type 1 - Chinese unit conversion]")
    check("query_type is 1 (chill_chat)", result6.query_type == QueryType.CHILL_CHAT)

    # Test 7: Translation - Chinese
    result7 = classifier.classify("翻译成英文：我爱你")
    print("\n[Type 1 - Chinese translation]")
    check("query_type is 1 (chill_chat)", result7.query_type == QueryType.CHILL_CHAT)

    # Test 8: Geography - Chinese
    result8 = classifier.classify("北京是哪个国家的首都")
    print("\n[Type 1 - Chinese geography]")
    check("query_type is 1 (chill_chat)", result8.query_type == QueryType.CHILL_CHAT)

    # Test 9: Music recommendation - Chinese
    result9 = classifier.classify("推荐一首好听的歌")
    print("\n[Type 1 - Chinese music recommendation]")
    check("query_type is 1 (chill_chat)", result9.query_type == QueryType.CHILL_CHAT)

    # Test 10: Joke - Chinese
    result10 = classifier.classify("给我讲个笑话")
    print("\n[Type 1 - Chinese joke]")
    check("query_type is 1 (chill_chat)", result10.query_type == QueryType.CHILL_CHAT)

    # Test 11: Change poem - Chinese
    result11 = classifier.classify("把静夜思换成望庐山瀑布")
    print("\n[Type 1 - Chinese change poem]")
    check("query_type is 1 (chill_chat)", result11.query_type == QueryType.CHILL_CHAT)

    #  Type 2: Task-Specific Tests 

    # Test 12: Navigation - Chinese
    result12 = classifier.classify("帮我导航到最近的加油站")
    print("\n[Type 2 - Chinese navigation]")
    check("query_type is 2 (task_specific)", result12.query_type == QueryType.TASK_SPECIFIC)

    # Test 13: Navigation - English
    result13 = classifier.classify("Navigate to the nearest gas station")
    print("\n[Type 2 - English navigation]")
    check("query_type is 2 (task_specific)", result13.query_type == QueryType.TASK_SPECIFIC)

    # Test 14: Media - Chinese
    result14 = classifier.classify("播放周杰伦的晴天")
    print("\n[Type 2 - Chinese media playback]")
    check("query_type is 2 (task_specific)", result14.query_type == QueryType.TASK_SPECIFIC)

    # Test 15: HVAC - Chinese
    result15 = classifier.classify("把空调调到24度")
    print("\n[Type 2 - Chinese HVAC control]")
    check("query_type is 2 (task_specific)", result15.query_type == QueryType.TASK_SPECIFIC)

    # Test 16: Window control - English
    result16 = classifier.classify("Open the windows")
    print("\n[Type 2 - English window control]")
    check("query_type is 2 (task_specific)", result16.query_type == QueryType.TASK_SPECIFIC)

    #  Type 3: Meaningless Tests 

    # Test 17: Random keyboard characters
    result17 = classifier.classify("asdfghjkl123")
    print("\n[Type 3 - Random keyboard characters]")
    check("query_type is 3 (meaningless)", result17.query_type == QueryType.MEANINGLESS)

    # Test 18: Meaningless Chinese
    result18 = classifier.classify("呃呃呃啊啊啊")
    print("\n[Type 3 - Meaningless Chinese]")
    check("query_type is 3 (meaningless)", result18.query_type == QueryType.MEANINGLESS)

    # Test 19: Repeated characters
    result19 = classifier.classify("哈哈哈哈嘿嘿")
    print("\n[Type 3 - Repeated characters]")
    check("query_type is 3 (meaningless)", result19.query_type == QueryType.MEANINGLESS)

    # Test 20: Random numbers
    result20 = classifier.classify("1234567890")
    print("\n[Type 3 - Random numbers]")
    check("query_type is 3 (meaningless)", result20.query_type == QueryType.MEANINGLESS)

    #  Convenience Methods 

    # Test 21: Convenience methods
    print("\n[convenience methods]")
    check("is_chill_chat returns bool", isinstance(classifier.is_chill_chat("你好"), bool))
    check("is_task_specific returns bool", isinstance(classifier.is_task_specific("打开空调"), bool))
    check("is_meaningless returns bool", isinstance(classifier.is_meaningless("哈哈哈"), bool))
    check("is_chill_chat matches classify", classifier.is_chill_chat("你好") == (classifier.classify("你好").query_type == QueryType.CHILL_CHAT))
    check("is_meaningless matches classify", classifier.is_meaningless("哈哈哈") == (classifier.classify("哈哈哈").query_type == QueryType.MEANINGLESS))

    #  LLM Failure Fallback 

    # Test 22: LLM failure fallback
    class FailingLLM:
        def invoke(self, prompt: str) -> MockOutput:
            raise RuntimeError("simulated LLM failure")

    classifier2 = QueryClassifier(FailingLLM())
    result22 = classifier2.classify("随便什么都行")
    print("\n[LLM failure fallback]")
    check("falls back to task_specific (type 2)", result22.query_type == QueryType.TASK_SPECIFIC)
    check("confidence is 0.0", result22.confidence == 0.0)

    # Summary
    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 40}")
    import sys

    sys.exit(0 if failed == 0 else 1)
