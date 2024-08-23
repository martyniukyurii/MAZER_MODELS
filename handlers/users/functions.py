from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton

from data.config import lang
from handlers.users.states import UserState


async def start_banned(message: types.Message, state: FSMContext):
    await message.answer(lang.get('ukr').get('start_banned'),
                         reply_markup=types.ReplyKeyboardRemove())


async def start_login(message: types.Message, state: FSMContext):
    await message.answer(lang.get('ukr').get('start_user').get("text").format(model_name=message.from_user.full_name),
                         reply_markup=types.ReplyKeyboardRemove())


async def start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    data = await state.get_data()
    print(data)
    if not data.get("language"):
        await message.answer("Please, choose the language/Будь ласка, виберіть мову",
                             reply_markup=types.InlineKeyboardMarkup(
                                 inline_keyboard=[[
                                     types.InlineKeyboardButton("🇺🇦УКРАЇНСЬКА🇺🇦", callback_data="ukr"),
                                     types.InlineKeyboardButton("🇬🇧ENGLISH🇬🇧", callback_data="eng")]]
                             ))
        await state.set_state(UserState.language.state)
    else:
        l10 = lang.get(data.get("language")).get("start_user")
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


async def language_choose(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ukr" or call.data == "eng":
        await state.update_data({"language": call.data})
        await call.message.edit_text(
            lang.get(call.data).get("start_user").get("language_chooses").get("text").format(lang=call.data))
    await state.reset_state(with_data=False)
    await start(message=call.message, state=state)


def registered_users() -> list[str]:
    return []


def banned_users() -> list[str]:
    return []


def admins() -> list[str]:
    return []


async def register_user():
    pass


async def send_notification_to_agent():
    pass


def create_keyboard_from_dict(keyboard_dict):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, value in keyboard_dict.items():
        if key == "SendPhoneNumberButton":
            button = types.KeyboardButton(text=value, request_contact=True)
        else:
            button = types.KeyboardButton(text=value)
        keyboard.add(button)
    return keyboard


def create_inline_keyboard_from_dict(keyboard_dict):
    keyboard = types.InlineKeyboardMarkup(row_width=3)  # Установлюємо 3 кнопки в рядку

    for text, callback_data in keyboard_dict.items():
        button = types.InlineKeyboardButton(text=text, callback_data=callback_data)
        keyboard.add(button)  # Додаємо кнопку до клавіатури

    return keyboard