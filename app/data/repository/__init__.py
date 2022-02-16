from typing import Type

from sqlmodel import select, Session, SQLModel

from ..db import engine


class BaseRepository:
    model: Type[SQLModel]

    @classmethod
    def create(cls, **kwargs) -> SQLModel:
        db_model = cls.model(**kwargs)

        with Session(engine) as session:
            session.add(db_model)
            session.commit()
            session.refresh(db_model)

        return db_model

    @classmethod
    def get_all(cls, offset: int = 0, limit: int = 100) -> list[SQLModel] | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .offset(offset)
                                .limit(limit)
                                ).unique().all()

    @classmethod
    def get_model_by_id(cls, _id: int) -> SQLModel | None:
        with Session(engine) as session:
            return session.get(cls.model, _id)

    @classmethod
    def get_model_by_attr(cls, **kwargs) -> SQLModel | None:
        with Session(engine) as session:
            return session.exec(select(cls.model)
                                .filter_by(**kwargs)
                                ).first()

    @classmethod
    def update_model(cls, db_model: SQLModel, new_data: dict) -> SQLModel:
        for key, value in new_data.items():
            setattr(db_model, key, value)

        with Session(engine) as session:
            session.add(db_model)
            session.commit()
            session.refresh(db_model)

        return db_model

    @classmethod
    def delete_model(cls, db_model: SQLModel) -> None:
        with Session(engine) as session:
            session.delete(db_model)
            session.commit()
