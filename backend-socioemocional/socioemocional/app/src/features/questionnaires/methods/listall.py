from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from . import BaseHandler
from src.infrastructure.utils import remove_accents
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.infrastructure.results.questionnaire import QuestionnaireResult
from src.domains.team import Team
from src.domains.questionnaire import Questionnaire
from typing import List
from uuid import UUID

# Request
class Query(PageRequest):
    search: str | None = None

# Handle
class ListAll(BaseHandler[Query, PageResult[QuestionnaireResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query, team_ids: List[UUID] = None):
        query = self.db.query(Questionnaire).not_deleted()

        if request.search:
            search = remove_accents(request.search.lower())

            query = query.filter(
                Questionnaire.title.ilike(f'%{search}%')
            )
        
        if team_ids:
            query = query.join(Questionnaire.teams).filter(Team.id.in_(team_ids))

        return paginate(query, request, QuestionnaireResult)