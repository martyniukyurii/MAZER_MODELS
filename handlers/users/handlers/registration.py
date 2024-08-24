import re

import flag
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import lang
from handlers.users.functions import create_keyboard_from_dict, create_inline_keyboard_from_dict
from handlers.users.states import UserState
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "UpdateInformationButton")
async def update_information_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.registration.state)
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
    l10 = lang.get(data.get("language")).get("start_user").get("register_user").get("registration_steps")
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
        else:
            await message.answer(l10.get(key).get("text"),
                                 reply_markup=types.ReplyKeyboardRemove())
        break
    else:
        await message.answer(
            lang.get(data.get("language")).get("start_user").get("register_user").get("registration_finish"),
            reply_markup=types.ReplyKeyboardMarkup())

        # await message.answer(lang.get(data.get("language")).get("update_your_information").get("text").format(
        #     full_name=register_data.get("B_full_name"),
        #     phone_number=register_data.get("A_phone_number"),
        #     email=register_data.get("D_email"),
        #     citizenship=f'{register_data.get("C_citizenship")} {flag.flag(register_data.get("citizenship"))}',
        #     height=register_data.get("E_height"),
        #     bust=register_data.get("F_bust"),
        #     waist=register_data.get("G_waist"),
        #     hips=register_data.get("H_hips"),
        #     shoe_size=register_data.get("I_shoe_size"),
        #     hair_color=register_data.get("J_hair_color")
        # ),
        #     reply_markup=create_inline_keyboard_from_dict(lang.get(data.get("language")).get("update_your_information").get("keyboard")))
        #
        # await state.set_state(UserState.update_information.state)
