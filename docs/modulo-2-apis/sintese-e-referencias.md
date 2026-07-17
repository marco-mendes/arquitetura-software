# Síntese e referências

## O fio do módulo

Arquitetar uma API é desenhar um compromisso entre equipes e sistemas. O compromisso começa na necessidade do consumidor, usa a semântica do protocolo, modela sucesso e falha, explicita tempo e repetição, e termina em evidência reproduzível. Framework e ferramenta ajudam a executar essa intenção; não substituem a decisão.

Guarde sete ideias:

1. Contrato é comportamento observável, não uma cópia da implementação.
2. REST usa recursos, representações e interface uniforme; JSON sobre HTTP não basta para caracterizá-lo.
3. Métodos, status e cabeçalhos HTTP carregam semântica útil.
4. Erros, paginação, idempotência e evolução pertencem ao contrato.
5. RPC, GraphQL e gRPC são alternativas contextuais, não etapas inferiores ou superiores.
6. Gateway aplica políticas de entrada, mas não resolve sozinho diferenças semânticas.
7. OpenAPI, Bruno, Spectral e testes observam aspectos diferentes e devem concordar.

O exemplo `POST /elegibilidades` demonstra aceitação com `202` e acompanhamento por `Location`. A escolha não promete decisão final. O armazenamento em memória torna a oficina simples e evidencia o que falta para múltiplas instâncias e reinícios. O próximo módulo usará essas operações para discutir limites de serviços, propriedade de dados e coordenação.

## Checklist de revisão

Antes de publicar um contrato, verifique:

- consumidor e tarefa estão identificados;
- nomes pertencem à linguagem da fronteira;
- método, status e cabeçalhos preservam a semântica HTTP;
- schemas distinguem campos obrigatórios e opcionais;
- erros têm código estável e não expõem internals;
- repetição e idempotência têm política explícita quando relevantes;
- coleções têm ordenação, limite e continuação;
- mudanças aditivas e incompatíveis têm estratégia;
- exemplos validam e executam;
- contrato, implementação e testes não divergem;
- limitações e gatilhos de revisão estão registrados.

## Especificações primárias

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): fonte normativa para métodos, status, campos e semântica HTTP.
- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0): estrutura normativa usada pelo contrato do laboratório.
- [REST — dissertação de Roy Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm): definição original das restrições do estilo.
- [GraphQL Specification](https://spec.graphql.org/): linguagem, sistema de tipos e execução.
- [Protocol Buffers — Language Guide](https://protobuf.dev/programming-guides/proto3/): regras do formato usado frequentemente com gRPC.

## Estilos e tecnologias

- [Introdução oficial ao gRPC](https://grpc.io/docs/what-is-grpc/introduction/): serviços, métodos e mensagens.
- [Guia oficial do GraphQL](https://graphql.org/learn/): schemas, consultas e evolução.
- [FastAPI](https://fastapi.tiangolo.com/): documentação da implementação Python e geração OpenAPI.
- [Spring Boot para aplicações web](https://docs.spring.io/spring-boot/reference/web/servlet.html): referência para controladores e aplicações servlet.
- [ASP.NET Core Web API](https://learn.microsoft.com/en-us/aspnet/core/web-api/): referência para APIs em .NET.

## Ferramentas

- [Documentação do Bruno](https://docs.usebruno.com/): importação e execução de coleções locais.
- [Documentação do Spectral](https://docs.stoplight.io/docs/spectral/): lint de contratos e regras personalizadas.
- [Node.js](https://nodejs.org/en/download): instalação do runtime que fornece npm e npx.
- [TestClient do FastAPI](https://fastapi.tiangolo.com/tutorial/testing/): testes HTTP em processo.
- [Documentação do Uvicorn](https://www.uvicorn.org/): servidor ASGI usado na oficina.

## Continuidade

Atualize a baseline do projeto com o contrato validado, exemplos, mapa de erros, diagramas e `ADR-002`. Na preparação do módulo 3, marque para cada operação: capacidade responsável, dados que precisa possuir, efeito de falha parcial e estado que precisa sobreviver a reinício. Essas respostas ajudarão a distinguir fronteira de API de fronteira de serviço.
