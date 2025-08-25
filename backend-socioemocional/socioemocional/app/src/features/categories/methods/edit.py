from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel
from . import BaseHandler
from src.domains.category import Category
from uuid import UUID
from src.infrastructure.validations.existence import entity_id_exists, field_error

# Request
class Command(BaseModel):
    id: UUID
    title: str
    description: str

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if not entity_id_exists(self.db, Category, request.id):
            raise field_error("id", "Categoria não encontrada.")
        
        if (self.db.query(Category)
            .not_deleted()
            .filter(and_(Category.title.ilike(f'%{request.title}%'), Category.id != request.id))
            .first()):
            raise HTTPException(status_code=400, detail="Este título já está cadastrado em uma categoria de competência.")
        
        entity: Category = (self.db
                 .query(Category)
                 .not_deleted()
                 .filter(Category.id == request.id)
                 .first())
        
        entity.update(request.title, request.description)
        
        self.db.commit()
        return Response(status_code=200)