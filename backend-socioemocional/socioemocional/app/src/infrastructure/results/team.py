from src.infrastructure.results.base import BaseResult
from src.infrastructure.results.default import IdNameResult
from typing import List
from uuid import UUID

class TeamSimpleResult(BaseResult):
    id: UUID
    name: str
    
class TeamResult(BaseResult):
    id: UUID
    name: str
    
    managers: List[IdNameResult]