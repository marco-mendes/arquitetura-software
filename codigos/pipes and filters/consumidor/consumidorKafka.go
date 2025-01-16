// Pacote Principal (main):
// O ponto de entrada do programa. Contém a função main que é executada quando o programa é iniciado.

package main

import (
	"fmt"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	fmt.Println("Iniciando consumidor...")

	// Configuração do Consumidor Kafka:
	// Cria uma nova instância de kafka.NewConsumer com as configurações básicas:
	// - bootstrap.servers: Endereço do servidor Kafka ao qual o consumidor se conectará.
	// - group.id: ID do grupo de consumidores. Consumidores no mesmo grupo compartilham a carga de trabalho de consumir mensagens de um tópico.
	// - auto.offset.reset: Política de reset de offset. earliest significa que o consumidor começará a ler mensagens a partir do início do tópico se não houver um offset inicial.
	consumer, _ := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9092",
		"group.id":          "meu-grupo",
		"auto.offset.reset": "earliest",
	})
	defer consumer.Close()

	fmt.Println("Conectado ao Kafka. Inscrevendo-se no tópico...")

	// Inscrição no Tópico:
	// Inscreve o consumidor no tópico (canal) 'entrada' usando o método Subscribe.
	// Isso permite que o consumidor receba mensagens enviadas para esse tópico.
	consumer.Subscribe("entrada", nil)

	fmt.Println("Consumidor Kafka iniciado. Aguardando mensagens...")

	// Loop de Consumo de Mensagens:
	// Um loop infinito que chama consumer.ReadMessage(-1) para ler mensagens do tópico.
	// Quando uma mensagem é recebida, ela é impressa no console.
	for {
		msg, _ := consumer.ReadMessage(-1)
		fmt.Printf("Mensagem recebida: %s\n", string(msg.Value))
	}
}
