# Fast API

**Artigo de apoio / tutorial de gerenciamento de dependências com *poetry***

[Usando o Poetry em seus projetos python](https://medium.com/@volneycasas/usando-o-poetry-em-seus-projetos-python-70be5f018281)

### Passo a Passo com Poetry:

Instalar o Poetry

```bash
    pip install poetry
```

Criando um novo projeto com Poetry. Evitar criar com hífens ou espaços, priorizar o underline (_) caso for necessário.
```bash
    poetry new meu_projeto
```

Adicionando dependências no projeto (bibliotecas), exemplo:

```bash
    poetry add fastapi
```
OBS. Substitua fastapi pela bilioteca que deseja instalar.

Instalando as dependências do projeto:

```bash
    poetry install fastapi
```

Para inicializar o ambiente virtual do poetry:

```bash
    poetry shell
```
OBS. Caso der erro, rode o comando abaixo e rode novamente o *poetry shell*:

```bash
    poetry self add poetry-plugin-shell
```

Para inicializar a aplicação (é necessário estar no mesmo diretório):

```bash
    poetry run uvicorn main:app --reload
```

No caso da estrutura do projeto realizado, é necessário indicar onde está o arquivo main, então colocamos src.main:app (necessário estar no diretório 'fast_api/app'):

```bash
    poetry run uvicorn src.main:app --reload
```

#### Dicas

Para atualizar dependências específicas do projeto:

```bash
    poetry update fastapi
```

### Passo a Passo com Alembic (gerenciador de migrações de bancos de dados)

Instale o alembic com o poetry:

```bash
    poetry add alembic
    poetry install
```

Inicialize o alembic:

```bash
    alembic init <nome-da-pasta>
    alembic init migrations
```

Gerando a migração:
```bash
    alembic revision --autogenerate -m "create users table"
```

Aplicando a migração:
```bash
    alembic upgrade head
```

OBS. Talvez seja necessário ajustar as migrações auto geradas pelo alembic, então sempre verifique se as migrations estão corretas e sem erros de lógica / regra de negócio.

### Docker

Caso seja necessário que API fique dentro de um container e se conectar a um banco que está em outro container do docker, é necessário colocar como string de conexão *host.docker.internal:<porta>* ou apenas *host.docker.internal* e definir a porta posteriormente.

Sempre que for acrescentado uma nova biblioteca, ou mesmo antes de subir a aplicação em um container do Docker, é recomendado validar com:

```bash
    poetry check
    poetry lock
    poetry install
```

Isso ajuda a garantir que o pyproject.toml está correto antes de empacotar no Docker.

Quando tudo certo, subir o container docker com:

```bash
    docker-compose up -d --build
```