# Projeto integrador: plataforma hospitalar

O projeto integrador conecta os seis encontros em uma única decisão arquitetural evolutiva. Você trabalhará como arquiteto ou arquiteta de uma plataforma hospitalar que troca informações com planos de saúde e laboratórios. O desafio é arquitetural: não exige conhecimento clínico nem decisões sobre diagnóstico ou tratamento.

Em vez de criar seis soluções independentes, a turma mantém uma baseline de arquitetura. A cada encontro, novas decisões, contratos e evidências são incorporados ao que já existe. Uma decisão anterior pode ser revisada, desde que a mudança e suas consequências sejam registradas.

## Comece por aqui

1. Leia o [contexto hospitalar](contexto-hospitalar.md) e delimite o problema.
2. Consulte os [seis incrementos](incrementos.md) antes de iniciar cada encontro.
3. Use os [modelos de entrega](modelos-de-entrega.md) para manter os artefatos comparáveis.
4. Verifique os [critérios de avaliação](criterios-de-avaliacao.md) durante o trabalho, não apenas ao final.

## A linha cumulativa

| Encontro | Pergunta arquitetural | Evolução da baseline |
| --- | --- | --- |
| 1 — Estilos | Como organizar responsabilidades e justificar a estrutura inicial? | Contexto, atributos de qualidade, estilo e primeiro ADR |
| 2 — APIs | Como preservar significado e segurança nas integrações? | Contratos externos acrescentados à arquitetura inicial |
| 3 — Serviços | Onde ficam limites, dados e coordenação distribuída? | Componentes e responsabilidades refinados a partir dos contratos |
| 4 — Governança | Como tornar decisões e operação consistentes entre serviços? | Políticas, telemetria e evolução dos contratos |
| 5 — Eventos | Onde a colaboração assíncrona reduz acoplamento sem ocultar riscos? | Eventos, consistência e recuperação incorporados aos fluxos existentes |
| 6 — Nuvem | Como operar a solução sob falhas e demanda variável? | Topologia, observabilidade, recuperação e evidência final |

## Resultado esperado

Ao final, a entrega forma um dossiê arquitetural coerente: modelos conectados, ADRs, contratos, decisões sobre dados e eventos, controles de governança, visão de implantação e evidências reproduzíveis. O objetivo não é acumular diagramas, mas demonstrar por que a solução evoluiu e como se pode verificar se as decisões atendem ao contexto.

Termos novos podem ser consultados no [glossário](../referencia/glossario.md); padrões recorrentes estão reunidos no [catálogo de padrões](../referencia/catalogo-de-padroes.md).
