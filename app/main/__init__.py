from flask import Blueprint

# single blueprint, used by routes.py
main_bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
)

from app.main import routes    # noqa: E402  keeps routes attached to main_bp
