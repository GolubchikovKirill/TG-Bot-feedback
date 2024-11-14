from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import messages, buttons
from database import init_db

import asyncio

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Инициализация базы данных
init_db()

# Подключение маршрутизаторов
dp.include_router(messages.router)
dp.include_router(buttons.router)

# Запуск бота
async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())

