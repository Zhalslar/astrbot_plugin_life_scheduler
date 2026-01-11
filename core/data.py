import datetime
from dataclasses import dataclass
from typing import Literal, Union

# =========================
# 类型定义
# =========================

ScheduleStatus = Literal["ok", "failed"]

DateLike = Union[  # noqa: UP007
    datetime.datetime,
    datetime.date,
    int,  # timestamp
    float,  # timestamp
]


# =========================
# 工具函数（时间归一化）
# =========================


def to_date_str(value: DateLike) -> str:
    """统一将时间输入转为 yyyy-mm-dd 字符串"""
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, int | float):
        return datetime.datetime.fromtimestamp(value).date().isoformat()
    raise TypeError(f"Unsupported date type: {type(value)}")


# =========================
# 数据结构
# =========================


@dataclass(slots=True)
class ScheduleData:
    """单日数据（date 只作为内部 key，不对外暴露格式责任）"""

    date: str  # yyyy-mm-dd
    outfit: str = ""
    schedule: str = ""
    status: ScheduleStatus = "ok"


# =========================
# 数据管理器（纯存取）
# =========================


class ScheduleDataManager:
    """纯数据层，只负责存取"""

    def __init__(self):
        self._data: dict[str, ScheduleData] = {}

    def has(self, date: DateLike) -> bool:
        return to_date_str(date) in self._data

    def get(self, date: DateLike) -> ScheduleData | None:
        return self._data.get(to_date_str(date))

    def set(self, data: ScheduleData) -> None:
        self._data[data.date] = data

    def remove(self, date: DateLike) -> None:
        self._data.pop(to_date_str(date), None)

    def all(self) -> dict[str, ScheduleData]:
        return dict(self._data)


