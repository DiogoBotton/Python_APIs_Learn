from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, Integer
import uuid

from data.database import Base
from abstractions.domain_base import DomainBase
from enums.role_type import RoleType

class RoleTypeFlag(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return int(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return RoleType(value) if value is not None else None

class User(DomainBase, Base):
    __tablename__= 'users'

    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    roles = Column(RoleTypeFlag, nullable=False, default=RoleType.Common)

    # TODO: Realizar funções 'set_roles' e 'has_roles'