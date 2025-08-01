from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase

class TeamUser(DomainBase, Base):
    __tablename__ = 'team_users'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)

    user = relationship("User", back_populates="team_users")
    team = relationship("Team", back_populates="users")

    def __init__(self, user_id: UUID, team_id: UUID):
        self.user_id = user_id
        self.team_id = team_id