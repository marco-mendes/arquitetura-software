# Arquitetura de APIs

**Encontro:** 2 de 6

**Resultado principal:** decidir em que situação uma capacidade de negócio se torna fronteira pública, escolher o estilo de interação adequado a cada consumidor e projetar um contrato compreensível, evolutivo e verificável.

Uma API conecta sistemas, parceiros e dispositivos em ecossistemas digitais e viabiliza modelos de negócio inteiros, de modo que não se limita a uma interface técnica. A organização que expõe uma API transforma nomes, formatos e métodos em compromissos públicos, assim como os estados e os erros. A decisão central deixa de ser a escolha do *framework* e passa a ser a definição do contrato que permite colaboração sem expor decisões internas. API também não é sinônimo de REST, JSON ou URL. Os contextos web, mobile e cloud pedem estilos, protocolos e formatos de dados próprios de cada contexto de uso. A mesma diferença vale para a integração entre organizações, o omnichannel e a IoT.

## O que este módulo cobre

O percurso trata a API como um **estilo arquitetural** e abrange os planos descritos na lista abaixo.

- **Fundamentos:** a web como ecossistema, o HTTP como protocolo com semântica e a API como fronteira de colaboração em que interface, contrato e implementação são camadas distintas.
- **Estilos e tipos:** REST e as restrições de Fielding comparados a RPC, GraphQL e gRPC e a WebSocket e SOAP segundo a necessidade do consumidor, além dos tipos de APIs conforme o contexto de solução.
- **Contrato e evolução:** OpenAPI como promessa explícita e erros como parte do contrato, com paginação, idempotência e versionamento tratados como decisões de compatibilidade.
- **Borda e plataforma:** *gateway* de API e adaptadores, as capacidades de desenvolvimento, execução e engajamento de uma plataforma e a agenda do arquiteto.

## Questão orientadora

A organização precisa expor capacidades a consumidores que ela não controla, como aplicações web e móveis, parceiros e outras nuvens ou dispositivos. A questão orientadora do encontro se desdobra nas perguntas abaixo.

- Quais fronteiras merecem se tornar contrato público e quais devem permanecer internas?
- Que estilo de interação atende cada consumidor sem restringir a evolução do sistema?
- O que a borda e a plataforma precisam oferecer para que dezenas de APIs continuem seguras, observáveis e compatíveis ao longo dos anos?

A pergunta do encontro é arquitetural e trata das promessas que uma fronteira pública faz, do custo dessas promessas e da forma de evoluir a fronteira sem quebrar os consumidores que dependem dela. O raciocínio segue a sequência abaixo.

> capacidade de negócio → consumidor → estilo de interação → contrato observável → borda e plataforma → evolução compatível

O laboratório aplica esse raciocínio num recorte mínimo de duas operações de elegibilidade. O recorte basta para observar contrato, semântica e verificação sem que um domínio extenso encubra o argumento arquitetural.

## Objetivos de aprendizagem

Ao concluir o percurso, você será capaz de:

1. explicar API como fronteira de colaboração, separando interface, contrato e implementação.
2. comparar REST, RPC e GraphQL e também gRPC, WebSocket e SOAP pela necessidade do consumidor.
3. reconhecer os tipos de APIs conforme o contexto de solução e suas consequências.
4. modelar sucesso, erro, evolução e compatibilidade em OpenAPI.
5. explicar *gateway*, adaptador e as capacidades de uma plataforma de APIs.
6. produzir evidência com FastAPI e `TestClient` e com Bruno, Spectral e Ocelot.

## Percurso em nove páginas

1. **Visão geral:** delimita problema, resultado e contrato do encontro.
2. **Conceitos:** apresenta o estilo de APIs e os fundamentos da web, as restrições REST de Fielding e a evolução do contrato.
3. **Padrões e decisões:** apresenta os tipos de APIs por contexto, a lente da plataforma e a agenda do arquiteto.
4. **Exemplo arquitetural:** percorre o contrato de elegibilidade completo e expõe a mesma capacidade por gRPC, GraphQL e WebSocket, com programas Python executáveis.
5. **Estudo de caso:** aplica as decisões à plataforma hospitalar e às integrações externas.
6. **[Casos reais](casos-reais.md):** acompanha a abertura da API do Twitter, a formação de um ecossistema de clientes e os três fechamentos posteriores dessa API.
7. **Oficina de ferramentas:** executa FastAPI e OpenAPI com Bruno e Spectral, os testes automatizados e a extensão com o *gateway* Ocelot.
8. **Exercícios:** pratica os seis níveis da Taxonomia de Bloom.
9. **Síntese e referências:** consolida o método e aponta fontes públicas.

## Entregas do encontro

As entregas do encontro são o `openapi.yaml` validado, a execução no Bruno, os testes de contrato e o `ADR-002`. O conjunto permite comparar a intenção, a implementação e a perspectiva do consumidor.

O [incremento 2 do projeto integrador](../projeto-integrador/incrementos.md#incremento-2-contratos-de-apis-e-integracoes-externas) reutiliza essas evidências. Consulte o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md) para preservar as fronteiras e o [template de ADR](../referencia/template-adr.md) para registrar a decisão.
