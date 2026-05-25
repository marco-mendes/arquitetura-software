# REST com HTTP/2 (Preparação para HTTP/3)

Implementação didática de API REST usando HTTP/2 com Hypercorn, como preparação para HTTP/3.

## Arquitetura HTTP/3

HTTP/3 é a terceira versão principal do protocolo HTTP, que utiliza QUIC como protocolo de transporte em vez de TCP. Esta mudança fundamental traz melhorias significativas de desempenho, especialmente em redes instáveis.

**Características principais:**
- **QUIC como transporte**: Baseado em UDP em vez de TCP, reduzindo latência de estabelecimento de conexão
- **Multiplexação independente**: Elimina o bloqueio de head-of-line do HTTP/2
- **Migração de conexão**: Mantém conexões ativas mesmo quando o endereço IP muda (útil para dispositivos móveis)
- **TLS 1.3 integrado**: Segurança incorporada no protocolo
- **Correção de erros avançada**: Recuperação mais rápida de pacotes perdidos

**Especificação oficial:** [RFC 9114 - HTTP/3](https://datatracker.ietf.org/doc/html/rfc9114)

## Sobre esta Implementação

Esta implementação usa HTTP/2 com Hypercorn como uma preparação para HTTP/3. HTTP/2 já implementa várias melhorias importantes como multiplexação de requisições e compressão de cabeçalhos, que são mantidas no HTTP/3.

A transição completa para HTTP/3 requer:
1. Suporte a QUIC (baseado em UDP)
2. Bibliotecas específicas como aioquic (que requer Rust)
3. Configurações de rede e certificados TLS

## Estrutura do Projeto

- `servidor/`
  - `app.py`: Aplicação FastAPI configurada para HTTP/2 via Hypercorn
- `cliente/`
  - `cliente.py`: Cliente de exemplo que consome a API usando HTTP/2

## Instruções de Execução

### Instalação de Dependências

```bash
# A partir da raiz do projeto
pip install -r rest_http3/requirements.txt
```

### Executar o Servidor (HTTP/1.1)

Para simplicidade, vamos usar HTTP/1.1 para testes iniciais:

```bash
# A partir da raiz do projeto
hypercorn rest_http3.servidor.app:app --bind 0.0.0.0:8000
```

### Executar o Cliente

```bash
# A partir da raiz do projeto
python -m rest_http3.cliente.cliente
```

Para usar o cliente com HTTP/1.1, edite a variável `HTTP2_ENABLED` no arquivo `cliente.py` para `False`.

## Observações Técnicas

Esta implementação usa HTTP/1.1 com Hypercorn como base, mas está estruturada para facilitar a transição para HTTP/2 e HTTP/3:

1. **Hypercorn**: Servidor ASGI que suporta HTTP/1.1, HTTP/2 e tem suporte experimental para HTTP/3
2. **Cliente assíncrono**: O cliente usa httpx com suporte a diferentes versões do protocolo HTTP
3. **Evolução**: Esta implementação pode ser expandida para HTTP/3 quando o suporte em Python estiver mais maduro

### Caminho para HTTP/2 e HTTP/3

Para habilitar HTTP/2 completo, seria necessário:
1. Gerar certificados TLS (requer biblioteca cryptography com Rust)
2. Executar Hypercorn com os parâmetros de certificado

Para uma implementação completa de HTTP/3 no futuro, seria necessário:
1. Instalar Rust e ferramentas de desenvolvimento
2. Adicionar aioquic às dependências
3. Configurar Hypercorn com suporte a QUIC
4. Atualizar o cliente para usar HTTP/3 nativo

Para uma implementação de produção atual, considere usar um servidor proxy como Nginx ou Envoy com módulos HTTP/3 na frente da sua aplicação Python.
