from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from uuid import UUID
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from src.infrastructure.results.answer_option import AnswerOptionResult

# Request
class Query(BaseModel):
    id: UUID
    
    @field_validator('id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id é obrigatório.')
        return v

# Handle
class Detail(BaseHandler[Query, AnswerOptionResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(AnswerOption)
                 .not_deleted()
                 .filter(AnswerOption.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Tipo de resposta não encontrada.")

        return query