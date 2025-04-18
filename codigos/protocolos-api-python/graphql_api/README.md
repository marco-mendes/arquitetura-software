# GraphQL API

Implementação didática de API GraphQL usando Ariadne (schema-first) e Starlette.

## Arquitetura do GraphQL

GraphQL é uma linguagem de consulta para APIs e um runtime para executar essas consultas com seus dados existentes. Diferente de REST, GraphQL permite que os clientes solicitem exatamente os dados que precisam, evitando over-fetching e under-fetching de informações.

**Características principais:**
- **Schema-first**: Define um contrato forte entre cliente e servidor
- **Resolvers**: Funções que determinam como os dados são obtidos
- **Single endpoint**: Todas as operações passam por um único endpoint
- **Introspection**: Capacidade de consultar o próprio schema
- **Tipagem forte**: Todos os tipos são explicitamente definidos

**Especificação oficial:** [GraphQL Specification](https://spec.graphql.org/)

## Estrutura do Projeto

- `servidor/`
  - `app.py`: Configuração do servidor ASGI com Ariadne
  - `schema.py`: Definição do schema GraphQL e resolvers
- `cliente/`
  - `cliente.py`: Cliente de exemplo que consome a API GraphQL

## Instruções de Execução

### Instalação de Dependências

```bash
# A partir da raiz do projeto
pip install -r graphql_api/requirements.txt
```

### Executar o Servidor

```bash
# A partir da raiz do projeto
uvicorn graphql_api.servidor.app:app --host 0.0.0.0 --port 9000
```

### Executar o Cliente

```bash
# A partir da raiz do projeto
python -m graphql_api.cliente.cliente
```

## Interface Gráfica

Após iniciar o servidor, você pode acessar a interface gráfica do GraphQL Playground em:
http://localhost:9000

Esta interface permite explorar o schema e testar consultas interativamente.
