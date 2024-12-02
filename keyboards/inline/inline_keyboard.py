from aiogram import types


def create_inline_keyboard_from_dict(keyboard_dict):
    keyboard = types.InlineKeyboardMarkup()

    # Ініціалізуємо список для кнопок в поточному рядку
    current_row = []

    for callback_data, text in keyboard_dict.items():
        button = types.InlineKeyboardButton(text=text, callback_data=callback_data)
        current_row.append(button)

        # Додаємо рядок до клавіатури, коли досягнуто 3 кнопки
        if len(current_row) == 3:
            keyboard.add(*current_row)
            current_row = []  # Очищаємо список для наступного рядка

    # Додаємо останній рядок, якщо є неповний
    if current_row:
        keyboard.add(*current_row)

    return keyboard