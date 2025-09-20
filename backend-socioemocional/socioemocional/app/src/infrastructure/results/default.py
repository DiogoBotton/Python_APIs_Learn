import uuid
from src.infrastructure.results.base import BaseResult
        
class RegisterResult(BaseResult):
    id: uuid.UUID

class IdNameResult(BaseResult):
    id: uuid.UUID
    name: str
    
class IdTitleResult(BaseResult):
    id: uuid.UUID
    title: str