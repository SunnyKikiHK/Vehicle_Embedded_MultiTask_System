# User Profile Agent — Reference

## Intent ID Map

| Intent ID | Intent Key | Intent Name (CN) |
|-----------|-----------|-----------------|
| 75 | Set_Timbre_Female | 设置为女声 |
| 76 | Only_Main | 仅主驾可唤醒 |
| 315 | Main_And_Vice | 主副驾可唤醒 |
| 20 | Change_Timbre | 切换音色 |
| 406 | Set_Timbre_Male | 设置为男声 |
| 302 | Set_Timbre_Child | 设置为童声 |
| 239 | Set_Timbre_Default | 设置为默认 |
| 116 | Set_Voice | 设置为指定音色 |
| 292 | Set_Voice_Style | 切换语音风格 |
| 286 | Set_Speech_By_Speed | 设置语速 |
| 129 | Set_Wakeup_Words | 修改为指定唤醒词 |
| 216 | Ask_Wakeup_Words | 询问修改唤醒词 |
| 362 | Delete_Wakeup_Words | 删除唤醒词 |
| 349 | Open_Free_Wakeup | 开启免唤醒 |
| 331 | Close_Free_Wakeup | 关闭免唤醒 |
| 388 | Open_Continuous_Dialogue | 开启连续对话 |
| 310 | Close_Continuous_Dialogue | 关闭连续对话 |
| 391 | Set_Continuous_Dialogue | 设置对话时长 |
| 415 | Open_Online_NLU | 打开在线语音 |
| 333 | Close_Online_NLU | 关闭在线语音 |
| 256 | Open_Sds_Config | 打开语音设置 |
| 390 | Close_Sds_Config | 关闭语音设置 |
| 41 | View_Learning_Content | 查看交互式学习 |
| 254 | Open_Interactive_Learning | 打开交互学习 |
| 361 | Close_Interactive_Learning | 关闭交互学习 |
| 111 | Open_Training_Camp | 打开语音训练营 |
| 224 | Close_Training_Cmap | 关闭语音训练营 |
| 212 | Open_Skill_Instruction | 打开语音技能介绍 |
| 218 | Close_Skill_Instruction | 关闭语音技能介绍 |
| 420 | Open_Voice_Wakeup | 打开语音唤醒 |
| 242 | Close_Voice_Wakeup | 关闭语音唤醒 |
| 409 | Open_Safety_Alarm | 打开安全提醒 |
| 77 | Close_Safety_Alarm | 关闭安全提醒 |

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
agents: User Profile Agent, User Profile Agent (continuous dialogue)
```

## Timbre Options

| Timbre | Voice Pack | Gender | Character |
|--------|-----------|--------|-----------|
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
