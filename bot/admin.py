# admin.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import DATABASE_URL  # Подключаем URL для базы данных

# Создаем Flask приложение
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для таблицы feedback
class UserFeedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    feedback_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    chat_id = db.Column(db.BigInteger)
    user_id = db.Column(db.Integer)
    feedback_text = db.Column(db.Text)

# Создание базы данных, если она не существует
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

