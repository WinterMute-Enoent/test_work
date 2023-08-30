import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize bot and dispatcher
bot = Bot(token='6650215277:AAHbEMAVj6VW2GG8zimWE08Fw082LM0zT18')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Настройка доступа к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
SPREADSHEET_ID = '1VeidJ6vxB3lDYFQHNJP2rfF76Yck59wQhggB6NNquSg'
worksheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Параметры логгирования
logging.basicConfig(level=logging.INFO)

# Параметры сохранения лога в файл
log_file = 'app_log.txt'
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setLevel(logging.INFO)  # Тут устанавливается уровень логгирования

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Обработка логгирования
logging.getLogger('').addHandler(file_handler)


# Приветственное сообщение
welcome_message = "Приветствую! Введи любое сообщение для сбора данных. По всем вопросам, пожалуйста, обращайся https://t.me/Winter_Mute_ENOENT. Хорошего дня! 😊"

# Обработка команд
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(welcome_message)

# Обработка сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_message(message: types.Message):
    try:
        username = message.from_user.username
        text = message.text
        timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')  # Преобразование datetime в строку

        data = [username, text, timestamp]
        worksheet.append_row(data)
        await message.answer("Данные успешно записаны в таблицу)")
    except Exception as e:
        error_message = "Произошла ошибка. Пожалуйста, попробуй позже("
        logging.error(f"{error_message}: {str(e)}")
        await message.answer(error_message)

if __name__ == '__main__':
    from aiogram import executor
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)
