# WebSocket API

Implementação didática de API WebSocket usando FastAPI e websockets.

## Arquitetura WebSocket

WebSocket é um protocolo de comunicação bidirecional que fornece um canal de comunicação full-duplex sobre uma única conexão TCP. Diferente do modelo tradicional de requisição-resposta do HTTP, WebSockets permitem comunicação em tempo real entre cliente e servidor.

**Características principais:**
- **Comunicação bidirecional**: Permite que servidor e cliente enviem mensagens independentemente
- **Conexão persistente**: Mantém uma única conexão TCP aberta, reduzindo overhead
- **Baixa latência**: Ideal para aplicações em tempo real
- **Eficiente**: Menor overhead de cabeçalhos em comparação com polling HTTP
- **Compatível com web**: Funciona através de firewalls e proxies que suportam HTTP

**Especificação oficial:** [RFC 6455 - The WebSocket Protocol](https://tools.ietf.org/html/rfc6455)

## Estrutura do Projeto

- `servidor/`
  - `app.py`: Aplicação FastAPI com endpoints WebSocket
- `cliente/`
  - `cliente.py`: Cliente de exemplo que se conecta via WebSocket

## Instruções de Execução

### Instalação de Dependências

```bash
# A partir da raiz do projeto
pip install -r websocket/requirements.txt
```

### Executar o Servidor

```bash
# A partir da raiz do projeto
uvicorn websocket.servidor.app:app --host 0.0.0.0 --port 7001
```

### Executar o Cliente

```bash
# A partir da raiz do projeto
python -m websocket.cliente.cliente
```

## Casos de Uso Comuns

WebSockets são ideais para aplicações que requerem comunicação em tempo real, como:
- Chat e mensageria
- Notificações em tempo real
- Jogos online
- Dashboards com atualizações ao vivo
- Colaboração em tempo real

## Observações Técnicas

Esta implementação utiliza FastAPI, que fornece suporte nativo a WebSockets através da biblioteca `websockets`. O cliente é implementado usando a biblioteca `websocket-client` para Python.
