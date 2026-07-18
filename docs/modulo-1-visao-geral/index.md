# Módulo 1 — Visão geral de estilos arquiteturais

**Encontro:** 1 de 6

**Resultado principal:** comparar formas de organizar um sistema e justificar uma estrutura inicial com forças, limites e evidências verificáveis.

Arquitetura começa quando uma equipe identifica decisões estruturais, explicita prioridades e verifica consequências. Este módulo evita tratar desenho como decoração ou preferência técnica como verdade universal.

Ao final do percurso, você será capaz de reconhecer componente, conector e fronteira; formular um atributo de qualidade como cenário observável; localizar Camadas, MVC, Hexagonal, Microkernel, DDD, microsserviços, APIs, eventos, nuvem e contêineres em um mesmo mapa sem tratá-los como sinônimos; comparar camadas, Pipes and Filters, microkernel e monólito modular; e registrar uma decisão em um ADR. A oficina transforma essas ideias em uma comparação executável, um teste e um diagrama como código.

## Questão orientadora

Considere uma solução que precisa mudar regras com frequência, processar uma quantidade crescente de itens e continuar compreensível para diferentes equipes. Qual estrutura favorece cada necessidade? Que custo acompanha a escolha? Que execução permitiria descobrir se a promessa se confirma?

Não existe resposta baseada apenas no nome do domínio. Uma alternativa é adequada quando suas propriedades respondem às forças relevantes dentro das restrições conhecidas. O mesmo estilo pode ser apropriado em um contexto e inadequado em outro. Por isso, a unidade de raciocínio deste encontro será:

> contexto → força priorizada → alternativas → consequências → evidência → decisão revisável

Consulte o [glossário compartilhado](../referencia/glossario.md) sempre que um termo novo aparecer. Para transformar expressões vagas como “rápido” ou “fácil de manter” em cenários, use a página de [atributos de qualidade](../referencia/atributos-de-qualidade.md). O registro final segue o [template de ADR](../referencia/template-adr.md), usado também no projeto integrador.

## Percurso em oito páginas

Visão geral, conceitos e decisões formam a base; exemplo e estudo de caso aplicam a comparação; oficina e exercícios produzem evidências; síntese encerra o encontro.

## Como estudar

Leia as três primeiras páginas em ordem. Elas constroem conceitos antes de introduzir o caso hospitalar. No exemplo, pergunte a cada elemento “qual responsabilidade está aqui?” e “como ele se comunica?”. Na oficina, não se limite a obter uma saída verde: compare o resultado antes e depois de mudar a prioridade. Nos exercícios avançados, preserve hipóteses e declare o que ainda precisaria ser medido.

O módulo oferece três profundidades. **Essencial em aula** cobre vocabulário, comparação básica, teste e ADR. **Exploração em dupla** acrescenta discussão de alternativas e alteração de forças. **Extensão** conecta ferramentas de verificação arquitetural e cenários mais exigentes. As três trilhas usam a mesma baseline; aprofundar não significa criar uma solução paralela.

## Antes da oficina: o que você fará de fato

A [oficina](oficina-de-ferramentas.md) apresenta a aplicação didática existente, seu local, a preparação e o que cada comando observa. Você executará `tests/test_estilos.py`, guardará a saída, alterará um cenário e registrará um mini-ADR. Isso evidencia o comparador, não uma solução em produção.

## Entregas do encontro

Ao concluir, guarde quatro artefatos pequenos e conectados: uma matriz de alternativas, o resultado reproduzível do teste `test_estilos.py`, um diagrama Structurizr Lite e um mini-ADR. Nenhum deles prova sozinho que a arquitetura é adequada. Em conjunto, mostram como a decisão foi formulada, quais consequências foram aceitas e onde a turma pode revisar a hipótese.

O [incremento 1 do projeto integrador](../projeto-integrador/incrementos.md#incremento-1-estrutura-e-decisoes-iniciais) reutiliza esses artefatos para formar a primeira baseline da plataforma. A intenção não é prever todos os encontros, mas iniciar uma cadeia de decisões coerente e evolutiva.
