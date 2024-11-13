token = "7698358102:AAFO1_CPrcLjJUSlIMfxSWBAl0s8vWuJNtw"


import logging, asyncio, sys
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove
)

from keyboards import main_menu_kb, emergency_kb, settings_kb, languages_kb, keyboard_friend, create_friends_keyboard
from db import get_db_connection, init_db
from forms import FriendForm
from ans import res

# Initialize bot and dispatcher
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Define a router for the commands and callbacks
router = Router()


# Handle the /start command
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Welcome! Choose an option:", reply_markup=main_menu_kb)


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
        await callback_query.message.answer(res)
    elif route == "contacts":
        await callback_query.message.answer("Choose an option", reply_markup=keyboard_friend.as_markup(resize_keyboard=True))
    elif route == "language":
        await callback_query.message.answer(
            "What language you want to choose", reply_markup=languages_kb
        )
        
@router.message(F.text == "Добавить друга")
async def add_friend_handler(message: Message, state: FSMContext):
    await state.set_state(FriendForm.adding)
    await message.answer("Отправьте профиль друга для добавления (@username или user_id):")

@router.message(F.text, FriendForm.adding)
async def process_add_friend(message: Message, state: FSMContext):
    friend_username = message.text
    if friend_username.startswith('@')==False:
        await message.answer("Пожалуста введите коректное имя пользователя начинающийся с @")
    else:
        friend_id = message.from_user.id  # Replace as needed
        user_id = message.from_user.id

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO friends (user_id, friend_id, username) VALUES (?, ?, ?)',
                    (user_id, friend_id, friend_username))
        conn.commit()
        conn.close()

        await message.answer(f"{friend_username} добавлен в список друзей.")
        await state.clear()

# Remove friend handler
@router.message(F.text == "Удалить друга")
async def remove_friend_handler(message: Message):
    user_id = message.from_user.id
    keyboard = create_friends_keyboard(user_id)
    await message.answer("Выберите друга для удаления:", reply_markup=keyboard)

# Callback query handler for removing friend
@router.callback_query(F.data.startswith("friend_"))
async def callback_delete_friend_handler(call: CallbackQuery):
    friend_id = int(call.data.split("_")[1])
    user_id = call.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM friends WHERE user_id = ? AND friend_id = ?', (user_id, friend_id))
    conn.commit()
    conn.close()

    await call.answer("Друг удалён из списка.")
    await call.message.delete()

# Edit friend handler
@router.message(F.text == "Редактировать друга")
async def edit_friend_handler(message: Message):
    user_id = message.from_user.id
    keyboard = create_friends_keyboard(user_id)
    await message.answer("Выберите друга для редактирования:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("friend_"))
async def callback_edit_friend_handler(call: CallbackQuery, state: FSMContext):
    friend_id = int(call.data.split("_")[1])
    await state.update_data(friend_id=friend_id)
    await state.set_state(FriendForm.editing_username)
    await call.message.answer("Введите новое имя для друга:")

@router.message(F.text, FriendForm.editing_username)
async def process_edit_friend(message: Message, state: FSMContext):
    new_username = message.text
    data = await state.get_data()
    friend_id = data['friend_id']
    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE friends SET username = ? WHERE user_id = ? AND friend_id = ?',
                   (new_username, user_id, friend_id))
    conn.commit()
    conn.close()

    await message.answer(f"Имя друга обновлено на {new_username}.")
    await state.clear()


@router.message(F.text == "Редактировать друга")
async def edit_friend_handler(message: Message):
    user_id = message.from_user.id
    keyboard = create_friends_keyboard(user_id)
    await message.answer("Выберите друга для редактирования:", reply_markup=keyboard)
    
# Show friends handler
@router.message(F.text == "Показать список друзей")
async def show_friends_handler(message: Message):
    user_id = message.from_user.id
    keyboard = create_friends_keyboard(user_id)

    if keyboard.inline_keyboard:
        await message.answer("Ваши друзья:", reply_markup=keyboard)
    else:
        await message.answer("Список друзей пуст.")

# Register router to dispatcher
dp.include_router(router)

async def main() -> None:
    await dp.start_polling(bot)


# Start polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    asyncio.run(main())
