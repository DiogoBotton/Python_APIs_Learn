from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from uuid import UUID
from . import BaseHandler
from src.domains.questionnaire import Questionnaire
from src.infrastructure.results.questionnaire import QuestionnaireResult

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Detail(BaseHandler[Query, QuestionnaireResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(Questionnaire)
                 .not_deleted()
                 .filter(Questionnaire.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Questionário não encontrado.")

        return query