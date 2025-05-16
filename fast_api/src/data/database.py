import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote

from src.infraestructure.queries import SoftDeleteQuery
from settings import Settings

# USERNAME = os.getenv('DB_USERNAME', 'dbadmin')
# PASSWORD = os.getenv('DB_PASSWORD', 'Wolfros!#$123')
# HOST = os.getenv('DB_HOST', 'localhost')
# PORT = os.getenv('DB_PORT', '5434')
# DB_NAME = os.getenv('DB_NAME', 'widgets_db')

# if USERNAME is None or PASSWORD is None:
#     raise Exception("É necessário definir as variáveis de ambiente 'DB_USERNAME' e 'DB_PASSWORD'")

# PASSWORD = quote(PASSWORD)
# DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

DATABASE_URL = Settings().DATABASE_URL
#print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    query_cls=SoftDeleteQuery))
Base = declarative_base()

# Dependência para adquirir a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()