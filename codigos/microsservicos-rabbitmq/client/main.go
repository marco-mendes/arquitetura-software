package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

// Produto representa um produto com ID, nome e preço
type Produto struct {
	ID    int     `json:"id"`
	Nome  string  `json:"nome"`
	Preco float64 `json:"preco"`
}

// Pedido representa um pedido com ID, ID do produto e quantidade
type Pedido struct {
	ID         int `json:"id"`
	ProdutoID  int `json:"produtoId"`
	Quantidade int `json:"quantidade"`
}

// fetchData faz uma requisição HTTP GET e retorna o corpo da resposta
func fetchData(url string) ([]byte, error) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, fmt.Errorf("erro ao fazer requisição: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("erro: status code %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("erro ao ler resposta: %w", err)
	}

	return body, nil
}

// printProdutos faz a requisição e imprime os produtos
func printProdutos() {
	body, err := fetchData("http://localhost:3000/produtos")
	if err != nil {
		log.Fatalf("Erro ao obter produtos: %s", err)
	}

	var produtos []Produto
	if err := json.Unmarshal(body, &produtos); err != nil {
		log.Fatalf("Erro ao desserializar produtos: %s", err)
	}

	fmt.Println("Produtos:")
	for _, produto := range produtos {
		fmt.Printf("ID: %d, Nome: %s, Preço: %.2f\n", produto.ID, produto.Nome, produto.Preco)
	}
}

// printPedidos faz a requisição e imprime os pedidos
func printPedidos() {
	body, err := fetchData("http://localhost:3000/pedidos")
	if err != nil {
		log.Fatalf("Erro ao obter pedidos: %s", err)
	}

	var pedidos []Pedido
	if err := json.Unmarshal(body, &pedidos); err != nil {
		log.Fatalf("Erro ao desserializar pedidos: %s", err)
	}

	fmt.Println("Pedidos:")
	for _, pedido := range pedidos {
		fmt.Printf("ID: %d, ProdutoID: %d, Quantidade: %d\n", pedido.ID, pedido.ProdutoID, pedido.Quantidade)
	}
}

func main() {
	printProdutos()
	printPedidos()
}
