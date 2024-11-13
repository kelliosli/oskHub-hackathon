token = "8007691524:AAHlAWiy_hFIAX_R_YdNwJlAKNNrp38A4xQ"


import json
import logging, asyncio, sys
from aiogram import F, Bot, Dispatcher, Router, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards import (
    languages_kb,
    keyboard_friend,
    create_friends_keyboard,
    keyboard_back,
)
from db import get_db_connection, get_friends_user_ids, init_db
from forms import FriendForm
from ans import res
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards import main_menu_kb, emergency_kb, settings_kb
# from utils import send_message_to_contacts

language = "en"

# Initialize bot and dispatcher
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Define a router for the commands and callbacks
router = Router()


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


@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "latitude:  {}\nlongitude: {}".format(lat, lon)
    # await message.answer(reply, reply_markup=ReplyKeyboardRemove())
    for username, user_id in get_friends_user_ids(message.from_user.id):
        await bot.send_message(user_id, message.from_user.username + " IS IN DANGER!")

    await message.answer(
        reply + "\tWhat is your emergency:",
        reply_markup=emergency_kb,
    )


# @router.message(F.text == "🚨 Emergency 🚨")
# async def add_emergency_handler(message: Message):
#     await message.answer(
#         "What is your emergency:",
#         reply_markup=emergency_kb.as_markup(resize_keyboard=True),
#     )


@router.callback_query(
    lambda c: c.data.startswith("next_step") or c.data.endswith(".json")
)
async def handle_trauma_step(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    trauma_file = (
        callback_query.data.split("/")[1]
        if callback_query.data.startswith("next_step")
        else callback_query.data
    )

    # Load the trauma data
    with open(f"traumas/{trauma_file}", "r", encoding="utf-8") as f:
        trauma_data = json.load(f)

    # Extract step index
    if callback_query.data.startswith("next_step"):
        _, _, step_index = callback_query.data.split("/")
        step_index = int(step_index)
    else:
        step_index = 0  # Start with the first step

    # Get the current step
    step = trauma_data["steps"][step_index]
    step_text = step["text"].get(language, step["text"][language])
    step_image = step["image"]

    # Send the step message with image
    next_kb = None
    if step_index < len(trauma_data["steps"]) - 1:
        next_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Next Step",
                        callback_data=f"next_step/{trauma_file}/{step_index + 1}",
                    )
                ]
            ]
        )

    # Send the step (photo + text) with the "Next Step" button if applicable
    await bot.send_photo(
        chat_id=user_id,
        photo=step_image,
        caption=step_text,
        reply_markup=next_kb,
    )


# ==


@router.message(F.text == "Настройки")
async def add_settings_handler(message: Message):
    await message.answer(
        "Settings!!!",
        reply_markup=settings_kb.as_markup(resize_keyboard=True),
    )


@router.message(F.text == "Близкие друзья")
async def add_friends_handler(message: Message):
    await message.answer(
        "Friends",
        reply_markup=keyboard_friend.as_markup(resize_keyboard=True),
    )


@router.message(F.text == "Ресурсы")
async def add_resources_handler(message: Message):
    await message.answer(res, reply_markup=main_menu_kb.as_markup(resize_keyboard=True))

@router.message(F.text == "Назад")
async def add_resources_handler(message: Message):
    await message.answer(res, reply_markup=main_menu_kb.as_markup(resize_keyboard=True))

@router.message(F.text == "Добавить друга")
async def add_friend_handler(message: Message, state: FSMContext):
    await state.set_state(FriendForm.adding)
    await message.answer(
        "Отправьте профиль друга для добавления (@username или user_id):",
        reply_markup=keyboard_back.as_markup(resize_keyboard=True),
    )
    


@router.message(F.text == "Выйти")
async def add_leave_handler(message: Message, state: FSMContext):
    await state.set_state(FriendForm.adding)
    await message.answer(
        text="Выход...",
        reply_markup=main_menu_kb.as_markup(resize_keyboard=True),
    )


@router.message(F.text, FriendForm.adding)
async def process_add_friend(message: Message, state: FSMContext):
    friend_username = message.text
    if friend_username == "Назад":
        await message.answer(
            "Отмена", reply_markup=keyboard_friend.as_markup(resize_keyboard=True)
        )
        await state.clear()
    elif friend_username.startswith("@") == False:
        await message.answer(
            "Пожалуста введите коректное имя пользователя начинающийся с @"
        )
    else:
        user_id = message.from_user.id

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO friends (user_id, username) VALUES (?, ?)",
            (user_id, friend_username),
        )
        conn.commit()
        conn.close()

        await message.answer(
            f"{friend_username} добавлен в список друзей.",
            reply_markup=keyboard_friend.as_markup(resize_keyboard=True),
        )
        await state.clear()


# Remove friend handler
@router.message(F.text == "Удалить друга")
async def remove_friend_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # keyboard = create_friends_keyboard(user_id)
    await state.set_state(FriendForm.removing)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, user_id FROM friends WHERE user_id = ?", (user_id,)
    )
    friends = cursor.fetchall()
    print("friends: ", friends)
    conn.close()
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.button(text="Назад")
    for username, user_id in friends:
        keyboard1.button(text=username)
    await message.answer(
        "Выберите друга для удаления:",
        reply_markup=keyboard1.as_markup(resize_keyboard=True),
    )


# Callback query handler for removing friend
@router.message(F.text, FriendForm.removing)
async def callback_delete_friend_handler(message: Message, state: FSMContext):
    username = message.text[1:]
    if username == "Назад":
        await message.answer(
            "Отмена", reply_markup=keyboard_friend.as_markup(resize_keyboard=True)
        )
        await state.clear()
    else:
        user_id = message.from_user.id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM friends WHERE user_id = ? AND username = ?",
            (user_id, "@" + username),
        )
        conn.commit()
        conn.close()

        await message.answer(
            f"Друг удалён из списка: {username}",
            reply_markup=keyboard_friend.as_markup(resize_keyboard=True),
        )
        await state.clear()


# Show friends handler
@router.message(F.text == "Показать список друзей")
async def show_friends_handler(message: Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, user_id FROM friends WHERE user_id = ?", (user_id,)
    )
    friends = cursor.fetchall()
    conn.close()
    res = ""
    for username, friend_id in friends:
        res += f"{username} "
    if res:
        await message.answer(
            f"Ваши друзья: {res}",
            reply_markup=keyboard_friend.as_markup(resize_keyboard=True),
        )
    else:
        await message.answer(
            "Список друзей пуст.",
            reply_markup=keyboard_friend.as_markup(resize_keyboard=True),
        )


# Register router to dispatcher
dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)


# Start polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    asyncio.run(main())
    
