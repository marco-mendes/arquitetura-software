# Catálogo de padrões

Este catálogo localiza os padrões no percurso da disciplina. A escolha de um padrão depende do problema, das forças e das consequências; o nome não substitui a análise.

| Padrão ou estilo | Finalidade principal | Módulo de referência |
| --- | --- | --- |
| Camadas | Separar responsabilidades por níveis de abstração | 1 — Estilos |
| Pipes and Filters | Compor transformações independentes em fluxo | 1 — Estilos |
| Microkernel | Manter um núcleo estável com extensões substituíveis | 1 — Estilos |
| ADR | Registrar contexto, alternativas, decisão e consequências | 1 — Estilos |
| API Gateway | Centralizar entrada e políticas transversais de APIs | 2 — APIs |
| Backend for Frontend | Adaptar contratos às necessidades de uma experiência | 2 — APIs |
| Strangler Fig | Migrar gradualmente uma capacidade existente | 3 — Serviços |
| Saga | Coordenar transações distribuídas por ações e compensações | 3 — Serviços |
| CQRS | Separar modelos de escrita e leitura quando suas forças divergem | 3 — Serviços |
| Chassi de serviço | Padronizar capacidades operacionais recorrentes | 3 — Serviços |
| Gateway com políticas | Aplicar autenticação, limites e roteamento de modo consistente | 4 — Governança |
| Broker | Desacoplar produtores e consumidores por mensageria | 5 — Eventos |
| Mediator | Centralizar coordenação de eventos quando o fluxo exige orquestração | 5 — Eventos |
| Outbox transacional | Publicar mudanças de dados e eventos com recuperação confiável | 5 — Eventos |
| Consumidor idempotente | Tornar repetição de mensagens segura | 5 — Eventos |
| Health checks | Expor condições de vida e prontidão separadamente | 6 — Nuvem |
| Rollback | Retornar a uma versão conhecida após uma implantação inadequada | 6 — Nuvem |

## Leitura recomendada

Ao encontrar um padrão, identifique o contexto em que ele funciona, a força que resolve, a nova complexidade introduzida e a evidência que mostrará se a escolha foi adequada.
