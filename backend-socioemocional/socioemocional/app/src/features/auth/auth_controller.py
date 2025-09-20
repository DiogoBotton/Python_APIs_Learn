from fastapi import APIRouter, Depends, Body
from src.features.auth.methods import auth
from src.infrastructure.results.auth import TokenResult

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("", summary='Autenticação de usuário', response_model=TokenResult)
def auth_user(command: auth.Command = Body(...),
                handler: auth.Auth = Depends()):
    return handler.execute(command)