from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from src.data.database import get_db
from src.features.users.methods import listall, create, detail
from src.infraestructure.results.user import UserResult
from src.infraestructure.results.default import RegisterResult
from src.infraestructure.pagination.models import PageResult
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos os usuários", response_model=PageResult[UserResult])
def list_users(query: listall.Query = Depends(),
              db: Session = Depends(get_db)):
    return listall.Handle().execute(db, query)

@router.get("/{id}", summary="Retorna um usuário por id", response_model=UserResult)
def detail_user(id: UUID,
              db: Session = Depends(get_db)):
    query = detail.Query
    query.id = id
    return detail.Handle().execute(db, query)

@router.post("", summary='Cria um usuário', response_model=RegisterResult)
def create_user(command: create.Command = Body(...),
                db: Session = Depends(get_db)):
    return create.Handle().execute(db, command)