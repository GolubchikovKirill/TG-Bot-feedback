#bot/admin.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import UserFeedback  # Импортируем модель из database.py
from config import DATABASE_URL  # Подключаем URL для базы данных
from dotenv import load_dotenv  # Для загрузки переменных из .env
import os  # Для доступа к переменным окружения

# Загрузка переменных из .env
load_dotenv()

# Создаем Flask приложение
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")  # Загрузка секретного ключа из .env

db = SQLAlchemy(app)

# Инициализация базы данных вручную
def init_db():
    with app.app_context():
        db.create_all()

# Админ-панель с возможностью управления отзывами
class FeedbackModelView(ModelView):
    # Указываем, какие поля будут отображаться в списке
    column_list = ['id', 'feedback_type', 'content', 'created_at', 'chat_id', 'user_id', 'feedback_text']
    form_columns = ['feedback_type', 'content', 'created_at', 'chat_id', 'user_id', 'feedback_text']
    can_create = True  # Можно создавать записи
    can_edit = True    # Можно редактировать записи
    can_delete = True  # Можно удалять записи

# Создание админ-панели
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(FeedbackModelView(UserFeedback, db.session))

# Инициализация базы данных вручную
init_db()

if __name__ == '__main__':
    app.run(debug=True)



