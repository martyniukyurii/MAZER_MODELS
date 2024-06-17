import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import lang
# from handlers.users.db import search
from handlers.users.functions import start
from loader import dp



@dp.message_handler()
async def error(message: types.Message, state: FSMContext):
    await start(message, state)
