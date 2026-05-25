package main

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)


// Função para lidar com conexões WebSocket
func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	log.Println("Handshake recebido")

	// Faz o upgrade da conexão HTTP para WebSocket
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Erro ao fazer upgrade para WebSocket: %v", err)
		return
	}
	defer closeWebSocket(conn)

	log.Println("Conexão WebSocket estabelecida!")

	// Lê e ecoa mensagens
	readAndEchoMessages(conn)
}

// Configuração do WebSocket Upgrader com suporte para permessage-deflate
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true // Permite conexões de qualquer origem
	},
	EnableCompression: true, // Habilita a compressão permessage-deflate
}


// Função para fechar a conexão WebSocket
func closeWebSocket(conn *websocket.Conn) {
	err := conn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
	if err != nil {
		log.Printf("Erro ao enviar mensagem de fechamento: %v", err)
	}
	conn.Close()
	log.Println("Conexão WebSocket encerrada!")
}

// Função para ler e ecoar mensagens
func readAndEchoMessages(conn *websocket.Conn) {
	for {
		// Lê mensagem do cliente
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			log.Printf("Erro ao ler mensagem: %v", err)
			break
		}
		log.Printf("Mensagem recebida do cliente: %s", message)

		message = []byte("Retorno do servidor!")

		// Envia a mensagem de volta para o cliente
		err = conn.WriteMessage(messageType, message)
		if err != nil {
			log.Printf("Erro ao enviar mensagem: %v", err)
			break
		}
		log.Printf("Mensagem enviada de volta para o cliente: %s", message)
	}
}

func main() {
	http.HandleFunc("/ws", handleWebSocket)
	log.Println("Servidor WebSocket seguro (WSS) rodando na porta 8443...")

	// Certificado e chave (substitua pelos seus arquivos de certificado e chave)
	certFile := "server.crt"
	keyFile := "server.key"

	if err := http.ListenAndServeTLS(":8443", certFile, keyFile, nil); err != nil {
		log.Fatalf("Erro ao iniciar o servidor TLS: %v", err)
	}
}
