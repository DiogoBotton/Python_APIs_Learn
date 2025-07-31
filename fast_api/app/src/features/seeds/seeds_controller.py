from fastapi import APIRouter, HTTPException, Depends, Body
from src.features.seeds.methods import seeds
from settings import Settings

router = APIRouter(prefix="/dev/seeds", tags=["Seeds"])

@router.post("", summary='Cria dados padrões no banco de dados da aplicação')
def execute_seeds(handler: seeds.Seeds = Depends()):
    if Settings().ENVIRONMENT != "development":
        raise HTTPException(status_code=400, detail=f"Seed não permitido para o ambiente atual: [{Settings.ENVIRONMENT}].")
    return handler.execute()