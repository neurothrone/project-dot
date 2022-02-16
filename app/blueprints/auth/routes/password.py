from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.password import (
    ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm)
from app.controllers.user import UserController
from app.services import email_service


@bp_auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.is_password_valid(form.old_password.data):
            current_user.password = form.password.data
            current_user.save()
            flash("Your password has been updated.")
            return redirect(url_for("open.view_profile", username=current_user.username))
        else:
            flash("Invalid password.")
    return render_template("auth/change_password.html",
                           form=form,
                           title="DoT - Change Password")


@bp_auth.route("/reset", methods=["GET", "POST"])
def reset_password():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = UserController.get_model_by_email(form.email.data.lower())
        if user:
            token = user.generate_reset_token()
            email_service.send_email(user.email, "Reset Your Password",
                       "auth/email/reset_password",
                       user=user, token=token)
        flash("An email with instructions to reset your password has been "
              "sent to you.", category="info")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html",
                           form=form,
                           title="DoT - Reset Your Password")


@bp_auth.route("/reset/<token>", methods=["GET", "POST"])
def reset_password_request(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if UserController.is_password_reset(token, form.password.data):
            flash("Your password has been updated.", category="success")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)
