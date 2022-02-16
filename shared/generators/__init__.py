from abc import ABC, abstractmethod
from typing import Type

# from app.controllers import TController, TModel
from sqlmodel import SQLModel

from app.controllers import BaseController


class BaseGenerator(ABC):
    # controller: TController = None
    controller: Type[BaseController] = None
    model_in: Type[SQLModel]

    @classmethod
    # def generate(cls) -> TModel:
    def generate(cls) -> SQLModel:
        return cls.controller.create(cls.model_in(**cls.random_data()))

    @classmethod
    # def generate_many(cls, amount: int) -> List[TModel]:
    def generate_many(cls, amount: int) -> list[SQLModel]:
        return [cls.generate() for _ in range(amount)]

    @classmethod
    @abstractmethod
    def random_data(cls) -> dict:
        pass
