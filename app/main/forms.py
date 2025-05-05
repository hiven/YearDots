from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired
from flask import current_app


class AddHabitForm(FlaskForm):
    name   = StringField("Habit Name", validators=[DataRequired()])
    colour = SelectField("Dot Colour", validators=[DataRequired()], coerce=str)
    submit = SubmitField("Save Habit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        palette = current_app.config["HABIT_COLOURS"]
        self.colour.choices = [(c, c) for c in palette]
        if not self.colour.data:
            self.colour.data = palette[0]


class AddActivityForm(FlaskForm):
    habit_id  = SelectField("Habit", coerce=int, validators=[DataRequired()])
    date      = DateField("Date", validators=[DataRequired()])
    completed = BooleanField("Completed")
    note      = TextAreaField("Note")
    submit    = SubmitField("Save Activity")
