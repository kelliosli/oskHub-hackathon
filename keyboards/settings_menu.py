from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def settings_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Manage Contacts"), KeyboardButton("Select Language"))
    return keyboard


def language_selection_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("English"), KeyboardButton("Russian"), KeyboardButton("Kazakh")
    )
    return keyboard
