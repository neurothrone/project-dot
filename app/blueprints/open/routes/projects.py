from flask import flash, make_response, redirect, render_template, request, url_for

from .. import bp_open
from app.controllers.project import ProjectController


@bp_open.get("/projects")
def projects():
    search_text = request.args.get("search_text", "")
    page = request.args.get("page", 1, type=int)
    paginator = ProjectController.get_all_by_ilike_title_paginated(search_text, page)
    return render_template("open/projects/index.html",
                           search_text=search_text,
                           paginator=paginator)


@bp_open.get("/projects/search")
def search_projects():
    # htmx passes a header
    is_htmx_request = "HX-Request" in request.headers
    search_text = request.args.get("search_text", "")
    page = request.args.get("page", 1, type=int)
    paginator = ProjectController.get_all_by_ilike_title_paginated(search_text, page)

    # if HTMX-originated return a partial response
    if is_htmx_request:
        html = render_template(
            "open/shared/partials/projects_search_results.html",
            search_text=search_text,
            paginator=paginator)
        return make_response(html)

    # return a full response
    return render_template("open/shared/partials/search.html",
                           search_text=search_text,
                           paginator=paginator)


@bp_open.get("/projects/<int:project_id>")
def view_project(project_id: int):
    if not (project := ProjectController.get_by_id(project_id)):
        flash("There is no project by that id.", category="error")
        return redirect(url_for(".index"))

    return render_template("open/projects/view_project.html",
                           project=project)
