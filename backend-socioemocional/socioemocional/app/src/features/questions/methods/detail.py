from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from uuid import UUID
from . import BaseHandler
from src.domains.question import Question
from src.infrastructure.results.question import QuestionResult

# Request
class Query(BaseModel):
    id: UUID
    
    @field_validator('id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id é obrigatório.')
        return v

# Handle
class Detail(BaseHandler[Query, QuestionResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(Question)
                 .not_deleted()
                 .filter(Question.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Questão não encontrada.")

        return query