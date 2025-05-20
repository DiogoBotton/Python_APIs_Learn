from pydantic import BaseModel
import uuid

class RegisterResult(BaseModel):
    id: uuid.UUID

    class Config:
        from_attributes = True  # Permite converter de SQLAlchemy para Pydantic