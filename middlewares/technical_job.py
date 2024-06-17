import datetime
from typing import Any

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import lang

blocked_interval_start = datetime.time(5, 0)
blocked_interval_end = datetime.time(12, 45)


class BlockHandlersMiddleware(BaseMiddleware):
    def is_technical_job(self):
        current_time = datetime.datetime.now().time()
        if blocked_interval_start <= current_time <= blocked_interval_end:
            return True
        return False

    async def on_process_message(
            self, event: types.Message, data: dict) -> Any:

        if self.is_technical_job():
            await event.answer(lang.get("ukr").get("start_not_access"))
            raise CancelHandler()
            

        return
