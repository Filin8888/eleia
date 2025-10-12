# admin.py
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask import redirect, url_for, request
from flask_login import current_user
from models import User, Post
from extentions import db


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "role", None) == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.login", next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "role", None) == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.login", next=request.url))


# 🔒 Безпечний базовий клас для адмінки
class SecureModelView(ModelView):
    def is_accessible(self):
        # тільки для залогінених адмінів
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # якщо не має доступу — редирект на логін
        return redirect(url_for('main.login', next=request.url))


# 👤 Вигляд моделі користувача
class UserAdminView(SecureModelView):
    column_list = ('id', 'username', 'email', 'role')
    form_columns = ('username', 'email', 'password_hash', 'role')
    column_editable_list = ('role',)
    can_create = False  # користувачів створює форма реєстрації
    can_delete = True




def init_admin(app):
    # 1️⃣ створюємо екземпляр адмінки
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

    # 2️⃣ додаємо моделі
    admin.add_view(UserAdminView(User, db.session, category="Models"))
    admin.add_view(SecureModelView(Post, db.session, category="Models"))

    # 3️⃣ додаємо посилання "На сайт"
    admin.add_link(MenuLink(name="На сайт", url="/blog"))

    
    
