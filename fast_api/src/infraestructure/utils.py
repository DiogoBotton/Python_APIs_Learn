import unicodedata

def remove_accents(input_str: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')