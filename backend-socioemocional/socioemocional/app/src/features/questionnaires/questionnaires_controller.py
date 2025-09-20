from typing import List
from fastapi import APIRouter, Depends, Body, Query as FastQuery
from src.features.questionnaires.methods import listall, create, detail, edit, delete
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from src.infrastructure.results.questionnaire import QuestionnaireResult
from uuid import UUID

router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos os questionários", dependencies=[Depends(JWTBearer())], response_model=PageResult[QuestionnaireResult])
def list_function(query: listall.Query = Depends(),
                  team_ids: List[UUID] = FastQuery(None),
              handler: listall.ListAll = Depends()):
    return handler.execute(query, team_ids)

@router.get("/{id}", summary="Retorna um questionário por id", dependencies=[Depends(JWTBearer())], response_model=QuestionnaireResult)
def detail_function(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria um questionário', dependencies=[Depends(JWTBearer())], response_model=RegisterResult)
def create_function(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    """
    Status:
    
    - Ativo = 1
    - Rascunho = 2
    - Inativo = 3
    """
    return handler.execute(command)

@router.put("", summary="Edita um questionário por id", dependencies=[Depends(JWTBearer())])
def edit_function(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta um questionário por id", dependencies=[Depends(JWTBearer())])
def delete_function(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)