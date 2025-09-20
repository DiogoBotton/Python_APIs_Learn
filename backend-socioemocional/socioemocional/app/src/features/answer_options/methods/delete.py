from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from uuid import UUID

# Request
class Command(BaseModel):
    id: UUID

    @field_validator('id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id é obrigatório.')
        return v

# Handle
class Delete(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        entity: AnswerOption = (self.db
                 .query(AnswerOption)
                 .not_deleted()
                 .filter(AnswerOption.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Tipo de resposta não encontrada.")
        
        entity.soft_delete()
        
        self.db.commit()
        return Response(status_code=200)