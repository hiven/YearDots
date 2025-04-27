from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from app.video import video_bp
app.register_blueprint(video_bp)

# Create the database tables
with app.app_context():
    db.create_all()
