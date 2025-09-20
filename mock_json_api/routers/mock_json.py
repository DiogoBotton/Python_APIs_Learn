from fastapi import APIRouter, HTTPException, UploadFile, File
import os
import json

main_path = os.path.dirname(__file__)
files_path = os.path.join(main_path, '..', 'files')

router = APIRouter(tags=["Mock Jsons"])

@router.get("/json", summary='Retorna um json específico')
async def get_json(filename: str | None = 'example.json'):
    """
    Retorna o conteúdo de um arquivo JSON específico.
    
    - **filename**: Nome do arquivo JSON a ser retornado. Padrão é 'example.json'.
    """
    file_path = os.path.join(files_path, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)

    return questions

@router.get("/files", summary='Retorna todos os arquivos jsons disponíveis')
async def get_files():
    """
    Retorna uma lista com todos os arquivos JSON disponíveis.
    """
    files = [f for f in os.listdir(files_path)]
    return {"files": files}

@router.post("/upload-file", summary='Faz o upload de um arquivo')
async def upload_file(file: UploadFile = File(...)):
    """
    Faz o upload de um arquivo JSON.
    - **file**: Arquivo JSON a ser enviado.
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .json são permitidos")
    
    file_location = os.path.join(files_path, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
        
    return {"info": f"Arquivo '{file.filename}' salvo em '{file_location}'"}

@router.delete("/files/{filename}", summary='Deleta um arquivo específico')
async def delete_file(filename: str):
    """
    Deleta um arquivo JSON específico.
    - **filename**: Nome do arquivo JSON a ser deletado.
    
    Não é permitido deletar o arquivo padrão 'example.json'.
    """
    file_path = os.path.join(files_path, filename)
    if filename == 'example.json':
        raise HTTPException(status_code=403, detail="Não é permitido deletar o arquivo padrão 'example.json'")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    os.remove(file_path)
    return {"info": f"Arquivo '{filename}' deletado com sucesso"}