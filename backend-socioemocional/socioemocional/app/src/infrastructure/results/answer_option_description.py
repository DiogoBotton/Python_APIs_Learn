    
from src.infrastructure.results.base import BaseResult
from uuid import UUID

class AnswerOptionDescriptionResult(BaseResult):
    id: UUID
    description: str
    question_id: UUID
    answer_option_id: UUID