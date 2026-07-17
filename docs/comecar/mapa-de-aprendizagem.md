# Mapa de aprendizagem

Os seis encontros formam uma progressão: primeiro se aprende a descrever estruturas; depois, a projetar interações; em seguida, a distribuir responsabilidades; por fim, a governar, desacoplar e operar a solução.

| Encontro | Pergunta orientadora | Capacidade desenvolvida | Incremento do projeto |
| --- | --- | --- | --- |
| 1 — Estilos | Como reconhecer a forma estrutural de uma solução? | Comparar estilos por restrições e atributos de qualidade | Contexto, forças e decisão de estilo |
| 2 — APIs | Como tornar uma interação explícita e evolutiva? | Projetar contratos e avaliar compatibilidade | Contrato de uma capacidade hospitalar |
| 3 — Serviços | Onde ficam responsabilidades e dados? | Delimitar fronteiras e colaboração distribuída | Mapa de serviços e propriedade de dados |
| 4 — Governança | Como orientar e observar interações em produção? | Definir políticas e sinais operacionais | Políticas, telemetria e decisão registrada |
| 5 — Eventos | Quando a colaboração deve ser assíncrona? | Selecionar padrões e tratar repetição e falha | Eventos, consumidores e garantias |
| 6 — Nuvem | Como sustentar a solução sob mudança e falha? | Projetar implantação, escalabilidade e recuperação | Topologia operacional e estratégia de recuperação |

## Dependências entre os encontros

O contrato do segundo encontro usa o vocabulário estrutural do primeiro. As fronteiras do terceiro dão contexto às políticas do quarto e aos eventos do quinto. O sexto encontro reúne essas decisões em uma topologia implantável. Cada incremento pode revisar decisões anteriores quando uma evidência nova alterar as forças do problema.

## Resultado final

Ao concluir o percurso, o estudante terá um dossiê arquitetural enxuto: contexto, diagramas, contratos, fronteiras, políticas, eventos, topologia e ADRs sustentados por evidências.
