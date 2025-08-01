from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .associations import team_questionnaire_association

class Questionnaire(DomainBase, Base):
    __tablename__ = 'questionnaires'

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    competence_id = Column(UUID(as_uuid=True), ForeignKey("competences.id"), nullable=False)

    teams = relationship("Team", secondary=team_questionnaire_association, back_populates="questionnaires")

    competence = relationship("Competence", back_populates="questionnaires")
    questions = relationship("Question", back_populates="questionnaire")
    evaluations = relationship("Evaluation", back_populates="questionnaire")

    def __init__(self, title: str, description: str, competence_id: UUID):
        self.title = title
        self.description = description
        self.competence_id = competence_id

    def update(self, title: str, description: str, competence_id: UUID):
        self.title = title
        self.description = description
        self.competence_id = competence_id