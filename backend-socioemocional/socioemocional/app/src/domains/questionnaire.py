from sqlalchemy import Column, ForeignKey, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.domains.enums.questionnaire_status import QuestionnaireStatus
from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .associations import team_questionnaire_association

class Questionnaire(DomainBase, Base):
    __tablename__ = 'questionnaires'

    title = Column(String, nullable=False) # TODO: Talvez não terá mais essa coluna
    description = Column(String, nullable=False)
    status = Column(SqlEnum(QuestionnaireStatus), nullable=False)
    competence_id = Column(UUID(as_uuid=True), ForeignKey("competences.id"), nullable=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    teams = relationship("Team", secondary=team_questionnaire_association, back_populates="questionnaires")

    created_by = relationship("User", back_populates="questionnaires_created", foreign_keys=[created_by_id])
    competence = relationship("Competence", back_populates="questionnaires")
    questions = relationship("Question", back_populates="questionnaire")
    evaluations = relationship("Evaluation", back_populates="questionnaire")

    def __init__(self, title: str, description: str, status: QuestionnaireStatus, competence_id: UUID, created_by_id: UUID):
        self.title = title
        self.description = description
        self.status = status
        self.competence_id = competence_id
        self.created_by_id = created_by_id

    def update(self, title: str, description: str, status: QuestionnaireStatus, competence_id: UUID):
        self.title = title
        self.description = description
        self.status = status
        self.competence_id = competence_id