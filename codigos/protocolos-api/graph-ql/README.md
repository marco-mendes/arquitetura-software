# Tutorial sobre GraphQL com Exemplo em Go

Este documento fornece uma introdução ao GraphQL, um tutorial para configurar e executar um servidor e cliente GraphQL em Go, além de referências adicionais para aprender mais.

---

## O que é GraphQL?

**GraphQL** é uma linguagem de consulta para APIs, bem como um ambiente de execução para atender essas consultas com base em seus dados existentes. Desenvolvido pelo Facebook, o GraphQL permite:

- Consultas flexíveis e precisas, retornando exatamente os dados solicitados.
- Redução de chamadas redundantes à API.
- Uso eficiente em redes com largura de banda limitada.

### Principais Conceitos:

1. **Schema**: Define os tipos de dados disponíveis na API e como eles se relacionam.
2. **Query**: Usada para recuperar dados do servidor.
3. **Mutation**: Usada para modificar dados no servidor.
4. **Resolver**: Uma função responsável por processar as consultas e retornar os dados correspondentes.

---

## Sobre o Exemplo

Neste projeto, criamos:

1. **Servidor GraphQL**: Gera dados fictícios de pedidos e produtos, expostos via uma API GraphQL.
2. **Cliente GraphQL**: Realiza consultas GraphQL ao servidor e demonstra a flexibilidade do GraphQL.

Os dados simulados incluem:

- **Pedidos**: Contêm informações como ID, cliente, data e uma lista de produtos.
- **Produtos**: Contêm informações como ID, nome, descrição e preço.

---

## Configuração e Execução

### Dependências

Certifique-se de ter Go instalado em sua máquina e as seguintes bibliotecas:

```bash
go get github.com/graph-gophers/graphql-go
go get github.com/graph-gophers/graphql-go/relay
```

### Servidor

O servidor GraphQL está no arquivo `main.go` dentro do subdiretório `server`. Ele expõe dois tipos principais (`Pedido` e `Produto`) e uma query para listar todos os pedidos ou obter detalhes de um pedido específico.

**Para executar o servidor:**

1. Navegue até o diretório `server`:
   ```bash
   cd server
   ```

2. Inicie o servidor:
   ```bash
   go run main.go
   ```

O servidor estará disponível em: [http://localhost:8080/graphql](http://localhost:8080/graphql).

### Cliente

O cliente GraphQL está no arquivo `main.go` dentro do subdiretório `client`. Ele envia várias consultas ao servidor, exibindo os resultados no console.

**Para executar o cliente:**

1. Navegue até o diretório `client`:
   ```bash
   cd client
   ```

2. Execute o cliente:
   ```bash
   go run main.go
   ```

O cliente enviará quatro consultas diferentes ao servidor e exibirá as respostas:

1. **Consulta 1**: Todos os pedidos com apenas cliente e data.
2. **Consulta 2**: Detalhes completos de um pedido específico.
3. **Consulta 3**: Todos os produtos de um pedido específico.
4. **Consulta 4**: Todos os pedidos com detalhes completos.

---

## Estrutura do Código

### Servidor

O servidor define dois tipos principais no esquema:

1. **Produto**:
   ```graphql
   type Produto {
       id: ID!
       nome: String!
       descricao: String!
       preco: Float!
   }
   ```

2. **Pedido**:
   ```graphql
   type Pedido {
       id: ID!
       cliente: String!
       data: String!
       produtos: [Produto!]!
   }
   ```

O resolver implementa as funções necessárias para processar as queries do cliente, como:

- `Pedidos()`: Retorna todos os pedidos.
- `Pedido(id: ID!)`: Retorna detalhes de um pedido específico.

### Cliente

O cliente utiliza o pacote `net/http` para enviar consultas ao servidor. Exemplos de consultas incluem:

- **Consulta 1**: Recupera apenas cliente e data de todos os pedidos:
  ```graphql
  {
      pedidos {
          cliente
          data
      }
  }
  ```

- **Consulta 2**: Recupera detalhes completos de um pedido específico:
  ```graphql
  {
      pedido(id: "1") {
          id
          cliente
          data
          produtos {
              id
              nome
              descricao
              preco
          }
      }
  }
  ```

---

## Exemplos de Respostas

1. **Consulta 1**: Todos os pedidos com cliente e data:
   ```json
   {
     "pedidos": [
       { "cliente": "Enzo Cardoso", "data": "2025-01-20" },
       { "cliente": "Sofia Pereira", "data": "2025-01-21" }
     ]
   }
   ```

2. **Consulta 2**: Detalhes completos do pedido 1:
   ```json
   {
     "pedido": {
       "id": "1",
       "cliente": "Enzo Cardoso",
       "data": "2025-01-20",
       "produtos": [
         { "id": "101", "nome": "Caneta", "descricao": "Caneta esferográfica azul", "preco": 1.5 },
         { "id": "102", "nome": "Caderno", "descricao": "Caderno de 100 folhas", "preco": 10.0 }
       ]
     }
   }
   ```

---

## Recursos Adicionais

1. **Documentação Oficial do GraphQL**: [https://graphql.org/](https://graphql.org/)
2. **Biblioteca graphql-go**: [https://github.com/graph-gophers/graphql-go](https://github.com/graph-gophers/graphql-go)
3. **Tutorial Interativo**: [https://www.howtographql.com/](https://www.howtographql.com/)

Este projeto é um ponto de partida para explorar as possibilidades do GraphQL. Experimente criar suas próprias queries e expandir o esquema para atender a novos casos de uso!

