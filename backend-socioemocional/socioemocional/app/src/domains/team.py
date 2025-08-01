from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .associations import team_user_association, team_manager_association, team_questionnaire_association

class Team(DomainBase, Base):
    __tablename__ = 'teams'

    name = Column(String, nullable=False)

    users = relationship("User", secondary=team_user_association, back_populates="teams")
    managers = relationship("User", secondary=team_manager_association, back_populates="managed_teams")
    questionnaires = relationship("Questionnaire", secondary=team_questionnaire_association, back_populates="teams")

    def __init__(self, name: str):
        self.name = name

    def update(self, name: str):
        self.name = name