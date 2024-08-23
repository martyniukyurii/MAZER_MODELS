from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang


async def set_up_the_call():
    pass


async def start_admin(message: types.Message, state: FSMContext):
    await message.answer(lang.get('ukr').get('start_banned'))