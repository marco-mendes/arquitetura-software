Para rodar o Kafka
```sh
docker-compose up
```

Para enviar as mensagens
```sh
go produtor/produtorKafka.go
```

Para consumir as mensagens
```sh
go consumidor/consumidorKafka.go
```
