import os


class Config:
    # your .env already provides a full postgresql:// URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///local.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
