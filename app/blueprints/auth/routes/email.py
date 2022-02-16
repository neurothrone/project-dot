from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.email import ChangeEmailForm
from app.services import email_service


@bp_auth.route("/change-email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.is_password_valid(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            email_service.send_email(new_email, "Confirm your email address",
                                     "auth/email/change_email",
                                     user=current_user, token=token)
            flash("An email with instructions to confirm your new email "
                  "address has been sent to you.", category="info")
            return redirect(url_for("open.index"))
        else:
            flash("Invalid email or password.", category="error")
    return render_template("auth/change_email.html", form=form)


@bp_auth.route("/change_email/<token>")
@login_required
def change_email_request(token):
    if current_user.change_email(token):
        current_user.save()
        flash("Your email address has been updated.", category="success")
    else:
        flash("Invalid request.", category="error")
    return redirect(url_for("open.index"))
