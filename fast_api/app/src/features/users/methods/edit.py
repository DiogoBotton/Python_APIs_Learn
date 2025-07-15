from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.core.enums.role_type import RoleType
from src.core.user import User
from uuid import UUID
from src.infrastructure.validations.existence import entity_id_exists, field_error
from src.infrastructure.validations.fields import is_cpf, is_valid_email

# Request
class Command(BaseModel):
    id: UUID
    email: str
    cpf: str
    role: list[RoleType]
    
    @field_validator('cpf', mode='after')
    def valid_cpf(cls, v):
        if not is_cpf(v):
            raise ValueError('CPF inválido.')
        return v
    
    @field_validator('email', mode='after')
    def valid_email(cls, v):
        if not is_valid_email(v):
            raise ValueError('E-mail inválido.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if not entity_id_exists(self.db, User, request.id):
            raise field_error("id", "Usuário não encontrado.")
        
        entity: User = (self.db
                 .query(User)
                 .not_deleted()
                 .filter(User.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        entity.update(request.email, request.cpf, request.role)
        
        self.db.commit()
        return Response(status_code=200)