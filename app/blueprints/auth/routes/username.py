from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.username import ChangeUsernameForm


@bp_auth.get("/change_username")
@login_required
def change_username():
    return render_template("auth/change_username.html",
                           form=ChangeUsernameForm(current_user.username))


@bp_auth.post("/change_username")
@login_required
def change_username_post():
    form = ChangeUsernameForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data.lower()
        current_user.save()
        flash("Username changed successfully.", category="success")
        return redirect(url_for("open.view_profile", username=current_user.username))
    flash("Something went wrong when attempting to change username.", category="error")
    return render_template("auth/change_username.html",
                           form=ChangeUsernameForm(current_user.username))
