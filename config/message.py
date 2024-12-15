import types
from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart
import aiosqlite
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config.def_for_message import (add_user, user_exists, calories_to_db, insert_or_update_calories, calorie_analysis,
                                    delete_all_calories, add_new_income, add_new_expenses, delete_all_income)

from keyboards.kb import keyboard_start
from models.model_class import UserStateNorm, UserStateCalorie, UserStateIncome, UserStateExpenses


async def start_command(message: types.Message):
    user_id = message.from_user.id

    if await user_exists(user_id):
        await message.answer(f'Привет {message.from_user.full_name}', reply_markup=keyboard_start)
    else:
        await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
        await message.answer(f'Привет {message.from_user.full_name}', reply_markup=keyboard_start)


async def prompt_height(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Введите ваш рост в сантиметрах:")
    await state.set_state(UserStateNorm.height)

async def set_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(height=message.text)
        await message.answer("Введите ваш вес в килограммах:")
        await state.set_state(UserStateNorm.weight)
    else:
        await message.answer("Пожалуйста, введите корректное число для роста в сантиметрах.")
        await state.set_state(UserStateNorm.height)


async def prompt_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(weight=message.text)
        await message.answer('Введите свой возраст:')
        await state.set_state(UserStateNorm.age)
    else:
        await message.answer("Пожалуйста, введите корректное число для весв в килограммах.")
        await state.set_state(UserStateNorm.weight)


async def calculate_calories(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        data = await state.get_data()

        height = int(data['height'])
        weight = int(data['weight'])
        age = int(data['age'])
        user_id = message.from_user.id

        calories = 10 * weight + 6.25 * height - 5 * age + 5
        await calories_to_db(calories, user_id)
        await message.answer(f"Ваша норма калорий: {calories}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите корректное число для возраста.")
        await state.set_state(UserStateNorm.age)


async def get_calorie(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Введите сколько калорий вы потребили:")
    await state.set_state(UserStateCalorie.calorie)


async def add_calorie(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(calorie=message.text)

        data = await state.get_data()
        calorie = int(data['calorie'])
        user_id = message.from_user.id

        await insert_or_update_calories(calorie, user_id)
        comparison = await calorie_analysis(user_id)

        if comparison[0] > comparison[1]:
            await message.answer(f'Вы превысили норму калорий. Текущее значение: {comparison[0]}. Ваша норма: {comparison[1]}')
        else:
            await message.answer(f'Норма калорий не превышена. Текущее значение: {comparison[0]}. Ваша норма: {comparison[1]}')
    else:
        await message.answer("Пожалуйста, введите корректное число.")
        await state.set_state(UserStateCalorie.calorie)


async def delete_calories(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_all_calories(user_id)
    await callback_query.answer()
    await callback_query.message.answer("Ваша дневная норма калорий обнулена")


async def get_income(message: types.Message, state: FSMContext):
    await message.answer("Введите вашу прибыль:")
    await state.set_state(UserStateIncome.income_user)


async def add_income(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(income_user=message.text)
        data = await state.get_data()
        income = int(data['income_user'])
        user_id = message.from_user.id
        your_data = await add_new_income(income, user_id)
        await message.answer(f"Ваш доход добавлен в копилку. Текущее значение: {your_data}")
    else:
        await message.answer('Введите число вашего дохода')
        await state.set_state(UserStateIncome.income_user)


async def get_expenses(message: types.Message, state: FSMContext):
    await message.answer('Введите ваши расходы')
    await state.set_state(UserStateExpenses.expenses_user)


async def minus_expenses(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(expenses_user=message.text)
        data = await state.get_data()
        expenses = int(data['expenses_user'])
        user_id = message.from_user.id
        your_data = await add_new_expenses(expenses, user_id)
        await message.answer(f"Ваш расход вычтен из копилку. Текущее значение:{your_data}")
    else:
        await message.answer('Введите число ваших расходов')
        await state.set_state(UserStateExpenses.expenses_user)


async def delete_wallet(message: types.Message):
    user_id = message.from_user.id
    await delete_all_income(user_id)
    await message.answer('Кошелёк обнулён.')

def register_user_messages(dp: Dispatcher):
    dp.message.register(start_command, CommandStart())
    # норма калойрий
    dp.callback_query.register(prompt_height, F.data == 'norm_calorie')
    dp.message.register(set_weight, UserStateNorm.height)
    dp.message.register(prompt_age, UserStateNorm.weight)
    dp.message.register(calculate_calories, UserStateNorm.age)
    # добавить калории
    dp.callback_query.register(get_calorie, F.data == 'your_calorie')
    dp.message.register(add_calorie, UserStateCalorie.calorie)
    # обнуление калорий
    dp.callback_query.register(delete_calories, F.data == 'delete_calorie')
    # добавить доход
    dp.callback_query.register(get_income, F.data == 'income')
    dp.message.register(add_income, UserStateIncome.income_user)
    # добавить расход
    dp.callback_query.register(get_expenses, F.data == 'expense')
    dp.message.register(minus_expenses, UserStateExpenses.expenses_user)
    # обнулить кошелёк
    dp.callback_query.register(delete_wallet, F.data == 'delete_income')
