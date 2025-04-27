from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AddHabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class AddActivityForm(FlaskForm):
    habit_id = SelectField('Habit', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    completed = BooleanField('Completed')
    note = StringField('Note')  # <-- New note field
    submit = SubmitField('Save Activity')
