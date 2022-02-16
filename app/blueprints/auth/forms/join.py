from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from app.controllers.user import UserController


class JoinForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="Username required."),
        Length(min=6, max=24, message="Username should be between 6 to 24 characters long."),
        Regexp(regex="^[A-Za-z][A-Za-z0-9_.]*$",
               flags=0,
               message="Username must only have letters, "
                       "numbers, dots or underscores")])
    email = StringField("Email", validators=[
        DataRequired(message="Email required."),
        Email(message="That is not a valid email address."),
        Length(max=64, message="Email should not be longer than 64 characters.")])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password required."),
        EqualTo("password2", message="Passwords don't match.")])
    password2 = PasswordField("Confirm Password", validators=[
        DataRequired(message="Password required.")])
    submit = SubmitField("Sign Up")

    def validate_username(self, field: StringField):
        if UserController.get_model_by_username(field.data):
            raise ValidationError("Please use a different username.")

    def validate_email(self, field: StringField):
        if UserController.get_model_by_email(field.data):
            raise ValidationError("Please use a different email.")

    def validate_password(self, field):
        # TODO: don't accept simple password, use regex to verify
        if len(field.data) < 6:
            raise ValidationError("The password must be equal to or greater than 6 letters long.")
