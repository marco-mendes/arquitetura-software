# Microsserviços com RabbitMQ

Este projeto demonstra a implementação de microsserviços utilizando RabbitMQ para comunicação assíncrona entre serviços.

## Pré-requisitos

- Docker
- Docker Compose
- Go (Golang)

## Configuração do RabbitMQ

Para iniciar o RabbitMQ, utilize o Docker Compose. Certifique-se de estar no diretório onde o arquivo `docker-compose.yml` está localizado e execute o seguinte comando:

```sh
docker-compose up -d
```

Isso iniciará um contêiner RabbitMQ com a interface de gerenciamento disponível em `http://localhost:15672`. As credenciais padrão são `guest` para o usuário e `guest` para a senha.

## Executando os Serviços

### Serviço de Produtos

1. Navegue até o diretório `products-service`:
    ```sh
    cd products-service
    ```

2. Execute o serviço:
    ```sh
    go run main.go
    ```

O serviço de produtos estará disponível em `http://localhost:3001`.

### Serviço de Pedidos

1. Navegue até o diretório `orders-service`:
    ```sh
    cd orders-service
    ```

2. Execute o serviço:
    ```sh
    go run main.go
    ```

O serviço de pedidos estará disponível em `http://localhost:3002`.

## Endpoints

### Serviço de Produtos

- `GET /produtos`: Lista todos os produtos.
- `GET /produtos/{id}`: Obtém um produto específico pelo ID.

### Serviço de Pedidos

- `GET /pedidos`: Lista todos os pedidos.
- `GET /pedidos/{id}`: Obtém um pedido específico pelo ID, incluindo informações do produto associado.

## Comunicação entre Serviços

Os serviços utilizam RabbitMQ para comunicação assíncrona. O serviço de pedidos envia uma mensagem para a fila `produto_queue` para obter informações sobre um produto específico. O serviço de produtos consome essa mensagem, processa a solicitação e envia a resposta de volta para a fila de resposta especificada.

## Parando os Serviços

Para parar os serviços, pressione `Ctrl+C` no terminal onde os serviços estão sendo executados.

Para parar o RabbitMQ, execute:

```sh
docker-compose down
```