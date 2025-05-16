from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.data.database import get_db
from src.core import User
from src.core.enums.role_type import RoleType

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", summary="Lista todos os usuários")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).not_deleted().all()

@router.post("", summary='Cria um usuário')
def create_user( db: Session = Depends(get_db)):
    user = User( # TODO: Criar schemas (requests e responses)
        email = 'string2@email.com',
        cpf = '457484847854')
    user.set_roles([RoleType.Common])
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"iduser": user.id}