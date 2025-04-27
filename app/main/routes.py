from flask import render_template
import calendar
from app.main import main_bp

@main_bp.route('/')
def year_in_dots():
    year = 2025
    months = []

    for month in range(1, 13):
        month_name = calendar.month_abbr[month]
        num_days = calendar.monthrange(year, month)[1]
        first_weekday = calendar.monthrange(year, month)[0]  # 0 = Monday

        months.append({
            'name': month_name,
            'days': num_days,
            'start_empty': first_weekday
        })

    return render_template('main/index.html', months=months, year=year)
