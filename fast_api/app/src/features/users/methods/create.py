from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.user import User
from src.domains.enums.role_type import RoleType
from src.infrastructure.validations.fields import is_valid_email, is_cpf, is_valid_password
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.security.password import hash_password

# Request
class Command(BaseModel):
    email: str
    cpf: str
    password: str
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
    
    @field_validator('password', mode='after')
    def valid_password(cls, v):
        if not is_valid_password(v):
            raise ValueError('A senha precisa ter ao menos 6 caracteres, com letras maiúsculas e minúsculas, caracteres especiais e numéricos.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if (self.db.query(User)
            .not_deleted()
            .filter(or_(User.email == request.email, User.cpf == request.cpf))
            .first()):
            raise HTTPException(status_code=400, detail="Email ou CPF já cadastrado.")

        hashed_password = hash_password(request.password)
        entity = User(request.email, hashed_password, request.cpf, request.role)
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity