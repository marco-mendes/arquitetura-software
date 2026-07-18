# Módulo 1 — Visão geral de estilos arquiteturais

**Encontro:** 1 de 6

**Resultado principal:** comparar formas de organizar um sistema e justificar uma estrutura inicial com forças, limites e evidências verificáveis.

Arquitetura de software começa quando uma equipe identifica as decisões estruturais que serão caras de reverter, explicita prioridades e verifica consequências. Estilos arquiteturais são o vocabulário dessa conversa: nomes compartilhados para formas recorrentes de organizar responsabilidades, conexões e fronteiras. Este módulo evita dois extremos — tratar desenho como decoração e tratar preferência técnica como verdade universal.

## O que este módulo cobre

O percurso parte de um **mapa de quatro famílias de decisão** — organização interna, decomposição por domínio, integração e comunicação, execução e operação — para que cada estilo seja localizado antes de ser julgado. Sobre esse mapa, quatro estilos de organização interna são estudados em profundidade, com origem, características avaliadas por Richards e Ford, anti-padrões e critérios de uso:

- **Camadas**, o estilo mais difundido, com camadas abertas e fechadas, o anti-padrão do sumidouro e as variações MVC e DDD;
- **Pipes and Filters**, a decomposição em transformações com os quatro tipos canônicos de filtro;
- **Microkernel**, o núcleo estável estendido por plugins sob contrato;
- **Monólito modular**, capacidades autônomas dentro de uma única implantação, com fronteiras verificadas por ferramenta.

O fecho do módulo é o **ADR** — o registro de decisão arquitetural que transforma escolha em hipótese contestável, reutilizado em todos os encontros seguintes.

## Questão orientadora

Considere uma solução que precisa mudar regras com frequência, processar uma quantidade crescente de itens e continuar compreensível para diferentes equipes. Qual estrutura favorece cada necessidade? Que custo acompanha a escolha? Que evidência permitiria descobrir se a promessa se confirma?

Não existe resposta baseada apenas no nome do domínio. Uma alternativa é adequada quando suas propriedades respondem às forças relevantes dentro das restrições conhecidas. O mesmo estilo pode ser apropriado em um contexto e inadequado em outro. Por isso, a unidade de raciocínio deste encontro será:

> contexto → força priorizada → alternativas → consequências → evidência → decisão revisável

Consulte o [glossário compartilhado](../referencia/glossario.md) sempre que um termo novo aparecer. Para transformar expressões vagas como “rápido” ou “fácil de manter” em cenários, use a página de [atributos de qualidade](../referencia/atributos-de-qualidade.md). O registro final segue o [template de ADR](../referencia/template-adr.md), usado também no projeto integrador.

## Percurso em oito páginas

1. **Visão geral:** delimita problema, resultado e contrato do encontro.
2. **Conceitos:** apresenta o que é um estilo arquitetural e o mapa das quatro famílias de decisão.
3. **Padrões e decisões:** aprofunda Camadas, Pipes and Filters, Microkernel e Monólito modular, com figuras, características e anti-padrões, e apresenta o ADR.
4. **Exemplo arquitetural:** aplica os estilos ao caso hospitalar, da reserva em camadas ao pipeline de faturamento.
5. **Estudo de caso:** compara alternativas para a plataforma hospitalar com forças e evidências.
6. **Oficina de ferramentas:** executa os três exemplos de estilos e captura evidências de comportamento.
7. **Exercícios:** pratica os seis níveis da Taxonomia de Bloom.
8. **Síntese e referências:** consolida o método e aponta fontes públicas.

## Como estudar

Leia as três primeiras páginas em ordem: elas constroem o vocabulário antes de introduzir o caso hospitalar. No exemplo, pergunte a cada elemento “qual responsabilidade está aqui?” e “como ele se comunica?”. Na oficina, não se limite a obter uma saída verde: compare o resultado antes e depois de mudar uma condição. Nos exercícios avançados, preserve hipóteses e declare o que ainda precisaria ser medido.

O módulo oferece três profundidades. **Essencial em aula** cobre vocabulário, comparação básica e evidência executável. **Exploração em dupla** acrescenta discussão de alternativas e alteração de condições. **Extensão** conecta cenários mais exigentes e verificação de fronteiras. As três trilhas usam a mesma baseline; aprofundar não significa criar uma solução paralela.

## Antes da oficina: o que você fará de fato

A [oficina](oficina-de-ferramentas.md) usa os três exemplos executáveis do repositório — um sistema em camadas, um pipeline de filtros e um núcleo com plugins. Você executará cada exemplo, guardará a saída, alterará uma condição e comparará o antes e o depois, relacionando a diferença observada à responsabilidade arquitetural do estilo. Os exercícios avançados continuam o trabalho no laboratório da plataforma hospitalar.

## Entregas do encontro

Ao concluir, guarde artefatos pequenos e conectados: as saídas de antes e depois de cada experimento com uma nota do que a diferença revelou, as entregas dos exercícios do seu nível e um mini-ADR registrando uma decisão com contexto, alternativas e consequências. Nenhum artefato prova sozinho que a arquitetura é adequada; em conjunto, eles mostram como a decisão foi formulada e onde a turma pode revisar a hipótese.

O [incremento 1 do projeto integrador](../projeto-integrador/incrementos.md#incremento-1-estrutura-e-decisoes-iniciais) reutiliza esses artefatos para formar a primeira baseline da plataforma. A intenção não é prever todos os encontros, mas iniciar uma cadeia de decisões coerente e evolutiva.
