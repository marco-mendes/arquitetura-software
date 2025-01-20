# HTTP/3 e QUIC com quic-go

Este projeto apresenta uma implementação mínima de um servidor e um cliente HTTP/3 utilizando a biblioteca `quic-go`, que fornece suporte robusto ao protocolo QUIC e HTTP/3 em Go.

---

## O que é HTTP/3 e QUIC?

**HTTP/3** é a próxima geração do protocolo HTTP, baseada no protocolo **QUIC** em vez do tradicional TCP. QUIC oferece comunicação mais rápida e confiável para a web, eliminando algumas das limitações do TCP.

### Principais vantagens do QUIC:

1. **Conexão mais rápida:** QUIC combina a conexão e o handshake TLS em uma única etapa, reduzindo a latência inicial.
2. **Multiplexação sem bloqueio:** Diferentemente do HTTP/2 sobre TCP, o QUIC evita bloqueios de cabeçalho (Head-of-Line Blocking).
3. **Resiliência a perdas de pacotes:** QUIC opera sobre UDP, permitindo maior flexibilidade em condições de rede instáveis.
4. **Melhor desempenho em redes móveis:** QUIC mantém conexões ativas mesmo durante trocas de IP ou mudanças de rede.

---

## Estrutura do Projeto

O projeto está dividido em dois subdiretórios:

1. **Servidor** (`server/main.go`): Implementa um servidor HTTP/3 que responde a requisições na porta 4433.
2. **Cliente** (`client/main.go`): Implementa um cliente que se conecta ao servidor e exibe as respostas recebidas.

### Requisitos

- Go 1.18 ou superior
- Biblioteca `quic-go`
- Certificados TLS (autoassinados ou válidos)

---

## Configuração de Certificados TLS

Antes de executar, é necessário criar um certificado TLS para a comunicação segura:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
```

Coloque os arquivos `server.key` e `server.crt` no diretório `server`.

---

## Código do Servidor

O servidor utiliza `http3.Server` da biblioteca `quic-go` para habilitar HTTP/3.

### Funcionamento:
1. Configuramos um servidor HTTP/3 escutando na porta 4433.
2. A função `handler` é associada ao endpoint `/`.
3. O servidor usa `ListenAndServeTLS` para aceitar conexões QUIC com suporte a HTTP/3.

Localização: `server/main.go`

```go
package main

import (
	"log"
	"net/http"

	"github.com/quic-go/quic-go/http3"
)

func handler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Olá, HTTP/3 com quic-go!"))
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handler)

	server := &http3.Server{
		Addr:    ":4433",
		Handler: mux,
	}

	log.Println("Servidor HTTP/3 rodando em https://localhost:4433")
	if err := server.ListenAndServeTLS("server.crt", "server.key"); err != nil {
		log.Fatal(err)
	}
}
```

---

## Código do Cliente

O cliente usa `http3.RoundTripper` para enviar uma solicitação HTTP/3 ao servidor e processar a resposta.

### Funcionamento:
1. Configuramos o cliente com `http3.RoundTripper`, que gerencia conexões QUIC.
2. Realizamos uma solicitação GET para `https://localhost:4433`.
3. Imprimimos o corpo da resposta.

Localização: `client/main.go`

```go
package main

import (
	"crypto/tls"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/quic-go/quic-go/http3"
)

func main() {
	client := &http.Client{
		Transport: &http3.RoundTripper{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}

	resp, err := client.Get("https://localhost:4433")
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Resposta do servidor: %s\n", body)
}
```

---

## Instruções para Execução

1. **Instale a biblioteca `quic-go`:**
   ```bash
   go get github.com/quic-go/quic-go/http3
   ```

2. **Gere os certificados TLS:**
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
   ```

3. **Execute o servidor:**
   Navegue até o diretório `server` e execute:
   ```bash
   go run main.go
   ```

4. **Execute o cliente:**
   Navegue até o diretório `client` e execute:
   ```bash
   go run main.go
   ```

---

## Resultados Esperados

- O servidor iniciará na porta `4433` e estará pronto para receber conexões HTTP/3.
- O cliente enviará uma solicitação ao servidor e exibirá a mensagem:

  ```
  Resposta do servidor: Olá, HTTP/3 com quic-go!
  ```

---

## Referências

- [Documentação do QUIC](https://www.chromium.org/quic/)
- [quic-go no GitHub](https://github.com/quic-go/quic-go)
- [RFC 9114 - HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)

