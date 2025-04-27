from app import db
from datetime import datetime

class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to habit records
    records = db.relationship('HabitRecord', backref='habit', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Habit {self.name}>'

class HabitRecord(db.Model):
    __tablename__ = 'habit_records'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<HabitRecord {self.habit_id} {self.date} {self.completed}>'
