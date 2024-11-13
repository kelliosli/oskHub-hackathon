token = "7698358102:AAFO1_CPrcLjJUSlIMfxSWBAl0s8vWuJNtw"


import logging, asyncio, sys
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
)
from keyboards import main_menu_kb

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher()

# Define a router for the commands and callbacks
router = Router()


# Handle the /start command
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Welcome! Choose an option:", reply_markup=main_menu_kb)


# Handle callback queries from inline keyboard
@router.callback_query()
async def handle_option(callback_query: CallbackQuery):
    if callback_query.data == "emergency":
        await callback_query.message.answer(
            "Welcome! Choose an option:", reply_markup=main_menu_kb
        )
    elif callback_query.data == "settings":
        response_text = "You chose Option 2!"
    elif callback_query.data == "resources":
        response_text = "You chose Option 3!"
    else:
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
