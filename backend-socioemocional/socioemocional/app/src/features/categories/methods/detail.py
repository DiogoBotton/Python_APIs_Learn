from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from uuid import UUID
from . import BaseHandler
from src.domains.category import Category
from src.infrastructure.results.category import CategoryResult

# Request
class Query(BaseModel):
    id: UUID

# Handle
class Detail(BaseHandler[Query, CategoryResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Query):
        query = (self.db
                 .query(Category)
                 .not_deleted()
                 .filter(Category.id == request.id)
                 .first())
        
        if query is None:
            raise HTTPException(status_code=404, detail="Categoria de competência não encontrada.")

        return query