from fastapi import HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from src.data.database import get_db
from pydantic import BaseModel
from src.domains.enums.import_users_cells import ImportUsersCells
from io import BytesIO
import openpyxl
from . import BaseHandler

# Request
class Command(BaseModel):
    pass

# Handle
class DownloadTemplate(BaseHandler[Command, StreamingResponse]):
    def __init__(self):
        pass
    
    async def execute(self, request: Command):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Usuários"

        # Cabeçalhos
        ws.append([cell.value for cell in ImportUsersCells])

        # Gera arquivo em memória
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)

        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=import_users_template.xlsx"}
        )