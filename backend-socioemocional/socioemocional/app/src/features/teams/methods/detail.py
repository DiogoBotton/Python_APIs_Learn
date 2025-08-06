from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from uuid import UUID
from . import BaseHandler
from src.domains.team import Team
from src.infrastructure.results.team import TeamResult

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Detail(BaseHandler[Query, TeamResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(Team)
                 .not_deleted()
                 .filter(Team.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Equipe não encontrada.")

        return query