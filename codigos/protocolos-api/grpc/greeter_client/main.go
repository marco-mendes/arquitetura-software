package main

import (
	"context"
	"flag"
	"log"
	"time"

	pb "grpc/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var (
	addr = flag.String("addr", "dns:///localhost:50051", "o endereço do servidor (com prefixo DNS)")
	name = flag.String("name", "mundo", "nome a ser saudado")
)

func main() {
	flag.Parse()

	// Configura uma nova conexão gRPC usando NewClient
	opts := []grpc.DialOption{
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	}

	conn, err := grpc.NewClient(*addr, opts...)
	if err != nil {
		log.Fatalf("não foi possível criar o cliente gRPC: %v", err)
	}
	defer func() {
		if err := conn.Close(); err != nil {
			log.Fatalf("Erro ao fechar a conexão: %v", err)
		}
	}()

	// Cria o cliente a partir da conexão
	client := pb.NewCumprimentadorClient(conn)

	// Configura o contexto para a chamada ao servidor
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// Realiza a chamada ao servidor
	r, err := client.DizerOla(ctx, &pb.SolicitacaoOla{Nome: *name})
	if err != nil {
		log.Fatalf("não foi possível saudar: %v", err)
	}
	log.Printf("Saudação: %s", r.GetMensagem())
}
