from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_feedback_inline_keyboard():
    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Что понравилось", callback_data="like")],
        [InlineKeyboardButton(text="Что можно добавить", callback_data="improve")]
    ])
    
    # Возвращаем клавиатуру
    return keyboard



