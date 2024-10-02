from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email ', validators=[DataRequired(), Email(message="INVALID EMAIL")])
    password = PasswordField('Password ', validators=[DataRequired()])
    submit = SubmitField('Login')