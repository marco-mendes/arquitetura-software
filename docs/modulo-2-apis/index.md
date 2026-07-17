# Módulo 2 — Arquitetura de APIs

**Encontro:** 2 de 6

**Resultado principal:** projetar um contrato de API compreensível, evolutivo e verificável, relacionando decisões HTTP às necessidades de consumidores e às fronteiras da plataforma hospitalar.

Uma API é uma fronteira pública entre quem oferece uma capacidade e quem depende dela. Nomes, formatos, métodos, estados, cabeçalhos, erros e expectativas temporais tornam-se compromissos. Mudar detalhe interno pode ser barato; mudar um compromisso usado por consumidores pode exigir coordenação e migração.

Este módulo parte do vocabulário arquitetural do encontro anterior e aproxima a lente. A estrutura inicial da plataforma identificou capacidades e integrações. Agora precisamos decidir como um consumidor pede uma consulta de elegibilidade, como descobre que ela foi aceita, como recupera o protocolo e como interpreta uma rejeição. A pergunta deixa de ser “qual framework usar?” e passa a ser “qual contrato permite colaboração sem expor decisões internas desnecessárias?”.

## Questão orientadora

Quando uma equipe chama `POST /elegibilidades`, o que ela pode assumir sobre o significado do recurso, o código `202`, o cabeçalho `Location`, o corpo JSON e os erros? Quais dessas promessas podem evoluir sem interromper consumidores existentes? Que evidência mostra que documento e execução continuam de acordo?

O raciocínio do encontro será:

> necessidade do consumidor → contrato observável → alternativa de interação → consequência → teste → evolução compatível

O laboratório implementa duas operações pequenas: `POST /elegibilidades` aceita um pedido e `GET /elegibilidades/{protocolo}` recupera o estado aceito. O recorte é intencional. Ele permite observar REST, HTTP e OpenAPI sem esconder o raciocínio sob um domínio extenso. O armazenamento é somente em memória: reiniciar o processo apaga os protocolos, comportamento adequado à oficina e inadequado para produção.

## Objetivos de aprendizagem

Ao concluir o percurso, você será capaz de:

1. explicar contrato, recurso, representação, método, status e cabeçalho no contexto de HTTP;
2. distinguir REST de uma simples API JSON e compará-lo com RPC, GraphQL e gRPC;
3. modelar sucesso e erro em OpenAPI, com exemplos executáveis;
4. analisar idempotência, paginação, versionamento e compatibilidade;
5. explicar o papel e os limites de um API gateway;
6. testar uma implementação FastAPI com `TestClient`, Bruno e Spectral;
7. registrar uma decisão de estilo e evolução sem confundir tecnologia com arquitetura.

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

Guarde quatro evidências: o arquivo `openapi.yaml` validado, uma execução de criação e consulta no Bruno, a saída dos testes de contrato e um `ADR-002` curto sobre estilo e evolução. A documentação isolada pode estar desatualizada; o servidor isolado pode executar algo não combinado; o cliente isolado pode usar somente o caminho feliz. O conjunto permite comparar intenção, implementação e perspectiva do consumidor.

O [incremento 2 do projeto integrador](../projeto-integrador/incrementos.md#incremento-2-contratos-de-apis-e-integracoes-externas) reutiliza essas evidências. Consulte o [contexto hospitalar](../projeto-integrador/contexto-hospitalar.md) para preservar as fronteiras e o [template de ADR](../referencia/template-adr.md) para registrar a decisão.
