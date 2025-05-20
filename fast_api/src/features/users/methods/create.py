from pydantic import BaseModel
from . import BaseFeature
from src.core.user import User
from src.core.enums.role_type import RoleType

# Request
class Command(BaseModel):
    email: str
    cpf: str
    role: list[RoleType]

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