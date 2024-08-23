import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import lang
from handlers.users.functions import start, language_choose
from handlers.users.states import UserState
from loader import dp


@dp.callback_query_handler(state=UserState.language)
async def language_is_chooses(call: types.CallbackQuery, state: FSMContext):
    await language_choose(call, state)


# @dp.message_handler()
# async def error(message: types.Message, state: FSMContext):
#     await message.answer("SomeError")
#     await start(message, state)
