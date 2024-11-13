from aiogram import types
from keyboards.settings_menu import settings_menu_keyboard


async def start_settings(message: types.Message):
    await message.reply("Settings options:", reply_markup=settings_menu_keyboard())
