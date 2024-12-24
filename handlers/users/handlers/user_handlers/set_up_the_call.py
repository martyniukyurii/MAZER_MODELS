from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start_functions_and_start_filters import login_start
from handlers.users.handlers.agent_handlers.agent_events import (
    send_notification_to_agent,
)
from handlers.users.db import find_in_db

from data.config import lang
from handlers.users.states import UserState
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "SetUpTheCallButton")
async def set_up_the_call_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.set_up_the_call.state)
    await call.message.delete()
    await set_up_the_call(call.message, state)


async def set_up_the_call(message: types.Message, state: FSMContext):
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("set_up_the_call")
    await message.answer(
        l10.get("text"),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        l10.get("keyboard").get("AgentButton"),
                        callback_data="AgentButton",
                    ),
                    types.InlineKeyboardButton(
                        l10.get("keyboard").get("OwnerButton"),
                        callback_data="OwnerButton",
                    ),
                ]
            ],
        ),
    )


@dp.callback_query_handler(
    lambda c: c.data in ["AgentButton", "OwnerButton"], state=UserState.set_up_the_call
)
async def finish_set_up_the_call(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    model = await find_in_db(
        collection_name="Model", data={"telegram_id": call.message.chat.id}
    )
    text_event = f"Модель {model.get('full_name_eng')} хоче зв'язатися з вами"

    if call.data == "AgentButton":
        agent = await find_in_db(
            collection_name="Agent", data={"telegram_id": model.agent_telegram_id}
        )
        await send_notification_to_agent(
            agent_id=agent.get("telegram_id"), event=text_event
        )
    elif call.data == "OwnerButton":
        owner = await find_in_db(collection_name="Agent", data={"ownership": True})
        await send_notification_to_agent(
            agent_id=owner.get("telegram_id"), event=text_event
        )

    await call.message.answer(
        lang.get(data.get("language")).get("set_up_the_call").get("success")
    )
    await login_start(message=call.message, state=state)
