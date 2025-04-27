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

    today = datetime.now().strftime('%Y-%m-%d')  # Format like "2025-04-28"

    habits = Habit.query.all()
    habit_id = request.args.get('habit_id', type=int)
    selected_habit = None

    if habits:
        if habit_id:
            selected_habit = Habit.query.get_or_404(habit_id)
        else:
            selected_habit = habits[0]

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
            'month_number': month  # real month number for date building
        })

    return render_template('index.html',
                           habits=habits,
                           selected_habit=selected_habit,
                           months=months,
                           year=year,
                           today=today,
                           completed_dates=completed_dates)

@main_bp.route('/add-habit', methods=['GET', 'POST'])
def add_habit():
    form = AddHabitForm()
    if form.validate_on_submit():
        new_habit = Habit(name=form.name.data)
        db.session.add(new_habit)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_habit.html', form=form)

@main_bp.route('/add-activity', methods=['GET', 'POST'])
def add_activity():
    form = AddActivityForm()
    habits = Habit.query.all()
    form.habit_id.choices = [(habit.id, habit.name) for habit in habits]

    # Pre-fill from query parameters
    habit_id_param = request.args.get('habit_id', type=int)
    date_param = request.args.get('date')

    if habit_id_param and not form.habit_id.data:
        form.habit_id.data = habit_id_param
    if date_param and not form.date.data:
        form.date.data = datetime.strptime(date_param, '%Y-%m-%d')

    if form.validate_on_submit():
        habit_id = form.habit_id.data
        date = form.date.data
        completed = form.completed.data

        record = HabitRecord.query.filter_by(habit_id=habit_id, date=date).first()

        if record:
            record.completed = completed
        else:
            record = HabitRecord(habit_id=habit_id, date=date, completed=completed)
            db.session.add(record)

        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add_activity.html', form=form)
