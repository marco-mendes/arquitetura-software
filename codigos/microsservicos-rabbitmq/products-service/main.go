package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/rabbitmq/amqp091-go"
)

// Produto representa um produto com ID, nome e preço
type Produto struct {
	ID    int     `json:"id"`
	Nome  string  `json:"nome"`
	Preco float64 `json:"preco"`
}

// Lista de produtos simulando um banco de dados
var listaProdutos = []Produto{
	{ID: 1, Nome: "Notebook", Preco: 2500},
	{ID: 2, Nome: "Smartphone", Preco: 1500},
}

// Rota para listar todos os produtos (via HTTP)
func listarProdutos(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(listaProdutos)
}

// Rota para obter um produto por ID (via HTTP)
func obterProduto(w http.ResponseWriter, r *http.Request) {
	parametros := mux.Vars(r)
	produtoID, _ := strconv.Atoi(parametros["id"])
	for _, produto := range listaProdutos {
		if produto.ID == produtoID {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(produto)
			return
		}
	}
	http.Error(w, "Produto não encontrado", http.StatusNotFound)
}

// Função para consumir mensagens da fila RabbitMQ
func consumirMensagens(canal *amqp091.Channel, nomeFila string, handler func(*amqp091.Channel, amqp091.Delivery)) {
	mensagens, err := canal.Consume(
		nomeFila,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Erro ao iniciar consumo: %v", err)
	}

	go func() {
		for mensagem := range mensagens {
			handler(canal, mensagem)
		}
	}()
}

// Handler para processar requisições de produtos via RabbitMQ
func handleProdutoRequest(canal *amqp091.Channel, mensagem amqp091.Delivery) {
	var produtoID int
	json.Unmarshal(mensagem.Body, &produtoID)
	for _, produto := range listaProdutos {
		if produto.ID == produtoID {
			resposta, _ := json.Marshal(produto)
			// Publica a resposta na fila de retorno
			canal.Publish(
				"",
				mensagem.ReplyTo,
				false,
				false,
				amqp091.Publishing{
					ContentType:   "application/json",
					CorrelationId: mensagem.CorrelationId,
					Body:          resposta,
				},
			)
			return
		}
	}
}

func main() {
	// Conexão com RabbitMQ
	conn, err := amqp091.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		log.Fatalf("Erro ao conectar ao RabbitMQ: %v", err)
	}
	defer conn.Close()

	canal, err := conn.Channel()
	if err != nil {
		log.Fatalf("Erro ao abrir o canal: %v", err)
	}
	defer canal.Close()

	// Declaração da fila
	fila, err := canal.QueueDeclare(
		"produto_queue",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Erro ao declarar a fila: %v", err)
	}

	// Consumo de mensagens da fila
	go consumirMensagens(canal, fila.Name, handleProdutoRequest)

	// Configuração do roteador HTTP
	roteador := mux.NewRouter()
	roteador.HandleFunc("/produtos", listarProdutos).Methods("GET")
	roteador.HandleFunc("/produtos/{id}", obterProduto).Methods("GET")

	// Inicialização do serviço
	fmt.Println("Serviço de Produtos rodando em http://localhost:3001")
	log.Fatal(http.ListenAndServe(":3001", roteador))
}
