from src.infrastructure.results.base import BaseResult
from uuid import UUID

class TeamResult(BaseResult):
    id: UUID
    name: str