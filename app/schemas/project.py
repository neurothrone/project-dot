from datetime import datetime

from pydantic import Field

from app.data.models.project import ProjectBase


class ProjectIn(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int


class ProjectUpdate(ProjectBase):
    title: str | None = Field(default=None, max_length=64)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
