# Protocolos de API em Python

Projeto didático para demonstração de diferentes protocolos de API (REST/HTTP2, REST/HTTP3, GraphQL, WebSocket, gRPC) em Python, usando um modelo de domínio simples de Pedidos e Produtos.

Cada protocolo tem sua própria pasta e implementação de servidor e cliente, todos compartilhando o mesmo modelo de domínio.

## Estrutura do Projeto

- `modelo_dominio/`: Modelo de domínio compartilhado
  - `produto.py`: Definição da entidade Produto
  - `pedido.py`: Definição da entidade Pedido
  - `repositorio.py`: Camada de persistência simulada

- `rest_http2/`: Implementação REST sobre HTTP/2
- `rest_http3/`: Implementação REST sobre HTTP/3
- `graphql_api/`: Implementação GraphQL
- `websocket/`: Implementação WebSocket
- `grpc/`: Implementação gRPC

## Protocolos Implementados

| Protocolo | Descrição | RFC/Especificação |
|-----------|-----------|-------------------|
| REST/HTTP2 | API REST sobre HTTP/2 com multiplexação de requisições | [RFC 7540](https://tools.ietf.org/html/rfc7540) |
| REST/HTTP3 | API REST sobre HTTP/3 com QUIC para transporte | [RFC 9114](https://datatracker.ietf.org/doc/html/rfc9114) |
| GraphQL | API com linguagem de consulta flexível e tipagem forte | [Especificação GraphQL](https://spec.graphql.org/) |
| WebSocket | Comunicação bidirecional em tempo real | [RFC 6455](https://tools.ietf.org/html/rfc6455) |
| gRPC | RPC com Protocol Buffers e HTTP/2 | [gRPC Spec](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) |

## Bibliotecas e Frameworks Utilizados

```
Protocolos de API em Python
│
├── REST/HTTP2
│   ├── Servidor: Flask + Hypercorn
│   └── Cliente: requests
│
├── REST/HTTP3
│   ├── Servidor: FastAPI + Hypercorn
│   └── Cliente: httpx (async)
│
├── GraphQL
│   ├── Servidor: Ariadne + Starlette
│   └── Cliente: httpx/requests
│
├── WebSocket
│   ├── Servidor: FastAPI + websockets
│   └── Cliente: websocket-client
│
└── gRPC
    ├── Servidor: grpcio + Protocol Buffers
    └── Cliente: grpcio
```

## Executando os Exemplos

Cada subdiretório contém seu próprio README com instruções específicas para executar o servidor e cliente correspondentes. Todos os comandos devem ser executados a partir da raiz do projeto.

## Requisitos Gerais

- Python 3.8+
- Dependências específicas listadas em cada subdiretório (`requirements.txt`)

## Ambiente Virtual

Recomenda-se criar um ambiente virtual para cada implementação:

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate
