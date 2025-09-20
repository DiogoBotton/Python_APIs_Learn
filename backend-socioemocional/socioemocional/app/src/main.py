from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST
from settings import Settings

from src.features.users import users_controller
from src.features.categories import categories_controller
from src.features.answer_option_descriptions import answer_option_descriptions_controller
from src.features.evaluation_answers import evaluation_answers_controller
from src.features.evaluations import evaluations_controller
from src.features.questionnaires import questionnaires_controller
from src.features.teams import teams_controller
from src.features.answer_options import answer_options_controller
from src.features.seeds import seeds_controller
from src.features.questions import questions_controller
from src.features.auth import auth_controller

app = FastAPI(
    title="Base API",
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

# Seed
if Settings().ENVIRONMENT == "development":
    app.include_router(seeds_controller.router)

# Controllers
app.include_router(auth_controller.router)
app.include_router(users_controller.router)
app.include_router(categories_controller.router)
app.include_router(teams_controller.router)
app.include_router(answer_options_controller.router)
app.include_router(answer_option_descriptions_controller.router)
app.include_router(questionnaires_controller.router)
app.include_router(questions_controller.router)
app.include_router(evaluations_controller.router)
app.include_router(evaluation_answers_controller.router)

# Interceptador de erros de validação de campos
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        message = err["msg"].replace('Value error, ', '')
        formatted_errors.append({
            "field": field,
            "message": message
        })

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"errors": formatted_errors}
    )