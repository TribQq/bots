import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram_calendar import calendar_callback, SimpleCalendar

from config import API_TOKEN

# API_TOKEN = '' uncomment and insert your telegram bot API key here
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# starting bot when user sends `/start` command, answering with inline calendar
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().create_calendar())


@dp.callback_query_handler(calendar_callback.filter())  # handler is processing only calendar_callback queries
async def process_name(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_calendar_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=ReplyKeyboardRemove()
        )
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)