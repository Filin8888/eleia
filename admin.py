# admin.py
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask import redirect, url_for, request
from flask_login import current_user
from models import User, Post
from extentions import db
# from flask_admin.form import FileUploadField
# from flask_admin.form.upload import ImageUploadInput
# import os
# from flask import current_app

# class PostAdminView(SecureModelView):
#     # вказуємо, які поля будуть відображатися у формі
#     form_columns = ['title', 'content', 'image_filename', 'user']

#     # замість "image_filename" будемо використовувати FileUploadField
#     form_extra_fields = {
#         'image_filename': FileUploadField(
#             'Зображення',
#             base_path=os.path.join(current_app.root_path, 'static/uploads'),
#             allow_overwrite=True,
#             namegen=lambda obj, file_data: secure_filename(file_data.filename)
#         )
#     }



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


admin = Admin(name="Адмінка", template_mode="bootstrap4", index_view=MyAdminIndexView(url="/admin"))


def init_admin(app):
    admin.init_app(app)

    # додаємо моделі
    admin.add_view(SecureModelView(User, db.session, category="Models"))
    admin.add_view(SecureModelView(Post, db.session, category="Models"))

    # Простий і робочий варіант: додаємо статичне посилання на /blog
    # (це не вимагає app_context та працює одразу)
    admin.add_link(MenuLink(name="На сайт", url="/blog"))

    # АЛЬТЕРНАТИВА (якщо потрібен url_for, наприклад через префікси blueprint):
    # with app.app_context():
    #     admin.add_link(MenuLink(name="На сайт", url=url_for("main.blog")))
