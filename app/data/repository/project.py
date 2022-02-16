from sqlmodel import select, Session

from . import BaseRepository, engine
from ..models.project import ProjectDB


class ProjectRepository(BaseRepository):
    model = ProjectDB

    @classmethod
    def get_by_title(cls, title: str) -> ProjectDB | None:
        return cls.get_model_by_attr(title=title)

    @classmethod
    def get_all_by_ilike_title(cls, search_for: str) -> list[ProjectDB]:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .where(cls.model.title.like(f"%{search_for}%"))
                                ).unique().all()

    @classmethod
    def get_all_projects_by_profile(cls, profile_id: int) -> list[ProjectDB]:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .filter_by(profile_id=profile_id)
                                ).unique().all()
