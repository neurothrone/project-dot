from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length

from app.controllers.user import UserController


class ChangeEmailForm(FlaskForm):
    email = StringField("New Email", validators=[
        DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[
        DataRequired()])

    submit = SubmitField("Change Email Address")

    def validate_email(self, field):
        if UserController.get_by_email(field.data.lower()):
            raise ValidationError("Email already registered.")
