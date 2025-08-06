from typing import List
from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.team import Team
from src.domains.user import User
from uuid import UUID

# Request
class Command(BaseModel):
    id: UUID
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
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):      
        if (self.db.query(Team)
            .not_deleted()
            .filter(and_(Team.title.ilike(f'%{request.title}%'), Team.id != request.id))
            .first()):
            raise HTTPException(status_code=400, detail="Este nome de equipe já está em uso.")
        
        entity: Team = (self.db
                 .query(Team)
                 .not_deleted()
                 .filter(Team.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Equipe não encontrada.")
        
        entity.update(request.name)

        managers = (
                self.db.query(User)
                .filter(User.id.in_(request.manager_ids))
                .all()
            )
        entity.managers = managers

        users = (
            self.db.query(User)
            .filter(User.id.in_(request.user_ids))
            .all()
        )
        entity.users = users
        
        self.db.commit()
        return Response(status_code=200)