package main

import (
	"fmt"
)

// Produto representa um produto com nome e preço
type Produto struct {
	Nome  string
	Preco float64
}

// RepositorioProduto define a interface para operações de repositório de produtos
// Esta interface permite a implementação de diferentes repositórios (MySQL, PostgreSQL, etc.)
type RepositorioProduto interface {
	Salvar(produto Produto)
	Listar() []Produto
}

// MySQLRepositorioProduto é uma implementação de RepositorioProduto para MySQL
// Esta estrutura armazena produtos em uma lista simulando um banco de dados MySQL
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
// Esta estrutura armazena produtos em uma lista simulando um banco de dados PostgreSQL
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

// ProdutoServico usa um repositório para gerenciar produtos
// Esta camada de serviço abstrai a lógica de negócios e interage com a camada de repositório
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
	// Configuração do serviço com repositório MySQL
	repositorioMySQL := &MySQLRepositorioProduto{}
	servicoMySQL := &ProdutoServico{repositorio: repositorioMySQL}

	servicoMySQL.AdicionarProduto("Notebook", 5000)
	servicoMySQL.ExibirProdutos()

	// Configuração do serviço com repositório PostgreSQL
	repositorioPostgreSQL := &PostgreSQLRepositorioProduto{}
	servicoPostgreSQL := &ProdutoServico{repositorio: repositorioPostgreSQL}

	servicoPostgreSQL.AdicionarProduto("Smartphone", 3000)
	servicoPostgreSQL.ExibirProdutos()
}
