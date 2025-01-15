package main

import (
	"fmt"
)

// Produto representa um produto com nome e preço
type Produto struct {
	Nome  string
	Preco float64
}

// Repositorio Produto define a interface para operações de repositório de produtos
type RepositorioProduto interface {
	Salvar(produto Produto)
	Listar() []Produto
}

// MySQLRepositorioProduto é uma implementação de RepositorioProduto para MySQL
type MySQLRepositorioProduto struct {
	produtos []Produto
}

func (r *MySQLRepositorioProduto) Salvar(produto Produto) {
	r.produtos = append(r.produtos, produto)
	fmt.Println("Produto salvo no MySQL.")
}

func (r *MySQLRepositorioProduto) Listar() []Produto {
	fmt.Println("Listando produtos do MySQL.")
	return r.produtos
}

// PostgreSQLRepositorioProduto é uma implementação de RepositorioProduto para PostgreSQL
type PostgreSQLRepositorioProduto struct {
	produtos []Produto
}

func (r *PostgreSQLRepositorioProduto) Salvar(produto Produto) {
	r.produtos = append(r.produtos, produto)
	fmt.Println("Produto salvo no PostgreSQL.")
}

func (r *PostgreSQLRepositorioProduto) Listar() []Produto {
	fmt.Println("Listando produtos do PostgreSQL.")
	return r.produtos
}

// Produto Servico usa um repositório para gerenciar produtos
type ProdutoServico struct {
	repositorio RepositorioProduto
}

func (s *ProdutoServico) AdicionarProduto(nome string, preco float64) {
	produto := Produto{Nome: nome, Preco: preco}
	s.repositorio.Salvar(produto)
}

func (s *ProdutoServico) ExibirProdutos() {
	produtos := s.repositorio.Listar()
	for _, produto := range produtos {
		fmt.Printf("Produto: %s, Preço: R$%.2f\n", produto.Nome, produto.Preco)
	}
}

func main() {
	repositorioMySQL := &MySQLRepositorioProduto{}
	servicoMySQL := &ProdutoServico{repositorio: repositorioMySQL}

	servicoMySQL.AdicionarProduto("Notebook", 5000)
	servicoMySQL.ExibirProdutos()

	repositorioPostgreSQL := &PostgreSQLRepositorioProduto{}
	servicoPostgreSQL := &ProdutoServico{repositorio: repositorioPostgreSQL}

	servicoPostgreSQL.AdicionarProduto("Smartphone", 3000)
	servicoPostgreSQL.ExibirProdutos()
}
