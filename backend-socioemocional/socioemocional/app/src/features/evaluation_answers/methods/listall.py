from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import field_validator
from . import BaseHandler
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.domains.evaluation_answer import EvaluationAnswer
from src.infrastructure.results.evaluation_answer import EvaluationAnswerResult
from uuid import UUID

# Request
class Query(PageRequest):
    evaluation_id: UUID
    
    @field_validator('evaluation_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id da questão é obrigatório.')
        return v

# Handle
class ListAll(BaseHandler[Query, PageResult[EvaluationAnswerResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db.query(EvaluationAnswer)
                 .not_deleted()
                 .filter(EvaluationAnswer.evaluation_id == request.evaluation_id))
        
        return paginate(query, request, EvaluationAnswerResult)