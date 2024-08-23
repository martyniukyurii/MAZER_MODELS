import re

import flag
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang
from handlers.users.functions import create_keyboard_from_dict
from handlers.users.handlers.update_information import update_information
from handlers.users.states import UserState
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "UpdateInformationButton")
async def update_information_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.registration.state)
    await update_information(call, state)
    data = await state.get_data()
    register_data = data.get("register_data")
    if not register_data:
        await state.update_data({"register_data": {}})

    await registration(message=call.message, state=state, is_information=False)


@dp.message_handler(state=UserState.registration, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def registration(message: types.Message, state: FSMContext, is_information: bool = True):
    await register_information(message, state, is_information)


async def register_information(message: types.Message, state: FSMContext, is_information=True):
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("start_user").get("register_user")
    print(data)
    register_data: dict = data.get("register_data")
    common_keys = sorted(set(l10.keys()) - set(register_data.keys()))
    print(common_keys)
    for key in common_keys:
        if is_information:
            pattern = l10.get(key).get("regex")
            text = message.text

            if message.contact:
                text = message.contact.phone_number

            text = flag.dflagize(text, subregions=False)
            if re.match(pattern, text):
                await message.answer(l10.get(key).get("success"))

                register_data.update({key: text})
                await state.update_data({"register_data": register_data})
                
                is_information = False
                continue
            else:
                await message.answer(l10.get(key).get("error"))

                break
        if l10.get(key).get("keyboard") != {}:

            await message.answer(l10.get(key).get("text"),
                                 reply_markup=create_keyboard_from_dict(l10.get(key).get("keyboard")))
            if l10.get(key) == "L_confirm":
                pass
        else:
            await message.answer(l10.get(key).get("text"),
                                 reply_markup=types.ReplyKeyboardRemove())
            if l10.get(key) == "L_confirm":
                pass
        break
    else:
        await message.answer("Finish")
