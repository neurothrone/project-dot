from math import ceil
from typing import Type

from pydantic import BaseModel


class Paginator:
    def __init__(self,
                 page: int,
                 items_per_page: int,
                 items: list,
                 model_out: Type[BaseModel] | None = None):
        self.page = page

        start = (page - 1) * items_per_page
        end = start + items_per_page

        self.total = len(items)
        self.pages = ceil(self.total / items_per_page)

        if end < len(items):
            self.next_num = page + 1
            self.has_next = True
        if page > 1:
            self.prev_num = page - 1
            self.has_prev = True

        items = items[start:start + items_per_page]
        self.items = [model_out.from_orm(item) for item in items] if model_out else items

    # def __init__(self):
    #     self.page: int = 1
    #     self.pages: int = 1
    #     self.next_num: str | None = None
    #     self.prev_num: str | None = None
    #     self.has_next: bool = False
    #     self.has_prev: bool = False
    #     self.total: int = 0
    #     self.items = []
