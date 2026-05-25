# Tutorial Completo para Projeto gRPC

## O que é RPC e gRPC

### RPC (Remote Procedure Call)
RPC é um protocolo que permite a execução de métodos remotos como se fossem locais. Ele abstrai a comunicação entre cliente e servidor, simplificando a troca de mensagens.

### gRPC
O gRPC é uma implementação moderna e eficiente do RPC criada pela Google. Ele utiliza HTTP/2 para comunicação, permitindo:
- Comunicação bidirecional.
- Streaming de dados.
- Alta performance e suporte a múltiplas linguagens.
- Serialização eficiente com Protobuf (Protocol Buffers).

---

## O que são arquivos Proto

Arquivos `.proto` definem:
1. **Mensagens**: Estruturas de dados usadas na comunicação entre cliente e servidor.
2. **Serviços**: Conjuntos de métodos RPC.

Exemplo de arquivo `.proto`:

```proto
syntax = "proto3";

package helloworld;

service Cumprimentador {
  rpc DizerOla (SolicitacaoOla) returns (RespostaOla);
}

message SolicitacaoOla {
  string nome = 1;
}

message RespostaOla {
  string mensagem = 1;
}
```

---

## Como compilar um arquivo Proto

1. Instale o `protoc`:
   - [Guia de instalação](https://grpc.io/docs/protoc-installation/).

2. Instale o plugin Go para Protobuf:
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

3. Compile o arquivo `.proto`:
```bash
protoc --go_out=. --go-grpc_out=. proto/helloworld.proto
```

Isso gerará os arquivos `helloworld.pb.go` e `helloworld_grpc.pb.go` na pasta `proto`.

---

## Estrutura do Projeto

```plaintext
protocolos-api/
├── grpc/
│   ├── greeter_client/
│   │   └── main.go
│   ├── greeter_server/
│   │   └── main.go
│   ├── proto/
│   │   ├── helloworld.proto
│   │   ├── helloworld.pb.go
│   │   └── helloworld_grpc.pb.go
├── go.mod
├── go.sum
```

---

## Como rodar o servidor e o cliente

### 1. Rodar o servidor

No diretório `greeter_server`, execute:

```bash
go run main.go
```

Saída esperada:
```plaintext
servidor escutando em [::]:50051
```

### 2. Rodar o cliente

No diretório `greeter_client`, execute:

```bash
go run main.go --name="SeuNome"
```

Saída esperada:
```plaintext
Saudação: Olá SeuNome
```

---

## Códigos Explicados

### Servidor (`greeter_server/main.go`)
O servidor implementa o serviço `Cumprimentador` definido no arquivo Proto:

```go
func (s *servidor) DizerOla(_ context.Context, in *pb.SolicitacaoOla) (*pb.RespostaOla, error) {
    log.Printf("Recebido: %v", in.GetNome())
    return &pb.RespostaOla{Mensagem: "Olá " + in.GetNome()}, nil
}
```

### Cliente (`greeter_client/main.go`)
O cliente realiza chamadas ao servidor usando o método `DizerOla`:

```go
r, err := client.DizerOla(ctx, &pb.SolicitacaoOla{Nome: *name})
```

---

## Dependências

1. Instale o módulo Go do gRPC:
```bash
go get google.golang.org/grpc
```

2. Instale o módulo Protobuf para Go:
```bash
go get google.golang.org/protobuf
```

---

## Possíveis Erros e Soluções

### Erro: `protoc: command not found`
Certifique-se de que o compilador `protoc` está instalado e no PATH.

### Erro: `unimplemented error`
Confirme que o método definido no servidor está corretamente registrado no serviço.

### Erro: `dial tcp [::1]:50051: connect: connection refused`
Verifique se o servidor está em execução antes de rodar o cliente.

---


