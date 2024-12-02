from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang
from handlers.users.db import find_in_db, save_to_db, delete_from_db
from handlers.users.start_functions_and_start_filters import admins
from keyboards.inline.inline_keyboard import create_inline_keyboard_from_dict
from loader import dp


# Хендлер який відловлює кнопку з відповіддю адміна, чи взяв він собі модель чи ні
@dp.callback_query_handler(lambda c: c.data.startswith("register_model"),
                           user_id=admins(), state=["*"])
async def register_model(call: types.CallbackQuery, state: FSMContext):
    model_telegram_id = int(call.data.split(":")[1])
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("agent_events").get("register_model")
    await call.message.edit_text(l10.get("text"))
    model = await find_in_db(collection_name="InQueue", data={"telegram_id": model_telegram_id})
    if model:
        model = dict(model)
        model.update({"agent_telegram_id": call.message.chat.id})
        await save_to_db(collection_name="Model", data=model)
        await delete_from_db(collection_name="InQueue", data={"telegram_id": model_telegram_id})

        await call.message.edit_text(l10.get("success").format(
            model_id=model.get("telegram_id"),
            name=model.get("full_name_eng"),
            username=model.get("telegram_username"))
        )
    else:
        await call.message.edit_text("цю модель вже хтось зареэстрував")



async def set_up_the_call():
    pass


async def start_admin(message: types.Message, state: FSMContext):
    l10 = lang.get('agents').get('start_agent')
    await message.answer(l10.get("text"),
                         reply_markup=create_inline_keyboard_from_dict(l10.get("keyboard")))
    await state.set_state()



async def send_notification_to_agent(agent_id, event):
    await dp.bot.send_message(
        chat_id=agent_id,
        text=event
    )

async def send_register_notification_to_agents(model_telegram_id):
    l10 = lang.get("agents").get("send_register_notification_to_agents")
    for admin in admins():
        await dp.bot.send_message(admin, l10.get("text").format(model_telegram_id=model_telegram_id),
                                  reply_markup=types.InlineKeyboardMarkup(
                                      inline_keyboard=create_inline_keyboard_from_dict({
                                          f"register_model:{model_telegram_id}": l10.get("keyboard").get("RegisterModel")
                                      })
                                  ))
