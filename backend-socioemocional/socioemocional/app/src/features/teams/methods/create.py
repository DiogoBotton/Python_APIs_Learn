from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.team import Team
from src.domains.user import User
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.validations.existence import entity_id_exists, field_error
from uuid import UUID
from typing import List

# Request
class Command(BaseModel):
    name: str
    user_ids: List[UUID] = []
    manager_ids: List[UUID] = []

    @field_validator('name', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Nome do time é obrigatório.')
        return v
    
    @field_validator('manager_ids', mode='after')
    def valid(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Id de gerentes é obrigatório.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if (self.db.query(Team)
            .not_deleted()
            .filter(Team.name.ilike(f'%{request.name}%'))
            .first()):
            raise HTTPException(status_code=400, detail="Este nome de equipe já está em uso.")
        
        entity = Team(request.name)
        entity.managers = (
                self.db.query(User)
                .filter(User.id.in_(request.manager_ids))
                .all()
            )

        if len(request.user_ids) > 0:
            users = (
                self.db.query(User)
                .filter(User.id.in_(request.user_ids))
                .all()
            )
            entity.users = users
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity