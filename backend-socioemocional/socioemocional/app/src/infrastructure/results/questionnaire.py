from src.infrastructure.results.default import IdTitleResult, IdNameResult
from src.infrastructure.results.base import BaseResult
from uuid import UUID
from src.domains.enums.questionnaire_status import QuestionnaireStatus
from .team import TeamSimpleResult
from typing import List

class QuestionnaireResult(BaseResult):
    id: UUID
    title: str
    description: str
    status: QuestionnaireStatus
    category: IdTitleResult

    teams: List[TeamSimpleResult]
    created_by: IdNameResult


class QuestionnaireSimpleResult(BaseResult):
    id: UUID
    title: str
    description: str
    status: QuestionnaireStatus
    category: IdTitleResult