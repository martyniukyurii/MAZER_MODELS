import pycountry
from aiogram import types
from aiogram.dispatcher import FSMContext
from pymongo import MongoClient

from data.config import lang, DB_NAME
from handlers.users.db import uri, find_in_db
from handlers.users.handlers.user_handlers.registration import registration_handler, please_wait_registration
from handlers.users.methods.hair_color import get_hair_description
from handlers.users.states import UserState


async def start_banned(message: types.Message, state: FSMContext):
    await message.answer(lang.get('ukr').get('start_banned'),
                         reply_markup=types.ReplyKeyboardRemove())


async def login_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    user = await find_in_db(collection_name="Model", data={"telegram_id": message.chat.id})
    register_data = {}
    register_data.update({
        "A_phone_number": user.get("phone_number"),
        "B_full_name": user.get("full_name_eng") if user.get("language") == "eng" else user.get("full_name_ukr"),
        "C_citizenship": pycountry.countries.get(name=user.get("citizenship")).alpha_2,
        "D_email": user.get("email"),
        "E_height": user.get("height"),
        "F_bust": user.get("bust"),
        "G_waist": user.get("waist"),
        "H_hips": user.get("hips"),
        "I_shoe_size": user.get("shoe_size"),
        "K_links": user.get("links"),
        "J_hair_color": get_hair_description(code=user.get("hair_code"),
                                             language=user.get("language"))
    })
    await state.update_data({"register_data": register_data,
                             "language": user.get("language"),
                             "is_user_registered": True})

    if not user.get("language"):
        await message.answer("Please, choose the language/Будь ласка, виберіть мову",
                             reply_markup=types.InlineKeyboardMarkup(
                                 inline_keyboard=[[
                                     types.InlineKeyboardButton("🇺🇦УКРАЇНСЬКА🇺🇦", callback_data="ukr"),
                                     types.InlineKeyboardButton("🇬🇧ENGLISH🇬🇧", callback_data="eng")]]
                             ))
        await state.set_state(UserState.language.state)
    else:
        l10 = lang.get(user.get("language")).get("start_user")
        await message.answer(l10.get("text").format(model_name=message.chat.full_name),
                             reply_markup=types.InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [
                                         types.InlineKeyboardButton(
                                             l10.get("keyboard").get("UpdateInformationButton"),
                                             callback_data="UpdateInformationButton"
                                         ),
                                         types.InlineKeyboardButton(
                                             l10.get("keyboard").get("UploadNewPictureButton"),
                                             callback_data="UploadNewPictureButton"
                                         )
                                     ],
                                     [
                                         types.InlineKeyboardButton(
                                             l10.get("keyboard").get("DownloadGuidesButton"),
                                             callback_data="DownloadGuidesButton"
                                         ),
                                         types.InlineKeyboardButton(
                                             l10.get("keyboard").get("SetUpTheCallButton"),
                                             callback_data="SetUpTheCallButton"
                                         )
                                     ],
                                     [
                                         types.InlineKeyboardButton(
                                             l10.get("keyboard").get("CheckYourStatusButton"),
                                             callback_data="CheckYourStatusButton"
                                         )
                                     ]
                                 ]
                             ))


async def inqueue_start(message: types.Message, state: FSMContext):
    await please_wait_registration(message, state)


async def registration_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    data = await state.get_data()
    if not data.get("language"):
        # Вибираємо мову
        await message.answer("Please, choose the language/Будь ласка, виберіть мову",
                             reply_markup=types.InlineKeyboardMarkup(
                                 inline_keyboard=[[
                                     types.InlineKeyboardButton("🇺🇦УКРАЇНСЬКА🇺🇦", callback_data="ukr"),
                                     types.InlineKeyboardButton("🇬🇧ENGLISH🇬🇧", callback_data="eng")]]
                             ))
        await state.set_state(UserState.language.state)

    else:
        data = await state.get_data()
        register_data = data.get("register_data")
        if not register_data:
            await state.update_data({"register_data": {}})
        await state.set_state(UserState.registration.state)
        await registration_handler(message=message, state=state, is_information=False)


def registered_users() -> list[str]:
    client = MongoClient(uri)  # Вкажіть свій URI
    db = client[DB_NAME]  # Назва вашої бази даних
    collection = db["Model"]  # Назва колекції

    users = collection.find({}, {'telegram_id': 1, '_id': 0})

    # Формуємо список з Telegram ID
    telegram_ids = [user['telegram_id'] for user in users]

    return telegram_ids


def inqueue_users() -> list[str]:
    client = MongoClient(uri)  # Вкажіть свій URI
    db = client[DB_NAME]  # Назва вашої бази даних
    collection = db["InQueue"]  # Назва колекції

    users = collection.find({}, {'telegram_id': 1, '_id': 0})

    # Формуємо список з Telegram ID
    telegram_ids = [user['telegram_id'] for user in users]

    return telegram_ids


def banned_users() -> list[str]:
    return []


def admins() -> list[int]:
    return [617710378]
