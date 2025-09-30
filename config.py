import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://eleia_adm:eleia@localhost:5432/eleia"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret"