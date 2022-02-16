from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp

from app.controllers.user import UserController


def validate_credentials(form, field):
    username = field.data
    password = form.password.data

    if not UserController.is_credentials_valid(username, password):
        raise ValidationError("Invalid credentials.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="Username required."),
        Length(min=6, max=24, message="Username should be between 6 to 24 characters long."),
        validate_credentials])
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password required."),
                    Length(min=6, max=32,
                           message="Password should be between 6 to 32 characters long.")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
