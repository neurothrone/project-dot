from . import BaseController
from app.config import settings
from app.data.repository.project import ProjectRepository
from app.schemas.complex import ProjectOutWithProfile
from app.schemas.project import ProjectIn, ProjectUpdate
from app.shared.paginator import Paginator


class ProjectController(BaseController):
    repository = ProjectRepository
    model_out = ProjectOutWithProfile
    model_name = "Project"
    model_plural_name = "Projects"

    @classmethod
    def create(cls, project_in: ProjectIn) -> ProjectOutWithProfile:
        model_db = super().create(project_in)
        return cls.model_out.from_orm(model_db)

    @classmethod
    def get_by_title(cls, title: str) -> ProjectOutWithProfile | None:
        return cls.repository.get_by_title(title)

    @classmethod
    def get_all_by_ilike_title(cls, search_for: str) -> list[ProjectOutWithProfile]:
        projects_db = cls.repository.get_all_by_ilike_title(search_for)
        return [cls.model_out.from_orm(project) for project in projects_db]

    @classmethod
    def get_all_projects_by_profile(cls, profile_id: int) -> list[ProjectOutWithProfile]:
        projects_db = cls.repository.get_all_projects_by_profile(profile_id)
        return [cls.model_out.from_orm(project) for project in projects_db]

    @classmethod
    def get_all_by_ilike_title_paginated(cls,
                                         search_for: str,
                                         page: int,
                                         ) -> Paginator:
        projects_db = cls.get_all_by_ilike_title(search_for)
        return Paginator(page, settings.PROJECTS_PER_PAGE, projects_db, cls.model_out)

    @classmethod
    def get_all_projects_by_profile_paginated(cls,
                                              profile_id: int,
                                              page: int,
                                              ) -> Paginator:
        projects_db = cls.get_all_projects_by_profile(profile_id)
        return Paginator(page, settings.PROJECTS_PER_PAGE, projects_db, cls.model_out)

    @classmethod
    def update_model(cls, _id: int, model_update: ProjectUpdate) -> ProjectOutWithProfile | None:
        if not (model_db := cls.repository.get_model_by_id(_id)):
            return None
        return cls.repository.update_model(model_db, model_update.dict(exclude_none=True))
