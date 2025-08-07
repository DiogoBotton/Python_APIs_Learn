from typing import List
from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.questionnaire import Questionnaire
from src.domains.competence import Competence
from src.domains.enums.questionnaire_status import QuestionnaireStatus
from src.domains.team import Team
from uuid import UUID
from src.infrastructure.validations.existence import entity_id_exists, field_error

# Request
class Command(BaseModel):
    id: UUID
    title: str
    description: str
    status: QuestionnaireStatus
    competence_id: UUID
    team_ids: List[UUID] = []


    @field_validator('title', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Título é obrigatório.')
        return v
    
    @field_validator('description', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Descrição é obrigatório.')
        return v
    
    @field_validator('competence_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id da Competência é obrigatório.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):      
        if not entity_id_exists(self.db, Competence, request.competence_id):
            raise field_error("competence_id", "Competência não encontrada.")
        
        if (self.db.query(Questionnaire)
            .not_deleted()
            .filter(and_(Questionnaire.title.ilike(f'%{request.title}%'), Questionnaire.id != request.id))
            .first()):
            raise HTTPException(status_code=400, detail="Este título já está cadastrado em um questionário.")
        
        entity: Questionnaire = (self.db
                 .query(Questionnaire)
                 .not_deleted()
                 .filter(Questionnaire.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Questionário não encontrado.")
        
        entity.update(request.title, request.description, request.status, request.competence_id)

        teams = (
                self.db.query(Team)
                .filter(Team.id.in_(request.team_ids))
                .all()
            )
        entity.teams = teams
        
        self.db.commit()
        return Response(status_code=200)