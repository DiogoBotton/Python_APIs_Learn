# Fast API

**Artigo de apoio / tutorial de gerenciamento de dependências com *poetry***

[Usando o Poetry em seus projetos python](https://medium.com/@volneycasas/usando-o-poetry-em-seus-projetos-python-70be5f018281)

### Passo a Passo:

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

#### Dicas

Para atualizar dependências específicas do projeto:

```bash
    poetry update fastapi
```