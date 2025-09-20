import unicodedata
import re

def remove_accents(input_str: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')

def remove_special_characters(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 ]*', '', s)

def get_column_values_by_header(ws, header_name: str):
    headers = [cell.value for cell in ws[1]]
    if header_name not in headers:
        raise ValueError(f"Coluna '{header_name}' não encontrada no Excel.")
    col_index = headers.index(header_name) + 1
    return [row[col_index - 1] for row in ws.iter_rows(min_row=2, values_only=True) if row[col_index - 1]]