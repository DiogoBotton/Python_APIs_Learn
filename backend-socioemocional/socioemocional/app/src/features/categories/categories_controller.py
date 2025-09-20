from fastapi import APIRouter, Depends, Body
from src.features.categories.methods import listall, create, detail, edit, delete
from src.infrastructure.results.category import CategoryResult
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from uuid import UUID

router = APIRouter(prefix="/categories", tags=["Questionnaire Categories"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos as categorias", dependencies=[Depends(JWTBearer())], response_model=PageResult[CategoryResult])
def list_users(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)

@router.get("/{id}", summary="Retorna uma categoria por id", dependencies=[Depends(JWTBearer())], response_model=CategoryResult)
def detail_user(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria uma categoria', dependencies=[Depends(JWTBearer())], response_model=RegisterResult)
def create_user(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    return handler.execute(command)

@router.put("", summary="Edita uma categoria por id", dependencies=[Depends(JWTBearer())])
def edit_user(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta uma categoria por id", dependencies=[Depends(JWTBearer())])
def delete_user(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)