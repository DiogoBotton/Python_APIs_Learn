from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.data.database import get_db
from pydantic import BaseModel
from src.domains.user import User
from src.infrastructure.results.auth import TokenResult
from src.infrastructure.security.token import generate_jwt_token
from src.infrastructure.utils import remove_special_characters

from . import BaseHandler

# Request
class Command(BaseModel):
    email: str
    cpf: str

# Handle
class Auth(BaseHandler[Command, TokenResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        user: User = (self.db.query(User)
            .not_deleted()
            .filter(and_(User.email == request.email, User.cpf == remove_special_characters(request.cpf)))
            .first())
        
        if not user:
            raise HTTPException(status_code=404, detail="E-mail ou CPF inválidos.")
        
        return TokenResult(token=generate_jwt_token(user))