from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_reply_keyboard():
    # Создаем кнопки с именованным аргументом text
    button1 = KeyboardButton(text="Обратная связь")
    button2 = KeyboardButton(text="Рекомендации")
    button3 = KeyboardButton(text="Помощь")
    
    # Создаем клавиатуру с кнопками
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2, button3]],  # Список кнопок
        resize_keyboard=True,  # Устанавливаем параметр для масштабирования
        one_time_keyboard=False  # Не скрывать клавиатуру после нажатия
    )
    
    return keyboard






