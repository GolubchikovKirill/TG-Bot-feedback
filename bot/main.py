#bot/main.py
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import messages, buttons
from database import init_db
import subprocess
import asyncio
import os

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Инициализация базы данных
init_db()

# Подключение маршрутизаторов
dp.include_router(messages.router)
dp.include_router(buttons.router)

# Запуск admin.py как отдельного процесса
def start_admin():
    try:
        admin_path = os.path.join(os.path.dirname(__file__), "admin.py")  # Путь к admin.py
        subprocess.Popen(["python3.13", admin_path])
        print("Admin.py запущен.")
    except Exception as e:
        print(f"Ошибка при запуске admin.py: {e}")

# Запуск бота
async def start_bot():
    # Запуск admin.py
    start_admin()
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())

