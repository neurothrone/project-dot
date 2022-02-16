from http import HTTPStatus

from flask import jsonify, request

from .. import bp_api, utils
from app.controllers.project import ProjectController, ProjectIn, ProjectUpdate


@bp_api.post("/projects")
def create_project():
    data = request.form
    project = ProjectController.create(ProjectIn(**data))
    return jsonify(project.dict()), HTTPStatus.CREATED


@bp_api.get("/projects")
def read_projects():
    data = [project.dict() for project in ProjectController.get_all()]
    return jsonify(data), HTTPStatus.OK


@bp_api.get("/projects/<int:project_id>")
def read_project(project_id: int):
    if project := ProjectController.get_by_id(project_id):
        return jsonify(project.dict()), HTTPStatus.OK
    return utils.jsonify_not_found("Project"), HTTPStatus.NOT_FOUND


@bp_api.patch("/projects/<int:project_id>")
def update_project(project_id: int):
    data = request.form
    project_update = ProjectUpdate(**data)
    if project := ProjectController.update_model(project_id, project_update):
        return jsonify(project.dict()), HTTPStatus.ACCEPTED
    return utils.jsonify_not_found("Project"), HTTPStatus.NOT_FOUND


@bp_api.delete("/projects/<int:project_id>")
def delete_project(project_id: int):
    if ProjectController.delete(project_id):
        return "", HTTPStatus.NO_CONTENT
    return utils.jsonify_not_found("Project"), HTTPStatus.NOT_FOUND
