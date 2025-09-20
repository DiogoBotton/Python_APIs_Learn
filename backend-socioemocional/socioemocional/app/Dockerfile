# slim: imagem do python 3.11 mais leve
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem criar virtualenv
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --only main --no-interaction --no-root

# Copia o restante do projeto
COPY . .

# Dá permissão de execução ao script
RUN chmod +x start.sh

# Expondo a porta (apenas boa prática, informativo, pois é definido no docker-compose)
EXPOSE 80

# Executa o script
CMD ["/bin/bash", "start.sh"]