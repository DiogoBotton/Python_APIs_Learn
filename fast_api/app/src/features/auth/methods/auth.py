from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from src.domains.user import User
from src.infrastructure.security.password import verify_password
from src.infrastructure.results.auth import TokenResult
from src.infrastructure.security.token import generate_jwt_token

from . import BaseHandler

# Request
class Command(BaseModel):
    email: str
    password: str

# Handle
class Auth(BaseHandler[Command, TokenResult]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):
        user: User = (self.db.query(User)
            .not_deleted()
            .filter(User.email == request.email)
            .first())
        
        if not user:
            raise HTTPException(status_code=404, detail="E-mail ou senha inválidos.")

        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=404, detail="E-mail ou senha inválidos.")
        
        return TokenResult(token=generate_jwt_token(user))