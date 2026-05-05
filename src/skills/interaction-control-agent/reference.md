# Interaction Control Agent — Reference

## Intent to MCP Tool Mapping

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Confirm | show_notification | `{"title": "确认", "content": "操作已确认"}` | 确定 |
|| Cancel | show_notification | `{"title": "取消", "content": "操作已取消"}` | 取消 |
|| List_Select | show_notification | `{"title": "选择", "content": "已选择第{index}项"}` | 列表选择 |
|| Open_Help | show_notification | `{"title": "帮助", "content": "帮助中心已打开"}` | 打开帮助 |
|| Close_Help | dismiss_notification | `{}` | 关闭帮助 |

## Shared Slot Type Definitions

### Index
```
value_range: 1-based positive integer
resolution: Select item at position Index from presented list. Default to 1.
agents: Interaction Control Agent
```

### Response
```
value_range: 1-8 Chinese characters or pinyin
resolution: Validate: not a common phrase, not reserved word, not offensive.
agents: Interaction Control Agent
```

## Response Word Validation Rules

- Minimum 1 character, maximum 8 characters
- Cannot be: 好, 是, 确定, 取消, 下一个, 退下
- Cannot match any existing wake word
- Should not be a single common character that could trigger accidentally
- Good examples: "知道了", "好的", "可以", "没问题", "好的好的"
