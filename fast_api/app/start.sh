#!/bin/bash
set -e

echo "▶️ Executando migrações Alembic..."
alembic upgrade head

echo "🚀 Iniciando aplicação FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port 80