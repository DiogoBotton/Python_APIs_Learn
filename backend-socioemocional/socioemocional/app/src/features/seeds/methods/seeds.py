from fastapi import Response, Depends
from pydantic import BaseModel
from src.infrastructure.data.seed_executor import SeedExecutor

from . import BaseHandler

# Request
class Command(BaseModel):
    pass

# Handle
class Seeds(BaseHandler[Command, Response]):
    def __init__(self, seed_executor: SeedExecutor = Depends()):
        self.seed_executor = seed_executor

    def execute(self):
        return self.seed_executor.execute()