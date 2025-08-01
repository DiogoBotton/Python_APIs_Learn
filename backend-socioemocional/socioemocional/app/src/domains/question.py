from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class Question(DomainBase, Base):
    __tablename__ = 'questions'

    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    questionnaire_id = Column(UUID(as_uuid=True), ForeignKey("questionnaires.id"), nullable=False)

    questionnaire = relationship("Questionnaire", back_populates="questions")
    descriptions = relationship("AnswerOptionDescription", back_populates="question")
    evaluation_answers = relationship("EvaluationAnswer", back_populates="question")

    def __init__(self, title: str, order: int, questionnaire_id: UUID):
        self.title = title
        self.order = order
        self.questionnaire_id = questionnaire_id

    def update(self, title: str, order: int):
        self.title = title
        self.order = order