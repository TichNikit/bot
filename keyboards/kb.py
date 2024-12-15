from aiogram import types

keyboard_start = [
    [types.InlineKeyboardButton(text="Норма калорий", callback_data='norm_calorie')],
    [types.InlineKeyboardButton(text="Добавить калории", callback_data='your_calorie')],
    [types.InlineKeyboardButton(text="Обнулить калории", callback_data='delete_calorie')],
    [types.InlineKeyboardButton(text="Добавить ваши доходы", callback_data='income')],
    [types.InlineKeyboardButton(text="Добавить ваши расходы", callback_data='expense')],
    [types.InlineKeyboardButton(text="Обнулить кошелёк", callback_data='delete_income')]]
keyboard_start = types.InlineKeyboardMarkup(inline_keyboard=keyboard_start)
