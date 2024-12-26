from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.states import AgentState
from handlers.users.start_functions_and_start_filters import registered_users
from handlers.users.db import find_in_db
from handlers.users.handlers.agent_handlers.agent_events import start_admin
from loader import dp
from data.config import lang


@dp.callback_query_handler(lambda c: c.data == "SendMailingButton")
async def update_information_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AgentState.send_mailing.state)
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("send_mailing")
    model_ids = registered_users()
    
    for id in model_ids:
        model = find_in_db(collection_name="Model", data={"telegram_id": int(id)})
        if model and model.get("agent_telegram_id") == call.from_user.id:
            await dp.bot.send_message(chat_id=id, text=l10.get("text"))
    await call.message.delete()
    await call.message.answer(lang.get("agents").get("start_agent").get("success"))
    await start_admin(call.message, state)
