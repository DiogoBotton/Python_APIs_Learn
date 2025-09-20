from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel
from . import BaseHandler
from src.domains.category import Category
from src.infrastructure.results.default import RegisterResult

# Request
class Command(BaseModel):
    title: str
    description: str

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if (self.db.query(Category)
            .not_deleted()
            .filter(Category.title.ilike(f'%{request.title}%'))
            .first()):
            raise HTTPException(status_code=400, detail="Este título já está cadastrado em uma categoria de competência.")
        
        entity = Category(request.title, request.description)
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity