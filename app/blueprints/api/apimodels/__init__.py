from abc import ABC, abstractmethod

from app.shared.operation import Operation


class APIModelBase(ABC):
    def __init__(self):
        self.detail: str = ""
        self.status_code: int | None = None
        self.was_successful: bool = False

    @abstractmethod
    def exec(self) -> None:
        pass

    @abstractmethod
    def to_response(self) -> tuple:
        pass

    def load(self, operation: Operation):
        self.detail = operation.detail
        self.status_code = operation.status_code
        self.was_successful = operation.was_successful
