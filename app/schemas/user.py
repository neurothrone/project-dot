from datetime import datetime

from pydantic import EmailStr

from app.data.models.user import UserBase
from app.shared.access import AccessLevel


class UserIn(UserBase):
    password: str
    is_confirmed: bool = False


class UserOut(UserBase):
    id: int
    created_at: datetime
    is_confirmed: bool

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self):
        return self.username

    @property
    def is_admin(self) -> bool:
        return self.has_access(AccessLevel.ADMIN)

    def has_access(self, level: AccessLevel) -> bool:
        return self.access_level >= level


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    access_level: AccessLevel | None = None


class AnonymousUser:
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return True

    @classmethod
    def get_id(cls):
        return None

    @property
    def is_admin(self) -> bool:
        return False

    @property
    def access_level(self) -> AccessLevel:
        return AccessLevel.GUEST
