token = "8007691524:AAHlAWiy_hFIAX_R_YdNwJlAKNNrp38A4xQ"
import logging, asyncio, sys
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery,
)

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher()

# Define a router for the commands and callbacks
router = Router()

# Define the inline keyboard
inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Option 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Option 2", callback_data="option_2")],
    ]
)


@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    reply = "latitude:  {}\nlongitude: {}".format(lat, lon)
    await message.answer(reply, reply_markup=ReplyKeyboardRemove())


# Handle the /start command
@router.message(Command("start"))
async def cmd_locate_me(message: Message):
    await message.answer(
        "Click on the the button below to share your location",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Share Position", request_location=True)]]
        ),
    )


# Handle callback queries from inline keyboard
@router.callback_query()
async def handle_option(callback_query: CallbackQuery):
    if callback_query.data == "option_1":
        response_text = "You chose Option 1!"
    elif callback_query.data == "option_2":
        response_text = "You chose Option 2!"
    else:
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
    print("started")
    asyncio.run(main())
