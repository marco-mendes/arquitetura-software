package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type graphqlRequest struct {
	Query string `json:"query"`
}

type graphqlResponse struct {
	Data json.RawMessage `json:"data"`
}

func main() {
	// Consulta 1: Todos os pedidos com apenas cliente e data
	query1 := `{
        pedidos {
            cliente
            data
        }
    }`
	executeQuery(query1)

	// Consulta 2: Detalhes completos de um pedido específico
	query2 := `{
        pedido(id: "1") {
            id
            cliente
            data
            produtos {
                id
                nome
                descricao
                preco
            }
        }
    }`
	executeQuery(query2)

	// Consulta 3: Todos os produtos de um pedido específico
	query3 := `{
        pedido(id: "2") {
            produtos {
                id
                nome
                descricao
                preco
            }
        }
    }`
	executeQuery(query3)

	// Consulta 4: Todos os pedidos com detalhes completos
	query4 := `{
        pedidos {
            id
            cliente
            data
            produtos {
                id
                nome
                descricao
                preco
            }
        }
    }`
	executeQuery(query4)
}

func executeQuery(query string) {
	fmt.Println("Executando consulta:")
	fmt.Println(query)
	fmt.Println()

	requestBody, _ := json.Marshal(graphqlRequest{Query: query})
	resp, err := http.Post("http://localhost:8080/graphql", "application/json", 
                            bytes.NewBuffer(requestBody))
	if err != nil {
		log.Fatalf("Erro na requisição: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var gqlResponse graphqlResponse
	err = json.Unmarshal(body, &gqlResponse)
	if err != nil {
		log.Fatalf("Erro ao processar resposta: %v", err)
	}

	fmt.Printf("Resposta: %s\n", gqlResponse.Data)
	fmt.Println()
}
