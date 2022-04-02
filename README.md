# Inspeções API

## Instalação (Local)

__Requisitos:__

* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

```shell
docker-compose up
```

A aplicação estará disponível em: <http://localhost:8080>

## Documentação da API

Acesse a documentação da API no endpoint <http://localhost:8080/docs>

## DEBUG

Para realizar o debug de uma funcionalidade que está sendo construída, realize os seguintes passos:

1. Inicie os containers da API:

    ```shell
    docker-compose up
    ```

2. Inicie o debug da IDE anexada ao container já em execução (VS Code apenas):

![Debug Demonstration](assets/debug_demonstration.gif)

## Boas Práticas

* Realize a formatação do código segundo o padrão do projeto. Comando:

    ```shell
    make code-formatting
    ```
