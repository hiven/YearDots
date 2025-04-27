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
            'month_number': month
        })

    return render_template('index.html',
                           habits=habits,
                           selected_habit=selected_habit,
                           months=months,
                           year=year,
                           today=today,
                           completed_dates=completed_dates)
