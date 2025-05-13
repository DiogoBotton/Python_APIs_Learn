import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote

from core.extensions.queries import SoftDeleteQuery

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST', 'db')
PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'widgets_db')

if USERNAME is None or PASSWORD is None:
    raise Exception("É necessário definir as variáveis de ambiente 'DB_USERNAME' e 'DB_PASSWORD'")

PASSWORD = quote(PASSWORD)

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = SessionLocal.query_property(query_cls=SoftDeleteQuery)

# Dependência para adquirir a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        SessionLocal.remove()