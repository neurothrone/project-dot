from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.login import LoginForm
from app.controllers.user import UserController


@bp_auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("open.index"))
    return render_template("auth/login.html", form=LoginForm(), title="DoT - Login")


@bp_auth.post("/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserController.get_model_by_username(form.username.data)
        login_user(user, form.remember_me.data)

        flash("You have successfully logged in.", category="success")
        next_page = request.args.get("next")

        # Use of url_parse() for increased security against possible attackers that could
        # insert a malicious url as the next page. This ensures that any redirect is only
        # within the same site.
        if not next_page or not next_page.startswith("/") or url_parse(next_page).netloc != "":
            next_page = url_for("open.index")

        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@bp_auth.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", category="success")
    return redirect(url_for("open.index"))
