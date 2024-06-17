from aiogram import types
from aiogram.dispatcher import FSMContext

# from data.config import admins
from handlers.users.functions import start
from loader import dp


@dp.message_handler(commands="start")
async def user_start(message: types.Message, state: FSMContext):
    await start(message=message, state=state)


# @dp.message_handler(commands="start", user_id=admins)
# async def admin_start(message: types.Message, state: FSMContext):
#     await start(message=message, state=state)
#     # TODO convertors to db, and give access to users
