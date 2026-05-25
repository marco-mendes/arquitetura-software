# Projeto de WebSocket

Este projeto demonstra a implementação de um servidor WebSocket em Go e um cliente WebSocket em Go. O WebSocket é um protocolo de comunicação bidirecional que permite a comunicação em tempo real entre um cliente e um servidor.

## Protocolo WebSocket

O WebSocket é um protocolo de comunicação que fornece canais de comunicação full-duplex sobre uma única conexão TCP. Ele é projetado para ser implementado em navegadores e servidores da web, mas pode ser usado por qualquer aplicativo cliente/servidor. O WebSocket é iniciado por uma solicitação HTTP de handshake, que é atualizada para uma conexão WebSocket.

### Vantagens do WebSocket

- **Comunicação em tempo real:** Permite a troca de mensagens em tempo real entre o cliente e o servidor.
- **Baixa latência:** Reduz a latência de comunicação em comparação com o polling HTTP.
- **Eficiência:** Usa uma única conexão TCP para comunicação bidirecional, reduzindo a sobrecarga de conexão.

## Estrutura do Projeto

- `server/`: Contém o código do servidor WebSocket.
- `client/`: Contém o código do cliente WebSocket.

### Código do Servidor

O servidor WebSocket é implementado em Go e usa a biblioteca `gorilla/websocket` para gerenciar conexões WebSocket.

### Arquivo: `server/server.go`

```go
package main

import (
    "log"
    "net/http"

    "github.com/gorilla/websocket"
)

// Configuração do WebSocket Upgrader com suporte para permessage-deflate
var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        return true // Permite conexões de qualquer origem
    },
    EnableCompression: true, // Habilita a compressão permessage-deflate
}

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
    log.Println("Servidor WebSocket rodando na porta 8443...")
    if err := http.ListenAndServeTLS(":8443", "server.crt", "server.key", nil); err != nil {
        log.Fatalf("Erro ao iniciar o servidor: %v", err)
    }
}
```
### Código do Cliente

O cliente WebSocket é implementado em Go e também usa a biblioteca gorilla/websocket para gerenciar conexões WebSocket.

Arquivo: client/client.go

```go
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
    err = conn.WriteMessage(websocket.TextMessage, []byte("Olá, servidor WebSocket!"))
    if err != nil {
        log.Fatalf("Erro ao enviar mensagem: %v", err)
    }
    log.Println("Mensagem enviada para o servidor: Olá, servidor WebSocket!")

    // Ler mensagem do servidor
    _, message, err := conn.ReadMessage()
    if err != nil {
        log.Fatalf("Erro ao ler mensagem: %v", err)
    }
    fmt.Printf("Mensagem recebida do servidor: %s\n", message)
}
````

## Como rodar

### Pré-requisitos
Go 1.16 ou superior
Certificado SSL (server.crt) e chave privada (server.key)

### Rodando o Servidor
1. Navegue até o diretório server:
````
cd server
````
2. Execute o servidor
````
go run server.go

````
O servidor WebSocket estará disponível em https://localhost:8443/ws


### Rodando o Cliente
1. Navegue até o diretório client:

````
cd client
````
2. Execute o cliente:
```
go run client.go
````

Saida do Servidor
````
Servidor WebSocket rodando na porta 8443...
Handshake recebido
Conexão WebSocket estabelecida!
Mensagem recebida do cliente: Olá, servidor WebSocket!
Mensagem enviada de volta para o cliente: Retorno do servidor!
Conexão WebSocket encerrada!
````



Saida do cliente
```
Conectando a wss://localhost:8443/ws
Mensagem enviada para o servidor: Olá, servidor WebSocket!
Mensagem recebida do servidor: Retorno do servidor!
Conexão WebSocket encerrada!
```