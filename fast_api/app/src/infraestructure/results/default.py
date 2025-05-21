import uuid
from src.infraestructure.results.base import BaseResult
        
class RegisterResult(BaseResult):
    id: uuid.UUID
