from src.infrastructure.results.base import BaseResult
from uuid import UUID
from src.infrastructure.results.default import IdTitleResult

class EvaluationAnswerResult(BaseResult):
    id: UUID
    answer_option_title: str
    question_title: str
    answer_option_description_title: str

    answer_option: IdTitleResult
    question: IdTitleResult