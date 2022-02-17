from datetime import datetime

from pydantic import Field

from .base import SQLModelBase
from ..shared.gravatar import gravatar_hash


class ProfileBase(SQLModelBase):
    name: str | None = Field(default=None, max_length=32)
    surname: str | None = Field(default=None, max_length=32)
    city: str | None = Field(default=None, max_length=64)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None)

    social_website: str | None = None
    social_github: str | None = None
    social_linkedin: str | None = None
    social_youtube: str | None = None


class ProfileIn(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    last_seen_at: datetime
    avatar_hash: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.name} {self.surname}" if self.name and self.surname else ""

    def gravatar(self, size=100, default="identicon", rating="g"):
        # gravatar default size is 80x80 pixels
        url = "https://secure.gravatar.com/avatar"
        _hash = self.avatar_hash or gravatar_hash(self.account.email)
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=_hash, size=size, default=default, rating=rating)


class ProfileUpdate(ProfileBase):
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)
