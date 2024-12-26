from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.handlers.agent_handlers.agent_events import start_admin
from handlers.users.start_functions_and_start_filters import (
    registration_start,
    banned_users,
    start_banned,
    login_start,
    registered_users,
    admins,
    inqueue_users,
    inqueue_start,
)
from loader import dp


@dp.message_handler(commands="start", state="*")
async def user_start_registration(message: types.Message, state: FSMContext):
    user_id = message.chat.id

    if user_id in banned_users():
        await start_banned(message, state)
    elif user_id in admins():
        await start_admin(message=message, state=state)
    elif user_id in inqueue_users():
        await inqueue_start(message=message, state=state)
    elif user_id in registered_users():
        await login_start(message, state)
    else:
        await registration_start(message, state)
