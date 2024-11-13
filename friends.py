from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FriendsForm(StatesGroup):
    operation_type = State()  # add, remove, list
    nickname = State()  # add, remove


friends_router = Router()
