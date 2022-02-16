from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[
        DataRequired()])
    password = PasswordField("New password", validators=[
        DataRequired(), EqualTo('password2', message="Passwords must match.")])
    password2 = PasswordField("Confirm new password",
                              validators=[DataRequired()])

    submit = SubmitField("Change Password")


class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(), Length(1, 64), Email()])

    submit = SubmitField("Reset Password")


class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password", validators=[
        DataRequired(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[
        DataRequired()])

    submit = SubmitField("Reset Password")
