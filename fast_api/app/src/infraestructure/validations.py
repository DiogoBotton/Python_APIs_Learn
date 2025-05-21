import re
from validate_docbr import CPF, CNPJ

def is_cpf(v):
    return CPF().validate(v)

def is_cnpj(v):
    return CNPJ().validate(v)

def is_valid_email(v):
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(email_regex, v)    