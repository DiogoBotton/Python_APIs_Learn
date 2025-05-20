from pydantic import BaseModel, EmailStr, field_validator, model_validator
from . import BaseFeature
from src.core.user import User
from src.core.enums.role_type import RoleType
from src.infraestructure.validations import is_valid_email, is_cpf

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
class Handle(BaseFeature):
    def execute(self, db, request: Command):
        user = User(email = request.email,
                    cpf = request.cpf)
        user.set_roles(request.role)
    
        db.add(user)
        db.commit()
        db.refresh(user)
        return user