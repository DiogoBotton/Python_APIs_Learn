from fastapi import APIRouter, Depends
from src.features.evaluation_answers.methods import listall
from src.infrastructure.pagination.models import PageResult
from src.infrastructure.security.routes import JWTBearer
from src.infrastructure.results.evaluation_answer import EvaluationAnswerResult

router = APIRouter(prefix="/evaluation_answers", tags=["Evaluations Answers"])

@router.get("", summary="Lista todas a respostas de uma avaliação especifica", dependencies=[Depends(JWTBearer())], response_model=PageResult[EvaluationAnswerResult])
def list_function(query: listall.Query = Depends(),
              handler: listall.ListAll = Depends()):
    return handler.execute(query)