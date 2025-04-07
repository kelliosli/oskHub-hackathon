token = "YOUR_TOKEN"


import logging, asyncio, sys
from aiogram import F, Bot, Dispatcher, Router, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram_i18n import I18nContext, I18nMiddleware, LazyProxy
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from aiogram_i18n.lazy.filter import LazyFilter
from aiogram_i18n.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards import languages_kb, keyboard_friend, create_friends_keyboard,keyboard_back
from db import get_db_connection, init_db
from forms import FriendForm
from ans import res
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import sqlite3

from aiogram_i18n import I18nMiddleware

# Initialize bot and dispatcher
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)



i18n = I18nMiddleware("bot", "locales", default_locale="ru")
dp.middleware.setup(i18n)
# Define a router for the commands and callbacks
router = Router()

_ = i18n.gettext

main_menu_kb = ReplyKeyboardBuilder()
main_menu_kb.button(text=_("🚨 Emergency 🚨"))
main_menu_kb.button(text=_("Settings"))
main_menu_kb.button(text=_("Resources"))

# Меню настроек
settings_kb = ReplyKeyboardBuilder()
settings_kb.button(text=_("Close Friends"))
settings_kb.button(text=_("Language"))

emergency_kb = ReplyKeyboardBuilder()
emergency_kb.button(text="Кровотечения")
emergency_kb.button(text="Перелом")
emergency_kb.button(text="Другое")
emergency_kb.button(text="Кровотечения")
emergency_kb.button(text="Перелом")
emergency_kb.button(text="Другое")
emergency_kb.button(text="Кровотечения")
emergency_kb.button(text="Перелом")
emergency_kb.button(text="Другое")
emergency_kb.button(text="Кровотечения")
emergency_kb.button(text="Перелом")
emergency_kb.button(text="Другое")


# Handle the /start command
@router.message(Command("start"))
async def send_welcome(message: Message):
    
    user_id = message.from_user.id
    username = message.from_user.username
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if the user is already registered
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    # If user not found, insert the new user into the database
    if user is None:
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()

    await message.answer(
        "Welcome! Choose an option:",
        reply_markup=main_menu_kb.as_markup(resize_keyboard=True),
    )


@router.message(F.text == "🚨 Emergency 🚨")
async def add_emergency_handler(message: Message):
    await message.answer(
        "What is your emergency:",
        reply_markup=emergency_kb.as_markup(resize_keyboard=True),
    )


@router.message(F.text == "Settings")
async def add_settings_handler(message: Message):
    await message.answer("Настройки")


@router.message(F.text == "Resources")
async def add_resources_handler(message: Message):
    await message.answer("Resources!!!")


# Handle callback queries from inline keyboard
@router.callback_query()
async def handle_option(callback_query: CallbackQuery):
    route = callback_query.data

    if route == "emergency":
        await callback_query.message.answer(
            "What is your emergency:", reply_markup=emergency_kb
        )
    elif route == "settings":
        await callback_query.message.answer("Settings:", reply_markup=settings_kb)
    elif route == "resources":
        response_text = "Resources!"
    elif route == "contacts":
        response_text = "Contacts!"
    elif route == "language":
        await callback_query.message.answer(
            "What language you want to choose", reply_markup=languages_kb
        )
        
@router.message(F.text == "Добавить друга")
async def add_friend_handler(message: Message, state: FSMContext):
    await state.set_state(FriendForm.adding)
    await message.answer("Отправьте профиль друга для добавления (@username или user_id):", reply_markup=keyboard_back.as_markup(resize_keyboard=True))

@router.message(F.text, FriendForm.adding)
async def process_add_friend(message: Message, state: FSMContext):
    friend_username = message.text
    if friend_username == "Назад" or friend_username == "Артқа" or friend_username == "Back":
        await message.answer("Отмена", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
        await state.clear()
    elif friend_username.startswith('@')==False:
        await message.answer("Пожалуста введите коректное имя пользователя начинающийся с @")
    else:
        user_id = message.from_user.id

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO friends (user_id, username) VALUES (?, ?)',
                    (user_id, friend_username))
        conn.commit()
        conn.close()

        await message.answer(f"{friend_username} добавлен в список друзей.", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
        await state.clear()

# Remove friend handler
@router.message(F.text == "Удалить друга")
async def remove_friend_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # keyboard = create_friends_keyboard(user_id)
    await state.set_state(FriendForm.removing)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, user_id FROM friends WHERE user_id = ?', (user_id,))
    friends = cursor.fetchall()
    conn.close()
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.button(text='Назад')
    for username, friend_id in friends:
        keyboard1.button(text=username)
    await message.answer("Выберите друга для удаления:", reply_markup=keyboard1.as_markup(resize_keyboard=True))

# Callback query handler for removing friend
@router.message(F.text, FriendForm.removing)
async def callback_delete_friend_handler(message: Message, state: FSMContext):
    username = message.text[1:]
    if username == "Назад":
        await message.answer("Отмена", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
        await state.clear()
    else:
        user_id = message.from_user.id
        print(username, user_id)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM friends WHERE user_id = ? AND username = ?', (user_id, username))
        conn.commit()
        conn.close()

        await message.answer(f"Друг удалён из списка.{username}", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
        await state.clear()


    
# Show friends handler
@router.message(F.text == "Показать список друзей")
async def show_friends_handler(message: Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, user_id FROM friends WHERE user_id = ?', (user_id,))
    friends = cursor.fetchall()
    conn.close()
    res = ''
    for username, friend_id in friends:
        res += f'{username} '
    if res:
        await message.answer(f"Ваши друзья: {res}", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
    else:
        await message.answer("Список друзей пуст.", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))

# Register router to dispatcher
dp.include_router(router)

async def main() -> None:
    await dp.start_polling(bot)


# Start polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    i18n_middleware = I18nMiddleware(core=FluentRuntimeCore(path="locales/{locale}/LC_MESSAGES"))
    i18n_middleware.setup(dispatcher=dp)
    asyncio.run(main())
