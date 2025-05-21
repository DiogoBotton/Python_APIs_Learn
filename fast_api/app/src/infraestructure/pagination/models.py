from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List
from math import ceil

T = TypeVar("T")

class PageRequest(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(30, ge=1, le=100)

class PageResult(BaseModel, Generic[T]):
    page: int
    page_size: int
    total: int
    page_count: int
    is_first_page: bool
    is_last_page: bool
    items: List[T]

    @classmethod
    def create(cls, *, items: List[T], total: int, page: int, page_size: int):
        page_count = ceil(total / page_size)
        return cls(
            page=page,
            page_size=page_size,
            total=total,
            page_count=page_count,
            is_first_page=page <= 1,
            is_last_page=page >= page_count,
            items=items
        )