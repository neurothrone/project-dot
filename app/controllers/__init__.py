from typing import Type

from app.data.repository import BaseRepository, SQLModel


class BaseController:
    repository: Type[BaseRepository]
    model_out: Type[SQLModel]
    model_name: str = "Object"
    model_plural_name: str = "Objects"

    @classmethod
    def create(cls, model_in: SQLModel) -> SQLModel:
        return cls.repository.create(**model_in.dict())

    @classmethod
    def get_all(cls,
                offset: int = 0,
                limit: int = 100
                ) -> list[SQLModel] | None:
        return [cls.model_out.from_orm(model_db) for model_db in
                cls.repository.get_all(offset, limit)]

    @classmethod
    def get_by_id(cls, _id: int) -> SQLModel | None:
        model_db = cls.repository.get_model_by_id(_id)
        return cls.model_out.from_orm(model_db) if model_db else None

    @classmethod
    def get_model_by_attr(cls, **kwargs) -> SQLModel | None:
        return cls.repository.get_model_by_attr(**kwargs)

    @classmethod
    def update_model(cls, _id: int, model_update: SQLModel) -> SQLModel | None:
        if not (model_db := cls.repository.get_model_by_id(_id)):
            return None
        return cls.repository.update_model(model_db, model_update.dict(exclude_none=True))

    @classmethod
    def delete(cls, _id: int) -> bool:
        if model_db := cls.repository.get_model_by_id(_id):
            cls.repository.delete_model(model_db)
            return True
        return False
