from typing import Type

from sqlmodel import select, Session

from ..db import engine
from ..models.base import TSQLModelDB


class BaseRepository:
    model: Type[TSQLModelDB]

    @classmethod
    def create(cls, **kwargs) -> TSQLModelDB:
        db_model = cls.model(**kwargs)
        db_model.save()
        return db_model

    @classmethod
    def get_all(cls, offset: int = 0, limit: int = 100) -> list[TSQLModelDB] | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .offset(offset)
                                .limit(limit)
                                ).unique().all()

    @classmethod
    def get_model_by_id(cls, _id: int) -> TSQLModelDB | None:
        with Session(engine) as session:
            return session.get(cls.model, _id)

    @classmethod
    def get_model_by_attr(cls, **kwargs) -> TSQLModelDB | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .filter_by(**kwargs)
                                ).first()

    @classmethod
    def update_model(cls, db_model: TSQLModelDB, new_data: dict) -> TSQLModelDB:
        for key, value in new_data.items():
            setattr(db_model, key, value)

        db_model.save()
        return db_model

    @classmethod
    def delete_model(cls, db_model: TSQLModelDB) -> None:
        db_model.delete()
