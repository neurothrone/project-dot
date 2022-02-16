from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.join import JoinForm
from app.controllers.user import UserController
from app.services import email_service

from app.schemas.user import UserIn


@bp_auth.get("/join")
def join():
    if current_user.is_authenticated:
        return redirect(url_for("open.index"))
    return render_template("auth/join.html", form=JoinForm())


@bp_auth.post("/join")
def join_post():
    form = JoinForm()
    if form.validate_on_submit():
        user = UserIn(username=form.username.data.lower(),
                      email=form.email.data.lower(),
                      password=form.password.data)
        UserController.create_with_profile(user)
        flash("You have successfully registered", category="success")
        return redirect(url_for("auth.login"))

        # user = UserController.create(email=form.email.data.lower(),
        #                              username=form.username.data.lower(),
        #                              password=form.password.data)

        # token = user.generate_confirmation_token()
        # email_service.send_email(user.email, "Confirm Your Account",
        #                          "auth/email/confirm", user=user, token=token)
        # flash("A confirmation email has been sent to you by email.", category="info")
        # login_user(user)
        # return redirect(url_for("auth.unconfirmed"))
    return render_template("auth/join.html", form=form)
