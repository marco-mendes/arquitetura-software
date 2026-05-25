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
		Addr:    ":4433", // Porta do servidor
		Handler: mux,
	}

	log.Println("Servidor HTTP/3 rodando em https://localhost:4433")
	err := server.ListenAndServeTLS("server.crt", "server.key")
	if err != nil {
		log.Fatal(err)
	}
}
