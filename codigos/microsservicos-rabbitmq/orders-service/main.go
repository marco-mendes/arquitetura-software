package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"sync"

	"github.com/gorilla/mux"
	"github.com/rabbitmq/amqp091-go"
)

// Pedido representa um pedido com ID, ID do produto e quantidade
type Pedido struct {
	ID         int `json:"id"`
	ProdutoID  int `json:"produtoId"`
	Quantidade int `json:"quantidade"`
}

// Produto representa um produto
type Produto struct {
	ID    int     `json:"id"`
	Nome  string  `json:"nome"`
	Preco float64 `json:"preco"`
}

// PedidoComProduto representa um pedido completo com informações do produto
type PedidoComProduto struct {
	Pedido
	Produto Produto `json:"produto"`
}

var (
	listaPedidos    = []Pedido{{ID: 1, ProdutoID: 1, Quantidade: 2}, {ID: 2, ProdutoID: 2, Quantidade: 1}}
	mapaRespostas   sync.Map
	canalRabbitMQ   *amqp091.Channel
	filaResposta    amqp091.Queue
	conexaoRabbitMQ *amqp091.Connection
)

func obterProduto(produtoID int) (Produto, error) {
	idCorrelacao := strconv.Itoa(rand.Int())
	corpoMensagem := []byte(strconv.Itoa(produtoID))

	// Envia mensagem para a fila de produtos
	err := canalRabbitMQ.Publish(
		"",
		"produto_queue",
		false,
		false,
		amqp091.Publishing{
			ContentType:   "application/json",
			CorrelationId: idCorrelacao,
			ReplyTo:       filaResposta.Name,
			Body:          corpoMensagem,
		},
	)
	if err != nil {
		return Produto{}, fmt.Errorf("erro ao enviar mensagem: %v", err)
	}

	// Aguarda a resposta
	canalResposta := make(chan Produto)
	mapaRespostas.Store(idCorrelacao, canalResposta)
	defer mapaRespostas.Delete(idCorrelacao)

	produto := <-canalResposta
	return produto, nil
}

func consumirRespostas() {
	msgs, _ := canalRabbitMQ.Consume(
		filaResposta.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)

	go func() {
		for msg := range msgs {
			if canalResposta, ok := mapaRespostas.Load(msg.CorrelationId); ok {
				var produto Produto
				json.Unmarshal(msg.Body, &produto)
				canalResposta.(chan Produto) <- produto
			}
		}
	}()
}

func listarPedidos(w http.ResponseWriter, r *http.Request) {
	var pedidosComProdutos []PedidoComProduto

	for _, pedido := range listaPedidos {
		produto, err := obterProduto(pedido.ProdutoID)
		if err != nil {
			http.Error(w, "Erro ao obter produto", http.StatusInternalServerError)
			return
		}

		pedidosComProdutos = append(pedidosComProdutos, PedidoComProduto{
			Pedido:  pedido,
			Produto: produto,
		})
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(pedidosComProdutos)
}

func main() {
	// Conecta ao RabbitMQ
	var err error
	conexaoRabbitMQ, err = amqp091.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		log.Fatalf("Erro ao conectar ao RabbitMQ: %v", err)
	}
	defer conexaoRabbitMQ.Close()

	canalRabbitMQ, err = conexaoRabbitMQ.Channel()
	if err != nil {
		log.Fatalf("Erro ao abrir canal: %v", err)
	}
	defer canalRabbitMQ.Close()

	// Declara fila de respostas
	filaResposta, err = canalRabbitMQ.QueueDeclare(
		"",
		false,
		true,
		true,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Erro ao declarar fila de respostas: %v", err)
	}

	// Inicia consumo das respostas
	consumirRespostas()

	// Roteador HTTP
	r := mux.NewRouter()
	r.HandleFunc("/pedidos", listarPedidos).Methods("GET")

	fmt.Println("Serviço de Pedidos rodando em http://localhost:3002")
	log.Fatal(http.ListenAndServe(":3002", r))
}
