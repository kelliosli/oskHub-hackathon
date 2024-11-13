from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from db import get_db_connection


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


keyboard_back = ReplyKeyboardBuilder()
keyboard_back.button(text='Назад')

def create_friends_keyboard(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, user_id FROM friends WHERE user_id = ?', (user_id,))
    friends = cursor.fetchall()
    conn.close()

    keyboard = ReplyKeyboardBuilder()
    for username, friend_id in friends:
        keyboard.button(text=username, callback_data=f"friend_{username[1:]}")
    return keyboard.as_markup()