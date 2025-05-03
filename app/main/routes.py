"""
Main routes – only two calendar views:
    • week  → Mon-Sun of the current week
    • total → last 30 days rolling
"""
from datetime import datetime, timedelta

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from app import db
from app.models import Habit, HabitRecord
from app.main.forms import AddHabitForm, AddActivityForm

main_bp = Blueprint("main", __name__, template_folder="templates")


# ─── helpers ─────────────────────────────────────────────────────────────
def _date_span(view: str):
    """Return list[YYYY-MM-DD] covering the chosen view."""
    today = datetime.now().date()

    if view == "week":
        monday = today - timedelta(days=today.weekday())
        return [
            (monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)
        ]

    # "total": today-29 … today
    return [
        (today - timedelta(days=delta)).strftime("%Y-%m-%d")
        for delta in range(29, -1, -1)
    ]


def _completed_by_habit(records):
    bucket = {}
    for rec in records:
        if rec.completed:
            bucket.setdefault(rec.habit_id, set()).add(
                rec.date.strftime("%Y-%m-%d")
            )
    return bucket


# ─── calendar view ───────────────────────────────────────────────────────
@main_bp.route("/")
def index():
    view = request.args.get("view", default="week")  # week | total

    habits = Habit.query.order_by(Habit.name).all()
    records = HabitRecord.query.filter(
        HabitRecord.habit_id.in_([h.id for h in habits])
    ).all()

    completed = _completed_by_habit(records)
    habit_blocks = [
        {"habit": h, "completed_dates": completed.get(h.id, set())}
        for h in habits
    ]

    return render_template(
        "index.html",
        view=view,
        today=datetime.now().strftime("%Y-%m-%d"),
        dates=_date_span(view),
        habit_blocks=habit_blocks,
    )


# ─── remaining CRUD routes (unchanged) ───────────────────────────────────
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
    form = AddHabitForm(obj=habit)
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


@main_bp.route("/add-activity", methods=["GET", "POST"])
def add_activity():
    form = AddActivityForm()
    form.habit_id.choices = [(h.id, h.name) for h in Habit.query.all()]

    habit_q = request.args.get("habit_id", type=int)
    date_q = request.args.get("date")

    if habit_q and not form.habit_id.data:
        form.habit_id.data = habit_q
    if date_q and not form.date.data:
        form.date.data = datetime.strptime(date_q, "%Y-%m-%d")

    existing = (
        HabitRecord.query.filter_by(
            habit_id=form.habit_id.data, date=form.date.data
        ).first()
        if form.habit_id.data and form.date.data
        else None
    )
    if request.method == "GET" and existing:
        form.completed.data = existing.completed
        form.note.data = existing.note

    if form.validate_on_submit():
        rec = (
            HabitRecord.query.filter_by(
                habit_id=form.habit_id.data, date=form.date.data
            ).first()
            or HabitRecord(habit_id=form.habit_id.data, date=form.date.data)
        )
        rec.completed = form.completed.data
        rec.note = form.note.data
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("add_activity.html", form=form)
