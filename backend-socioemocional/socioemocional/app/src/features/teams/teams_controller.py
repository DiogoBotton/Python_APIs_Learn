from fastapi import APIRouter, Depends, Body
from src.features.teams.methods import listall, create, detail, edit, delete
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from src.infrastructure.results.team import TeamSimpleResult, TeamResult
from uuid import UUID

router = APIRouter(prefix="/teams", tags=["Teams"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todas as equipes", dependencies=[Depends(JWTBearer())], response_model=PageResult[TeamSimpleResult])
def list_function(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)

@router.get("/{id}", summary="Retorna uma equipe por id", dependencies=[Depends(JWTBearer())], response_model=TeamResult)
def detail_function(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria uma equipe', dependencies=[Depends(JWTBearer())], response_model=RegisterResult)
def create_function(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    return handler.execute(command)

@router.put("", summary="Edita uma equipe por id", dependencies=[Depends(JWTBearer())])
def edit_function(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta uma equipe por id", dependencies=[Depends(JWTBearer())])
def delete_function(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)