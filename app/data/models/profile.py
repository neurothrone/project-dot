import hashlib
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from .user import UserDB

from .base import SQLModelDBBase
from .project import ProjectDB
from app.shared.gravatar import gravatar_hash


class ProfileDB(SQLModelDBBase, table=True):
    __tablename__ = "profiles"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=32)
    surname: str | None = Field(default=None, max_length=32)
    city: str | None = Field(default=None, max_length=64)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None)

    social_website: str | None = None
    social_github: str | None = None
    social_linkedin: str | None = None
    social_youtube: str | None = None

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
            self.avatar_hash = gravatar_hash(self.account.email)
