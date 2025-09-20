from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from src.infrastructure.validations.existence import entity_id_exists, field_error
from . import BaseHandler
from src.domains.question import Question
from src.domains.questionnaire import Questionnaire
from src.domains.answer_option_description import AnswerOptionDescription
from src.domains.answer_option import AnswerOption
from src.infrastructure.results.default import RegisterResult
from typing import List
from uuid import UUID

# Request
class DescriptionRequest(BaseModel):
    description: str
    answer_option_id: UUID
    
class Command(BaseModel):
    title: str
    order: int
    questionnaire_id: UUID
    question_descriptions: List[DescriptionRequest]

    @field_validator('title', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Título da questão é obrigatório.')
        return v
    
    @field_validator('order', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Ordem da questão é obrigatório.')
        return v
    
    @field_validator('questionnaire_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id do questionário é obrigatório.')
        return v
    
    @field_validator('question_descriptions', mode='after')
    def valid(cls, v):
        if not v and len(v) == 0:
            raise ValueError('Descrição das respostas é obrigatório.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if not entity_id_exists(self.db, Questionnaire, request.questionnaire_id):
            raise field_error("questionnaire_id", "Questionário não encontrado.")
        
        for d in request.question_descriptions:
            if not entity_id_exists(self.db, AnswerOption, d.answer_option_id):
                raise field_error("answer_option_id", "Tipo da resposta não encontrada.")
        
        entity = Question(request.title, request.order, request.questionnaire_id)
            
        entity.descriptions = [AnswerOptionDescription(d.description, None, d.answer_option_id)
                               for d in request.question_descriptions]
        
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity