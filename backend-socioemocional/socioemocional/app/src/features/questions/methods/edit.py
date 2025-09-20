from typing import List, Optional
from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from src.infrastructure.validations.existence import entity_id_exists, field_error
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from src.domains.question import Question
from src.domains.answer_option_description import AnswerOptionDescription
from uuid import UUID

class DescriptionRequest(BaseModel):
    id: Optional[UUID] = None
    description: str
    answer_option_id: UUID
    
class Command(BaseModel):
    id: UUID
    title: str
    question_descriptions: List[DescriptionRequest]

    @field_validator('title', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Título da questão é obrigatório.')
        return v
    
    @field_validator('question_descriptions', mode='after')
    def valid(cls, v):
        if not v and len(v) == 0:
            raise ValueError('Descrição das respostas é obrigatório.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        entity: Question = (self.db
                 .query(Question)
                 .not_deleted()
                 .filter(Question.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Questão não encontrada.")
        
        for d in request.question_descriptions:
            if not entity_id_exists(self.db, AnswerOption, d.answer_option_id):
                raise field_error("answer_option_id", "Tipo da resposta não encontrada.")
        
        question_description_ids = [item.id for item in request.question_descriptions if item.id is not None]
        new_descriptions = [item for item in request.question_descriptions if item.id is None]
        
        descriptions = (
            self.db.query(AnswerOptionDescription)
            .filter(AnswerOptionDescription.id.in_(question_description_ids))
            .all()
        )
        
        # Valida caso algum id não exista
        if len(question_description_ids) != len(descriptions):
            descriptions_ids = [item.id for item in descriptions]
            no_exists_ids = [id for id in question_description_ids if id not in descriptions_ids]
            if len(no_exists_ids) > 0:
                raise HTTPException(status_code=404, detail={"no_exists_ids": no_exists_ids})
        
        entity.update(request.title)
        
        description_map = {item.id: item.description for item in request.question_descriptions}
        
        # Edita descrições existentes
        for d in descriptions:
            if d.id in description_map:
                d.update(description_map[d.id])
                
        # Cria novas descrições
        for new in new_descriptions:
            new_entity = AnswerOptionDescription(
                description=new.description,
                question_id=entity.id,
                answer_option_id=new.answer_option_id
            )
            self.db.add(new_entity)
        
        self.db.commit()
        return Response(status_code=200)