from enum import Enum

class ImportUsersCells(str, Enum):
    Nome = "Nome"
    Email = "Email"
    CPF = "CPF"
    Cargo = "Cargo"
    Equipe = "Equipe"
    GerenteEquipe = "Gerente da Equipe"