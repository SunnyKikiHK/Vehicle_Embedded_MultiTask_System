---
name: user-profile-agent
description: Implements User Profile Agent intents in the vehicle embedded multi-task system. Handles voice assistant personalization: wake words, timbre, speech speed, dialogue mode, continuous dialogue, and voice training. Use when the user mentions voice settings, wake word, timbre, voice, speech speed, wake up, continuous dialogue, or voice training. Trigger terms: 唤醒词, 音色, 语速, 免唤醒, 连续对话, 语音设置, 声音, 男声, 女声, 童声.
---

# User Profile Agent — Voice Assistant Personalization Skill

## Agent Overview

**Handles:** Voice assistant personalization: wake words, timbre, speech speed, dialogue mode, continuous dialogue, and voice training/onboarding.
**Total intents: 35**
**Shared slot types:** `Wake`, `Voice`, `Style`, `Speed`, `Time`

## Core Intent Categories

### Voice Timbre

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置为女声 | Set_Timbre_Female | — | Set female voice |
| 设置为男声 | Set_Timbre_Male | — | Set male voice |
| 设置为童声 | Set_Timbre_Child | — | Set child voice |
| 设置为默认 | Set_Timbre_Default | — | Reset to default voice |
| 切换音色 | Change_Timbre | — | Switch voice timbre |
| 设置为指定音色 | Set_Voice | Voice | Set a specific voice preset |
| 切换语音风格 | Set_Voice_Style | Style | Switch voice style (e.g., energetic, calm) |

### Wake Word

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 修改为指定唤醒词 | Set_Wakeup_Words | Wake | Set custom wake word |
| 询问修改唤醒词 | Ask_Wakeup_Words | — | Ask about wake word modification |
| 删除唤醒词 | Delete_Wakeup_Words | — | Delete custom wake word |
| 开启免唤醒 | Open_Free_Wakeup | — | Enable continuous listening (no wake word) |
| 关闭免唤醒 | Close_Free_Wakeup | — | Disable continuous listening |

### Dialogue Mode

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 开启连续对话 | Open_Continuous_Dialogue | — | Enable multi-turn dialogue |
| 关闭连续对话 | Close_Continuous_Dialogue | — | Disable multi-turn dialogue |
| 设置对话时长 | Set_Continuous_Dialogue | Time | Set dialogue session duration |

### Wake-up Configuration

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 仅主驾可唤醒 | Only_Main | — | Only driver can wake assistant |
| 主副驾可唤醒 | Main_And_Vice | — | Both driver and passenger can wake |

### Speech Settings

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 设置语速 | Set_Speech_By_Speed | Speed | Set TTS speech rate |

### Online/Cloud NLU

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开在线语音 | Open_Online_NLU | — | Enable cloud NLU processing |
| 关闭在线语音 | Close_Online_NLU | — | Disable cloud NLU |

### Settings App

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开语音设置 | Open_Sds_Config | — | Open voice assistant settings |
| 关闭语音设置 | Close_Sds_Config | — | Close voice settings |

### Learning & Training

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 查看交互式学习 | View_Learning_Content | — | View interactive learning content |
| 打开交互学习 | Open_Interactive_Learning | — | Open interactive tutorial |
| 关闭交互学习 | Close_Interactive_Learning | — | Close interactive tutorial |
| 打开语音训练营 | Open_Training_Camp | — | Open voice training camp |
| 关闭语音训练营 | Close_Training_Cmap | — | Close voice training camp |
| 打开语音技能介绍 | Open_Skill_Instruction | — | Open skill introduction |
| 关闭语音技能介绍 | Close_Skill_Instruction | — | Close skill introduction |

### Safety & Alerts

| Intent | Key | Slots | Description |
|--------|-----|-------|-------------|
| 打开语音唤醒 | Open_Voice_Wakeup | — | Enable voice wake |
| 关闭语音唤醒 | Close_Voice_Wakeup | — | Disable voice wake |
| 打开安全提醒 | Open_Safety_Alarm | — | Enable safety alerts |
| 关闭安全提醒 | Close_Safety_Alarm | — | Disable safety alerts |

## Slot Resolution Rules

- **Voice**: Named voice preset (e.g., `小德`, `小晴`, `小宇`). Resolve against available voice packs.
- **Wake**: Custom wake word string. Min 2 characters, max 8. Alphanumeric + Chinese characters.
- **Style**: Voice style: `活力`, `温柔`, `正式`, `活泼`, `磁性`. Default to `正式`.
- **Speed**: TTS speed as percentage: `50%`–`200%`. Default to `100%`.
- **Time**: For continuous dialogue session duration: in minutes. Range 1–30 min. Default to 5 min.
- When **user changes timbre**, confirm the new voice by speaking a sample phrase.

## Implementation Checklist

When implementing a new User Profile intent:

1. **Match the intent key** (e.g., `Set_Timbre_Female`) to the skill function.
2. **Execute the setting change** via the voice assistant config API.
3. **Confirm the change** with a natural response, optionally speaking a sample phrase.
4. **Save SlotContext** to Redis with `agent=User Profile Agent`, `intent=<matched_intent>`, and extracted slots.
5. **Persist the setting** in the user profile for session persistence.

## Response Templates

```
女声: "已切换到女声。"
男声: "已切换到男声。"
童声: "已切换到童声。"
自定义音色: "已切换到{voice}音色。"
语速: "语速已调整为{speed}。"
免唤醒开: "免唤醒已开启，无需说唤醒词即可对话。"
连续对话开: "连续对话已开启，可连续对话{time}分钟。"
唤醒词设置: "唤醒词已设置为{wake}。"
```

## Additional Resources

- Full intent table and intent ID map: [reference.md](reference.md)
- Annotated conversation examples: [examples.md](examples.md)
