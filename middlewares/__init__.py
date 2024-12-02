from aiogram import Dispatcher

# from .technical_job import BlockHandlersMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    # dp.middleware.setup(BlockHandlersMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
