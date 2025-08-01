import re
from validate_docbr import CPF, CNPJ

def is_cpf(v):
    return CPF().validate(v)

def is_cnpj(v):
    return CNPJ().validate(v)

def is_valid_email(v):
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(email_regex, v)

def is_valid_password(password: str) -> bool:
    password_regex = (
        r"^(?=.*[a-z])"       # pelo menos uma letra minúscula
        r"(?=.*[A-Z])"        # pelo menos uma letra maiúscula
        r"(?=.*\d)"           # pelo menos um número
        r"(?=.*[^A-Za-z0-9])" # pelo menos um caractere especial
        r".{6,}$"             # pelo menos 6 caracteres
    )
    return bool(re.match(password_regex, password))