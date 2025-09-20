from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from . import BaseHandler
from src.infrastructure.utils import remove_accents
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.domains.question import Question
from src.infrastructure.results.question import QuestionSimpleResult
from uuid import UUID

# Request
class Query(PageRequest):
    search: str | None = None
    questionnaire_id: UUID | None = None

# Handle
class ListAll(BaseHandler[Query, PageResult[QuestionSimpleResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = self.db.query(Question).not_deleted()

        if request.search:
            search = remove_accents(request.search.lower())

            query = query.filter(
                Question.title.ilike(f'%{search}%')
            )
        
        if request.questionnaire_id:
            query = query.filter(
                Question.questionnaire_id == request.questionnaire_id
            )
        
        query = query.order_by(Question.order)

        return paginate(query, request, QuestionSimpleResult)