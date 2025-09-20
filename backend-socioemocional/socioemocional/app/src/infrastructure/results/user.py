from src.infrastructure.results.base import BaseResult
from uuid import UUID

class UserResult(BaseResult):
    id: UUID
    name: str
    email: str
    cpf: str
    role: int