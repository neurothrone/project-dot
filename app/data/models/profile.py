import hashlib
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    # from .project import ProjectDB
    from .user import UserDB

from .project import ProjectDB


class ProfileBase(SQLModel):
    name: str | None = Field(default=None, max_length=32)
    surname: str | None = Field(default=None, max_length=32)
    city: str | None = Field(default=None, max_length=64)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None)

    social_website: str | None = None
    social_github: str | None = None
    social_linkedin: str | None = None
    social_youtube: str | None = None


class ProfileDB(ProfileBase, table=True):
    __tablename__ = "profiles"

    id: int | None = Field(default=None, primary_key=True)
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)

    avatar_hash: str | None = Field(default=None, max_length=32)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    account: Optional["UserDB"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs=dict(lazy="joined")
    )
    projects: list[ProjectDB] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs=dict(lazy="joined",
                                    cascade="all, delete")
    )

    def create_gravatar(self) -> None:
        if self.account and self.account.email and not self.avatar_hash:
            self.avatar_hash = self.gravatar_hash()

    def gravatar_hash(self):
        # Gravatar service requires email to be lowercase.
        # MD5 support in Python works on bytes and not on strings, therefor the
        # string must first be encoded into bytes.
        return hashlib.md5(self.account.email.lower().encode("utf-8")).hexdigest()
