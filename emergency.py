import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from traumas import load_trauma_data

API_TOKEN = "8007691524:AAHlAWiy_hFIAX_R_YdNwJlAKNNrp38A4xQ"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Define a router for the commands and callbacks
router = Router()

language = "en"  # Default language


# !== keyboards
emergency_kb = InlineKeyboardMarkup(inline_keyboard=[])


# Language selection command
@router.message(Command("start"))
async def start(message: types.Message):
    # user_id = message.from_user.id

    # Creating inline keyboard for trauma options based on the selected language
    traumas = load_trauma_data(language)
    emergency_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=trauma_data["title"], callback_data=trauma_file)]
            for trauma_file, trauma_data in traumas.items()
        ]
    )

    await message.answer("Choose a trauma type:", reply_markup=emergency_kb)


@router.callback_query(
    lambda c: c.data.startswith("next_step") or c.data.endswith(".json")
)
async def handle_trauma_step(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    trauma_file = (
        callback_query.data.split("/")[1]
        if callback_query.data.startswith("next_step")
        else callback_query.data
    )

    # Load the trauma data
    with open(f"traumas/{trauma_file}", "r", encoding="utf-8") as f:
        trauma_data = json.load(f)

    # Extract step index
    if callback_query.data.startswith("next_step"):
        _, _, step_index = callback_query.data.split("/")
        step_index = int(step_index)
    else:
        step_index = 0  # Start with the first step

    # Get the current step
    step = trauma_data["steps"][step_index]
    step_text = step["text"].get(language, step["text"]["en"])
    step_image = step["image"]

    # Send the step message with image
    next_kb = None
    if step_index < len(trauma_data["steps"]) - 1:
        next_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Next Step",
                        callback_data=f"next_step/{trauma_file}/{step_index + 1}",
                    )
                ]
            ]
        )

    # Send the step (photo + text) with the "Next Step" button if applicable
    await bot.send_photo(
        chat_id=user_id,
        photo=step_image,
        caption=step_text,
        reply_markup=next_kb,
    )


# ==

# Register router to dispatcher
dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("started")
    asyncio.run(main())


# @router.callback_query()
# async def handle_option(callback_query: CallbackQuery):
#     route = callback_query.data

#     # !==
#     if route == "emergency":
#         await callback_query.message.answer(
#             "What is your emergency:", reply_markup=emergency_kb
#         )
#     # ==
