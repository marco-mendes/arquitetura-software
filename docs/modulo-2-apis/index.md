# Módulo 2 — Arquitetura de APIs

**Encontro:** 2 de 6

**Resultado principal:** projetar um contrato de API compreensível, evolutivo e verificável, relacionando decisões HTTP às necessidades de consumidores e às fronteiras da plataforma hospitalar.

Uma API é uma fronteira pública: nomes, formatos, métodos, estados, cabeçalhos e erros tornam-se compromissos. A questão não é “qual framework usar?”, mas “qual contrato permite colaboração sem expor decisões internas?”. API também não é sinônimo de REST, JSON ou URL: REST/HTTP, RPC, GraphQL, gRPC, WebSocket e SOAP/XML serão comparados pela necessidade do consumidor.

## Questão orientadora

Quando uma equipe chama `POST /elegibilidades`, o que ela pode assumir sobre o significado do recurso, o código `202`, o cabeçalho `Location`, o corpo JSON e os erros? Quais dessas promessas podem evoluir sem interromper consumidores existentes? Que evidência mostra que documento e execução continuam de acordo?

O raciocínio do encontro será:

> necessidade do consumidor → contrato observável → alternativa de interação → consequência → teste → evolução compatível

O laboratório implementa duas operações pequenas: `POST /elegibilidades` aceita um pedido e `GET /elegibilidades/{protocolo}` recupera o estado aceito. O recorte é intencional. Ele permite observar REST, HTTP e OpenAPI sem esconder o raciocínio sob um domínio extenso. O armazenamento é somente em memória: reiniciar o processo apaga os protocolos, comportamento adequado à oficina e inadequado para produção.

## Mapa do encontro

1. Consumidor, contrato e alternativas de interação.
2. Ciclo, plataforma e evolução de APIs.
3. Gateway, adaptador e integração externa.
4. OpenAPI, Bruno, Spectral e testes como evidências complementares.

## Objetivos de aprendizagem

Ao concluir o percurso, você será capaz de:

1. explicar contrato, recurso, HTTP, status e cabeçalho;
2. comparar REST, RPC, GraphQL, gRPC e WebSocket;
3. modelar sucesso, erro, evolução e compatibilidade em OpenAPI;
4. explicar gateway, adaptador e plataforma de APIs;
5. produzir evidência com FastAPI, `TestClient`, Bruno e Spectral.

## Percurso em oito páginas

1. **Visão geral:** delimita problema, resultado e contrato do encontro.
2. **Conceitos:** constrói o vocabulário de API e semântica HTTP.
3. **Padrões e decisões:** compara estilos, evolução e gateway pelas forças do contexto.
4. **Exemplo arquitetural:** percorre o contrato de elegibilidade de ponta a ponta.
5. **Estudo de caso:** aplica as decisões à plataforma hospitalar e às integrações externas.
6. **Oficina de ferramentas:** executa FastAPI, OpenAPI, Bruno, Spectral e testes automatizados.
7. **Exercícios:** pratica os seis níveis da Taxonomia de Bloom.
8. **Síntese e referências:** consolida o método e aponta fontes públicas.

## Entregas do encontro

Guarde `openapi.yaml` validado, execução Bruno, testes de contrato e `ADR-002`. O conjunto compara intenção, implementação e perspectiva do consumidor.

O [incremento 2 do projeto integrador](../projeto-integrador/incrementos.md#incremento-2-contratos-de-apis-e-integracoes-externas) reutiliza essas evidências. Consulte o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md) para preservar as fronteiras e o [template de ADR](../referencia/template-adr.md) para registrar a decisão.
