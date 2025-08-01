from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class AnswerOption(DomainBase, Base):
    __tablename__ = 'answer_options'

    title = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)

    descriptions = relationship("AnswerOptionDescription", back_populates="answer_option")
    evaluation_answers = relationship("EvaluationAnswer", back_populates="answer_option")

    def __init__(self, title: str, value: int, order: int):
        self.title = title
        self.value = value
        self.order = order

    def update(self, title: str, value: int, order: int):
        self.title = title
        self.value = value
        self.order = order