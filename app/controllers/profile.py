from http import HTTPStatus

from . import BaseController
from app.data.repository.profile import ProfileRepository
from app.schemas.complex import ProfileOutWithProjects
from app.schemas.profile import ProfileOut, ProfileUpdate
from app.schemas.project import ProjectIn
from .project import ProjectController
from .user import UserController

from app.shared.operation import Operation


class ProfileController(BaseController):
    repository = ProfileRepository
    model_out = ProfileOutWithProjects
    model_name: str = "Profile"
    model_plural_name: str = "Profiles"

    @classmethod
    def get_by_name(cls, name: str) -> ProfileOut | None:
        profile_db = cls.get_model_by_attr(name=name)
        return cls.model_out.from_orm(profile_db) if profile_db else None

    @classmethod
    def add_project_to_user(cls, project_in: ProjectIn, user_id: int) -> Operation:
        user_db = UserController.repository.get_model_by_id(user_id)

        if not user_db:
            return Operation(detail="User not found",
                             status_code=HTTPStatus.NOT_FOUND)

        project_db = ProjectController.repository.create(**project_in.dict())
        cls.repository.add_project(project_db, user_db.profile)
        return Operation(status_code=HTTPStatus.CREATED, was_successful=True)

    # NOTE: for testing purposes
    @classmethod
    def add_existing_project_to_user(cls, project_id: int, user_id: int) -> Operation:
        project_db = ProjectController.repository.get_model_by_id(project_id)
        user_db = UserController.repository.get_model_by_id(user_id)

        if not project_db:
            return Operation(detail="Project not found",
                             status_code=HTTPStatus.NOT_FOUND)
        if not user_db:
            return Operation(detail="User not found",
                             status_code=HTTPStatus.NOT_FOUND)

        operation = Operation()
        try:
            cls.repository.add_project(project_db, user_db.profile)
            operation.status_code = HTTPStatus.OK
            operation.was_successful = True
        except ValueError as error:
            operation.detail = str(error)
            operation.status_code = HTTPStatus.BAD_REQUEST
        return operation

    @classmethod
    def remove_project_from_user(cls, project_id: int, user_id: int) -> Operation:
        project_db = ProjectController.repository.get_model_by_id(project_id)
        user_db = UserController.repository.get_model_by_id(user_id)

        if not project_db:
            return Operation(detail="Project not found",
                             status_code=HTTPStatus.NOT_FOUND)

        if not user_db:
            return Operation(detail="User not found",
                             status_code=HTTPStatus.NOT_FOUND)

        cls.repository.remove_project(project_db, user_db.profile)
        return Operation(status_code=HTTPStatus.NO_CONTENT, was_successful=True)

    @classmethod
    def ping_user(cls, profile_id: int) -> None:
        cls.update_model(profile_id, ProfileUpdate())
