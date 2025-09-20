from typing import List
from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from uuid import UUID

# Request
class Command(BaseModel):
    id: UUID
    title: str
    value: int

    @field_validator('name', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Nome do time é obrigatório.')
        return v
    
    @field_validator('value', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Valor do tipo da resposta é obrigatória.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):      
        if (self.db.query(AnswerOption)
            .not_deleted()
            .filter(and_(AnswerOption.title.ilike(f'%{request.title}%'), AnswerOption.id != request.id))
            .first()):
            raise HTTPException(status_code=400, detail="Este título de tipo de resposta já está em uso.")
        
        entity: AnswerOption = (self.db
                 .query(AnswerOption)
                 .not_deleted()
                 .filter(AnswerOption.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Tipo de resposta não encontrada.")
        
        entity.update(request.title, request.value)
        
        self.db.commit()
        return Response(status_code=200)