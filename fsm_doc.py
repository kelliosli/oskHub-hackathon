from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Замените 'YOUR_TOKEN_HERE' на токен вашего бота
API_TOKEN = "YOUR_TOKEN_HERE"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Определяем класс состояний
class Form(StatesGroup):
    name = State()  # Первое состояние - ввод имени
    age = State()  # Второе состояние - ввод возраста


# Начало сценария, переходим в состояние ввода имени
@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    await Form.name.set()
    await message.answer("Как тебя зовут?")


# Обработка имени и переход к состоянию ввода возраста
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохраняем имя в контексте
    await Form.next()  # Переходим к следующему состоянию (ввод возраста)
    await message.answer("Сколько тебе лет?")


# Обработка возраста и завершение сценария
@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Сохраняем возраст в контексте

    # Получаем все данные
    user_data = await state.get_data()
    await message.answer(
        f"Тебя зовут {user_data['name']} и тебе {user_data['age']} лет."
    )

    # Завершаем состояние
    await state.finish()


if name == "__main__":
    executor.start_polling(dp, skip_updates=True)
