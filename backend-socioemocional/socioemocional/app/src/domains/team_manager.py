from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class TeamManager(DomainBase, Base):
    __tablename__ = 'team_managers'

    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)

    manager = relationship("User", back_populates="team_managed")
    team = relationship("Team", back_populates="managers")

    def __init__(self, manager_id: UUID, team_id: UUID):
        self.manager_id = manager_id
        self.team_id = team_id