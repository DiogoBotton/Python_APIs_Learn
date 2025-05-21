from src.infraestructure.results.base import BaseResult
from uuid import UUID

class UserResult(BaseResult):
    id: UUID
    email: str
    cpf: str
    roles: int