from src.infrastructure.results.base import BaseResult
from uuid import UUID

class AnswerOptionResult(BaseResult):
    id: UUID
    title: str
    value: int
    order: int