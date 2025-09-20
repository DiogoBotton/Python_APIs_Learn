from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from src.infrastructure.results.default import RegisterResult

# Request
class Command(BaseModel):
    title: str
    value: int
    order: int

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
    
    @field_validator('order', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Ordem do tipo da resposta é obrigatória.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if (self.db.query(AnswerOption)
            .not_deleted()
            .filter(AnswerOption.title.ilike(f'%{request.title}%'))
            .first()):
            raise HTTPException(status_code=400, detail="Este título de resposta já está em uso.")
        
        entity = AnswerOption(request.title, request.value, request.order)
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity