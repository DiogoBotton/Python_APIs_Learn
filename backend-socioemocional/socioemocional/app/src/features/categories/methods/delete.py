from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.category import Category
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
        entity: Category = (self.db
                 .query(Category)
                 .not_deleted()
                 .filter(Category.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada.")
        
        if len(entity.questionnaires) > 0:
            raise HTTPException(status_code=404, detail="Não é possível deletar uma categoria com questionários vinculados.")
        
        entity.soft_delete()
        
        self.db.commit()
        return Response(status_code=200)