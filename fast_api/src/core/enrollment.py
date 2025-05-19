from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from src.data.database import Base
from .abstractions.domain_base import DomainBase

class Enrollment(DomainBase, Base):
    __tablename__= 'enrollment'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Relacionamentos reversos (n:1)
    user = relationship('User', back_populates='enrollments') # Qual usuário é referenciado
    course = relationship('Course', back_populates='enrollments') # Qual curso é referenciado