from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class AnswerOptionDescription(DomainBase, Base):
    __tablename__ = 'answer_option_descriptions'

    description = Column(String, nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    answer_option_id = Column(UUID(as_uuid=True), ForeignKey("answer_options.id"), nullable=False)

    question = relationship("Question", back_populates="descriptions")
    answer_option = relationship("AnswerOption", back_populates="descriptions")

    def __init__(self, description: str, question_id: UUID, answer_option_id: UUID):
        self.description = description
        self.question_id = question_id
        self.answer_option_id = answer_option_id

    def update(self, description: str, question_id: UUID, answer_option_id: UUID):
        self.description = description
        self.question_id = question_id
        self.answer_option_id = answer_option_id