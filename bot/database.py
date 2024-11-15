#bot/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from config import DATABASE_URL

# Настройка подключения к базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель для таблицы user_feedback
class UserFeedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    feedback_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default="CURRENT_TIMESTAMP")
    chat_id = Column(BigInteger, nullable=True)
    user_id = Column(Integer, nullable=True)
    feedback_text = Column(Text, nullable=True)

# Инициализация базы данных (создание таблиц)
def init_db():
    Base.metadata.create_all(bind=engine)

# Функция сохранения отзыва
def save_feedback(user_id: int, feedback_type: str, feedback_text: str):
    db = SessionLocal()
    try:
        print(f"Обработка отзыва для user_id: {user_id}")

        # Проверяем, есть ли уже отзыв от этого пользователя
        existing_feedback = db.query(UserFeedback).filter(UserFeedback.user_id == user_id).first()
        if existing_feedback:
            print(f"Найден существующий отзыв для user_id: {user_id}")
            if existing_feedback.feedback_type != feedback_type or existing_feedback.feedback_text != feedback_text:
                print(f"Данные изменились. Обновляем отзыв для user_id: {user_id}")
                existing_feedback.feedback_type = feedback_type
                existing_feedback.feedback_text = feedback_text
                db.commit()  # Сохраняем изменения
                print(f"Отзыв пользователя с user_id {user_id} был обновлен.")
            else:
                print(f"Отзыв пользователя с user_id {user_id} уже актуален. Обновлений не требуется.")
        else:
            print(f"Отзыв для user_id {user_id} не найден. Добавляем новый.")
            feedback = UserFeedback(user_id=user_id, feedback_type=feedback_type, feedback_text=feedback_text)
            db.add(feedback)
            db.commit()
            print("Отзыв успешно сохранен.")
    except IntegrityError as e:
        db.rollback()
        print(f"Ошибка сохранения отзыва: {e.orig}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка сохранения отзыва: {e}")
    finally:
        db.close()  # Закрываем сессию









