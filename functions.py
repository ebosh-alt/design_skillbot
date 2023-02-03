from aiogram import types


def create_keyboard(name_buttons: list) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=len(name_buttons), resize_keyboard=True)
    array = []
    for name_button in name_buttons:
        array.append(
            types.KeyboardButton(text=name_button)
        )
    keyboard.add(*array)
    return keyboard
