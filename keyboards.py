from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from db import get_db_connection


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Emergency", callback_data="emergency")],
        [InlineKeyboardButton(text="Settings", callback_data="settings")],
        [InlineKeyboardButton(text="Resources", callback_data="resources")],
    ]
)


emergency_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кровотечения", callback_data="trauma")],
        [InlineKeyboardButton(text="Перелом", callback_data="trauma")],
        [InlineKeyboardButton(text="Другое", callback_data="trauma")],
    ]
)

settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Близкие друзья", callback_data="contacts")],
        [InlineKeyboardButton(text="Язык", callback_data="language")],
    ]
)

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
keyboard_friend.button(text='Назад')


def create_friends_keyboard(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, user_id FROM friends WHERE user_id = ?', (user_id,))
    friends = cursor.fetchall()
    conn.close()

    keyboard = InlineKeyboardBuilder()
    for username, friend_id in friends:
        keyboard.button(text=username, callback_data=f"friend_{username}")
    return keyboard.as_markup()