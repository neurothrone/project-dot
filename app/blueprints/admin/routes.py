from datetime import datetime

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.blueprints.admin import bp_admin


@bp_admin.before_request
def admin_pages_before_request():
    if not current_user.is_admin:
        return redirect(url_for("main.index"))


@bp_admin.get("/")
@login_required
def index():
    return render_template("admin/index.html")


@bp_admin.get("/sandbox")
@login_required
def sandbox():
    now = datetime.utcnow()
    return render_template("admin/sandbox.html",
                           now=now,
                           title="DoT - Sandbox")
