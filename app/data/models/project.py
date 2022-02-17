from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from .profile import ProfileDB

from .base import SQLModelBase


class ProjectBase(SQLModelBase):
    title: str = Field(max_length=64)
    description: str | None = None

    # TODO: HTTPUrl validators
    demo_link: str | None = None
    source_link: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectDB(ProjectBase, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)

    profile_id: int | None = Field(default=None, foreign_key="profiles.id")
    owner: Optional["ProfileDB"] = Relationship(
        back_populates="projects",
        sa_relationship_kwargs=dict(lazy="joined")
    )
