from sqlalchemy import Column, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .enums.role_type import RoleType
from .associations import team_user_association, team_manager_association

class User(DomainBase, Base):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cpf = Column(String, nullable=False, unique=True)
    role = Column(SqlEnum(RoleType), nullable=False)

    teams = relationship("Team", secondary=team_user_association, back_populates="users")
    managed_teams = relationship("Team", secondary=team_manager_association, back_populates="managers")

    evaluations_created = relationship("Evaluation", back_populates="created_by", foreign_keys="Evaluation.created_by_id")
    evaluations_received = relationship("Evaluation", back_populates="evaluated_person", foreign_keys="Evaluation.evaluated_person_id")
    questionnaires_created = relationship("Questionnaire", back_populates="created_by", foreign_keys="Questionnaire.created_by_id")

    def __init__(self, name: str, email: str, cpf: str, role: RoleType):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.role = role
        
    def update(self, name: str, email: str, role: RoleType):
        self.name = name
        self.email = email
        self.role = role