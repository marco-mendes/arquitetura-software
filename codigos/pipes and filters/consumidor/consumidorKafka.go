package main

import (
	"fmt"
	"log"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	fmt.Println("Iniciando consumidor...")

	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "meu-grupo",
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		log.Fatalf("Erro ao configurar consumidor: %v", err)
	}
	defer consumer.Close()

	fmt.Println("Conectado ao Kafka. Inscrevendo-se no tópico...")
	err = consumer.Subscribe("entrada", nil)
	if err != nil {
		log.Fatalf("Erro ao se inscrever no tópico: %v", err)
	}

	fmt.Println("Consumidor Kafka iniciado. Aguardando mensagens...")

	for {
		msg, err := consumer.ReadMessage(-1)
		if err == nil {
			fmt.Printf("Mensagem recebida: %s\n", string(msg.Value))
		} else {
			fmt.Printf("Erro ao consumir mensagem: %v\n", err)
		}
	}
}
