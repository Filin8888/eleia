from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_login import LoginManager
from extentions import db
from admin import init_admin
from flask_migrate import Migrate
from email.message import EmailMessage
import smtplib
import os
from models import User


login_manager = LoginManager()  # створюємо менеджер логіну


def create_app():
    app = Flask(__name__)                   # створюємо Flask-додаток
    app.config.from_object(Config)          # завантажуємо налаштування з config.py
    db.init_app(app)                        # прив’язуємо SQLAlchemy до Flask

    login_manager.init_app(app)             # прив'язуємо до Flask
    login_manager.login_view = "main.login" # маршрут для редиректу, якщо не залогінений

    # @app.route('/')
    # def index():
    #     return render_template('index.html')

    EMAIL_FROM = os.getenv("EMAIL_FROM")      # твій email
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    # EMAIL_TO = os.getenv("EMAIL_TO")          # куди приходять заявки

    def send_email(username, contact, message):
        
        msg = EmailMessage()
        msg["Subject"] = "Нова заявка на консультацію"
        msg["From"] = EMAIL_FROM
        msg["To"] = "eleiia.kp@gmail.com"
        msg["Reply-To"] = contact  # 👈 КЛЮЧОВЕ

        msg.set_content(f"""
                            Імʼя: {username}
                            Контакт: {contact}
                            Повідомлення:{message}
                        """)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        if "@" not in contact or "." not in contact:
            return "Invalid email", 400

    @app.route("/consultation", methods=["GET", "POST"])
    def consultation():
        if request.method == "POST":
            username = request.form["username"]
            contact = request.form["contact"]
            message = request.form["message"]

            send_email(username, contact, message)

            flash("Заявку відправлено! Ми звʼяжемось з вами.")
            return redirect(url_for("consultation"))
        
        return render_template("consultation.html")

    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/team')
    def team():
        return render_template('team.html')
    
    @app.route('/first')
    def first():
        return render_template('first.html')
    
    @app.route('/gimnazia')
    def gimnazia():
        return render_template('gimnazia.html')
    
    @app.route('/online')
    def online():
        return render_template('online.html')
    
    @app.route('/akademia')
    def akademia():
        return render_template('akademia.html')
    
    @app.route('/methodichka')
    def methodichka():
        return render_template('methodichka.html')
    
    @app.route('/learn')
    def learn():
        return render_template('learn.html')
    
    @app.route('/pedagog')
    def pedagog():
        return render_template('pedagog.html')
    
    @app.route('/havchik')
    def havchik():
        return render_template('havchik.html')
    
    @app.route('/prozorist')
    def prozorist():
        return render_template('prozorist.html')
    
    @app.route('/prava_baza')
    def prava_baza():
        return render_template('prava_baza.html')
    
    @app.route('/strategii')
    def strategii():
        return render_template('strategii.html')
    
    @app.route('/pologenia')
    def pologenia():
        return render_template('pologenia.html')
    


    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # реєструємо маршрути
    from routes import main_bp
    app.register_blueprint(main_bp)

    # створюємо таблиці
    with app.app_context():
        db.create_all()

    # підключаємо адмінку
    init_admin(app)

    # ✅ ініціалізація Flask-Migrate
    migrate = Migrate(app, db)




    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
