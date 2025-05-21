from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from . import BaseHandler
from src.core.user import User
from src.infrastructure.utils import remove_accents
from src.infrastructure.pagination.models import PageRequest, PageResult
from src.infrastructure.pagination.functions import paginate
from src.infrastructure.results.user import UserResult

# Request
class Query(PageRequest):
    search: str | None = None

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

        return paginate(query, request, UserResult)