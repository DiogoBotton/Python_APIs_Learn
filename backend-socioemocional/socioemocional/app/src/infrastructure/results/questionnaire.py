from src.infrastructure.results.base import BaseResult
from uuid import UUID
from src.domains.enums.questionnaire_status import QuestionnaireStatus
from .team import TeamResult
from typing import List

class QuestionnaireResult(BaseResult):
    id: UUID
    title: str
    description: str
    status: QuestionnaireStatus
    competence_id: UUID

    teams: List[TeamResult]


class QuestionnaireSimpleResult(BaseResult):
    id: UUID
    title: str
    description: str
    status: QuestionnaireStatus
    competence_id: UUID