import calendar
from collections import defaultdict
from datetime import datetime, timedelta

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_wtf.csrf import validate_csrf, CSRFError

from app import db
from app.main import main_bp
from app.main.forms import AddHabitForm, AddActivityForm
from app.models import Habit, HabitRecord


# ──────────────────────────────────────────────────────────────
@main_bp.route("/")
def index():
    year = request.args.get("year", type=int) or datetime.now().year
    view = request.args.get("view", default="year")          # week | month | year

    today        = datetime.now().strftime("%Y-%m-%d")
    current_year = datetime.now().year

    habits = Habit.query.order_by(Habit.name).all()

    # one query for the lot
    records = HabitRecord.query.filter(
        HabitRecord.habit_id.in_([h.id for h in habits])
    ).all()

    completed_by_habit = defaultdict(set)
    active_years       = set()

    for r in records:
        active_years.add(r.date.year)
        if r.completed:
            completed_by_habit[r.habit_id].add(r.date.strftime("%Y-%m-%d"))

    habit_blocks = [
        {
            "habit": habit,
            "completed_dates": completed_by_habit.get(habit.id, set()),
        }
        for habit in habits
    ]

    months_or_days = build_calendar_structure(view, year, current_year)

    return render_template(
        "index.html",
        view=view,
        year=year,
        current_year=current_year,
        today=today,
        habit_blocks=habit_blocks,
        months_or_days=months_or_days,
        active_years=active_years,
    )


# ──────────────────────────────────────────────────────────────
def build_calendar_structure(view: str, year: int, current_year: int):
    """Return the list the template needs for the selected view."""
    if view == "week":
        today_dt = datetime.now()
        start    = today_dt - timedelta(days=today_dt.weekday())   # Monday
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    if view == "month":
        month  = datetime.now().month if year == current_year else 1
        ndays  = calendar.monthrange(year, month)[1]
        return [f"{year}-{month:02d}-{d:02d}" for d in range(1, ndays + 1)]

    # full year
    months = []
    for m in range(1, 13):
        ndays, first_wkday = calendar.monthrange(year, m)
        months.append({
            "name": calendar.month_abbr[m],
            "days": ndays,
            "start_empty": first_wkday,
            "month_number": m,
        })
    return months


# ──────────────────────────────────────────────────────────────
@main_bp.route("/add-habit", methods=["GET", "POST"])
def add_habit():
    form = AddHabitForm()
    if form.validate_on_submit():
        db.session.add(Habit(name=form.name.data))
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add_habit.html", form=form)


@main_bp.route("/manage-habits")
def manage_habits():
    return render_template("manage_habits.html", habits=Habit.query.all())


@main_bp.route("/edit-habit/<int:habit_id>", methods=["GET", "POST"])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    form  = AddHabitForm(obj=habit)
    if form.validate_on_submit():
        habit.name = form.name.data
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("edit_habit.html", form=form, habit=habit)


@main_bp.route("/delete-habit/<int:habit_id>", methods=["POST"])
def delete_habit(habit_id):
    db.session.delete(Habit.query.get_or_404(habit_id))
    db.session.commit()
    return redirect(url_for("main.manage_habits"))


# ──────────────────────────────────────────────────────────────
@main_bp.route("/add-activity", methods=["GET", "POST"])
def add_activity():
    form = AddActivityForm()
    form.habit_id.choices = [(h.id, h.name) for h in Habit.query.all()]

    habit_q = request.args.get("habit_id", type=int)
    date_q  = request.args.get("date")

    if habit_q and not form.habit_id.data:
        form.habit_id.data = habit_q
    if date_q and not form.date.data:
        form.date.data = datetime.strptime(date_q, "%Y-%m-%d")

    existing = (
        HabitRecord.query.filter_by(
            habit_id=form.habit_id.data, date=form.date.data
        ).first()
        if form.habit_id.data and form.date.data else None
    )

    if request.method == "GET" and existing:
        form.completed.data = existing.completed
        form.note.data      = existing.note

    if form.validate_on_submit():
        rec = (
            HabitRecord.query.filter_by(
                habit_id=form.habit_id.data, date=form.date.data
            ).first()
            or HabitRecord(habit_id=form.habit_id.data, date=form.date.data)
        )
        rec.completed = form.completed.data
        rec.note      = form.note.data
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("add_activity.html", form=form)


