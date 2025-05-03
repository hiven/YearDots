from os import getenv
from dotenv import load_dotenv

load_dotenv()                               # reads .env locally

class Config:
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY", "dev-key")
