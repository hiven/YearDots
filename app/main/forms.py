from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddHabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class AddActivityForm(FlaskForm):
    habit_id = SelectField('Habit', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    completed = BooleanField('Completed')
    note = TextAreaField('Note')
    submit = SubmitField('Save Activity')
