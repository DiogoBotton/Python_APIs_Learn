from fastapi import HTTPException
from . import BaseFeature
from src.core.user import User
from pydantic import BaseModel
from uuid import UUID

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Handle(BaseFeature):
    def execute(self, db, request: Query):
        query = (db
                 .query(User)
                 .not_deleted()
                 .filter(User.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return query