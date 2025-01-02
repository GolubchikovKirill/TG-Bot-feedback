#bot/handlers/messages.py
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from keyboards.reply import ReplyKeyboardManager
from keyboards.inline import InlineKeyboardManager
from database import feedback_repository

logger = logging.getLogger(__name__)

class MessageHandler:
    """Класс для обработки сообщений бота"""
    def __init__(self):
        self.router = Router()
        self.reply_keyboard = ReplyKeyboardManager()
        self.inline_keyboard = InlineKeyboardManager()
        self._setup_handlers()

    def _setup_handlers(self):
        """Настройка обработчиков сообщений"""
        self.router.message.register(self.start_command_handler, Command("start"))
        self.router.message.register(self.feedback_message, F.text == "Обратная связь")
        self.router.message.register(self.help_command_handler, Command("help"))
        self.router.message.register(self.help_command_handler, F.text == "Помощь")
        self.router.message.register(self.stats_command_handler, Command("stats"))
        self.router.message.register(self.recommendations_message, F.text == "Рекомендации")

    async def start_command_handler(self, message: types.Message):
        """Обработчик команды /start"""
        try:
            await message.answer(
                "<b>Уважаемый студент! Я <s>бот</s> кот для сбора обратной связи после групповой консультации.</b>\n"
                "<b>Для того, чтобы поделиться тем, что тебе понравилось и/или ты хотел бы добавить, нажми кнопку ниже.</b>",
                parse_mode="HTML",
                reply_markup=self.reply_keyboard.get_main_keyboard()
            )
            logger.info(f"Пользователь {message.from_user.id} запустил бота")
        except Exception as e:
            logger.error(f"Ошибка при обработке команды start: {e}")
            await self._handle_error(message)

    async def feedback_message(self, message: types.Message):
        """Обработчик кнопки 'Обратная связь'"""
        try:
            await message.answer(
                "<b>Выберите тип обратной связи.</b>",
                parse_mode="HTML",
                reply_markup=self.inline_keyboard.get_feedback_keyboard()
            )
            logger.info(f"Пользователь {message.from_user.id} открыл меню обратной связи")
        except TelegramBadRequest as e:
            logger.error(f"Ошибка Telegram при отправке сообщения: {e}")
            await self._handle_error(message)
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            await self._handle_error(message)

    async def help_command_handler(self, message: types.Message):
        """Обработчик команды /help"""
        try:
            await message.answer(
                "<b>Для того, чтобы оставить обратную связь, нужно нажать на кнопку -Обратная связь-.</b>\n"
                "<b>В появившемся сообщении выбрать тип обратной связи.</b>\n"
                "<b>После этого написать свое сообщение для обратной связи.</b>\n"
                "<b>Кнопка -Рекомендации- еще в разработке.</b>",
                parse_mode="HTML",
                reply_markup=self.reply_keyboard.get_main_keyboard()
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке справки: {e}")
            await self._handle_error(message)

    async def stats_command_handler(self, message: types.Message):
        """Обработчик команды /stats"""
        try:
            stats = feedback_repository.get_feedback_stats()
            await message.answer(
                "<b>📊 Статистика отзывов:</b>\n\n"
                f"Всего отзывов: {stats['total']}\n"
                f"Положительных: {stats['likes']}\n"
                f"Предложений по улучшению: {stats['improvements']}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            await message.answer("Не удалось получить статистику. Попробуйте позже.")

    async def recommendations_message(self, message: types.Message):
        """Обработчик кнопки 'Рекомендации'"""
        await message.answer(
            "🔄 Функция рекомендаций находится в разработке.\n"
            "Следите за обновлениями!",
            reply_markup=self.reply_keyboard.get_main_keyboard()
        )

    async def _handle_error(self, message: types.Message):
        """Обработка ошибок с отправкой сообщения пользователю"""
        await message.answer(
            "❌ Произошла ошибка при обработке вашего запроса.\n"
            "Пожалуйста, попробуйте позже или обратитесь к администратору.",
            reply_markup=self.reply_keyboard.get_main_keyboard()
        )

# Создаем экземпляр обработчика сообщений
message_handler = MessageHandler()
router = message_handler.router
