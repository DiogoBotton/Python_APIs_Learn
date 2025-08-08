from fastapi import APIRouter, Depends, Body
from src.features.answer_option_descriptions.methods import listall
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from src.infrastructure.results.answer_option_description import AnswerOptionDescriptionResult
from uuid import UUID

router = APIRouter(prefix="/answer_option_descriptions", tags=["Answer Option Descriptions"])

@router.get("", summary="Lista todos as descrições de respostas de uma questão especifica", dependencies=[Depends(JWTBearer())], response_model=PageResult[AnswerOptionDescriptionResult])
def list_function(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)