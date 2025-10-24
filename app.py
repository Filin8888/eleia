from flask import Flask, render_template
from config import Config
from flask_login import LoginManager
from extentions import db
from admin import init_admin
from flask_migrate import Migrate




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
