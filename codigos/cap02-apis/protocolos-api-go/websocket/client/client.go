package main

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/url"

	"github.com/gorilla/websocket"
)

func main() {
	u := url.URL{Scheme: "wss", Host: "localhost:8443", Path: "/ws"}
	fmt.Printf("Conectando a %s\n", u.String())

	dialer := websocket.Dialer{
		TLSClientConfig:   &tls.Config{InsecureSkipVerify: true},
		EnableCompression: true, // Habilita a compressão permessage-deflate
	}

	conn, _, err := dialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatalf("Erro ao conectar ao WebSocket: %v", err)
	}
	defer func() {
		err := conn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
		if err != nil {
			log.Printf("Erro ao enviar mensagem de fechamento: %v", err)
		}
		conn.Close()
		log.Println("Conexão WebSocket encerrada!")
	}()

	// Enviar mensagem para o servidor
	mensagem := "Ola, servidor WebSocket!"
	err = conn.WriteMessage(websocket.TextMessage, []byte(mensagem))
	if err != nil {
		log.Fatalf("Erro ao enviar mensagem: %v", err)
	}
	log.Println("Mensagem enviada para o servidor:   " + mensagem)

	// Ler mensagem do servidor
	_, message, err := conn.ReadMessage()
	if err != nil {
		log.Fatalf("Erro ao ler mensagem: %v", err)
	}
	fmt.Printf("Mensagem recebida do servidor: %s\n", message)

}
