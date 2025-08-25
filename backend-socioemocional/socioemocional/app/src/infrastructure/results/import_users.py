from typing import List
from src.infrastructure.results.base import BaseResult

class ImportUserErrorResult(BaseResult):
    nome: str | None
    email: str | None
    cpf: str | None
    cargo: str | None
    equipe: str | None
    gerenteEquipe: str | None
    errors: List[str]

class ImportUserResult(BaseResult):
    imported_users_count: int
    error_import_users: List[ImportUserErrorResult]