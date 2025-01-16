package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

// Pedido representa um pedido com ID, ID do produto e quantidade
type Pedido struct {
	ID         int `json:"id"`
	ProdutoID  int `json:"produtoId"`
	Quantidade int `json:"quantidade"`
}

// Lista de pedidos simulando um banco de dados
var pedidos = []Pedido{
	{ID: 1, ProdutoID: 1, Quantidade: 2},
	{ID: 2, ProdutoID: 2, Quantidade: 1},
}

// Rota para listar pedidos
func listarPedidos(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(pedidos)
}

// Rota para obter um pedido por ID
func obterPedido(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id, _ := strconv.Atoi(params["id"])
	for _, pedido := range pedidos {
		if pedido.ID == id {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(pedido)
			return
		}
	}
	http.Error(w, "Pedido não encontrado", http.StatusNotFound)
}

func main() {
	// Cria um novo roteador
	r := mux.NewRouter()

	// Define as rotas do serviço
	r.HandleFunc("/pedidos", listarPedidos).Methods("GET")
	r.HandleFunc("/pedidos/{id}", obterPedido).Methods("GET")

	// Inicializa o serviço
	fmt.Println("Serviço de Pedidos rodando em http://localhost:3002")
	log.Fatal(http.ListenAndServe(":3002", r))
}
