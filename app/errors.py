from http import HTTPStatus

import werkzeug.exceptions
from flask import Flask, render_template


def register_error_handlers(_app: Flask) -> None:
    @_app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request_error(error):
        return render_template("errors/400.html"), HTTPStatus.BAD_REQUEST

    @_app.errorhandler(HTTPStatus.UNAUTHORIZED)
    def bad_request_error(error):
        return render_template("errors/401.html"), HTTPStatus.UNAUTHORIZED

    @_app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found_error(error):
        err: werkzeug.exceptions.NotFound = error
        message = err.description if err.description else str(error).split(":")[-1].strip()
        return render_template("errors/404.html", message=message), HTTPStatus.NOT_FOUND

    @_app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def not_found_error(error):
        return render_template("errors/500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
