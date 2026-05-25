# Go Kong API

Este é um projeto mínimo em Go que usa o gateway de API Kong operando em Docker.

## Explicação do Código

### Arquivo `main.go`

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Olá, este é um servidor Go interagindo com o Kong!")
    })

    fmt.Println("Servidor rodando na porta 8080...")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        fmt.Println("Erro ao iniciar o servidor:", err)
    }
}
```

Este código cria um servidor HTTP simples em Go que responde com a mensagem "Olá, este é um servidor Go interagindo com o Kong!" para qualquer requisição na raiz (/). O servidor é configurado para rodar na porta 8080.

Arquivo Dockerfile

```sh
FROM golang:1.18-alpine

WORKDIR /app

COPY . .

RUN go build -o main .

CMD ["./main"]
```
Este Dockerfile define como construir a imagem Docker para o serviço Go. Ele usa a imagem base golang:1.18-alpine, copia o código-fonte para o contêiner, compila o binário Go e define o comando para iniciar o servidor.

Arquivo docker-compose.yml

```sh
version: '3.8'

services:
  kong:
    image: kong:latest
    ports:
      - "8000:8000"
      - "8001:8001"
    environment:
      KONG_DATABASE: "off"
      KONG_PROXY_LISTEN: "0.0.0.0:8000"
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
    networks:
      - kong-net

  go-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    networks:
      - kong-net

networks:
  kong-net:
    driver: bridge
```

Este arquivo docker-compose.yml define dois serviços: kong e go-app. O serviço kong usa a imagem oficial do Kong e expõe as portas 8000 (proxy) e 8001 (admin). O serviço go-app constrói a imagem Docker para o aplicativo Go usando o Dockerfile e expõe a porta 8080. Ambos os serviços estão conectados à mesma rede Docker kong-net.

Como Rodar a Aplicação

Inicie os contêineres com o Docker Compose:

```sh
docker-compose up --build
```
 
Agora, o Kong estará roteando as requisições para o seu serviço Go. Você pode acessar o serviço através do Kong em

```sh
http://localhost:8000/ 
```

