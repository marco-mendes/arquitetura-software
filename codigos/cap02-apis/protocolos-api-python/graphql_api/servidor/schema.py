from ariadne import QueryType, MutationType, make_executable_schema, gql, ObjectType
from modelo_dominio.produto import Produto
from modelo_dominio.pedido import Pedido
from modelo_dominio.repositorio import RepositorioProduto, RepositorioPedido

# Schema GraphQL
schema_str = gql('''
type Produto {
  codigo: String!
  nome: String!
  preco: Float!
}

type Pedido {
  codigo: String!
  data: String!
  preco_total: Float!
  produtos: [Produto!]!
}

type Query {
  produtos: [Produto!]!
  produto(codigo: String!): Produto
  pedidos: [Pedido!]!
  pedido(codigo: String!): Pedido
}

input ProdutoInput {
  nome: String!
  preco: Float!
}

input PedidoInput {
  produtos: [String!]!
}

type Mutation {
  criarProduto(input: ProdutoInput!): Produto
  criarPedido(input: PedidoInput!): Pedido
}
''')

# Repositórios compartilhados
repo_produtos = RepositorioProduto()
repo_pedidos = RepositorioPedido()

# Dados iniciais para facilitar testes
def seed():
    p1 = Produto(nome="Notebook", preco=3500.0)
    p2 = Produto(nome="Smartphone", preco=2000.0)
    repo_produtos.adicionar(p1)
    repo_produtos.adicionar(p2)
    ped = Pedido()
    ped.adicionar_produto(p1)
    repo_pedidos.adicionar(ped)
seed()

query = QueryType()
mutation = MutationType()
pedido_obj = ObjectType("Pedido")

@query.field("produtos")
def resolve_produtos(*_):
    return repo_produtos.listar_todos()

@query.field("produto")
def resolve_produto(*_, codigo):
    return repo_produtos.obter_por_id(codigo)

@query.field("pedidos")
def resolve_pedidos(*_):
    return repo_pedidos.listar_todos()

@query.field("pedido")
def resolve_pedido(*_, codigo):
    return repo_pedidos.obter_por_id(codigo)

@mutation.field("criarProduto")
def resolve_criar_produto(*_, input):
    novo = Produto(nome=input["nome"], preco=input["preco"])
    repo_produtos.adicionar(novo)
    return novo

@mutation.field("criarPedido")
def resolve_criar_pedido(*_, input):
    ped = Pedido()
    for cod in input.get("produtos", []):
        prod = repo_produtos.obter_por_id(cod)
        if prod:
            ped.adicionar_produto(prod)
    repo_pedidos.adicionar(ped)
    return ped

@pedido_obj.field("produtos")
def resolve_pedido_produtos(obj, *_):
    return obj.produtos

schema = make_executable_schema(schema_str, [query, mutation, pedido_obj])
