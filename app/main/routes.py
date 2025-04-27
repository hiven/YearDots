from flask import render_template, request, redirect, url_for
from app.main import main_bp
from app.main.forms import AddHabitForm, AddActivityForm
from app.models import Habit, HabitRecord
from app import db
import calendar
from datetime import datetime

@main_bp.route('/')
def index():
    year = request.args.get('year', type=int)
    if not year:
        year = datetime.now().year

    today = datetime.now().strftime('%Y-%m-%d')
    current_year = datetime.now().year  # Pass separately

    habits = Habit.query.all()
    habit_id = request.args.get('habit_id', type=int)
    selected_habit = None

    if habits:
        if habit_id:
            selected_habit = Habit.query.get_or_404(habit_id)
        else:
            selected_habit = habits[0]

    # Find years where there are HabitRecords
    active_years = set()
    all_records = HabitRecord.query.all()
    for record in all_records:
        active_years.add(record.date.year)

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
            'start_empty': first_weekday,
            'month_number': month
        })

    return render_template('index.html',
                           habits=habits,
                           selected_habit=selected_habit,
                           months=months,
                           year=year,
                           current_year=current_year,
                           today=today,
                           completed_dates=completed_dates,
                           active_years=active_years)
