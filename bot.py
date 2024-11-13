import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from config import BOT_TOKEN
from handlers import emergency, settings, resources
from keyboards.main_menu import main_menu_keyboard
from utils.location_utils import request_location_keyboard
# from locales import en, ru, kz  # Import language resources

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Load Language Files
LANGUAGES = {"en": en, "ru": ru, "kz": kz}


# Register Handlers
async def register_handlers():
    dp.message.register(start, commands={"start"})
    dp.message.register(emergency.start_emergency, commands={"emergency"})
    dp.message.register(settings.start_settings, commands={"settings"})
    dp.message.register(resources.start_resources, commands={"resources"})


@dp.message(F.text == "/start")
async def start(message: Message):
    # Select language from user or default to English
    user_language = "en"  # Retrieve this from user settings in database
    lang = LANGUAGES[user_language]

    await message.reply(lang["welcome"], reply_markup=main_menu_keyboard())


async def main():
    await register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
