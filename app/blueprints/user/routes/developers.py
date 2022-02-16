from flask import render_template
from flask_login import current_user, login_required

from .. import bp_user
from app.controllers.profile import ProfileController


@bp_user.before_app_request
def before_app_request():
    if current_user.is_authenticated:
        ProfileController.ping_user(current_user.profile.id)


@bp_user.get("/settings")
@login_required
def settings():
    return render_template("auth/settings.html",
                           title="Settings - DoT")
