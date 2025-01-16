package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

// Produto representa um produto com ID, nome e preço
type Produto struct {
	ID    int     `json:"id"`
	Nome  string  `json:"nome"`
	Preco float64 `json:"preco"`
}

// Lista de produtos simulando um banco de dados
var produtos = []Produto{
	{ID: 1, Nome: "Notebook", Preco: 2500},
	{ID: 2, Nome: "Smartphone", Preco: 1500},
}

// Rota para listar produtos
func listarProdutos(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(produtos)
}

// Rota para obter um produto por ID
func obterProduto(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])
	for _, produto := range produtos {
		if produto.ID == id {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(produto)
			return
		}
	}
	http.Error(w, "Produto não encontrado", http.StatusNotFound)
}

func main() {
	// Cria um novo roteador
	r := mux.NewRouter()

	// Define as rotas do serviço
	r.HandleFunc("/produtos", listarProdutos).Methods("GET")
	r.HandleFunc("/produtos/{id}", obterProduto).Methods("GET")

	// Inicializa o serviço
	fmt.Println("Serviço de Produtos rodando em http://localhost:3001")
	log.Fatal(http.ListenAndServe(":3001", r))
}
