from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.core.user import User
from src.core.enums.role_type import RoleType
from src.infrastructure.validations.fields import is_valid_email, is_cpf
from src.infrastructure.results.default import RegisterResult

# Request
class Command(BaseModel):
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
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if (self.db.query(User)
            .not_deleted()
            .filter(User.email == request.email or User.cpf == request.cpf)
            .first()):
            raise HTTPException(status_code=400, detail="Email ou CPF já cadastrado.")

        entity = User(request.email, request.cpf, request.role)
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity