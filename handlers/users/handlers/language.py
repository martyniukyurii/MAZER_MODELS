from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang
from handlers.users.start_functions_and_start_filters import registration_start, registered_users, login_start
from handlers.users.states import UserState
from loader import dp


@dp.callback_query_handler(state=UserState.language)
async def language_is_chooses(call: types.CallbackQuery, state: FSMContext):
    await language_choose(call, state)


async def language_choose(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ukr" or call.data == "eng":
        await state.update_data({"language": call.data})
        await call.message.edit_text(
            lang.get(call.data).get("start_user").get("language_chooses").get("text").format(lang=call.data))
    await state.reset_state(with_data=False)
    if call.message.chat.id in registered_users():
        await login_start(message=call.message, state=state)
    else:
        await registration_start(message=call.message, state=state)