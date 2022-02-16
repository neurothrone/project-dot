from sqlmodel import Session

from . import BaseRepository, engine
from ..models.profile import ProfileDB, ProjectDB


class ProfileRepository(BaseRepository):
    model = ProfileDB

    @classmethod
    def add_project(cls, project: ProjectDB, profile: ProfileDB) -> None:
        if cls.has_project(project, profile):
            raise ValueError("That profile already has that project")

        profile.projects.append(project)

        with Session(engine) as session:
            session.add(profile)
            session.commit()
            session.refresh(profile)
        # profile.save()

    @classmethod
    def remove_project(cls, project: ProjectDB, profile: ProfileDB) -> None:
        if not cls.has_project(project, profile):
            raise ValueError("That profile does not have that project")

        with Session(engine) as session:
            profile.projects.remove(project)
            session.add(profile)
            session.commit()
            session.refresh(profile)

        with Session(engine) as session:
            session.delete(project)
            session.commit()

        # profile.save()

    @classmethod
    def has_project(cls, project: ProjectDB, profile: ProfileDB) -> bool:
        if not profile.projects:
            return False

        for owned_project in profile.projects:
            if owned_project.id == project.id:
                return True
        return False
