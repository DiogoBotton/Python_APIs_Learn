from sqlalchemy import Column, ForeignKey, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .enums.evaluation_type import EvaluationType

class Evaluation(DomainBase, Base):
    __tablename__ = 'evaluations'

    evaluation_type = Column(SqlEnum(EvaluationType), nullable=False)
    observation = Column(String)
    answer_evaluated_person = Column(String)

    evaluated_person_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    questionnaire_id = Column(UUID(as_uuid=True), ForeignKey("questionnaires.id"), nullable=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    created_by = relationship("User", back_populates="evaluations_created", foreign_keys=[created_by_id])
    evaluated_person = relationship("User", back_populates="evaluations_received", foreign_keys=[evaluated_person_id])
    questionnaire = relationship("Questionnaire", back_populates="evaluations")

    def __init__(self, evaluation_type: EvaluationType, observation: str, questionnaire_id: UUID, created_by_id: UUID, evaluated_person_id: None | UUID):
        self.evaluation_type = evaluation_type
        self.observation = observation
        self.questionnaire_id = questionnaire_id
        self.created_by_id = created_by_id
        self.evaluated_person_id = evaluated_person_id

    def answer_evaluation(self, answer_evaluated_person: str):
        self.answer_evaluated_person = answer_evaluated_person