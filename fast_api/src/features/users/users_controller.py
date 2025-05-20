from fastapi import APIRouter, Depends, Body
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.data.database import get_db
from src.core import User
from src.core.enums.role_type import RoleType
from src.features.users.methods import listall
from src.features.users.methods import create
from src.infraestructure.schema_results.user_schemas import UserResult
from src.infraestructure.schema_results.register_result import RegisterResult

router = APIRouter(prefix="/users", tags=["Users"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos os usuários", response_model=list[UserResult])
def get_users(query: listall.Query = Depends(),
              db: Session = Depends(get_db)):
    return listall.Handle().execute(db, query)

@router.post("", summary='Cria um usuário', response_model=RegisterResult)
def create_user(command: create.Command = Body(...),
                db: Session = Depends(get_db)):
    return create.Handle().execute(db, command)