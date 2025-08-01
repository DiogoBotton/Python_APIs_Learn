import uuid
from src.infrastructure.results.base import BaseResult
        
class RegisterResult(BaseResult):
    id: uuid.UUID
