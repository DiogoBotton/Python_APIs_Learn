from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from uuid import UUID
from . import BaseHandler
from src.domains.user import User
from src.infrastructure.results.user import UserResult

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Detail(BaseHandler[Query, UserResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(User)
                 .not_deleted()
                 .filter(User.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return query