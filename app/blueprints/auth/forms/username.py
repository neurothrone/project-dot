from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app.controllers.user import UserController


class ChangeUsernameForm(FlaskForm):
    username = StringField("New Username", validators=[
        DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[
        DataRequired()])

    submit = SubmitField("Change Username")

    def __init__(self, original_username: str, *args, **kwargs) -> None:
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username: StringField) -> None:
        if username.data != self.original_username:
            if not UserController.get_by_username(self.username.data):
                raise ValidationError("Please use a different username.")
