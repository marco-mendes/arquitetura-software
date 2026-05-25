# REST sobre HTTP/2

Implementação didática de API REST usando HTTP/2 (Flask + Hypercorn).

## Arquitetura HTTP/2

HTTP/2 é uma evolução significativa do protocolo HTTP que introduz várias melhorias de desempenho em relação ao HTTP/1.1, mantendo a mesma semântica HTTP.

**Características principais:**
- **Multiplexação**: Múltiplas requisições e respostas podem ser enviadas simultaneamente através de uma única conexão TCP
- **Compressão de cabeçalhos**: Reduz o overhead de rede
- **Server Push**: Permite ao servidor enviar recursos ao cliente antes mesmo que sejam solicitados
- **Priorização de streams**: Permite que recursos críticos sejam carregados primeiro
- **Binário**: Protocolo binário em vez de texto, tornando o parsing mais eficiente

**Especificação oficial:** [RFC 7540 - HTTP/2](https://tools.ietf.org/html/rfc7540)

## Estrutura do Projeto

- `servidor/`
  - `app.py`: Aplicação Flask configurada para HTTP/2 via Hypercorn
- `cliente/`
  - `cliente.py`: Cliente de exemplo que consome a API REST/HTTP2

## Instruções de Execução

### Instalação de Dependências

```bash
# A partir da raiz do projeto
pip install -r rest_http2/requirements.txt
```

### Executar o Servidor

```bash
# A partir da raiz do projeto
hypercorn rest_http2.servidor.app:app --bind 0.0.0.0:5001
```

### Executar o Cliente

```bash
# A partir da raiz do projeto
python -m rest_http2.cliente.cliente
```

## Observações Técnicas

Para uma implementação completa de HTTP/2, seria necessário utilizar TLS/SSL (HTTPS), pois a maioria dos navegadores só suporta HTTP/2 sobre TLS. No entanto, para fins didáticos, esta implementação pode ser testada sem TLS usando o Hypercorn, que suporta HTTP/2 sem criptografia (h2c).
