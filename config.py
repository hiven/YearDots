import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://yeardotsdb_user:m8UtCgbPCWyzBzVthRHq7WKBHGjHrVY2@dpg-d072bl2li9vc73esbh20-a/yeardotsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
