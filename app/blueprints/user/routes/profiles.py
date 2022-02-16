import imghdr
import os
import uuid

from PIL import Image
from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from .. import bp_user
from ..forms import EditProfileForm
from app.controllers.profile import ProfileController
from app.schemas.profile import ProfileIn


@bp_user.get("/edit-profile")
@login_required
def edit_profile():
    return render_template("user/profiles/edit_profile.html",
                           form=EditProfileForm(obj=current_user.profile))


@bp_user.post("/edit-profile")
@login_required
def edit_profile_post():
    # TODO: allow user to change username? Put in Settings instead of here

    # TODO: move all this logic into a ViewModel, pass the request form data
    # TODO: custom to_response() with make_response()

    form = EditProfileForm()
    if form.validate_on_submit():
        # Pass form data to EditProfileViewModel
        # delete non-essential fields
        # Use ProfileController to update the profile
        data = form.data
        ProfileController.update_model(current_user.profile.id, ProfileIn(**data))

        # image logic
        # if form.profile_image.data:
        #     file = form.profile_image.data
        #     image_id = str(uuid.uuid4())
        #     file_name = image_id + ".png"
        #     file_path = os.path.join(current_app.config["PROFILES_IMAGE_DIR"], file_name)
        #     Image.open(file).save(file_path)
        #     _image_resize(current_app.config["PROFILES_IMAGE_DIR"], image_id, 300, "sm")
        # else:
        #     image_id = None
        # if form.profile_image.data:
        #     file = form.profile_image.data
        #     image_id = str(uuid.uuid4())
        #     file_name = image_id + ".png"
        #     file_path = os.path.join(current_app.config["UPLOAD_PATH_PROFILES"], file_name)
        #     Image.open(file).save(file_path)
        #     image_id = _image_resize(current_app.config["UPLOAD_PATH_PROFILES"], image_id, 300, "sm")
        #
        #     os.remove(file_path)
        # else:
        #     image_id = None

        # data["profile_image"] = image_id

        # ProfileController.update(current_user.profile, data)

        flash(message="Changes to profile saved.", category="success")
        return redirect(url_for("open.view_profile", username=current_user.username))
    else:
        flash(message="Changes to profile not saved.", category="error")

    return render_template("user/profiles/edit_profile.html", form=form)


def _image_resize(original_file_path, image_id, image_base, extension) -> str:
    file_path = os.path.join(original_file_path, image_id + ".png")
    image = Image.open(file_path)
    wpercent = (image_base / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((image_base, hsize), Image.ANTIALIAS)
    modified_file_name = image_id + "." + extension + ".png"
    modified_file_path = os.path.join(original_file_path, image_id + "." + extension + ".png")
    image.save(modified_file_path)
    return modified_file_name


# @bp_main.post("/profile/upload")
# @login_required
def upload_profile_image():
    uploaded_file = request.files["profile_image"]
    filename = secure_filename(uploaded_file.filename)
    if filename:
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config["ALLOWED_UPLOAD_EXTENSIONS"] or file_ext != validate_image(
                uploaded_file.stream):
            abort(400)

    uploaded_file.save(os.path.join(current_app.config["UPLOAD_PATH_PROFILES"], current_user.username))
    return redirect()


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    _format = imghdr.what(None, header)
    if not _format:
        return None
    return "." + (_format if _format != "jpeg" else "jpg")
