from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import questions

app = FastAPI(
    title="API Questions",
    docs_url="/docs" # URL para disponibilização do Swagger UI
)

# Libera o CORS da API para requisições via http
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(questions.router)