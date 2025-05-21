# TODO: Criar classe para abstrair methods (simular handle do Mediator)
from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy.orm import Session

class BaseFeature(ABC):
    @abstractmethod
    def execute(self, db: Session, request: BaseModel): # TODO: Tentar adicionar snippet para o "not_deleted"
        """Deve ser implementado pelas subclasses"""
        raise NotImplementedError("Feature não implementada.")