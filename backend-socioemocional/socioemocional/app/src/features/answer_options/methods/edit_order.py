from typing import List
from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.data.database import get_db
from sqlalchemy import and_ 
from pydantic import BaseModel, field_validator
from . import BaseHandler
from src.domains.answer_option import AnswerOption
from uuid import UUID

# Request
class OrderRequest(BaseModel):
    id: UUID
    order: int

class Command(BaseModel):
    answer_option_orders: List[OrderRequest]

    @field_validator('answer_option_orders', mode='after')
    def valid(cls, v):
        if not v and len(v) == 0:
            raise ValueError('Ordenação dos tipos de resposta é obrigatório.')
        return v

# Handle
class Edit(BaseHandler[Command, Response]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def execute(self, request: Command):      
        # Lista de ids
        ids = [item.id for item in request.answer_option_orders]
        
        # Busca todas as entidades com os ids enviados
        answer_options = (
            self.db.query(AnswerOption)
            .filter(AnswerOption.id.in_(ids))
            .all()
        )
        
        if len(ids) != len(answer_options):
            answer_options_ids = [item.id for item in answer_options]
            no_exists_ids = []
            for id in ids:
                if id not in answer_options_ids:
                    no_exists_ids.append(id)
            
            if len(no_exists_ids) > 0:
                raise HTTPException(status_code=404, detail={"no_exists_ids": no_exists_ids})
            
        # Cria um dicionario com o id como chave e o campo order como valor
        order_map = {item.id: item.order for item in request.answer_option_orders}
        
        # Atualiza a ordem de cada entidade
        for option in answer_options:
            if option.id in order_map:
                option.update_order(order_map[option.id])
        
        self.db.commit()
        return Response(status_code=200)