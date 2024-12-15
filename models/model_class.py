from aiogram.fsm.state import StatesGroup, State

class UserStateNorm(StatesGroup):
    height = State()
    weight = State()
    age = State()


class UserStateCalorie(StatesGroup):
    calorie = State()


class UserStateIncome(StatesGroup):
    income_user = State()


class UserStateExpenses(StatesGroup):
    expenses_user = State()