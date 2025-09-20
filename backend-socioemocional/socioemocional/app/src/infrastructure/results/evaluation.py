from src.infrastructure.results.base import BaseResult
from uuid import UUID
from src.domains.enums.evaluation_type import EvaluationType
from src.infrastructure.results.default import IdNameResult, IdTitleResult

class EvaluationResult(BaseResult):
    id: UUID
    observation: str
    answer_evaluated_person: str | None
    evaluation_type: EvaluationType
    created_by: IdNameResult
    questionnaire: IdTitleResult
    evaluated_person: IdNameResult | None