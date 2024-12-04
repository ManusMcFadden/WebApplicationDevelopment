from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, NumberRange

class SignupForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class WorkoutForm(FlaskForm):
    workout = SelectField('Workout', validators=[DataRequired()], choices=[])
    sets = IntegerField('Sets', validators=[
        DataRequired(), InputRequired(), NumberRange(min=1, message="Sets must be a positive, non-zero number.")
    ])
    reps = IntegerField('Reps', validators=[
        DataRequired(), NumberRange(min=1, max=12, message="Reps must be between 1 and 12.")
    ])
    difficulty = IntegerField('Difficulty', validators=[
        DataRequired(), NumberRange(min=6, max=10, message="Difficulty must be between 6 and 10.")
    ])
    weight = IntegerField('Weight', validators=[
        DataRequired(), InputRequired(), NumberRange(min=1, message="Weight must be a positive, non-zero number.")
    ])
    notes = TextAreaField('Notes', validators=[DataRequired()])