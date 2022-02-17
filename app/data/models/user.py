from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, Relationship

from .base import SQLModelDBBase
from app.shared.access import AccessLevel

if TYPE_CHECKING:
    from .profile import ProfileDB


class UserDB(SQLModelDBBase, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: EmailStr = Field(index=True)
    hashed_password: str
    is_confirmed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    access_level: AccessLevel = Field(default=AccessLevel.USER,
                                      sa_column=Column(Enum(AccessLevel),
                                                       nullable=False))

    profile: Optional["ProfileDB"] = Relationship(
        back_populates="account",
        sa_relationship_kwargs=dict(uselist=False,
                                    cascade="all, delete",
                                    single_parent=True,
                                    lazy="joined")
    )
