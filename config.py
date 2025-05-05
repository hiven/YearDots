import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (os.getenv("DATABASE_URL") or "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")

    # Colour palette for per‑habit dots
    HABIT_COLOURS = [
        "#007aff",  # blue (default)
        "#4caf50",  # green
        "#ff5722",  # orange
        "#9c27b0",  # purple
    ]
