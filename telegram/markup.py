from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ----- Menu -------

button_today = KeyboardButton('📈 Сегодняшняя статистика')
button_month = KeyboardButton('🗓 За текущий месяц')
button_expenses = KeyboardButton('🖊 Последние внесённые расходы')
button_categories = KeyboardButton('🧾 Категории трат')

mainMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(button_today, button_month, button_expenses, button_categories)




