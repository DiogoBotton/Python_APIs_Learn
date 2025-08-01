from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel
from . import BaseHandler
from src.domains.competence import Competence
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
        if not entity_id_exists(self.db, Competence, request.id):
            raise field_error("id", "Competência não encontrada.")
        
        if (self.db.query(Competence)
            .not_deleted()
            .filter(and_(Competence.title.ilike(f'%{request.title}%'), Competence.id != request.id))
            .first()):
            raise HTTPException(status_code=400, detail="Este título já está cadastrado em uma competência.")
        
        entity: Competence = (self.db
                 .query(Competence)
                 .not_deleted()
                 .filter(Competence.id == request.id)
                 .first())
        
        entity.update(request.title, request.description)
        
        self.db.commit()
        return Response(status_code=200)