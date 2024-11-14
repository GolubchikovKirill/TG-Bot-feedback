from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import save_feedback

router = Router()

# Определяем состояния для ожидания отзыва
class FeedbackStates(StatesGroup):
    waiting_for_feedback_text = State()

# Обработчик для кнопки "Что понравилось"
@router.callback_query(lambda callback: callback.data == "like")
async def handle_like(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем нажатие сразу
    await state.update_data(feedback_type="Понравилось")
    await callback.message.answer("Напишите, что вам понравилось:")
    await state.set_state(FeedbackStates.waiting_for_feedback_text)

# Обработчик для кнопки "Что можно улучшить"
@router.callback_query(lambda callback: callback.data == "improve")
async def handle_improve(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем нажатие сразу
    await state.update_data(feedback_type="Добавить")
    await callback.message.answer("Напишите, что можно улучшить:")
    await state.set_state(FeedbackStates.waiting_for_feedback_text)

# Обработчик для получения текста отзыва после выбора типа
@router.message(FeedbackStates.waiting_for_feedback_text, F.text)
async def feedback_text_received(msg: Message, state: FSMContext):
    data = await state.get_data()
    feedback_type = data.get("feedback_type")
    feedback_text = msg.text

    # Сохранение отзыва в базе данных с обработкой возможных ошибок
    try:
        save_feedback(user_id=msg.from_user.id, feedback_type=feedback_type, feedback_text=feedback_text)
        await msg.answer("Благодарим за обратную связь!")
    except Exception as e:
        await msg.answer(f"Произошла ошибка при сохранении отзыва: {e}")
    finally:
        await state.clear()

