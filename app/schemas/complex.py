from .profile import ProfileOut
from .project import ProjectOut
from .user import UserOut


class UserOutWithProfile(UserOut):
    profile: ProfileOut | None = None


class ProfileOutWithUser(ProfileOut):
    account: UserOut | None = None


class ProfileOutWithProjects(ProfileOut):
    projects: list[ProjectOut]


class UserOutWithProfileWithProjects(UserOut):
    profile: ProfileOutWithProjects | None


class ProjectOutWithProfile(ProjectOut):
    owner: ProfileOutWithUser | None = None
