from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel


class PostDB(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published_at: datetime = Field(default_factory=datetime.utcnow)
