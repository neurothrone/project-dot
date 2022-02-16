from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL


class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[
        Length(min=0, max=32)])
    surname = StringField("Surname", validators=[
        Length(min=0, max=32)])
    city = StringField("City", validators=[
        Length(min=0, max=64)])
    profile_image = FileField("Profile Image", validators=[
        FileAllowed(["jpg", "png"], message="Image must be of type jpg or png.")])
    headline = TextAreaField("Headline", validators=[
        Length(min=0, max=255)])
    bio = TextAreaField("Bio", validators=[
        Length(min=0, max=2000)])

    social_website = StringField("Website", validators=[
        # URL(message="That is not a valid URL.")])
        Optional(), URL(message="That is not a valid URL.")])
    social_github = StringField("GitHub", validators=[
        Optional(), URL(message="That is not a valid URL.")])
    social_linkedin = StringField("Linkedin", validators=[
        Optional(), URL(message="That is not a valid URL.")])
    social_youtube = StringField("YouTube", validators=[
        Optional(), URL(message="That is not a valid URL.")])

    submit = SubmitField("Save changes")


class BaseProjectForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired(), Length(min=1, max=64)])
    description = TextAreaField("Description", validators=[
        Length(min=0, max=2000)])

    demo_link = StringField("Demo link", validators=[
        Optional(), URL(message="That is not a valid URL.")])
    source_link = StringField("Source Link", validators=[
        Optional(), URL(message="That is not a valid URL.")])


class EditProjectForm(BaseProjectForm):
    submit = SubmitField("Save Changes")


class NewProjectForm(BaseProjectForm):
    submit = SubmitField("Create Project")
