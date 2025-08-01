import unicodedata
import re

def remove_accents(input_str: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')

def remove_special_characters(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 ]*', '', s)