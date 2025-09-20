from fastapi import Depends
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_
from src.data.database import get_db
from . import BaseHandler
from src.domains.team import Team
from src.domains.user import User
from src.infrastructure.utils import remove_accents
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.infrastructure.results.user import UserResult
from uuid import UUID

# Request
class Query(PageRequest):
    search: str | None = None
    team_id: UUID | None = None

# Handle
class ListAll(BaseHandler[Query, PageResult[UserResult]]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = self.db.query(User).not_deleted()

        if request.search:
            search = remove_accents(request.search.lower())

            query = query.filter(
                User.email.ilike(f'%{search}%') |
                User.cpf.ilike(f'%{search}%')
            )
        
        if request.team_id:
            user_team_alias = aliased(Team)
            manager_team_alias = aliased(Team)
            
            query = query\
                .outerjoin(user_team_alias, User.teams)\
                .outerjoin(manager_team_alias, User.managed_teams)\
                .filter(or_(user_team_alias.id == request.team_id, manager_team_alias.id == request.team_id))\
                .distinct()
            
        return paginate(query, request, UserResult)