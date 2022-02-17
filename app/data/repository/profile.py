from . import BaseRepository
from ..models.profile import ProfileDB, ProjectDB


class ProfileRepository(BaseRepository):
    model = ProfileDB

    @classmethod
    def add_project(cls, project: ProjectDB, profile: ProfileDB) -> None:
        if cls.has_project(project, profile):
            raise ValueError("That profile already has that project")

        profile.projects.append(project)
        profile.save()

    @classmethod
    def remove_project(cls, project: ProjectDB, profile: ProfileDB) -> None:
        if not cls.has_project(project, profile):
            raise ValueError("That profile does not have that project")

        profile.projects.remove(project)
        profile.save()
        project.delete()

    @classmethod
    def has_project(cls, project: ProjectDB, profile: ProfileDB) -> bool:
        if not profile.projects:
            return False

        for owned_project in profile.projects:
            if owned_project.id == project.id:
                return True
        return False
