# Padrões e decisões para APIs

## Começar pelo problema do consumidor

Antes dos endpoints, identifique consumidor, resultado, tempo, dados e falhas. API é decisão de colaboração, não rotas derivadas de tabelas. Na elegibilidade, `202` com `Location` promete aceitação e acompanhamento, não aprovação nem mecanismo de processamento.

## Um processo arquitetural para construir APIs

O processo não é uma sequência burocrática. Ele diminui o risco de implementar uma interface tecnicamente correta e inutilizável para o consumidor.

```mermaid
flowchart LR
    A[Identificar consumidor\ne resultado] --> B[Delimitar capacidade\ne responsabilidade]
    B --> C[Comparar forma\nde interação]
    C --> D[Desenhar contrato\ne exemplos]
    D --> E[Implementar\ne testar]
    E --> F[Publicar, descobrir\ne observar uso]
    F --> G[Evoluir ou retirar\ncom transição]
    G -. evidência de uso .-> C
```

*Figura 6 — Ciclo de decisão de uma API, da necessidade do consumidor à evolução observada.*

**Leitura textual da figura:** a equipe identifica consumidor e resultado, delimita a capacidade e compara formas de interação antes de desenhar o contrato. Depois implementa, testa, publica e observa uso. Evidências de uso retornam à comparação de alternativas quando a API precisa evoluir ou ser retirada.

Para cada etapa, guarde cenário, responsabilidade, contrato, teste, referência de consumo e telemetria. FastAPI, Spring Boot e ASP.NET Core implementam; OpenAPI, Spectral e Bruno tornam a promessa analisável. Nenhuma ferramenta decide se a operação pertence à API ou se uma integração deve ser assíncrona.

## Comparar formas de interação pelas mesmas forças

Uma solução pode combinar estilos por critério explícito: REST/HTTP para recursos acessíveis a múltiplos clientes, GraphQL para leituras com seleção muito variável, gRPC para colaboração interna tipada e streaming, WebSocket para canal bidirecional e SOAP/XML para o contrato de um parceiro. A escolha não é um ranking.

Compare unidade de colaboração, descoberta, evolução, cache, operação e risco. Para tela móvel variável, GraphQL é hipótese a testar por número de chamadas, autorização e cache. Para processos internos, gRPC só ajuda se a medida incluir dependências lentas. SOAP/TISS é restrição de fronteira, não ordem para a plataforma inteira falar XML.

## Contract-first, code-first e compatibilidade

**Contract-first** revisa contrato e exemplos antes do servidor; **code-first** gera documentação de rotas e tipos. Escolha fonte principal e sentinelas contra deriva. Aqui, `contratos/openapi.yaml`, `src/hospital/api/main.py` e `tests/test_api_contract.py` são perspectivas diferentes, não prova de equivalência total.

Classifique mudanças como aditiva, restritiva, semântica ou remoção. Campo opcional tende a ser aditivo; trocar o significado de `recebida` quebra mesmo mantendo a forma. Versão no caminho é visível, cabeçalho preserva URI e negociação de mídia é mais precisa; nenhuma opção substitui inventário de consumidores e observação de uso.

## Paginação e idempotência são políticas, não adornos

Lista precisa declarar ordenação: `offset/limit` pode mover itens; cursor opaco pede expiração, filtro e erro válido. Para `POST`, chave de idempotência precisa declarar retenção, concorrência e corpo divergente. A API local não demonstra idempotência distribuída.

## Plataforma de APIs: capacidades, não catálogo de produtos

Uma plataforma de APIs reúne capacidades que tornam contratos construíveis, executáveis e encontráveis. Ela não precisa começar como uma compra corporativa, e a presença de um produto não substitui uma política de arquitetura.

```mermaid
flowchart TB
    D[Desenvolvimento\ncontrato, exemplos, lint, testes] --> X[API publicada]
    X --> R[Execução\nroteamento, TLS, limites, telemetria]
    X --> E[Engajamento\ndocumentação, catálogo, suporte]
    E --> D
    R --> D
```

*Figura 7 — Três capacidades conectadas de uma plataforma de APIs.*

**Leitura textual da figura:** desenvolvimento prepara contratos, exemplos, análise e testes; execução atende o tráfego com políticas técnicas; engajamento permite que consumidores encontrem, entendam e obtenham suporte. As setas de retorno mostram que telemetria e dúvidas de consumo devem alimentar o próximo ciclo de desenvolvimento.

Desenvolvimento responde por contrato, exemplos e testes; execução por tráfego, TLS, limites e telemetria; engajamento por descoberta e suporte. O laboratório usa uma versão mínima desse ciclo: repositório, OpenAPI, FastAPI, Bruno, Spectral e testes; não declara gateway ou catálogo empresarial.

## API gateway: borda pública, não centro do domínio

Um **API gateway** pode aplicar roteamento, TLS, autenticação técnica, limites, correlação e observabilidade. Não deve ser depósito de regras de negócio ou tradutor universal de conceitos externos.

```mermaid
flowchart LR
    C[Portal administrativo] --> G[Gateway\nrota, TLS, limite, correlação]
    G --> A[API de elegibilidade]
    G --> H[API de agenda]
    A --> L[Adaptador do laboratório\ntradução REST ↔ SOAP/TISS]
    L --> X[Laboratório parceiro]
```

*Figura 8 — Gateway na borda e adaptador junto à diferença semântica.*

**Leitura textual da figura:** o gateway concentra políticas técnicas e encaminha a chamada a APIs da plataforma. A tradução entre a linguagem interna e o SOAP/TISS do laboratório fica no adaptador, próximo da dependência externa. Assim, roteamento não é confundido com entendimento do domínio.

Agregação pede uma tela composta e medição de latência, falha e cache. Gateway sem necessidade de fronteira adiciona salto, configuração e operação. O módulo 4 aprofunda suas políticas.

## ADR-002: uma decisão que pode ser revisada

O ADR registra contexto, alternativas, decisão, consequências, evidência e gatilho. Na baseline, explique REST/HTTP, `202`, `Location`, OpenAPI, limites e sinais de revisão, como streaming, paginação ou idempotência forte.
