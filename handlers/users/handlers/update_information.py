from aiogram import types
from aiogram.dispatcher import FSMContext


from data.config import lang
from handlers.users.functions import create_inline_keyboard_from_dict


async def update_information(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("update_your_information")
    await call.message.edit_text(l10.get("text"),
                                 reply_markup=create_inline_keyboard_from_dict(keyboard_dict=l10.get("keyboard")))