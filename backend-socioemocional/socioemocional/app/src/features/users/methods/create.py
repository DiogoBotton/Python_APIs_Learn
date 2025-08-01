from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.user import User
from src.domains.enums.role_type import RoleType
from src.infrastructure.validations.fields import is_valid_email, is_cpf
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.utils import remove_special_characters
from src.infrastructure.services.email.email_service import EmailService

# Request
class Command(BaseModel):
    name: str
    email: str
    cpf: str
    role: RoleType
    
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
    def __init__(self, db: Session = Depends(get_db), emailService: EmailService = Depends()):
        self.db = db
        self.emailService = emailService

    async def execute(self, request: Command):
        if (self.db.query(User)
            .not_deleted()
            .filter(or_(User.email == request.email, User.cpf == remove_special_characters(request.cpf)))
            .first()):
            raise HTTPException(status_code=400, detail="Email ou CPF já cadastrado.")
        
        entity = User(request.name, request.email, remove_special_characters(request.cpf), request.role)

        await self.emailService.send_user_invite([
            {"email": entity.email, "name": entity.name}
            ])
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity