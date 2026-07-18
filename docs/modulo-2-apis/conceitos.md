# Conceitos fundamentais de APIs

## O Estilo de APIs

Uma API (Application Programming Interface) é um elemento central no desenvolvimento de software moderno, atuando como uma ponte que conecta diferentes sistemas, aplicações ou serviços, permitindo que eles se comuniquem de maneira estruturada e eficiente. Em essência, uma API define um conjunto de regras, protocolos e ferramentas que facilitam a interação entre componentes de software, promovendo a interoperabilidade e o reaproveitamento de funcionalidades.

Um exemplo da grande popularidade de APIs é a fundamentação Web, com REST e HTTP como carros-chefe.

![image](https://github.com/user-attachments/assets/393774d6-854a-48d2-8899-d0d19cb9ce57)

As APIs tornam possível o desenvolvimento modular e ágil, pois permitem que desenvolvedores integrem recursos de sistemas externos ou exponham os próprios serviços para consumo por terceiros. Um exemplo disso é a integração de aplicativos com serviços como mapas, pagamentos, redes sociais e até mesmo plataformas completas de e-commerce ou IoT. Dessa forma, os desenvolvedores podem se concentrar na lógica de suas aplicações sem precisar reinventar a funcionalidade básica que já foi criada e exposta por outros sistemas.

Uma característica essencial das APIs é que elas encapsulam a complexidade interna de um sistema, expondo apenas o que é necessário para que outros sistemas interajam com elas. Essa abstração promove segurança, já que os detalhes do funcionamento interno são protegidos, e permite atualizações ou mudanças internas sem afetar os sistemas conectados, desde que os contratos da API sejam mantidos.

No mercado atual, as APIs desempenham papéis estratégicos. Elas são o motor de ecossistemas digitais complexos, viabilizando modelos de negócios baseados em plataformas, como o oferecimento de serviços as-a-service (SaaS, PaaS). Por exemplo, uma empresa pode abrir APIs públicas para que desenvolvedores externos criem soluções complementares ao seu produto principal, fortalecendo o valor do seu ecossistema.

Além de serem amplamente utilizadas em sistemas móveis, aplicativos web e na comunicação entre micro serviços em arquiteturas distribuídas, as APIs são fundamentais para a transformação digital das organizações. Elas possibilitam a integração de legados e novos sistemas, acelerando inovações e garantindo escalabilidade nos processos.

Lembre-se uma API é muito mais do que uma interface técnica. Ela representa uma linguagem comum e estruturada que conecta sistemas, permite colaboração e inovações, e alinha as soluções tecnológicas às demandas crescentes de um mercado cada vez mais digital.

## API: fronteira de colaboração, não apenas uma URL

Uma **interface de programação de aplicações** (API) permite que aplicação web, móvel, nuvem, parceiro ou dispositivo use uma capacidade sem conhecer tabelas ou algoritmos internos. Separe três camadas:

| Camada        | Pergunta que responde                 | Exemplo na plataforma hospitalar                                   |
| ------------- | ------------------------------------- | ------------------------------------------------------------------ |
| Interface     | O que está disponível para interação? | `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`         |
| Contrato      | Que promessa é observável?            | campos obrigatórios, `202`, `Location`, `422` e schemas publicados |
| Implementação | Como a promessa é cumprida hoje?      | FastAPI, Pydantic e armazenamento em memória                       |

O **consumidor** depende do contrato, não do código ou banco. Trocar biblioteca ou armazenamento pode ser interno; renomear campo, mudar status ou remover operação pede transição. Contrato, governança e evidência — não apenas a URL — tornam a API reutilizável.

## Consumidores diferentes, necessidades diferentes

Não se escolhe um estilo por popularidade. Aplicação web tende a valorizar semântica HTTP e documentação; móvel, payload e rede; integração entre organizações, contrato durável e tradução de vocabulário; canal em tempo real, reconexão e ritmo. Uma API multicanal não precisa entregar a mesma representação a todos, mas precisa preservar o significado de negócio e declarar diferenças.

## Exemplo - A semância do HTTP

HTTP não é apenas um túnel para “chamar função remota”. Uma requisição combina método, alvo, cabeçalhos e, quando necessário, conteúdo; uma resposta combina status, cabeçalhos e conteúdo. Clientes, proxies, caches e ferramentas compreendem essa semântica.

Considere `POST /elegibilidades`. O método comunica que o cliente submete uma representação para processamento. A resposta `202 Accepted` informa aceitação, mas não afirma que a operadora já decidiu. `Location: /elegibilidades/{protocolo}` comunica onde acompanhar o recurso aceito. Cada elemento reduz uma ambiguidade diferente.

| Método   | Intenção comum                              | Propriedade relevante           |
| -------- | ------------------------------------------- | ------------------------------- |
| `GET`    | recuperar uma representação                 | seguro e idempotente            |
| `POST`   | submeter dados ou criar sob uma coleção     | não é idempotente por definição |
| `PUT`    | substituir o estado conhecido de um recurso | idempotente                     |
| `PATCH`  | aplicar alteração parcial                   | depende do formato da alteração |
| `DELETE` | remover a associação de um recurso          | idempotente na intenção         |

**Seguro** significa que o consumidor não pede mudança de estado; logs e métricas ainda podem existir. **Idempotente** significa que repetir a mesma intenção produz o mesmo efeito pretendido no servidor, embora a resposta ou metadados possam variar. Idempotência não equivale a deduplicação automática de uma transação distribuída.

## Recursos, representações e erros

Em REST, um **recurso** é algo identificado e manipulado por representações. A URI identifica; o JSON é a fotografia de uma representação naquele instante. A elegibilidade aceita não é o dicionário Python que a oficina guarda: amanhã ela pode vir de banco ou de outro serviço sem que o identificador público mude.

Por isso, rotas tendem a usar substantivos do vocabulário do consumidor, como `/elegibilidades`, `/agendamentos` e `/autorizacoes`. Verbos continuam existindo nos métodos e nas transições. Uma rota como `/aprovarAutomaticamente` pode ser uma operação RPC perfeitamente coerente, mas não deve ser chamada de REST só por usar JSON e HTTP.

Uma representação inclui dados necessários à tarefa, não tabelas internas: o laboratório retorna `protocolo`, `situacao` e `criado_em`. Famílias `2xx`, `4xx` e `5xx` distinguem sucesso, problema do consumidor e falha do servidor; `200`, `201`, `202`, `404`, `409` e `422` refinam a semântica. O schema `ErroAPI` usa `codigo` estável, `mensagem` legível e `detalhes` por campo para que o consumidor não dependa de texto livre.

## Restrições REST de Fielding

REST não é JSON sobre HTTP. **Cliente-servidor**, **sem estado** e **cache** delimitam colaboração; **interface uniforme** reúne identificação de recursos, representações, mensagens autodescritivas e hipermídia; **sistema em camadas** aceita intermediários; **código sob demanda** é opcional. Uma API HTTP não é automaticamente REST: rota com substantivo pode ser **RPC com aparência de recurso**. O laboratório usa recursos e mensagens HTTP, mas não demonstra todas as restrições.

## Além do HTTP - Estilos de APIs

REST, RPC, GraphQL, gRPC, WebSocket e SOAP resolvem interações distintas. O protocolo e o estilo devem ser avaliados pela necessidade do consumidor, topologia, volume, latência, evolução e operação.

```mermaid
flowchart LR
    C[Consumidor] --> R[REST / HTTP\nrecursos e representações]
    C --> Q[GraphQL\nschema e seleção de campos]
    C --> P[gRPC / RPC\noperação, mensagem e código gerado]
    C --> W[WebSocket\ncanal bidirecional persistente]
    C --> S[SOAP / XML\ncontrato XML e interoperabilidade legada]
    R --> N[Capacidade de negócio]
    Q --> N
    P --> N
    W --> N
    S --> N
```

**Texto alternativo:** um consumidor alcança a mesma capacidade por REST/HTTP, GraphQL, gRPC/RPC, WebSocket ou SOAP/XML.

*Figura 3 — Formas de interação entre um consumidor e a mesma capacidade de negócio. Fonte: curso.*

**Leitura textual:** as formas convergem na mesma capacidade: REST usa recursos, GraphQL seleciona campos, gRPC/RPC expõe operações, WebSocket mantém canal e SOAP/XML apoia contrato existente.

| Alternativa | Quando ajuda                             | Cuidado arquitetural                       |
| ----------- | ---------------------------------------- | ------------------------------------------ |
| REST/HTTP   | recursos em integrações web heterogêneas | não reduzir REST a nomes de URL            |
| RPC/gRPC    | comandos ou colaboração interna tipada   | evolução de métodos, mensagens e toolchain |
| GraphQL     | leituras com seleção variável            | custo, autorização e cache nos resolvers   |
| WebSocket   | atualização bidirecional em tempo real   | reconexão, ordenação e pressão de consumo  |
| SOAP/XML    | contrato de parceiro legado              | isolar tradução do domínio                 |

GraphQL exige schema e política para consultas caras. gRPC não garante baixo tempo de resposta se a dependência externa continua lenta. WebSocket não substitui evento durável ou mensageria. SOAP não exige que a plataforma moderna use XML. Em cada caso, o arquiteto registra a força que levou à escolha e a evidência que poderá revisá-la.

## O contrato verificável e a sua evolução

Cabeçalhos transportam metadados da interação: `Content-Type` descreve a representação enviada, `Accept` expressa os formatos aceitos, `Location` aponta um recurso relacionado, `ETag` identifica a versão de uma representação para cache ou concorrência, e um identificador de correlação conecta registros técnicos. OpenAPI descreve caminhos, operações, parâmetros, corpos, respostas e schemas em YAML ou JSON; no laboratório, `contratos/openapi.yaml` é a promessa explícita versionada. Um arquivo válido ainda pode ser um contrato fraco — tipo sem significado, erro ausente, exemplo incompatível: Spectral examina o documento, Bruno o consumo e `TestClient` a execução HTTP, perspectivas complementares.

![Anatomia de um contrato de API: cliente consome um contrato OpenAPI, a API processa a solicitação e responde 202 Accepted com Location para acompanhamento pela operadora de plano.](../assets/images/m02-anatomia-api.png)

*Figura 4 — Anatomia de um contrato de API. Fonte: curso.*

**Leitura textual da figura:** um cliente consulta o contrato OpenAPI e envia uma requisição à API. A API responde `202 Accepted` e `Location` para informar aceitação e o caminho de acompanhamento. Outro consumidor, como uma operadora, pode usar a mesma promessa sem conhecer a implementação do servidor.

Na evolução do contrato, a **paginação** por `offset/limit` pode repetir ou omitir itens em coleção mutável; um cursor opaco lida melhor com mudança, mas pede mais política — declare ordenação, continuação e filtros. Para a repetição segura de `POST`, uma chave de **idempotência** precisa de escopo, retenção, comparação e resposta divergente. O **versionamento** identifica uma linha de evolução incompatível; prefira campo opcional e significado preservado antes de abrir nova versão — remoção, obrigatoriedade ou unidade nova tendem a quebrar consumidores.
