#bot/handlers/messages.py
from aiogram import Router, types
from aiogram.filters import Command  # Импортируем Command для фильтрации команд
from keyboards.reply import get_reply_keyboard
from keyboards.inline import get_feedback_inline_keyboard

router = Router()

@router.message(Command("start"))  # Используем Command для команды "/start"
async def start_command_handler(message: types.Message):
    await message.answer(
        "<b>Уважаемый студент! Я <s>бот</s> кот для сбора обратной связи после групповой консультации.</b>\n"
        "<b>Для того, чтобы поделиться тем, что тебе понравилось и/или ты хотел бы добавить, нажми кнопку ниже.</b>",
        parse_mode="HTML",
        reply_markup=get_reply_keyboard()
    )
  
@router.message(lambda message: message.text == "Обратная связь")  # Используем lambda-функцию для проверки текста
async def feedback_message(message: types.Message):
    await message.answer("Выберите тип обратной связи", reply_markup=get_feedback_inline_keyboard())

@router.message(Command("help"))
@router.message(lambda message: message.text == "Помощь")  # Обрабатываем текст кнопки "Помощь"
async def help_command_handler(message: types.Message):
    await message.answer("Тут будет текст кнопки help", reply_markup=get_reply_keyboard())

# Обработчик для кнопки "Рекомендации"
@router.message(lambda message: message.text == "Рекомендации")
async def recommendations_message(message: types.Message):
    await message.answer("Здесь будут рекомендации по теме.", reply_markup=get_reply_keyboard())


