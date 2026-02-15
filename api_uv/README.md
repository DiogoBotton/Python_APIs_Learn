## Aprendendo gerenciador de bibliotecas UV

#### Primeiramente instale o `uv` com o comando abaixo (abrir terminal como admin):

```bash
    pip install uv
```

### Para inicializar o `uv` em um projeto, basta digitar:

```bash
    uv init <caminho>
    uv init . # Iniciará o uv na raiz do projeto
```

Será gerado 2 arquivos:

- .python-version (com a versão do python).
- pyproject.toml (dependencias e suas versões).

### Para adicionar/remover uma biblioteca

Para adicionar:

```bash
    uv add nome-biblioteca

    uv add fastapi # Instalação com dependências mínimas do fastApi

    uv add fastapi --extra standard # Instalação mais completa com todo o conjunto de dependências recomendadas para o fastApi
```

Para remover:

```bash
    uv remove <nome-da-biblioteca>
```

A biblioteca será adicionada dentro do arquivo `pyproject.toml`, dentro do array _dependencies_.

### Caso precise sincronizar (baixar) as dependências para seu ambiente

Basta digitar o comando abaixo, no mesmo diretório do projeto, que contém o arquivo `pyproject.toml`.

```bash
    uv sync
```

### Iniciar o projeto

Para iniciar o projeto, seja ele um script de console, por exemplo, digite:

```bash
    uv run <nome-arquivo>
    uv run main.py
```

No caso do FastAPI, digite:

```bash
    uv run fastapi dev # Necessário fastapi[standard]
```

Para rodar em produção, por exemplo, através de um container do docker há uma documentação na documentação do uv [Clicando aqui](https://docs.astral.sh/uv/guides/integration/fastapi/#migrating-an-existing-fastapi-project).
