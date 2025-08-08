    
from src.infrastructure.results.base import BaseResult
from uuid import UUID
from .default import IdTitleResult

class AnswerOptionDescriptionResult(BaseResult):
    id: UUID
    description: str
    
    question: IdTitleResult
    answer_option: IdTitleResult