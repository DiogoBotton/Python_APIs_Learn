from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from uuid import UUID
from . import BaseHandler
from src.domains.competence import Competence
from src.infrastructure.results.competence import CompetenceResult

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Detail(BaseHandler[Query, CompetenceResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(Competence)
                 .not_deleted()
                 .filter(Competence.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Competência não encontrada.")

        return query