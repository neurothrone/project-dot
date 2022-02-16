from http import HTTPStatus

from flask import render_template, request, jsonify

from . import bp_user


# TODO: bad request, unauhorized


@bp_user.app_errorhandler(HTTPStatus.FORBIDDEN)
def forbidden(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "forbidden"})
        response.status_code = HTTPStatus.FORBIDDEN
        return response
    return render_template("errors/403.html"), HTTPStatus.FORBIDDEN


@bp_user.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "not found"})
        response.status_code = HTTPStatus.NOT_FOUND
        return response
    return render_template("errors/404.html"), HTTPStatus.NOT_FOUND


@bp_user.app_errorhandler(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
def too_large_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "File is too large"})
        response.status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        return response
    return render_template("errors/413.html"), HTTPStatus.REQUEST_ENTITY_TOO_LARGE


@bp_user.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({"error": "internal server error"})
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return response

    return render_template("errors/500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
