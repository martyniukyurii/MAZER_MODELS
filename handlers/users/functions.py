from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang
from handlers.users.states import UserState


async def start(message: types.Message, state: FSMContext):
    await message.answer(lang.get('ukr').get('start_user'))
    # await UserState.search.set()


async def is_user_registered() -> bool:
    pass


async def is_user_banned() -> bool:
    pass


async def send_notification_to_agent():
    pass



