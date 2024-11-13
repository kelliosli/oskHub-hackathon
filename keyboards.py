from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


languages_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="Қазақша", callback_data="lang_kz")],
    ]
)
