from datetime import datetime
from app import db


class Habit(db.Model):
    __tablename__ = "habits"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship(
        "HabitRecord",
        backref="habit",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Habit {self.name}>"


class HabitRecord(db.Model):
    __tablename__ = "habit_records"

    id        = db.Column(db.Integer, primary_key=True)
    habit_id  = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    date      = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    note      = db.Column(db.String(255))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<HabitRecord {self.habit_id} {self.date} {self.completed}>"
