from datetime import datetime

from pydantic import Field

from .base import SQLModelBase


class ProjectBase(SQLModelBase):
    title: str = Field(max_length=64)
    description: str | None = None

    # TODO: HTTPUrl validators
    demo_link: str | None = None
    source_link: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectIn(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int


class ProjectUpdate(ProjectBase):
    title: str | None = Field(default=None, max_length=64)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
