from flask import render_template, request, jsonify, redirect, url_for
from app.main import main_bp
from app.models import Habit, HabitRecord
from app import db
import calendar
from datetime import datetime

@main_bp.route('/')
def index():
    year = 2025
    habits = Habit.query.all()

    habit_id = request.args.get('habit_id', type=int)
    if habit_id:
        selected_habit = Habit.query.get_or_404(habit_id)
    else:
        selected_habit = habits[0] if habits else None

    months = []
    completed_dates = set()

    if selected_habit:
        records = HabitRecord.query.filter_by(habit_id=selected_habit.id).all()
        completed_dates = {record.date.strftime('%Y-%m-%d') for record in records if record.completed}

    for month in range(1, 13):
        month_name = calendar.month_abbr[month]
        num_days = calendar.monthrange(year, month)[1]
        first_weekday = calendar.monthrange(year, month)[0]

        months.append({
            'name': month_name,
            'days': num_days,
            'start_empty': first_weekday
        })

    return render_template('index.html',
                           habits=habits,
                           selected_habit=selected_habit,
                           months=months,
                           year=year,
                           completed_dates=completed_dates)

@main_bp.route('/add-habit', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_habit = Habit(name=name)
            db.session.add(new_habit)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('add_habit.html')

@main_bp.route('/toggle', methods=['POST'])
def toggle_day():
    data = request.get_json()
    habit_id = data.get('habit_id')
    date_str = data.get('date')  # e.g., "2025-01-01"
    day_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    record = HabitRecord.query.filter_by(habit_id=habit_id, date=day_date).first()

    if record:
        record.completed = not record.completed
    else:
        record = HabitRecord(habit_id=habit_id, date=day_date, completed=True)
        db.session.add(record)

    db.session.commit()

    return jsonify(success=True, completed=record.completed)
