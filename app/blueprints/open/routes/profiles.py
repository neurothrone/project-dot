from flask import flash, redirect, render_template, request, url_for

from .. import bp_open
from app.controllers.project import ProjectController
from app.controllers.user import UserController


@bp_open.get("/profile/<username>")
def view_profile(username: str):
    if not (user := UserController.get_model_by_username(username)):
        flash("There is no user by that username.", category="error")
        return redirect(url_for(".index"))

    page = request.args.get("page", 1, type=int)
    paginator = ProjectController.get_all_projects_by_profile_paginated(
        user.profile.id, page)
    return render_template("open/profiles/view_profile.html",
                           paginator=paginator,
                           user=user,
                           username=user.username)
