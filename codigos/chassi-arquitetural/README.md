Conjunto de comandos para teste do Chassi Arquitetural

Teste de Saúde (sem autenticação):
```bash
curl http://localhost:8080/saude
```

Requisição válida:
```bash
curl -H "X-API-Key: chave-secreta-123" "http://localhost:8080/ola?nome=Arquiteto"
```

Teste de Rate Limiting (executar 6 vezes):
```bash
for i in {1..6}; do
  curl -H "X-API-Key: chave-secreta-123" "http://localhost:8080/ola?nome=Teste"
done
````

Teste de Circuit Breaker (forçar 4 erros):
```bash
Copy
for i in {1..4}; do
  curl -H "X-API-Key: chave-secreta-123" "http://localhost:8080/ola?nome=Erro&erro=true"
done
````