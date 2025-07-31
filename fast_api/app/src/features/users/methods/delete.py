from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.user import User
from uuid import UUID, uuid4

# Request
class Command(BaseModel):
    id: UUID

    @field_validator('id', mode='after')
    def valid_cpf(cls, v):
        if not v:
            raise ValueError('Id do widget é obrigatório.')
        return v

# Handle
class Delete(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        entity: User = (self.db
                 .query(User)
                 .not_deleted()
                 .filter(User.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrada.")
        
        entity.soft_delete()
        
        randomGuid = uuid4()
        entity.email = f'deleted_user_{randomGuid}'
        entity.cpf = f'deleted_user_{randomGuid}'
        
        self.db.commit()
        return Response(status_code=200)