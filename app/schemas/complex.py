from .profile import ProfileOut
from .project import ProjectOut
from .user import UserOut


class UserOutWithProfile(UserOut):
    profile: ProfileOut | None = None


class ProfileOutWithProjects(ProfileOut):
    projects: list[ProjectOut]


class UserOutAll(UserOut):
    profile: ProfileOutWithProjects


class ProfileOutWithUser(ProfileOut):
    account: UserOut | None = None


class ProjectOutWithProfile(ProjectOut):
    owner: ProfileOutWithUser | None = None
