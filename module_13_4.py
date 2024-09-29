from aiogram import Bot, Dispatcher,executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio



api = ''

bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Обработка команды start
@dp.message_handler(commands=['start'])
async def start_command(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. "
                         "Напиши «Calories», чтобы рассчитать необходимую дневную норму калорий!")

# Обработка текста 'Calories'
@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите ваш возраст:')# запрос age
    await UserState.age.set()


@dp.message_handler(state=UserState.age) #хендлер обработка ввода age.
async def set_growth(message, state):
    await state.update_data(age=int(message.text))#запись введеного age, в формате init.
    await message.answer('Введите ваш рост (в сантиметрах):')# запрос growth
    await UserState.next()


@dp.message_handler(state=UserState.growth)#хендлер обработка ввода growth.
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))#запись введеного growth, в формате init.
    await message.answer('Введите ваш вес (в килограммах):')# запрос weight
    await UserState.next()


@dp.message_handler(state=UserState.weight) #хендлер обработка ввода weight.
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))#запись введеного weight, в формате init.
    data = await state.get_data() # словарь введенных данных

    #получим данные из словаря
    age = data['age']
    growth = data['growth']
    weight = data['weight']


    calories = 10 * weight + 6.25 * growth - 5 * age + 5 # Рассчитаем калории.

    await message.answer(f"Ваша норма калорий: {calories:.0f} ккал")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
