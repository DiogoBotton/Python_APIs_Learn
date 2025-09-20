from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.enums.role_type import RoleType
from src.domains.user import User
from uuid import UUID
from src.infrastructure.validations.existence import entity_id_exists, field_error
from src.infrastructure.validations.fields import is_cpf, is_valid_email

# Request
class Command(BaseModel):
    id: UUID
    name: str
    email: str
    role: RoleType
    
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
        
        if entity.email != request.email:
            if (self.db.query(User)
                .not_deleted()
                .filter(and_(User.email == request.email, User.id != request.id))
                .first()):
                raise HTTPException(status_code=400, detail="Este e-mail já esta em uso na plataforma.")
        
        entity.update(request.name, request.email, request.role)
        
        self.db.commit()
        return Response(status_code=200)