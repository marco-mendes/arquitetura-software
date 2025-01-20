// gere um tutorial completo aqui

// Pacote main implementa um servidor para o serviço Cumprimentador.
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	pb "grpc/proto"

	"google.golang.org/grpc"
)

var (
	porta = flag.Int("porta", 50051, "A porta do servidor")
)

// servidor é usado para implementar helloworld.CumprimentadorServer.
type servidor struct {
	pb.UnimplementedCumprimentadorServer
}

// DizerOla implementa helloworld.CumprimentadorServer
func (s *servidor) DizerOla(_ context.Context, in *pb.SolicitacaoOla) (*pb.RespostaOla, error) {
	log.Printf("Recebido: %v", in.GetNome())
	return &pb.RespostaOla{Mensagem: "Olá " + in.GetNome()}, nil
}

func main() {
	flag.Parse()
	// Cria um listener na porta especificada
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *porta))
	if err != nil {
		log.Fatalf("falha ao escutar: %v", err)
	}
	// Cria uma nova instância do servidor gRPC
	s := grpc.NewServer()
	// Registra o servidor Cumprimentador no servidor gRPC
	pb.RegisterCumprimentadorServer(s, &servidor{})
	log.Printf("servidor escutando em %v", lis.Addr())
	// Inicia o servidor gRPC para aceitar conexões
	if err := s.Serve(lis); err != nil {
		log.Fatalf("falha ao servir: %v", err)
	}
}
