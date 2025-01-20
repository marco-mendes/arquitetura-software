package main

import (
	"log"
	"net/http"

	"github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
)

// Estruturas de dados
type Produto struct {
	ID        string
	Nome      string
	Descricao string
	Preco     float64
}

type Pedido struct {
	ID       string
	Cliente  string
	Data     string
	Produtos []Produto
}

// Banco de dados simulado
var pedidos = []Pedido{
	{
		ID:      "1",
		Cliente: "Enzo Cardoso",
		Data:    "2025-01-20",
		Produtos: []Produto{
			{ID: "101", Nome: "Caneta", Descricao: "Caneta esferográfica azul", Preco: 1.5},
			{ID: "102", Nome: "Caderno", Descricao: "Caderno de 100 folhas", Preco: 10.0},
		},
	},
	{
		ID:      "2",
		Cliente: "Sofia Pereira",
		Data:    "2025-01-21",
		Produtos: []Produto{
			{ID: "103", Nome: "Lápis", Descricao: "Lápis preto HB", Preco: 0.5},
		},
	},
}

// Esquema GraphQL
var schema = graphql.MustParseSchema(`
    type Produto {
        id: ID!
        nome: String!
        descricao: String!
        preco: Float!
    }

    type Pedido {
        id: ID!
        cliente: String!
        data: String!
        produtos: [Produto!]!
    }

    type Query {
        pedidos: [Pedido!]!
        pedido(id: ID!): Pedido
    }
`, &resolver{})

// Resolver
type resolver struct{}

func (r *resolver) Pedidos() []*pedidoResolver {
	res := make([]*pedidoResolver, len(pedidos))
	for i, p := range pedidos {
		res[i] = &pedidoResolver{p}
	}
	return res
}

func (r *resolver) Pedido(args struct{ ID graphql.ID }) *pedidoResolver {
	for _, p := range pedidos {
		if p.ID == string(args.ID) {
			return &pedidoResolver{p}
		}
	}
	return nil
}

type pedidoResolver struct {
	pedido Pedido
}

func (r *pedidoResolver) ID() graphql.ID {
	return graphql.ID(r.pedido.ID)
}

func (r *pedidoResolver) Cliente() string {
	return r.pedido.Cliente
}

func (r *pedidoResolver) Data() string {
	return r.pedido.Data
}

func (r *pedidoResolver) Produtos() []*produtoResolver {
	res := make([]*produtoResolver, len(r.pedido.Produtos))
	for i, prod := range r.pedido.Produtos {
		res[i] = &produtoResolver{prod}
	}
	return res
}

type produtoResolver struct {
	produto Produto
}

func (r *produtoResolver) ID() graphql.ID {
	return graphql.ID(r.produto.ID)
}

func (r *produtoResolver) Nome() string {
	return r.produto.Nome
}

func (r *produtoResolver) Descricao() string {
	return r.produto.Descricao
}

func (r *produtoResolver) Preco() float64 {
	return r.produto.Preco
}

func main() {
	http.Handle("/graphql", &relay.Handler{Schema: schema})
	log.Println("Servidor GraphQL rodando em http://localhost:8080/graphql")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
