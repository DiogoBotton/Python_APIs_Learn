from fastapi import APIRouter, Depends, Body
from src.features.competences.methods import listall, create, detail, edit, delete
from src.infrastructure.results.competence import CompetenceResult
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from uuid import UUID

router = APIRouter(prefix="/competences", tags=["Competences"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos as competências", dependencies=[Depends(JWTBearer())], response_model=PageResult[CompetenceResult])
def list_users(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)

@router.get("/{id}", summary="Retorna uma competência por id", dependencies=[Depends(JWTBearer())], response_model=CompetenceResult)
def detail_user(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria uma competência', dependencies=[Depends(JWTBearer())], response_model=RegisterResult)
def create_user(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    return handler.execute(command)

@router.put("", summary="Edita uma competência por id", dependencies=[Depends(JWTBearer())])
def edit_user(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta uma competência por id", dependencies=[Depends(JWTBearer())])
def delete_user(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)