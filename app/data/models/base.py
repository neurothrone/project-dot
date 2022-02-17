from typing import TypeVar

from sqlmodel import SQLModel, Session

from ..db import engine

TSQLModelDB = TypeVar("TSQLModelDB", bound="SQLModelDBBase")


class SQLModelDBBase(SQLModel):
    def save(self) -> None:
        with Session(engine) as session:
            session.add(self)
            session.commit()
            session.refresh(self)

    def delete(self) -> None:
        with Session(engine) as session:
            session.delete(self)
            session.commit()
