from flask import render_template, request, redirect, url_for
from app.main import main_bp
from app.main.forms import AddHabitForm, AddActivityForm
from app.models import Habit, HabitRecord
from app import db
import calendar
from datetime import datetime, timedelta

@main_bp.route('/')
def index():
    year = request.args.get('year', type=int)
    if not year:
        year = datetime.now().year

    view = request.args.get('view', default='year')  # 'week', 'month', or 'year'

    today = datetime.now().strftime('%Y-%m-%d')
    current_year = datetime.now().year

    habits = Habit.query.all()
    habit_id = request.args.get('habit_id', type=int)
    selected_habit = None

    if habits:
        if habit_id:
            selected_habit = Habit.query.get_or_404(habit_id)
        else:
            selected_habit = habits[0]

    # Find active years
    active_years = set()
    all_records = HabitRecord.query.all()
    for record in all_records:
        active_years.add(record.date.year)

    months = []
    completed_dates = set()

    if selected_habit:
        records = HabitRecord.query.filter_by(habit_id=selected_habit.id).all()
        completed_dates = {record.date.strftime('%Y-%m-%d') for record in records if record.completed}

    if view == 'week':
        # Show current week
        today_dt = datetime.now()
        start_of_week = today_dt - timedelta(days=today_dt.weekday())  # Monday
        week_days = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            if day.year == year:
                week_days.append(day.strftime('%Y-%m-%d'))
        months = week_days
    elif view == 'month':
        # Show current month
        this_month = datetime.now().month if year == current_year else 1
        num_days = calendar.monthrange(year, this_month)[1]
        month_days = []
        for day in range(1, num_days + 1):
            full_date = f"{year}-{this_month:02d}-{day:02d}"
            month_days.append(full_date)
        months = month_days
    else:
        # Full year
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
                           active_years=active_years,
                           view=view)
