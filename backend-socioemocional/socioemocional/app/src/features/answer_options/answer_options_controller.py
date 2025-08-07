from fastapi import APIRouter, Depends, Body
from src.features.answer_options.methods import listall, create, detail, edit, edit_order, delete
from src.infrastructure.results.default import RegisterResult
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from src.infrastructure.results.answer_option import AnswerOptionResult
from uuid import UUID

router = APIRouter(prefix="/answer_options", tags=["Answer Options"])

# response_model converte o resultado para o tipo especificado
@router.get("", summary="Lista todos os tipos de resposta", dependencies=[Depends(JWTBearer())], response_model=PageResult[AnswerOptionResult])
def list_function(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)

@router.get("/{id}", summary="Retorna um tipo de resposta por id", dependencies=[Depends(JWTBearer())], response_model=AnswerOptionResult)
def detail_function(id: UUID,
              handler: detail.Detail = Depends()):
    query = detail.Query
    query.id = id
    return handler.execute(query)

@router.post("", summary='Cria um tipo de resposta', dependencies=[Depends(JWTBearer())], response_model=RegisterResult)
def create_function(command: create.Command = Body(...),
                handler: create.Create = Depends()):
    return handler.execute(command)

@router.put("", summary="Edita um tipo de resposta por id", dependencies=[Depends(JWTBearer())])
def edit_function(command: edit.Command = Body(...),
                          handler: edit.Edit = Depends()):
    return handler.execute(command)

@router.put("/order", summary="Edita a ordem de todos os tipos de resposta", dependencies=[Depends(JWTBearer())])
def edit_order_function(command: edit_order.Command = Body(...),
                          handler: edit_order.Edit = Depends()):
    return handler.execute(command)

@router.delete("/{id}", summary="Deleta um tipo de resposta por id", dependencies=[Depends(JWTBearer())])
def delete_function(id: UUID,
                      handler: delete.Delete = Depends()):
    command = delete.Command
    command.id = id
    return handler.execute(command)