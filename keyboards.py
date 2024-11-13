from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Emergency", callback_data="emergency")],
        [InlineKeyboardButton(text="Settings", callback_data="settings")],
        [InlineKeyboardButton(text="Resources", callback_data="resources")],
    ]
)


emergency_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кровотечения", callback_data="trauma")],
        [InlineKeyboardButton(text="Перелом", callback_data="trauma")],
        [InlineKeyboardButton(text="Другое", callback_data="trauma")],
    ]
)

settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Близкие друзья", callback_data="contacts")],
        [InlineKeyboardButton(text="Язык", callback_data="language")],
    ]
)

languages_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="Қазақша", callback_data="lang_kz")],
    ]
)
