from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.admin_functions import start_admin
from handlers.users.functions import start, banned_users, start_banned, start_login, registered_users, admins
from loader import dp


@dp.message_handler(commands="start", user_id=banned_users(), state=["*"])
async def user_start_banned(message: types.Message, state: FSMContext):
    await start_banned(message, state)


@dp.message_handler(commands="start", user_id=registered_users(), state=["*"])
async def user_start_login(message: types.Message, state: FSMContext):
    await start_login(message, state)


@dp.message_handler(commands="start", user_id=admins(), state=["*"])
async def admin_start(message: types.Message, state: FSMContext):
    await start_admin(message=message, state=state)


@dp.message_handler(commands="start", state=["*"])
async def user_start_registration(message: types.Message, state: FSMContext):
    await start(message, state)

