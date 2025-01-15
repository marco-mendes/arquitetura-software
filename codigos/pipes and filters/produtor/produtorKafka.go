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

// Configura o produtor Kafka
func configurarProdutor(brokers string) (*kafka.Producer, error) {
	return kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": brokers})
}

// Envia mensagens para o Kafka
func enviarMensagens(producer *kafka.Producer, topic string, mensagens []Produto) error {
	for _, mensagem := range mensagens {
		msgBytes, err := json.Marshal(mensagem)
		if err != nil {
			return err
		}

		err = producer.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
			Value:          msgBytes,
		}, nil)
		if err != nil {
			return err
		}

		// Log da mensagem enviada
		log.Printf("Mensagem enviada: %s para o tópico: %s", string(msgBytes), topic)
	}

	producer.Flush(15 * 1000)
	return nil
}

func main() {
	produtos := []Produto{
		{ID: 0, Valor: 0},
		{ID: 1, Valor: 10},
		{ID: 2, Valor: 20},
		{ID: 3, Valor: 30},
		{ID: 4, Valor: 40},
	}

	producer, err := configurarProdutor("localhost:9092")
	if err != nil {
		log.Fatalf("Erro ao configurar produtor: %v", err)
	}
	defer producer.Close()

	if err := enviarMensagens(producer, "entrada", produtos); err != nil {
		log.Fatalf("Erro ao enviar mensagens: %v", err)
	}
	producer.Flush(15 * 1000)

	fmt.Println("Mensagens enviadas com sucesso.")
}
