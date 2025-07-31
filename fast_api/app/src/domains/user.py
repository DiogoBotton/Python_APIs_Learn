from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .enums.enum_type import IntFlagEnumType

from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .enums.role_type import RoleType

class User(DomainBase, Base):
    __tablename__= 'users'

    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    roles = Column(IntFlagEnumType(RoleType), nullable=False, default=RoleType.Common)

    # 1 usuário tem várias matriculas, quem referencia usuário? prop user da entidade 'Enrollment'
    enrollments = relationship('Enrollment', back_populates='user') # back_populates é qual a propriedade que realiza a referência inversa (de Enrollment para User), no caso, user

    # 1 usuário pode criar vários cursos
    courses_created = relationship('Course', back_populates='creator')

    def set_roles(self, roles: list[RoleType]):
        self.roles = RoleType(0)
        for role in roles:
            self.roles |= role
        
    def has_role(self, role: RoleType) -> bool:
        return (self.roles & role) == role
    
    def __init__(self, email: str, password: str, cpf: str, roles: list[RoleType]):
        self.email = email
        self.password = password
        self.cpf = cpf
        self.set_roles(roles)
        
    def update(self, email: str, cpf: str, roles: list[RoleType]):
        self.email = email
        self.cpf = cpf
        self.set_roles(roles)