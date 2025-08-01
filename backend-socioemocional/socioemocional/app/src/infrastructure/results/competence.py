from src.infrastructure.results.base import BaseResult
from uuid import UUID

class CompetenceResult(BaseResult):
    id: UUID
    title: str
    description: str