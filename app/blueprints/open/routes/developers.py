from flask import make_response, redirect, render_template, request, url_for

from .. import bp_open
from app.controllers.user import UserController


@bp_open.get("/")
def index():
    return redirect(url_for(".developers"))


@bp_open.get("/developers")
def developers():
    search_text = request.args.get("search_text", "")
    page = request.args.get("page", 1, type=int)
    paginator = UserController.get_all_ilike_username_paginated(search_text, page)
    return render_template("open/developers/index.html",
                           search_text=search_text,
                           paginator=paginator)


@bp_open.get("/developers/search")
def search_developers():
    # htmx passes a header
    is_htmx_request = "HX-Request" in request.headers
    search_text = request.args.get("search_text", "")
    page = request.args.get("page", 1, type=int)
    paginator = UserController.get_all_ilike_username_paginated(search_text, page)

    # if HTMX-originated return a partial response
    if is_htmx_request:
        html = render_template(
            "open/shared/partials/developers_search_results.html",
            search_text=search_text,
            paginator=paginator)
        return make_response(html)

    # return a full response
    return render_template("open/shared/partials/search.html",
                           search_text=search_text,
                           paginator=paginator)
