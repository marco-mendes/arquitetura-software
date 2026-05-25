package main

import (
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

// Configuração dos serviços
var (
	productsService = "http://localhost:3001"
	ordersService   = "http://localhost:3002"
)

// Cria um proxy reverso para um serviço específico
func createReverseProxy(target string) *httputil.ReverseProxy {
	url, _ := url.Parse(target)
	return httputil.NewSingleHostReverseProxy(url)
}

func logRequestAndResponse(proxy *httputil.ReverseProxy) {
	originalDirector := proxy.Director
	proxy.Director = func(req *http.Request) {
		originalDirector(req)
		log.Printf("Proxying request: %s %s", req.Method, req.URL.String())
	}

	proxy.ModifyResponse = func(resp *http.Response) error {
		log.Printf("Received response: %s %s - Status: %d", resp.Request.Method, resp.Request.URL.String(), resp.StatusCode)
		return nil
	}
}

func main() {
	// Proxy para o serviço de produtos
	http.HandleFunc("/produtos", func(w http.ResponseWriter, r *http.Request) {
		proxy := createReverseProxy(productsService)
		logRequestAndResponse(proxy)
		proxy.ServeHTTP(w, r)
	})

	// Proxy para o serviço de pedidos
	http.HandleFunc("/pedidos", func(w http.ResponseWriter, r *http.Request) {
		proxy := createReverseProxy(ordersService)
		logRequestAndResponse(proxy)
		proxy.ServeHTTP(w, r)
	})

	// Inicialização do servidor do API Gateway
	fmt.Println("API Gateway rodando em http://localhost:3000")
	log.Fatal(http.ListenAndServe(":3000", nil))
}
