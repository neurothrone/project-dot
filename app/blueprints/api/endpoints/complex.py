from flask import request

from .. import bp_api
from ..apimodels.complex import (
    AddProjectToUserAPIModel,
    AddExistingProjectToUserAPIModel,
    RemoveProjectFromUserAPIModel
)


@bp_api.post("/complex/add/<int:user_id>")
def add_project_to_user(user_id: int):
    am = AddProjectToUserAPIModel(request.form, user_id)
    am.exec()
    return am.to_response()


@bp_api.get("/complex/add/<int:project_id>/<int:user_id>")
def add_existing_project_to_user(project_id: int, user_id: int):
    am = AddExistingProjectToUserAPIModel(project_id, user_id)
    am.exec()
    return am.to_response()


@bp_api.delete("/complex/remove/<int:project_id>/<int:user_id>")
def remove_project_from_user(project_id: int, user_id: int):
    am = RemoveProjectFromUserAPIModel(project_id, user_id)
    am.exec()
    return am.to_response()
