import zoneinfo
from collections.abc import Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.star.context import Context

TaskCallable = Callable[[], Awaitable[object | None]]

class LifeScheduler:
    def __init__(
        self,
        context: Context,
        config: AstrBotConfig,
        task: TaskCallable,
    ):
        self.task = task
        tz = context.get_config().get("timezone")
        self.timezone = (
            zoneinfo.ZoneInfo(tz) if tz else zoneinfo.ZoneInfo("Asia/Shanghai")
        )
        self.scheduler = AsyncIOScheduler(timezone=self.timezone)
        self.schedule_time = config["schedule_time"]
        self.job = None

    def start(self):
        try:
            hour, minute = map(int, self.schedule_time.split(":"))
            self.job = self.scheduler.add_job(
                self.task,
                "cron",
                hour=hour,
                minute=minute,
                id="daily_schedule_gen",
            )
            self.scheduler.start()
            logger.info(f"Life Scheduler started at {self.schedule_time}")
        except Exception as e:
            logger.error(f"Failed to setup scheduler: {e}")

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()

    def update_schedule_time(self, new_time: str):
        if new_time == self.schedule_time:
            return

        try:
            hour, minute = map(int, self.schedule_time.split(":"))
            self.schedule_time = new_time
            if self.job:
                self.job.reschedule("cron", hour=hour, minute=minute)
                logger.info(f"Life Scheduler rescheduled to {hour}:{minute}")
        except Exception as e:
            logger.error(f"Failed to update scheduler: {e}")
