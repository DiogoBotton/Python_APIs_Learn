from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.database import Base, engine

# Importação necessária para importar os modelos do banco dados e criados com o create_all abaixo (caso estejam em pastas diferentes)
import core

# Criação automática do banco de dados
Base.metadata.create_all(bind=engine) # O banco de dados precisa existir antes de executar

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