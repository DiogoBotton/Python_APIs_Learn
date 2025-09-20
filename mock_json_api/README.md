## Subindo Container Docker de API no fly.io

Primeiramente instale o CLI do fly e crie uma conta no [fly.io](https://fly.io):

[Flyctl Download](https://fly.io/docs/flyctl/install/)

Será necessário colocar um cartão de crédito para fins de verificação, porém, se o uso ultrapassar US$ 5.00 (5 dólares) você será cobrado.

Crie o container docker (arquivo Dockerfile) e digite o comando:

```bash
    fly launch
```

## Subindo Container Docker de API no render.com

Faça o registro no [render.com](https://render.com/).

Não é necessário colocar um cartão de crédito.

Crie um projeto web (Web Services) e faça o vinculo com sua conta do GitHub.

Selecione uma tecnologia, no nosso caso, selecione Docker, pois configuramos um arquivo Dockerfile para subir a aplicação, porém, o Render é compatível com Python 3 e outras tecnologias. Caso não queira utilizar Docker, verifique se a tecnologia que você está desenvolvendo é compatível com o Render.

Em resumo, este processo fará o fluxo de CI/CD (Continuos Integration / Continuos Deployment - Integração Contínua / Implantação Contínua). Em outras palavras, sempre quando houver alterações na branch que você selecionar (por exemplo, branch `main`) haverá um pipeline (processo) que implantará seu novo código na nuvem do *Render* automaticamente.