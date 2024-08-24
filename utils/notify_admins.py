import logging

from aiogram import Dispatcher

# from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(617710378, "Бот Запущен и готов к работе")
    pass
    # for admin in admins:
    #     try:
    #         await dp.bot.send_message(admin, "Бот Запущен и готов к работе")
    #
    #     except Exception as err:
    #         logging.exception(err)
