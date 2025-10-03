from extentions import db
from models import User
from app import create_app   # беремо фабрику додатку

app = create_app()           # створюємо Flask-додаток

with app.app_context():
    admin = User(username="Yuri_admin", email="moiadress2005@gmail.com", role="admin")
    admin.set_password("123456")
    db.session.add(admin)
    db.session.commit()
    print("✅ Адмін створений")
