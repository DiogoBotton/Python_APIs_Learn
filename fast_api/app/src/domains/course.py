from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.data.database import Base
from .abstractions.domain_base import DomainBase
from .enums.role_type import RoleType

class Course(DomainBase, Base):
    __tablename__= 'courses'

    title = Column(String, nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Varios cursos tem 1 criador (usuário)
    creator = relationship('User', back_populates='courses_created')

    # Um curso pode ter várias matriculas
    enrollments = relationship('Enrollment', back_populates='course')