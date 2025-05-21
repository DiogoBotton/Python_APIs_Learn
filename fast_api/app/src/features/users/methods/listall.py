from . import BaseFeature
from src.core.user import User
from src.infraestructure.utils import remove_accents
from src.infraestructure.pagination.models import PageRequest
from src.infraestructure.pagination.functions import paginate
from src.infraestructure.results.user import UserResult

# Request
class Query(PageRequest):
    search: str | None = None

# Handle
class Handle(BaseFeature):
    def execute(self, db, request: Query):
        query = db.query(User).not_deleted()

        if request.search:
            search = remove_accents(request.search.lower())

            query = query.filter(
                User.email.ilike(f'%{search}%') |
                User.cpf.ilike(f'%{search}%')
            )

        return paginate(query, request, UserResult)