from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class TeamQuestionnaire(DomainBase, Base):
    __tablename__ = 'team_questionnaires'

    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    questionnaire_id = Column(UUID(as_uuid=True), ForeignKey("questionnaires.id"), nullable=False)

    team = relationship("Team", back_populates="questionnaires")
    questionnaire = relationship("Questionnaire", back_populates="team_questionnaires")

    def __init__(self, team_id: UUID, questionnaire_id: UUID ):
        self.team_id = team_id
        self.questionnaire_id = questionnaire_id