from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import get_db_connection
from traumas import load_trauma_data

language = "en"  # Default language


# Main Menu
main_menu_kb = ReplyKeyboardBuilder()
main_menu_kb.button(text="🚨 Emergency 🚨", request_location=True)
main_menu_kb.button(text="Settings")
main_menu_kb.button(text="Resources")
# =

# Settings
settings_kb = ReplyKeyboardBuilder()
settings_kb.button(text="Близкие друзья")
settings_kb.button(text="Язык")
# =

# Emergency
traumas = load_trauma_data(language)
emergency_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=trauma_data["title"], callback_data=trauma_file)]
        for trauma_file, trauma_data in traumas.items()
    ]
)
# =

# def get_keyboard_of_hospitals(lat, long):
#


languages_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="Қазақша", callback_data="lang_kz")],
    ]
)


keyboard_friend = ReplyKeyboardBuilder()
keyboard_friend.button(text="Добавить друга")
keyboard_friend.button(text="Удалить друга")
keyboard_friend.button(text="Показать список друзей")
keyboard_friend.button(text="Выйти")


keyboard_back = ReplyKeyboardBuilder()
keyboard_back.button(text="Назад")


def create_friends_keyboard(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, user_id FROM friends WHERE user_id = ?", (user_id,)
    )
    friends = cursor.fetchall()
    conn.close()

    keyboard = ReplyKeyboardBuilder()
    for username, friend_id in friends:
        keyboard.button(text=username, callback_data=f"friend_{username[1:]}")
    return keyboard.as_markup()
