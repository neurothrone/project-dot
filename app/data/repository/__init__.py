from typing import Type

from sqlmodel import select, Session, SQLModel

from ..db import engine
from ..models.base import TSQLModel


class BaseRepository:
    model: Type[TSQLModel]

    @classmethod
    def create(cls, **kwargs) -> TSQLModel:
        db_model = cls.model(**kwargs)
        db_model.save()
        return db_model

    @classmethod
    def get_all(cls, offset: int = 0, limit: int = 100) -> list[TSQLModel] | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .offset(offset)
                                .limit(limit)
                                ).unique().all()

    @classmethod
    def get_model_by_id(cls, _id: int) -> TSQLModel | None:
        with Session(engine) as session:
            return session.get(cls.model, _id)

    @classmethod
    def get_model_by_attr(cls, **kwargs) -> TSQLModel | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .filter_by(**kwargs)
                                ).first()

    @classmethod
    def update_model(cls, db_model: TSQLModel, new_data: dict) -> TSQLModel:
        for key, value in new_data.items():
            setattr(db_model, key, value)

        db_model.save()
        return db_model

    @classmethod
    def delete_model(cls, db_model: TSQLModel) -> None:
        db_model.delete()
