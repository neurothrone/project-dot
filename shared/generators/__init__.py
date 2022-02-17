from abc import ABC, abstractmethod
from typing import Type

from app.controllers import BaseController, TSQLModel


class BaseGenerator(ABC):
    controller: Type[BaseController] = None
    model_in: Type[TSQLModel]

    @classmethod
    def generate(cls) -> TSQLModel:
        return cls.controller.create(cls.model_in(**cls.random_data()))

    @classmethod
    def generate_many(cls, amount: int) -> list[TSQLModel]:
        return [cls.generate() for _ in range(amount)]

    @classmethod
    @abstractmethod
    def random_data(cls) -> dict:
        pass
