from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from . import BaseHandler
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.domains.evaluation import Evaluation
from src.infrastructure.results.evaluation import EvaluationResult
from uuid import UUID

# Request
class Query(PageRequest):
    questionnaire_id: UUID | None = None
    created_by_id: UUID | None = None
    evaluated_person_id: UUID | None = None

# Handle
class ListAll(BaseHandler[Query, PageResult[EvaluationResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = self.db.query(Evaluation).not_deleted()
        
        if request.questionnaire_id:
            query = query.filter(
                Evaluation.questionnaire_id == request.questionnaire_id
            )
        
        if request.created_by_id:
            query = query.filter(
                Evaluation.created_by_id == request.created_by_id
            )
            
        if request.evaluated_person_id:
            query = query.filter(
                Evaluation.evaluated_person_id == request.evaluated_person_id
            )

        return paginate(query, request, EvaluationResult)