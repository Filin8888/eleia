# маршрути (логіка сайту / API)
from flask import render_template, redirect, url_for, request, flash, session, Blueprint, abort
from models import User, Post, Comment, PostImage
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from extentions import db
import os
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import or_
from forms import PostForm, CommentForm
from utils import save_image


main_bp = Blueprint("main", __name__)


# =====================
#  Блог
# =====================
@main_bp.route("/blog", methods=["GET"])
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()  # якщо є поле created_at
    return render_template("blog.html", posts=posts)



# =====================
#  Реєстрація
# =====================
@main_bp.route("/register", methods=["GET", "POST"])
def register():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_password = request.form.get("password")
    if not user_name or not user_email or not user_password:
        flash("Всі поля обов'язкові для заповнення")
        return render_template("register.html")
    else:
        new_user = User(username=user_name, email=user_email)
        new_user.set_password(user_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Вас успішно зареєстровано")
        return redirect(url_for("main.blog"))

# =====================
# Логін
# =====================
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    identifier = request.form.get("username_of_email")
    password = request.form.get("password")

    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if user:
        check = user.check_password(password)
        if check:
            login_user(user)
            return redirect(url_for("main.blog"))
        else:
            flash("Невірний пароль")
            return render_template("login.html")
            
    else:
        flash("404: User not found")
        return render_template("login.html")



# =========================================
# Додавання посту 
# =========================================
@main_bp.route("/add_post", methods=["GET", "POST"])
@login_required
def add_post():
    if current_user.role in ['admin', 'moderator']:
        if request.method == "POST":
            title = request.form.get("title")   # беремо з форми
            content = request.form.get("content")

            if not title or not content:
                flash("Всі поля обов’язкові!", "danger")
                return redirect(url_for("main.create_post"))

            # створюємо пост, прив’язаний до користувача
            new_post = Post(
                title=title,
                content=content,
                user_id=current_user.id
            )
            db.session.add(new_post)
            db.session.commit()

            flash("Пост успішно доданий!", "success")
            return redirect(url_for("main.blog"))

        return render_template("create_post.html")


# ===================================================
# Видалення посту (тільки адмін, модератори та автор)
# ===================================================
@main_bp.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not post:
        flash("404: Post not found")
        return redirect(url_for("main.blog"))
    else:
        if current_user.role in ["admin", "moderator"] or current_user.id == post.user_id:
            db.session.delete(post)
            db.session.commit()
            flash("Пост видалено")
            return redirect(url_for("main.blog"))


# =====================
# Вихід
# =====================
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.blog"))

# =====================
# Сторінка Профілю
# =====================
@main_bp.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    from models import User
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)

# =====================
# Створити пост
# =====================
@main_bp.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()  # <- створюємо форму тут

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        # збереження зображень
        if form.images.data:  # якщо є файли
            for i, file in enumerate(form.images.data):
                filename = save_image(file)  # твоя функція збереження
                is_main = (i == int(form.main_image_index.data or 0))
                image = PostImage(filename=filename, post_id=post.id, is_main=is_main)
                db.session.add(image)
            db.session.commit()

        flash("Пост створено!", "success")
        return redirect(url_for("main.post", post_id=post.id))
    
      # Якщо GET або форма не пройшла валідацію
    return render_template("create_post.html", form=form)


    
# =====================
# Деталі посту
# =====================
@main_bp.route("/post/<int:post_id>", methods=["GET"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    comment_form = CommentForm()
    return render_template("post.html", post=post, comments=comments, comment_form=comment_form)

# =====================
# Видалення акаунту
# =====================
@main_bp.route("/delete_account/<int:user_id>", methods=["POST"])
@login_required
def delete_account(user_id):
    # користувач може видаляти лише свій акаунт
    if current_user.id != user_id:
        flash("❌ Ви не можете видалити чужий акаунт!", "danger")
        return redirect(url_for("main.profile", user_id=current_user.id))

    # видаляємо акаунт
    if current_user.id == user_id or current_user.role == 'admin':
        db.session.delete(current_user)
        db.session.commit()

    # розлогінюємо користувача
    logout_user()

    flash("✅ Ваш акаунт видалено!", "success")
    return redirect(url_for("main.blog"))

# =====================
# Вподобайки
# =====================
@main_bp.route("/post/<int:post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    if current_user in post.likes:
        post.likes.remove(current_user)
    else:
        post.likes.append(current_user)

    db.session.commit()
    return redirect(url_for("main.post", post_id=post.id))

# =====================
# Коментарі
# =====================
@main_bp.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get("content", "").strip()

    if not content:
        flash("Коментар не може бути порожнім.", "danger")
        return redirect(url_for("main.post", post_id=post.id))

    comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()

    flash("Коментар додано!", "success")
    return redirect(url_for("main.post", post_id=post.id))

# =====================
# Редагувати пост
# =====================
@main_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)  # заповнюємо форму даними посту

    # дозволяємо редагувати лише автору або адмінам
    if post.user_id != current_user.id and current_user.role != "admin":
        flash("У вас немає прав редагувати цей пост.", "danger")
        return redirect(url_for("main.post", post_id=post.id))

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        # якщо є зображення
        if form.images.data:
            for i, image_file in enumerate(form.images.data):
                filename = save_image(image_file)  # кожен файл окремо
                is_main = (i == int(form.main_image_index.data or 0))
                image = PostImage(filename=filename, post_id=post.id, is_main=is_main)
                db.session.add(image)
            db.session.commit()


        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for("main.post", post_id=post.id))

    return render_template("edit_post.html", post=post, form=form)


    
