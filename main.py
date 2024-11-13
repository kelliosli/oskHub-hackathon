token = "8007691524:AAHlAWiy_hFIAX_R_YdNwJlAKNNrp38A4xQ"


import logging, asyncio, sys
from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
)
from keyboards import languages_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher()

# Define a router for the commands and callbacks
router = Router()

main_menu_kb = ReplyKeyboardBuilder()
main_menu_kb.button(text="🚨 Emergency 🚨")
main_menu_kb.button(text="Settings")
main_menu_kb.button(text="Resources")

settings_kb = ReplyKeyboardBuilder()
settings_kb.button(text="Близкие друзья")
settings_kb.button(text="Язык")

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
    await message.answer("Settings!!!")


@router.message(F.text == "Resources")
async def add_resources_handler(message: Message):
    await message.answer("Resources!!!")


# Handle callback queries from inline keyboard
@router.callback_query()
async def handle_option(callback_query: CallbackQuery):
    route = callback_query.data

    if route == "contacts":
        response_text = "Contacts!"
    elif route == "language":
        await callback_query.message.answer(
            "What language you want to choose", reply_markup=languages_kb
        )
    else:
        # traumas
        response_text = "Unknown option."

    await callback_query.message.answer(response_text)
    await callback_query.answer()


# Register router to dispatcher
dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)


# Start polling
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
