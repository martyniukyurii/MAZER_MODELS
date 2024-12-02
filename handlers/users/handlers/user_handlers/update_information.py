import pycountry
from aiogram import types
from aiogram.dispatcher import FSMContext
from transliterate import translit

from data.config import lang
from handlers.users.db import save_to_db, find_in_db, update_to_db
from handlers.users.start_functions_and_start_filters import login_start
from handlers.users.handlers.agent_handlers.agent_events import send_register_notification_to_agents, \
    send_notification_to_agent
from handlers.users.handlers.user_handlers.registration import register_information, registration_handler, \
    please_wait_registration
from handlers.users.methods.hair_color import get_hair_code, get_hair_description
from handlers.users.states import UserState
from loader import dp


# Хендлер обробки кнопки з головного меню
@dp.callback_query_handler(lambda c: c.data == "UpdateInformationButton")
async def update_information_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.registration.state)
    await call.message.delete()
    data = await state.get_data()
    register_data = data.get("register_data")

    if not register_data:
        await state.update_data({"register_data": {}})

    await registration_handler(message=call.message, state=state, is_information=False)

#Хендлер який обробляє інлайн кнопки для зміни данних
@dp.callback_query_handler(state=UserState.update_information)
async def update(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await pop_from_register_state(call, state)


#Хендлер який обробляє просту кнопку для завершення змін і надсилання в БД
@dp.message_handler(state=UserState.update_information)
async def finish_update_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    l10 = lang.get(data.get("language")).get("start_user").get("register_user")
    if message.text == l10.get("registration_send_data").get("keyboard").get("SendRegistrationSubmitButton"):
        await state.reset_state(with_data=False)
        await message.bot.delete_message(message_id=data.get("message_to_delete"), chat_id=message.chat.id)
        # Деякі перетворення змінних
        register_data: dict = data.get("register_data")

        if data.get("language") == "eng":
            full_name_eng = register_data.get("B_full_name")
            full_name_ukr = translit(register_data.get("B_full_name"), 'uk')
        else:
            full_name_ukr = register_data.get("B_full_name")
            full_name_eng = translit(register_data.get("B_full_name"), 'uk', reversed=True)

        citizenship = pycountry.countries.get(alpha_2=register_data.get("C_citizenship").replace(":", ""))

        height = float(register_data.get("E_height"))
        bust = float(register_data.get("F_bust"))
        waist = float(register_data.get("G_waist"))
        hips = float(register_data.get("H_hips"))
        shoe_size = float(register_data.get("I_shoe_size"))

        hair_code = get_hair_code(text=register_data.get("J_hair_color"), language=data.get("language"))

        phone_number = register_data.get("A_phone_number")
        email = register_data.get("D_email")
        links = register_data.get("K_links")

        is_user_registered = data.get("is_user_registered")
        await message.answer(l10.get("registration_finish").get("text"), reply_markup=types.ReplyKeyboardRemove())
        if is_user_registered:
            await update_to_db(collection_name="Model", parameter={"telegram_id": message.chat.id},
                               data={
                                   "telegram_id": message.chat.id,
                                   "full_name_eng": full_name_eng,
                                   "full_name_ukr": full_name_ukr,
                                   "phone_number": phone_number,
                                   "email": email,
                                   "citizenship": citizenship.name,
                                   "height": height,
                                   "bust": bust,
                                   "waist": waist,
                                   "hips": hips,
                                   "shoe_size": shoe_size,
                                   "hair_code": hair_code,
                                   "links": links
                               })
            if data.get("agent_telegram_id"):
                deleted_data_stack: dict = data.get("deleted_data_stack")
                k: dict = lang.get("ukr").get("update_your_information").get("keyboard")
                old_new = "\n".join([f"{k[key]}': {deleted_data_stack[key]} -> {register_data[key]}" for key in deleted_data_stack.keys() & register_data.keys()])
                text_event = (f"Модель змінила {message.chat.id} свої особисті дані:\n"
                              f"{old_new}")


                await send_notification_to_agent(agent_id=data.get("agent_telegram_id"),
                                                 event=text_event)

            await login_start(message, state)
        else:
            await save_to_db(collection_name="InQueue", data={
                "language": data.get("language"),
                "telegram_id": message.chat.id,
                "telegram_name": message.chat.full_name,
                "telegram_username": message.chat.username,
                "balance": 0,
                "full_name_eng": full_name_eng,
                "full_name_ukr": full_name_ukr,
                "phone_number": phone_number,
                "email": email,
                "citizenship": citizenship.name,
                "height": height,
                "bust": bust,
                "waist": waist,
                "hips": hips,
                "shoe_size": shoe_size,
                "hair_code": hair_code,
                "links": links
            })

            await send_register_notification_to_agents(model_telegram_id=message.chat.id,
                                                       )

            await please_wait_registration(message, state)





# Функція яка видаляє вибраний юзером елемент і перекидає на форму вводу
async def pop_from_register_state(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_user_registered = data.get("is_user_registered")
    if is_user_registered:
        register_data: dict = {}

        user = await find_in_db(collection_name="Model", data={"telegram_id": call.message.chat.id})
        register_data.update({
            "A_phone_number": user.get("phone_number"),
            "B_full_name": user.get("full_name_eng") if data.get("language") == "eng" else user.get("full_name_ukr"),
            "C_citizenship": pycountry.countries.get(name=user.get("citizenship")).alpha_2,
            "D_email": user.get("email"),
            "E_height": user.get("height"),
            "F_bust": user.get("bust"),
            "G_waist": user.get("waist"),
            "H_hips": user.get("hips"),
            "I_shoe_size": user.get("shoe_size"),
            "K_links": user.get("links"),
            "J_hair_color": get_hair_description(code=user.get("hair_code"),
                                                 language=data.get("language"))
        })

        await state.update_data({"agent_telegram_id": user.get("agent_telegram_id")})


    else:
        register_data: dict = data.get("register_data")

    deleted_data_stack = {} if not data.get("deleted_data_stack") else data.get("deleted_data_stack")
    deleted_data_stack.update({call.data: register_data[call.data]})

    register_data.pop(call.data)
    await state.update_data({"register_data": register_data, "deleted_data_stack": deleted_data_stack})

    await state.set_state(UserState.registration.state)
    await register_information(message=call.message, state=state, is_information=False)


