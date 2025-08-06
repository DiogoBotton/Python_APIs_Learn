from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.competence import Competence
from src.domains.questionnaire import Questionnaire
from src.domains.enums.questionnaire_status import QuestionnaireStatus
from src.domains.team import Team
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.validations.existence import entity_id_exists, field_error
from uuid import UUID
from typing import List

# Request
class Command(BaseModel):
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
    
    @field_validator('status', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Status é obrigatório.')
        return v
    
    @field_validator('competence_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id da Competência é obrigatório.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        if not entity_id_exists(self.db, Competence, request.competence_id):
            raise field_error("competence_id", "Competência não encontrada.")
        
        if (self.db.query(Questionnaire)
            .not_deleted()
            .filter(Questionnaire.title.ilike(f'%{request.title}%'))
            .first()):
            raise HTTPException(status_code=400, detail="Este título já está cadastrado em um questionário.")
        
        entity = Questionnaire(request.title, request.description, request.status, request.competence_id)

        if len(request.team_ids) > 0:
            teams = (
                self.db.query(Team)
                .filter(Team.id.in_(request.team_ids))
                .all()
            )
            entity.teams = teams
    
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity