from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from src.data.database import Base, engine

from src.features.users import users_controller

# Criação automática do banco de dados (comentado pois o alembic já realiza isto)
#Base.metadata.create_all(bind=engine) # O banco de dados precisa existir antes de executar

app = FastAPI(
    title="Widgets API",
    docs_url="/docs", # URL para disponibilização do Swagger UI
)

# Libera o CORS da API para requisições via http
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(users_controller.router)