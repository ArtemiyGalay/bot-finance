"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
from aiogram import Bot, Dispatcher, executor, types
import markup
from telebot import types
import exceptions
import expenses
from categories import Categories


logging.basicConfig(level=logging.INFO)

API_TOKEN = "5366559478:AAFg40_LRnitgrRxSn2olbkGmSoB9LaYsao"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""

    await message.answer(
        "Бот для учёта расходов и доходов\n\n"
        "Добавить расход: 10 такси\n")
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user), reply_markup=markup.mainMenu)






@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(text=['🧾 Категории трат'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(text=['📈 Сегодняшняя статистика'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)



@dp.message_handler(text=['🗓 За текущий месяц'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(text=['🖊 Последние внесённые расходы'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text) # вызов модуля expenses (распарсивает текст)
    except exceptions.NotCorrectMessage as e: # в exceptions.py исключение
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)

@dp.message_handler(content_types=['📈 Сегодняшняя статистика','🗓 За текущий месяц','🖊 Последние внесённые расходы','🧾 Категории трат'])
def bot_massege(message):
    if message.chat_type == 'private':
        if message.text == '📈 Сегодняшняя статистика':
            bot.send_message(message.chat_type, 'Обрабатываю запрос: ' + today_statistics())
    elif message.text == '🗓 За текущий месяц':
        bot.send_message(message.chat_type, 'Обрабатываю запрос: ' + month_statistics())
    elif message.text == '🖊 Последние внесённые расходы':
        bot.send_message(message.chat_type, 'Обрабатываю запрос: ' + list_expenses())
    elif message.text == '🧾 Категории трат':
        bot.send_message(message.chat_type, 'Обрабатываю запрос: ' + categories_list())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
