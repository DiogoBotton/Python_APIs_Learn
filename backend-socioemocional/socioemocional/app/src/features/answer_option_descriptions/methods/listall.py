from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import field_validator
from . import BaseHandler
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.domains.answer_option_description import AnswerOptionDescription
from src.infrastructure.results.answer_option_description import AnswerOptionDescriptionResult
from uuid import UUID

# Request
class Query(PageRequest):
    question_id: UUID
    
    @field_validator('question_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id da questão é obrigatório.')
        return v

# Handle
class ListAll(BaseHandler[Query, PageResult[AnswerOptionDescriptionResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db.query(AnswerOptionDescription)
                 .not_deleted()
                 .filter(AnswerOptionDescription.question_id == request.question_id))
        
        return paginate(query, request, AnswerOptionDescriptionResult)