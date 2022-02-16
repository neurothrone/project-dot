from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user

from app.blueprints.auth import bp_auth
from app.blueprints.auth.forms.account import DeleteAccountForm


@bp_auth.get("/delete-account")
@login_required
def delete_account():
    return render_template("auth/delete_account.html",
                           form=DeleteAccountForm(),
                           title="DoT - Delete Account")


@bp_auth.post("/delete-account")
@login_required
def delete_account_post():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if current_user.is_password_valid(form.password.data):
            current_user.delete()
            logout_user()
            flash("Your account has been successfully deleted.", category="success")
            return redirect(url_for("open.index"))
        flash("Password was incorrect, please try again.", category="error")
    return render_template("auth/delete_account.html",
                           form=form,
                           title="DoT - Delete Account")
