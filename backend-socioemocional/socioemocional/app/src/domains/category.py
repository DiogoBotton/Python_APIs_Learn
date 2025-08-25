from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class Category(DomainBase, Base):
    __tablename__ = 'categories'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    questionnaires = relationship("Questionnaire", back_populates="category")

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def update(self, title: str, description: str):
        self.title = title
        self.description = description