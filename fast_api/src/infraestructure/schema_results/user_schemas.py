from pydantic import BaseModel
import uuid

class UserResult(BaseModel):
    id: uuid.UUID
    email: str
    cpf: str
    roles: int

    class Config:
        from_attributes = True  # Permite converter de SQLAlchemy para Pydantic