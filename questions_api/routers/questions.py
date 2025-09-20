from fastapi import APIRouter
import os
import json

main_path = os.path.dirname(__file__)
questions_path = os.path.join(main_path, '..', 'questions.json')

router = APIRouter(tags=["Questions"])

@router.post("/get-questions", summary='Retorna todas as questões')
async def get_questions():
    with open(questions_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)

    return questions