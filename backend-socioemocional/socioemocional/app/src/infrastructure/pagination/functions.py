from pydantic import BaseModel, Field
from typing import Type, TypeVar, List
from sqlalchemy.orm import Query
from .models import PageRequest, PageResult

T = TypeVar("T")

def paginate(query: Query, request: PageRequest, model: Type[T]) -> PageResult[T]:
    total = query.count()

    items = (
        query
        .offset((request.page - 1) * request.page_size)
        .limit(request.page_size)
        .all()
    )

    results: List[T] = [model.model_validate(i) for i in items]

    return PageResult[T].create(
        items=results,
        total=total,
        page=request.page,
        page_size=request.page_size
    )