"""
Main routes for the Habit Tracker Flask app.

Views provided by “/”:

    • ?view=week     – current ISO week (Mon-Sun, one horizontal row)
    • ?view=overall  – last 22 weeks as a 7 × 22 grid (Mon at top)

All date-grid helpers live in app/main/helpers.py.
"""
from datetime import datetime

from flask import (
    redirect,
    render_template,
    request,
    url_for,
)

from app import db
from app.models import Habit, HabitRecord
from app.main import main_bp
from app.main.forms import AddHabitForm, AddActivityForm
from app.main.helpers import (
    week_span,
    overall_grid,
    completed_by_habit,        # ← moved out of this file
)


# ── calendar page ──────────────────────────────────────────────────────
@main_bp.route("/")
def index():
    view = request.args.get("view", default="week")          # "week" | "overall"

    # data
    habits = Habit.query.order_by(Habit.name).all()
    records = HabitRecord.query.filter(
        HabitRecord.habit_id.in_([h.id for h in habits])
    ).all()

    completed = completed_by_habit(records)
    habit_blocks = [
        {"habit": h, "completed_dates": completed.get(h.id, set())}
        for h in habits
    ]

    # context for template
    context = dict(
        view=view,
        today=datetime.now().strftime("%Y-%m-%d"),
        habit_blocks=habit_blocks,
    )

    if view == "overall":
        context["overall_grid"] = overall_grid()          # 7 rows × 22 columns
    else:
        context["week_dates"] = week_span()               # 7 dates Mon-Sun

    return render_template("index.html", **context)


# ── CRUD routes ────────────────────────────────────────────────────────
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
    date_q  = request.args.get("date")

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
        form.note.data      = existing.note

    if form.validate_on_submit():
        rec = existing or HabitRecord(
            habit_id=form.habit_id.data, date=form.date.data
        )
        rec.completed = form.completed.data
        rec.note      = form.note.data
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("add_activity.html", form=form)
