from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def emergency_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Fire"),
        KeyboardButton("Injury/Trauma"),
        KeyboardButton("Lost"),
        KeyboardButton("Other"),
    )
    return keyboard
