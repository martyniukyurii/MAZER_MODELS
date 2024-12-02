from aiogram import types


def create_keyboard_from_dict(keyboard_dict):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key, value in keyboard_dict.items():
        if key == "SendPhoneNumberButton":
            button = types.KeyboardButton(text=value, request_contact=True)
        else:
            button = types.KeyboardButton(text=value)
        keyboard.add(button)
    return keyboard
