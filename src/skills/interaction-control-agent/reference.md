# Interaction Control Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 428 | Confirm | 确定 |
| 430 | Cancel | 取消 |
| 429 | List_Select | 列表选择 |
| 8 | Open_Two_Both | 同时打开 |
| 267 | Close_Two_Both | 同时关闭 |
| 398 | Open_Help | 打开帮助 |
| 43 | Close_Help | 关闭帮助 |
| 393 | Ask_Answer_Words | 询问修改应答词 |
| 289 | Get_Answer | 修改为指定应答词 |
| 417 | Delete_Answer_Words | 删除应答词 |

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
