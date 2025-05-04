from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db   = SQLAlchemy(app)

from app.main import main_bp
app.register_blueprint(main_bp)

with app.app_context():
    db.create_all()
