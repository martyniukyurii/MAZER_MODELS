import asyncio

from aiogram.contrib.middlewares.logging import LoggingMiddleware

# from handlers.users.db import create_database
from middlewares.technical_job import BlockHandlersMiddleware
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)
    # await create_database()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)


