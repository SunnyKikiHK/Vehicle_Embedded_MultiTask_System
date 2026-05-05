# User Profile Agent — Reference

## Intent to MCP Tool Mapping

**Note:** User Profile Agent intents primarily handle voice/TTS settings. Most of these don't map directly to MCP tools but are handled through the voice assistant configuration service. The examples below use `show_notification` as a placeholder - actual implementation would call voice-specific APIs.

|| Intent Key | Tool Name | Arguments | Intent Name (CN) |
||-----------|-----------|-----------|-----------------|
|| Set_Timbre_Female | show_notification | `{"title": "语音设置", "content": "已切换到女声"}` | 设置为女声 |
|| Only_Main | show_notification | `{"title": "语音设置", "content": "已设置仅主驾可唤醒"}` | 仅主驾可唤醒 |
|| Set_Voice | show_notification | `{"title": "语音设置", "content": "已切换音色"}` | 设置为指定音色 |
|| Set_Speech_By_Speed | show_notification | `{"title": "语音设置", "content": "语速已调整"}` | 设置语速 |
|| Open_Sds_Config | show_notification | `{"title": "设置", "content": "语音设置已打开"}` | 打开语音设置 |
|| Close_Voice_Wakeup | show_notification | `{"title": "语音设置", "content": "语音唤醒已关闭"}` | 关闭语音唤醒 |
|| Open_Continuous_Dialogue | show_notification | `{"title": "语音设置", "content": "连续对话已开启"}` | 开启连续对话 |
|| Close_Continuous_Dialogue | show_notification | `{"title": "语音设置", "content": "连续对话已关闭"}` | 关闭连续对话 |

## Shared Slot Type Definitions

### Voice
```
enum: 小德, 小晴, 小宇, 小雅, 磁性男声, 温柔女声, 活泼童声
resolution: Map to available voice pack. Default to 小德.
agents: User Profile Agent
```

### Wake
```
value_range: 2-8 characters, Chinese or alphanumeric
resolution: Validate wake word uniqueness and availability. Default to "小德小德".
agents: User Profile Agent
```

### Style
```
enum: 活力, 温柔, 正式, 活泼, 磁性, 沉稳
resolution: Map to TTS style parameter. Default to 正式.
agents: User Profile Agent
```

### Speed
```
value_range: 50-200 (percentage of normal speed)
resolution: Normalize to percentage. Default to 100.
agents: User Profile Agent
```

### Time
```
value_range: 1-30 minutes
resolution: Continuous dialogue session duration in minutes. Default to 5.
agents: User Profile Agent
```

## Timbre Options

|| Timbre | Voice Pack | Gender | Character |
|--------|-----------|--------|--------|
| 女声 | 小晴, 小雅 | Female | Warm, gentle |
| 男声 | 小德, 小宇 | Male | Deep, clear |
| 童声 | 小萌 | Child | Playful, high pitch |
| 默认 | 小德 | Male | Standard |

## Wake Word Rules

- Minimum 2 characters, maximum 8 characters
- Can use Chinese characters or pinyin letters
- Must not be a common phrase that could trigger accidentally
- Wake word takes effect after confirmation and training

## Continuous Dialogue Session

When enabled, the assistant remains active for `Time` minutes without needing to say the wake word again. Session resets on each successful exchange.
