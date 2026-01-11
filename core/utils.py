
import datetime
from dataclasses import dataclass, field


def time_desc(h=None):
    """返回中文时段：深夜/清晨/上午/中午/下午/晚上"""
    h = (h or datetime.datetime.now().hour) % 24
    return (
        "深夜"
        if h < 6
        else "清晨"
        if h < 9
        else "上午"
        if h < 12
        else "中午"
        if h < 14
        else "下午"
        if h < 18
        else "晚上"
        if h < 22
        else "深夜"
    )


@dataclass
class ChatReference:
    umo: str  # unified_msg_origin
    count: int = 20

    @staticmethod
    def from_dict(data: dict) -> "ChatReference":
        if not isinstance(data, dict):
            return ChatReference(umo="")
        return ChatReference(
            umo=str(data.get("umo", "")), count=int(data.get("count", 20))
        )

    def to_dict(self) -> dict:
        return {"umo": self.umo, "count": self.count}


@dataclass
class SchedulerConfig:
    schedule_time: str = "07:00"
    reference_history_days: int = 3
    reference_chats: list[ChatReference] = field(default_factory=list)
    prompt_template: str = """# Role: Life Scheduler
请根据以下信息，为自己规划一份今天的生活安排。请代入你的人设，生成的内容应富有生活气息和独特性。

## Context
- 日期：{date_str} {weekday} {holiday}
- 人设：{persona_desc}

## 🎲 今日创意约束（必须遵循）
- 今日主题：【{daily_theme}】- 请围绕这个主题安排今天的主要活动
- 心情色彩：【{mood_color}】- 今天的整体情绪基调，影响穿搭和活动选择
- 推荐穿搭风格：【{outfit_style}】- 今天的穿搭应该偏向这个风格
- 日程类型：【{schedule_type}】- 今天的日程安排应该偏向这个类型

## ⚠️ 多样性要求（重要）
1. **穿搭必须具体且独特**：不要用"修身针织裙"这种泛泛的描述，要有具体的颜色、款式、搭配细节
2. **日程必须有亮点**：每天至少有一个与众不同的活动或小确幸
3. **避免重复模式**：不要总是"早起-家务-午餐-下午茶-等主人回来"的固定套路

## 🚫 需要避免的重复内容
以下是最近几天的安排，今天必须有明显差异，不要重复相似的穿搭和活动：
{history_schedules}

## 💡 参考信息
- 近期对话记忆（可以从中获取灵感）：
{recent_chats}

## Tasks
1. outfit: 设计今日穿搭。{outfit_desc}请基于【{outfit_style}】风格，但要有创意变化。
2. schedule: 规划今日日程。围绕【{daily_theme}】主题和【{schedule_type}】类型，融入【{mood_color}】的情绪色彩。

## Output Format
请务必严格遵循 JSON 格式返回，不要包含 Markdown 代码块标记（如 ```json），也不要包含任何额外的解释文本。
格式如下：
{{
    "outfit": "具体描述今日穿搭（包含颜色、款式、配饰等细节）",
    "schedule": "生动描述今日日程（要有故事感和画面感，避免流水账）"
}}
"""
    outfit_desc: str = "具体描述颜色、款式、材质和搭配细节，让穿搭有画面感。"

    @staticmethod
    def from_dict(data: dict) -> "SchedulerConfig":
        config = SchedulerConfig()
        if not isinstance(data, dict):
            return config

        config.schedule_time = data.get("schedule_time", "07:00")
        config.reference_history_days = data.get("reference_history_days", 3)

        refs = data.get("reference_chats", [])
        if isinstance(refs, list):
            config.reference_chats = [
                ChatReference.from_dict(r) for r in refs if isinstance(r, dict)
            ]

        if "prompt_template" in data:
            config.prompt_template = data["prompt_template"]
        if "outfit_desc" in data:
            config.outfit_desc = data["outfit_desc"]

        return config

    def to_dict(self) -> dict:
        return {
            "schedule_time": self.schedule_time,
            "reference_history_days": self.reference_history_days,
            "reference_chats": [r.to_dict() for r in self.reference_chats],
            "prompt_template": self.prompt_template,
            "outfit_desc": self.outfit_desc,
        }



