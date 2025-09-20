from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from uuid import UUID
from fastapi.exceptions import RequestValidationError
from src.domains.abstractions.domain_base import DomainBase

def entity_id_exists(db: Session, entity: DomainBase, id: UUID):
    entity = (db
              .query(exists()
                     .where(entity.id == id and entity.deleted_at.is_(None)))
              .scalar())
    
    return entity

def field_error(field_name: str, message: str):
    return RequestValidationError(errors=[{
        "loc": ("body", field_name),
        "msg": message,
        "type": "value_error"
    }])