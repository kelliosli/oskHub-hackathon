from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton("Emergency"))
main_menu_keyboard.add(KeyboardButton("Settings"))
main_menu_keyboard.add(KeyboardButton("Resources"))
