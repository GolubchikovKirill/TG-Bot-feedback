#bot/handlers/messages.py
from aiogram import Router, types
from aiogram.filters import Command  # Импортируем Command для фильтрации команд
from keyboards.reply import get_reply_keyboard
from keyboards.inline import get_feedback_inline_keyboard

router = Router()

@router.message(Command("start"))  # Используем Command для команды "/start"
async def start_command_handler(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=get_reply_keyboard())
    
@router.message(lambda message: message.text == "Обратная связь")  # Используем lambda-функцию для проверки текста
async def feedback_message(message: types.Message):
    await message.answer("Выберите тип обратной связи:", reply_markup=get_feedback_inline_keyboard())


