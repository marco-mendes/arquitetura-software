package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

// Produto representa um produto com ID e valor
type Produto struct {
	ID    int `json:"id"`
	Valor int `json:"valor"`
}

// Envia mensagens para o Kafka
// Recebe um produtor Kafka, o nome do tópico e uma lista de produtos para enviar.
// Converte cada produto para JSON e envia como mensagem para o Kafka.
func enviarMensagens(producer *kafka.Producer, topic string, mensagens []Produto) {
	for _, mensagem := range mensagens {
		msgBytes, _ := json.Marshal(mensagem)

		producer.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
			Value:          msgBytes,
		}, nil)
		log.Printf("Mensagem enviada: %s para o tópico: %s", string(msgBytes), topic)
	}

	producer.Flush(15 * 1000)
}

func main() {
	produtos := []Produto{
		{ID: 0, Valor: 0},
		{ID: 1, Valor: 10},
		{ID: 2, Valor: 20},
		{ID: 3, Valor: 30},
		{ID: 4, Valor: 40},
	}

	// Configura o produtor Kafka diretamente na função main
	// Cria uma nova instância de kafka.NewProducer com as configurações básicas:
	// - bootstrap.servers: Endereço do servidor Kafka ao qual o produtor se conectará.
	producer, _ := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": "localhost:9092"})
	defer producer.Close()

	// Envia as mensagens para o tópico 'entrada'
	enviarMensagens(producer, "entrada", produtos)
	producer.Flush(15 * 1000)

	fmt.Println("Mensagens enviadas com sucesso.")
}
