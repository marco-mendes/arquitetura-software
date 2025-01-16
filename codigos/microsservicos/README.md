# Projeto de Microsserviços

Este projeto demonstra uma arquitetura de microsserviços simples com três serviços: `products-service`, `orders-service` e um `api-gateway`.

## Estrutura do Projeto

- `products-service`: Serviço responsável por gerenciar produtos.
- `orders-service`: Serviço responsável por gerenciar pedidos.
- `api-gateway`: Gateway que roteia as requisições para os serviços apropriados.

## Pré-requisitos

- Go 1.16 ou superior
- Docker (opcional, para rodar os serviços em containers)

## Como Rodar

### Rodando Localmente

1. Navegue até o diretório do projeto.

2. Inicie o `products-service`:
    ```sh
    cd products-service
    go run main.go
    ```

3. Inicie o `orders-service`:
    ```sh
    cd ../orders-service
    go run main.go
    ```

4. Inicie o `api-gateway`:
    ```sh
    cd ../api-gateway
    go run main.go
    ```


## Endpoints

### Products Service

- `GET /produtos`: Lista todos os produtos.
- `GET /produtos/{id}`: Obtém um produto pelo ID.

### Orders Service

- `GET /pedidos`: Lista todos os pedidos.
- `GET /pedidos/{id}`: Obtém um pedido pelo ID.

### API Gateway

- `GET /produtos`: Proxy para o serviço de produtos.
- `GET /pedidos`: Proxy para o serviço de pedidos.

## Exemplos de Requisições

### Listar Produtos

```sh
curl http://localhost:3000/produtos
```

### Obter Produto por ID

```sh
curl http://localhost:3000/produtos/1
```

### Listar Pedidos

```sh
curl http://localhost:3000/pedidos
```

### Obter Pedido por ID

```sh
curl http://localhost:3000/pedidos/1
```

## Logs

Os logs das requisições e respostas são exibidos no console onde os serviços estão rodando.

