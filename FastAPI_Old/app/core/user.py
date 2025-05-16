from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .enums.enum_type import IntFlagEnumType

from data.database import Base
from .abstractions.domain_base import DomainBase
from .enums.role_type import RoleType

class User(DomainBase, Base):
    __tablename__= 'users'

    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    roles = Column(IntFlagEnumType(RoleType), nullable=False, default=RoleType.Common)

    def set_roles(self, roles: list[RoleType]):
        self.roles = RoleType(0)
        for role in roles:
            self.roles |= role
        
    def has_role(self, role: RoleType) -> bool:
        return (self.roles & role) == role