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

Removendo uma dependência do projeto:

```bash
    poetry remove fastapi
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

As vezes quando a API não é usada por algum tempo, as bibliotecas precisam ser instaladas novamente. Basta rodar os comandos *poetry shell* e *poetry install*.

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

OBS 1. Talvez seja necessário ajustar as migrações auto geradas pelo alembic, então sempre verifique se as migrations estão corretas e sem erros de lógica / regra de negócio.
OBS 2. **Antes de aplicar a migração é necessário que o banco esteja criado no banco de dados (apenas o banco, não as tabelas)**.

### Docker

Caso seja necessário que API fique dentro de um container e se conectar a um banco que está em outro container do docker, é necessário colocar como string de conexão *host.docker.internal:<porta>* ou apenas *host.docker.internal* e definir a porta posteriormente.

Sempre que for acrescentado uma nova biblioteca, ou mesmo antes de subir a aplicação em um container do Docker, é recomendado validar com:

```bash
    poetry check
    poetry lock
    poetry install
```

Ou tente refazer o ambiente virtual, removendo todos os ambientes criados

```bash
    poetry env remove --all
    poetry env remove <nome_do_ambiente>
```

Isso ajuda a garantir que o pyproject.toml está correto antes de empacotar no Docker.

Quando tudo certo, subir o container docker com:

```bash
    docker-compose up -d --build
```

## Como criar as models com este padrão de API

Dentro da *app/src/domains* deverá ser criado todos os domínios de banco de dados, enums e abstrações necessárias.

Todas as classes devem herdar da classe pai *DomainBase*. Esta classe contem os atributos padrões que todas as entidades devem ter, sendo elas:

- id: Utiliza o algoritmo uuid7 para gerar os ids (primary keys);
- created_at: Data de criação do registro;
- updated_at: Data de atualização do registro;
- deleted_at: Data de exclusão do registro (soft delete).

Ao criar uma model é necessário importa-la no arquivo *app/src/domains/__init__.py* da seguinte forma:

```py
    # Necessário realizar a importação de todas as classes aqui
    from .user import User
```

Isto é necessário para que a geração e aplicação das migrações do banco de dados com o *alembic* funcione corretamente. O arquivo *app/migrations/env.py* precisa do contexto das models que serão criadas, para isso, é necessária a importação das classes.
Nesse mesmo arquivo é possível observar a seguinte importação na linha 9:

```py
    # Necessário realizar a importação da src.domains para ter os metadados das classes
    import src.domains
```