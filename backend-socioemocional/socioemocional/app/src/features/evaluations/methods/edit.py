from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.enums.evaluation_type import EvaluationType
from src.domains.evaluation import Evaluation
from uuid import UUID
    
class Command(BaseModel):
    id: UUID
    answer_evaluated_person: str

    @field_validator('answer_evaluated_person', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Resposta da pessoa avaliada é obrigatório.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        entity: Evaluation = (self.db
                 .query(Evaluation)
                 .not_deleted()
                 .filter(Evaluation.id == request.id)
                 .first())
        
        if entity is None:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada.")
        
        if entity.evaluation_type == EvaluationType.SelfAssessment:
            raise HTTPException(status_code=400, detail="Não é possível responder uma auto avaliação.")
        
        entity.answer_evaluation(request.answer_evaluated_person)
        
        self.db.commit()
        return Response(status_code=200)