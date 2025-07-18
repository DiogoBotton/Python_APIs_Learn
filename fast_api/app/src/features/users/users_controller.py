from fastapi import APIRouter, Depends, Body
from src.features.users.methods import listall, create, detail, edit, delete
from src.infrastructure.results.user import UserResult
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos os usuários", response_model=PageResult[UserResult])
def list_users(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)

@router.get("/{id}", summary="Retorna um usuário por id", response_model=UserResult)
def detail_user(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria um usuário', response_model=RegisterResult)
def create_user(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    return handler.execute(command)

@router.put("", summary="Edita um usuário por id")
def edit_user(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta um usuário por id")
def delete_user(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)