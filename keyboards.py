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
