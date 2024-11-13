token = "8007691524:AAHlAWiy_hFIAX_R_YdNwJlAKNNrp38A4xQ"


import logging, asyncio, sys
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
)
from keyboards import main_menu_kb, emergency_kb, settings_kb, languages_kb

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher()

# Define a router for the commands and callbacks
router = Router()

# contacts = ["@alphazhan", "@kelliosli"]
contacts_id = [5125986155, 499146021]


async def send_message_to_contacts(contacts_id: list, message: str):
    """Send a message to all contacts in the list."""
    for user_id in contacts_id:
        try:
            await bot.send_message(user_id, message)
            print(f"Message sent to {user_id}")
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")


# Handle the /start command
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Welcome! Choose an option:", reply_markup=main_menu_kb)


# Handle callback queries from inline keyboard
@router.callback_query()
async def handle_option(callback_query: CallbackQuery):
    route = callback_query.data
    print("user_id:", callback_query.from_user.id)
    print("user_name:", callback_query.from_user)

    if route == "emergency":
        await send_message_to_contacts(
            contacts_id, callback_query.from_user.username + " IS IN DANGER!"
        )
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
