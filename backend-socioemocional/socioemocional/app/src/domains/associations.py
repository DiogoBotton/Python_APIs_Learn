from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from src.data.database import Base

# Desta forma, a relação muitos para muitos (Many to Many) funciona de forma mais simples
# Por exemplo, é possível acessar a partir de teams a lista de usuários com: teams.users.remove(user) ou teams.users.append(user)

team_user_association = Table(
    "team_users",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("team_id", UUID(as_uuid=True), ForeignKey("teams.id"), primary_key=True),
)

team_questionnaire_association = Table(
    "team_questionnaires",
    Base.metadata,
    Column("team_id", UUID(as_uuid=True), ForeignKey("teams.id"), primary_key=True),
    Column("questionnaire_id", UUID(as_uuid=True), ForeignKey("questionnaires.id"), primary_key=True),
)

team_manager_association = Table(
    "team_managers",
    Base.metadata,
    Column("manager_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("team_id", UUID(as_uuid=True), ForeignKey("teams.id"), primary_key=True),
)