from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field

from .auth import AuthMixin
from .base import SQLModelBase
from app.shared.access import AccessLevel


class UserBase(SQLModelBase):
    username: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_level: AccessLevel = Field(default=AccessLevel.USER)


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
