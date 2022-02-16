from flask import jsonify

from . import APIModelBase
from app.controllers.profile import ProfileController
from app.schemas.project import ProjectIn
from app.shared.operation import Operation


class AddProjectToUserAPIModel(APIModelBase):
    def __init__(self, data: dict, user_id: int):
        super().__init__()

        self.data = data
        self.user_id = user_id

    def exec(self) -> None:
        operation: Operation = ProfileController.add_project_to_user(
            ProjectIn(**self.data), self.user_id)
        self.load(operation)

    def to_response(self) -> tuple:
        if self.was_successful:
            return "", self.status_code
        return jsonify(dict(detail=self.detail)), self.status_code


class RemoveProjectFromUserAPIModel(APIModelBase):
    def __init__(self, project_id: int, user_id: int):
        super().__init__()

        self.project_id = project_id
        self.user_id = user_id

    def exec(self) -> None:
        operation: Operation = ProfileController.remove_project_from_user(
            self.project_id, self.user_id)
        self.load(operation)

    def to_response(self) -> tuple:
        if self.was_successful:
            return "", self.status_code
        return jsonify(dict(detail=self.detail)), self.status_code


class AddExistingProjectToUserAPIModel(APIModelBase):
    def __init__(self, project_id: int, user_id: int):
        super().__init__()

        self.project_id = project_id
        self.user_id = user_id

    def exec(self) -> None:
        operation: Operation = ProfileController.add_existing_project_to_user(
            self.project_id, self.user_id)
        self.load(operation)

    def to_response(self) -> tuple:
        if self.was_successful:
            return "", self.status_code
        return jsonify(dict(detail=self.detail)), self.status_code
