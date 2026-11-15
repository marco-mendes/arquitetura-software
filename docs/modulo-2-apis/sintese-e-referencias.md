# Síntese e referências

## O fio do módulo

A arquitetura de uma API define um compromisso entre equipes e sistemas. O compromisso parte da necessidade do consumidor e usa a semântica do protocolo para modelar sucesso e falha. Ele também explicita o tempo de resposta e a política de repetição e se completa com evidência reproduzível. *Frameworks* e ferramentas ajudam a executar essa intenção, enquanto a decisão continua sob responsabilidade do arquiteto.

As ideias centrais do módulo estão na lista abaixo.

1. Contrato é o comportamento observável pelo consumidor e independe da forma da implementação.
2. REST usa recursos, representações e interface uniforme, de modo que JSON sobre HTTP não basta para caracterizá-lo.
3. Métodos, status e cabeçalhos HTTP carregam semântica útil.
4. Erros, paginação, idempotência e evolução pertencem ao contrato.
5. RPC, GraphQL, gRPC e WebSocket são alternativas escolhidas pelo contexto e não formam uma hierarquia de maturidade.
6. O *gateway* aplica políticas de entrada e não resolve sozinho diferenças semânticas.
7. OpenAPI, Bruno, Spectral e testes observam aspectos diferentes e devem concordar.

O exemplo `POST /elegibilidades` demonstra a aceitação com `202` e o acompanhamento por `Location`, escolha que não promete decisão final ao consumidor. O armazenamento em memória simplifica a oficina e evidencia o que falta para suportar múltiplas instâncias e reinícios do processo. O Módulo 3 usará essas operações para discutir limites de serviços, propriedade de dados e coordenação.

## Checklist de revisão

Antes de publicar um contrato, recomenda-se verificar os itens abaixo.

- Consumidor e tarefa estão identificados.
- Nomes pertencem à linguagem da fronteira.
- Método, status e cabeçalhos preservam a semântica HTTP.
- Schemas distinguem campos obrigatórios e opcionais.
- Erros têm código estável e não expõem detalhes internos.
- Repetição e idempotência têm política explícita quando relevantes.
- Coleções têm ordenação, limite e continuação.
- Mudanças aditivas e incompatíveis têm estratégia.
- Exemplos validam e executam.
- Contrato, implementação e testes não divergem.
- Limitações e gatilhos de revisão estão registrados.

## Especificações primárias

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110). Fonte normativa para métodos, status, campos e semântica HTTP.
- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0). Estrutura normativa usada pelo contrato do laboratório.
- [REST — dissertação de Roy Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm). Definição original das restrições do estilo.
- [GraphQL Specification](https://spec.graphql.org/). Linguagem, sistema de tipos e execução.
- [Protocol Buffers — Language Guide](https://protobuf.dev/programming-guides/proto3/). Regras do formato usado frequentemente com gRPC, incluindo a estabilidade dos números de campo.
- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455). Abertura da conexão por `Upgrade`, resposta `101` e troca de mensagens nas duas direções.

## Estilos e tecnologias

- [Introdução oficial ao gRPC](https://grpc.io/docs/what-is-grpc/introduction/). Serviços, métodos e mensagens.
- [Guia oficial do GraphQL](https://graphql.org/learn/). Schemas, consultas e evolução.
- [Códigos de status do gRPC](https://grpc.io/docs/guides/status-codes/). Significado de `NOT_FOUND`, `INVALID_ARGUMENT` e dos demais status.
- [gRPC-Web](https://grpc.io/docs/platforms/web/basics/). Chamada a serviços gRPC a partir do navegador por meio de um proxy.
- [Início rápido do gRPC em Python](https://grpc.io/docs/languages/python/quickstart/). Geração de código com `grpc_tools.protoc` e servidor em Python.
- [Desempenho no GraphQL](https://graphql.org/learn/performance/). Problema N+1, DataLoader e consultas por `GET`.
- [Ariadne](https://ariadnegraphql.org/). Biblioteca Python de GraphQL usada no exemplo, com schema escrito em SDL.
- [websockets](https://websockets.readthedocs.io/). Biblioteca Python de WebSocket usada no exemplo.
- [FastAPI](https://fastapi.tiangolo.com/). Documentação da implementação Python e geração OpenAPI.
- [Spring Boot para aplicações web](https://docs.spring.io/spring-boot/reference/web/servlet.html). Referência para controladores e aplicações servlet.
- [ASP.NET Core Web API](https://learn.microsoft.com/en-us/aspnet/core/web-api/). Referência para APIs em .NET.

## Ferramentas

- [Documentação do Bruno](https://docs.usebruno.com/). Importação e execução de coleções locais.
- [Repositório oficial do Spectral](https://github.com/stoplightio/spectral). Instalação, uso, rulesets e documentação mantida pelo projeto.
- [Instalação oficial do Python](https://docs.python.org/3/using/index.html). Preparação do interpretador por sistema operacional.
- [Site oficial do Homebrew](https://brew.sh/). Instalação do gerenciador usado nos comandos de macOS.
- [Node.js](https://nodejs.org/en/download). Instalação do runtime que fornece npm e npx.
- [TestClient do FastAPI](https://fastapi.tiangolo.com/tutorial/testing/). Testes HTTP em processo.
- [Documentação do Uvicorn](https://www.uvicorn.org/). Servidor ASGI usado na oficina.
- [Documentação do Ocelot](https://ocelot.readthedocs.io/). Gateway de API para .NET usado na extensão opcional da oficina.

## Continuidade

Atualize a *baseline* do projeto com o contrato validado e seus exemplos, o mapa de erros, os diagramas e o `ADR-002`. Na preparação do Módulo 3, registre para cada operação os itens da lista abaixo.

- Capacidade responsável pela operação.
- Dados que a operação precisa possuir.
- Efeito de uma falha parcial.
- Estado que precisa sobreviver a uma reinicialização.

As respostas ajudarão a distinguir a fronteira de API da fronteira de serviço no Módulo 3.
