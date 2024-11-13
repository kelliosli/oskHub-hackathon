from aiogram import types
from keyboards.emergency_menu import emergency_menu_keyboard
from services.notification_service import notify_contacts
from utils.location_utils import request_location


async def start_emergency(message: types.Message):
    await message.answer(
        "Please choose the type of emergency:", reply_markup=emergency_menu_keyboard()
    )


async def handle_emergency_type(callback_query: types.CallbackQuery):
    emergency_type = callback_query.data
    await request_location(callback_query.message)
    # Notify contacts with emergency details
    await notify_contacts(callback_query.from_user.id, emergency_type)
    await callback_query.answer("Emergency notification sent!")
