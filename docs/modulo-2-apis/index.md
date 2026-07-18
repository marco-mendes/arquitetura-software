# Módulo 2 — Arquitetura de APIs

**Encontro:** 2 de 6

**Resultado principal:** decidir onde uma capacidade de negócio vira fronteira pública, escolher o estilo de interação adequado a cada consumidor e projetar um contrato compreensível, evolutivo e verificável.

Uma API é mais do que uma interface técnica: é o elemento que conecta sistemas, parceiros e dispositivos em ecossistemas digitais, viabilizando modelos de negócio inteiros. Ao expor uma API, a organização transforma nomes, formatos, métodos, estados e erros em compromissos públicos. A questão deixa de ser “qual framework usar?” e passa a ser “qual contrato permite colaboração sem expor decisões internas?”. API também não é sinônimo de REST, JSON ou URL: web, mobile, cloud, integração entre organizações, omnichannel e IoT pedem estilos, protocolos e formatos diferentes.

## O que este módulo cobre

O percurso trata a API como um **estilo arquitetural** e percorre quatro planos:

- **Fundamentos:** a web como ecossistema, o HTTP como protocolo com semântica e a API como fronteira de colaboração — interface, contrato e implementação como camadas distintas;
- **Estilos e tipos:** REST e as restrições de Fielding, RPC, GraphQL, gRPC, WebSocket e SOAP, comparados pela necessidade do consumidor, e os tipos de APIs conforme o contexto de solução;
- **Contrato e evolução:** OpenAPI como promessa explícita, erros como parte do contrato, paginação, idempotência e versionamento como decisões de compatibilidade;
- **Borda e plataforma:** gateway de API, adaptadores e as três capacidades de uma plataforma — desenvolvimento, execução e engajamento —, fechando com a agenda do arquiteto para APIs.

## Questão orientadora

Sua organização precisa expor capacidades a consumidores que ela não controla: aplicações web e móveis, parceiros, outras nuvens e dispositivos. Quais fronteiras merecem virar contrato público — e quais devem permanecer internas? Que estilo de interação serve cada consumidor sem acorrentar a evolução do sistema? O que a borda e a plataforma precisam oferecer para que dezenas de APIs continuem seguras, observáveis e compatíveis ao longo dos anos?

A pergunta do encontro não é operacional — “como implemento um endpoint?” —, e sim arquitetural: quais promessas uma fronteira pública faz, a que custo, e como ela evolui sem quebrar quem depende dela. O raciocínio será:

> capacidade de negócio → consumidor → estilo de interação → contrato observável → borda e plataforma → evolução compatível

O laboratório materializa esse raciocínio num recorte mínimo de duas operações de elegibilidade, suficiente para observar contrato, semântica e verificação sem esconder o argumento sob um domínio extenso.

## Mapa do encontro

1. O estilo de APIs, os fundamentos da web e a semântica HTTP.
2. Tipos de APIs conforme o contexto e estilos de interação além do HTTP.
3. Contrato verificável: OpenAPI, erros, paginação, idempotência e versionamento.
4. Gateway, adaptador, plataforma de APIs e a agenda do arquiteto.
5. Evidências com FastAPI, Bruno, Spectral, testes automatizados e o gateway Ocelot.

## Objetivos de aprendizagem

Ao concluir o percurso, você será capaz de:

1. explicar API como fronteira de colaboração, separando interface, contrato e implementação;
2. comparar REST, RPC, GraphQL, gRPC, WebSocket e SOAP pela necessidade do consumidor;
3. reconhecer os tipos de APIs conforme o contexto de solução e suas consequências;
4. modelar sucesso, erro, evolução e compatibilidade em OpenAPI;
5. explicar gateway, adaptador e as capacidades de uma plataforma de APIs;
6. produzir evidência com FastAPI, `TestClient`, Bruno, Spectral e Ocelot.

## Percurso em oito páginas

1. **Visão geral:** delimita problema, resultado e contrato do encontro.
2. **Conceitos:** do estilo de APIs e dos fundamentos da web às restrições REST de Fielding e à evolução do contrato.
3. **Padrões e decisões:** tipos de APIs por contexto, a lente da plataforma e a agenda do arquiteto.
4. **Exemplo arquitetural:** percorre o contrato de elegibilidade de ponta a ponta.
5. **Estudo de caso:** aplica as decisões à plataforma hospitalar e às integrações externas.
6. **Oficina de ferramentas:** executa FastAPI, OpenAPI, Bruno, Spectral, testes automatizados e a extensão com o gateway Ocelot.
7. **Exercícios:** pratica os seis níveis da Taxonomia de Bloom.
8. **Síntese e referências:** consolida o método e aponta fontes públicas.

## Entregas do encontro

Guarde `openapi.yaml` validado, execução Bruno, testes de contrato e `ADR-002`. O conjunto compara intenção, implementação e perspectiva do consumidor.

O [incremento 2 do projeto integrador](../projeto-integrador/incrementos.md#incremento-2-contratos-de-apis-e-integracoes-externas) reutiliza essas evidências. Consulte o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md) para preservar as fronteiras e o [template de ADR](../referencia/template-adr.md) para registrar a decisão.
