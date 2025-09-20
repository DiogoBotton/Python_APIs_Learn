from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_ # Com SqlAlchemy é necessário utilizar a função or_ ou and_ para realizar consultas com operadores condicionais
from src.data.database import get_db
from pydantic import BaseModel, field_validator
from src.infrastructure.validations.existence import entity_id_exists, field_error
from . import BaseHandler
from src.domains.questionnaire import Questionnaire
from src.domains.answer_option_description import AnswerOptionDescription
from src.domains.user import User
from src.domains.question import Question
from src.domains.evaluation import Evaluation
from src.domains.evaluation_answer import EvaluationAnswer
from src.infrastructure.results.default import RegisterResult
from src.domains.enums.evaluation_type import EvaluationType
from src.infrastructure.security.actor import Actor
from typing import List
from uuid import UUID

# Request
class EvaluationAnswerRequest(BaseModel):
    answer_option_id: UUID
    question_id: UUID
    
class Command(BaseModel):
    observation: str
    evaluation_type: EvaluationType
    questionnaire_id: UUID
    evaluated_person_id: UUID | None = None
    evaluation_answers: List[EvaluationAnswerRequest]
    
    @field_validator('evaluation_type', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Tipo da avaliação é obrigatório.')
        return v
    
    @field_validator('questionnaire_id', mode='after')
    def valid(cls, v):
        if not v:
            raise ValueError('Id do questionário é obrigatório.')
        return v

# Handle
class Create(BaseHandler[Command, RegisterResult]):
    def __init__(self, db: Session = Depends(get_db), actor: Actor = Depends()):
        self.db = db
        self.actor = actor

    def execute(self, request: Command):
        if not entity_id_exists(self.db, Questionnaire, request.questionnaire_id):
            raise field_error("questionnaire_id", "Questionário não encontrado.")
        
        if request.evaluation_type != EvaluationType.SelfAssessment and not request.evaluated_person_id:
            raise field_error("evaluated_person_id", "Usuário avaliado é obrigatório quando não é uma auto avaliação.")
        
        if request.evaluated_person_id:
            if not entity_id_exists(self.db, User, request.evaluated_person_id):
                raise field_error("evaluated_person_id", "Usuário não encontrado.")
        
        question_ids = [item.question_id for item in request.evaluation_answers]
        answer_option_ids = [item.answer_option_id for item in request.evaluation_answers]
        
        questions: List[Question] = (self.db
                 .query(Question)
                 .not_deleted()
                 .filter(Question.id.in_(question_ids))
                 .all())
        
        answer_option_descriptions: List[AnswerOptionDescription] = (self.db
                 .query(AnswerOptionDescription)
                 #.options(joinedload(AnswerOptionDescription.answer_option))
                 .not_deleted()
                 .filter(
                    or_(*[
                        and_(
                            AnswerOptionDescription.answer_option_id == e.answer_option_id,
                            AnswerOptionDescription.question_id == e.question_id
                        ) for e in request.evaluation_answers
                    ])
                )
                .all()
        )
        
        # Valida se alguma question_id não existe
        if len(question_ids) != len(questions):
            ids = [item.id for item in questions]
            no_exists_ids = [id for id in question_ids if id not in ids]
            if len(no_exists_ids) > 0:
                raise HTTPException(status_code=404, detail={"question_no_exists_ids": [str(id) for id in no_exists_ids]})
            
        # Valida se alguma answer_option_id não existe
        if len(answer_option_ids) != len(answer_option_descriptions):
            ids = [item.answer_option_id for item in answer_option_descriptions]
            no_exists_ids = [id for id in answer_option_ids if id not in ids]
            if len(no_exists_ids) > 0:
                raise HTTPException(status_code=404, detail={"answer_option_no_exists_ids": [str(id) for id in no_exists_ids]})
            
        entity = Evaluation(request.evaluation_type, request.observation, request.questionnaire_id, self.actor.user_id, request.evaluated_person_id)
        
        question_map = {item.id: item for item in questions}
        description_map = {item.answer_option_id: item for item in answer_option_descriptions}
        
        evaluation_answers: List[EvaluationAnswer] = []
        for e in request.evaluation_answers:
            question_title = question_map[e.question_id].title
            answer_option_description = description_map[e.answer_option_id].description
            answer_option_title = description_map[e.answer_option_id].answer_option.title
            answer = EvaluationAnswer(answer_option_title, question_title, answer_option_description, e.answer_option_id, e.question_id)
            evaluation_answers.append(answer)
        
        entity.evaluation_answers = evaluation_answers
        
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity