from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.blueprints.auth import bp_auth
from app.services import email_service


@bp_auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        # TODO: called multiple times -> performance check
        # print("PING ME")

        if not current_user.is_confirmed \
                and request.endpoint \
                and request.blueprint != "auth" \
                and request.endpoint != "static":
            return redirect(url_for("auth.unconfirmed"))
        else:
            pass
            # current_user.ping()


@bp_auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("open.index"))

    if current_user.confirm(token):
        flash("You have confirmed your account. Thanks!", category="success")
        return redirect(url_for("user.edit_profile"))
    else:
        flash("The confirmation link is invalid or has expired.", category="error")

    return redirect(url_for("open.index"))


@bp_auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.is_confirmed:
        return redirect(url_for("open.index"))

    return render_template("auth/unconfirmed.html",
                           title="DoT - Confirm Your Account")


@bp_auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    email_service.send_email(current_user.email, "Confirm Your Account",
                             "auth/email/confirm", user=current_user, token=token)
    flash("A new confirmation email has been sent to you by email.", category="success")
    return redirect(url_for("open.index"))
