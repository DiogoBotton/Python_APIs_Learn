from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class EvaluationAnswer(DomainBase, Base):
    __tablename__ = 'evaluation_answers'

    answer_option_title = Column(String, nullable=False)
    question_title = Column(String, nullable=False)
    answer_option_description_title = Column(String, nullable=False)

    answer_option_id = Column(UUID(as_uuid=True), ForeignKey("answer_options.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("evaluations.id"), nullable=False)

    answer_option = relationship("AnswerOption", back_populates="evaluation_answers")
    question = relationship("Question", back_populates="evaluation_answers")
    evaluation = relationship("Evaluation", back_populates="evaluation_answers")

    def __init__(self, answer_option_title: str, question_title: str, answer_option_description_title: str, answer_option_id: UUID, question_id: UUID):
        self.answer_option_title = answer_option_title
        self.question_title = question_title
        self.answer_option_description_title = answer_option_description_title
        self.answer_option_id = answer_option_id
        self.question_id = question_id