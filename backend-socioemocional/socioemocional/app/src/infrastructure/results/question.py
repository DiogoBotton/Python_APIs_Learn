from src.infrastructure.results.base import BaseResult
from uuid import UUID
from .default import IdTitleResult
from .answer_option_description import AnswerOptionDescriptionResult
from typing import List

class QuestionSimpleResult(BaseResult):
    id: UUID
    title: str
    order: int
    
    questionnaire: IdTitleResult

class QuestionResult(BaseResult):
    id: UUID
    title: str
    order: int
    
    questionnaire: IdTitleResult
    
    descriptions: List[AnswerOptionDescriptionResult]