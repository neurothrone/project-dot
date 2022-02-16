from http import HTTPStatus

from flask import jsonify, request

from .. import bp_api, utils
from app.schemas.user import UserIn, UserUpdate
from app.controllers.user import UserController


@bp_api.post("/users")
def create_user():
    data = request.form
    # user = UserController.create(UserIn(**data))
    user = UserController.create_with_profile(UserIn(**data))
    return jsonify(user.dict()), HTTPStatus.CREATED


@bp_api.get("/users")
def read_users():
    data = [user.dict() for user in UserController.get_all()]
    return jsonify(data), HTTPStatus.OK


@bp_api.get("/users/<int:user_id>")
def read_user(user_id: int):
    if user := UserController.get_by_id(user_id):
        return jsonify(user.dict()), HTTPStatus.OK
    return utils.jsonify_not_found("User"), HTTPStatus.NOT_FOUND


@bp_api.patch("/users/<int:user_id>")
def update_user(user_id: int):
    data = request.form
    user_update = UserUpdate(**data)
    if user := UserController.update_model(user_id, user_update):
        return jsonify(user.dict()), HTTPStatus.ACCEPTED
    return utils.jsonify_not_found("User"), HTTPStatus.NOT_FOUND


@bp_api.delete("/users/<int:user_id>")
def delete_user(user_id: int):
    if UserController.delete(user_id):
        return "", HTTPStatus.NO_CONTENT
    return utils.jsonify_not_found("User"), HTTPStatus.NOT_FOUND
