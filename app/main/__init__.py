from flask import Blueprint

video_bp = Blueprint('video', __name__, template_folder='templates')
from app.video import routes
