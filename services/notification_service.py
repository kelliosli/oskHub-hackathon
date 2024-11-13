from aiogram import Bot
from data.db import get_contacts


async def notify_contacts(user_id, emergency_type):
    contacts = get_contacts(user_id)
    for contact in contacts:
        # Notify each contact with emergency details and user location
        await bot.send_message(
            contact.contact_id, f"Emergency: {emergency_type}. Location shared."
        )
