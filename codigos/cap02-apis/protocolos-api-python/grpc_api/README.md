# gRPC

Implementação didática de API gRPC usando grpcio e grpcio-tools.

## Arquitetura gRPC

gRPC é um framework de RPC (Remote Procedure Call) desenvolvido pelo Google, de alto desempenho e código aberto. Utiliza Protocol Buffers como linguagem de definição de interface (IDL) e HTTP/2 como protocolo de transporte.

**Características principais:**
- **Protocol Buffers**: Mecanismo eficiente de serialização binária, mais compacto que JSON ou XML
- **HTTP/2**: Aproveita recursos como multiplexação, compressão de cabeçalhos e streams bidirecionais
- **Fortemente tipado**: Contratos de API claros e validação automática
- **Suporte a múltiplas linguagens**: Geração automática de código cliente/servidor em várias linguagens
- **Streaming bidirecional**: Suporte a streams de requisição e resposta
- **Interceptores**: Para autenticação, logging, monitoramento, etc.

**Especificação oficial:** [gRPC Specification](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md)

## Estrutura do Projeto

- `protos/`
  - `produto.proto`: Definição dos serviços e mensagens para produtos
  - `pedido.proto`: Definição dos serviços e mensagens para pedidos
- `servidor/`
  - `app.py`: Implementação do servidor gRPC
- `cliente/`
  - `cliente.py`: Cliente de exemplo que consome a API gRPC

## Instruções de Execução

### Requisitos Especiais para gRPC

gRPC contém componentes nativos em C++ que precisam ser compilados. **Importante:** gRPC não é compatível com PyPy. Utilize obrigatoriamente o CPython para este exemplo.

#### Ambiente virtual com CPython (recomendado)

```bash
python3 -m venv .venv_cpython
source .venv_cpython/bin/activate  # Linux/macOS
# .venv_cpython\Scripts\activate  # Windows
pip install --upgrade pip setuptools wheel
pip install -r grpc_api/requirements.txt
```

- O arquivo `grpc_api/requirements.txt` deve conter:
  ```
  grpcio==1.62.2
  grpcio-tools==1.62.2
  protobuf>=4.21.6,<5.0dev
  ```
- Não utilize PyPy para rodar o gRPC, pois não há suporte oficial.

#### Solução de Problemas
- Certifique-se de ter as Command Line Tools do Xcode instaladas:
  ```bash
  xcode-select --install
  ```
- Se ocorrerem erros de compilação, tente atualizar o Xcode completo ou use uma versão mais antiga do Python (3.11 ou 3.10).
- Caso tenha usado PyPy antes, crie um novo ambiente virtual com CPython e repita os passos acima.

### Gerar Código a partir dos Arquivos .proto

```bash
# A partir da raiz do projeto
python -m grpc_tools.protoc -I grpc_api/protos --python_out=grpc_api/protos --grpc_python_out=grpc_api/protos grpc_api/protos/produto.proto grpc_api/protos/pedido.proto
```

### Executar o Servidor

```bash
# A partir da raiz do projeto
python -m grpc_api.servidor.app
```

### Executar o Cliente

```bash
# A partir da raiz do projeto
python -m grpc_api.cliente.cliente
```

## Vantagens do gRPC

- Desempenho superior em comparação com REST/JSON para comunicação entre serviços
- Geração automática de código cliente/servidor
- Suporte nativo a streaming
- Ideal para microsserviços e sistemas distribuídos de baixa latência

## Observação para Fins Didáticos

Para fins puramente didáticos, você pode estudar o código e a estrutura do projeto sem necessariamente executá-lo. Os outros protocolos implementados neste repositório (REST/HTTP2, REST/HTTP3, GraphQL, WebSocket) são mais fáceis de configurar e podem ser suficientes para entender os conceitos de APIs.
