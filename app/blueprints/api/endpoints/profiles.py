from http import HTTPStatus

from flask import jsonify, request

from .. import bp_api, utils
from app.controllers.profile import ProfileController
from app.schemas.profile import ProfileIn, ProfileUpdate


@bp_api.post("/profiles")
def create_profile():
    data = request.form
    profile = ProfileController.create(ProfileIn(**data))
    return jsonify(profile.dict()), HTTPStatus.CREATED


@bp_api.get("/profiles")
def read_profiles():
    data = [profile.dict() for profile in ProfileController.get_all()]
    return jsonify(data), HTTPStatus.OK


@bp_api.get("/profiles/<int:profile_id>")
def read_profile(profile_id: int):
    if profile := ProfileController.get_by_id(profile_id):
        return jsonify(profile.dict()), HTTPStatus.OK
    return utils.jsonify_not_found("Profile"), HTTPStatus.NOT_FOUND


@bp_api.patch("/profiles/<int:profile_id>")
def update_profile(profile_id: int):
    data = request.form
    profile_update = ProfileUpdate(**data)
    if profile := ProfileController.update_model(profile_id, profile_update):
        return jsonify(profile.dict()), HTTPStatus.ACCEPTED
    return utils.jsonify_not_found("Profile"), HTTPStatus.NOT_FOUND


@bp_api.delete("/profiles/<int:profile_id>")
def delete_profile(profile_id: int):
    if ProfileController.delete(profile_id):
        return "", HTTPStatus.NO_CONTENT
    return utils.jsonify_not_found("Profile"), HTTPStatus.NOT_FOUND
