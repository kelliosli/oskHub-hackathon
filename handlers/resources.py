from aiogram import types
from utils.i18n import get_text


async def start_resources(message: types.Message):
    resources_text = get_text("resources_help", message.from_user.language_code)
    await message.reply(resources_text)
