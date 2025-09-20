from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from . import BaseHandler
from src.infrastructure.utils import remove_accents
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.infrastructure.results.team import TeamSimpleResult
from src.domains.team import Team

# Request
class Query(PageRequest):
    search: str | None = None

# Handle
class ListAll(BaseHandler[Query, PageResult[TeamSimpleResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = self.db.query(Team).not_deleted()

        if request.search:
            search = remove_accents(request.search.lower())

            query = query.filter(
                Team.name.ilike(f'%{search}%')
            )

        return paginate(query, request, TeamSimpleResult)