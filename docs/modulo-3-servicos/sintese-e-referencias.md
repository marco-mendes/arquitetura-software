# Síntese e referências

Arquitetura de serviços começa com responsabilidade, não com rede. Capacidade de negócio ajuda a reconhecer resultados estáveis. Bounded context delimita linguagem e modelo. Coesão mantém juntas regras que mudam juntas; análise de acoplamento expõe dependências de contrato, tempo, dados, implantação e organização.

Monólito modular, macrosserviço e microsserviço são alternativas legítimas. A forma distribuída precisa de uma razão: autonomia de equipe e implantação, escala distinta, isolamento ou necessidade tecnológica. Sem isso, módulos fortes preservam opções com menor carga operacional.

Banco por serviço protege a autoridade sobre dados. Consumidores integram por contrato, evento ou projeção projetada, nunca por tabela alheia. Chamada síncrona é apropriada quando a resposta é necessária imediatamente, mas cria acoplamento temporal. Timeout e erro explícito tornam falhas parciais controláveis; repetição, fallback e circuit breaker dependem da semântica.

Consistência entre serviços requer estados intermediários e reconciliação. CAP explica a escolha de comportamento durante partições, não um rótulo universal. SAGA coordena transações locais com compensações imperfeitas. CQRS separa modelos de comando e consulta quando a assimetria justifica. Nenhum dos dois é requisito de microsserviços.

## Checklist de decisão

- O limite corresponde a linguagem, invariantes e capacidade reconhecíveis?
- Há um proprietário para cada dado e somente ele escreve?
- Existe necessidade comprovada de implantação independente?
- Chamadas síncronas têm timeout, erros e observação definidos?
- Estados intermediários e modelo de consistência são aceitáveis ao negócio?
- A equipe consegue operar a quantidade de unidades proposta?
- Existem testes de contrato e fronteira sem dependência de internals?
- A decisão registra sinais para consolidar ou extrair no futuro?

## Referências fundamentais e oficiais

- Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) — síntese pública de bounded context e outros padrões de modelagem.
- Martin Fowler e James Lewis, [Microservices](https://martinfowler.com/articles/microservices.html) — caracterização influente do estilo e de suas consequências.
- Martin Fowler, [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) — argumento para estabilizar limites antes de distribuir.
- Microsoft Azure Architecture Center, [CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) e [Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga) — descrições, forças e limitações.
- AWS Prescriptive Guidance, [Database per service](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/database-per-service.html) — propriedade e alternativas de persistência.
- Seth Gilbert e Nancy Lynch, [Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services](https://dl.acm.org/doi/10.1145/564585.564601) — formulação e prova formal relacionadas a CAP.
- PostgreSQL, [documentação atual](https://www.postgresql.org/docs/current/) — schemas, roles, transações e operação.
- Docker, [Compose file reference](https://docs.docker.com/reference/compose-file/) e [control startup order](https://docs.docker.com/compose/how-tos/startup-order/) — definição oficial de serviços, dependências e health checks.
- FastAPI, [documentação oficial](https://fastapi.tiangolo.com/) — aplicações, dependências e testes HTTP.
- Python, [guia de ambientes e plataformas](https://docs.python.org/3/using/index.html) — instalação nos sistemas usados na oficina.
- Spring, [Spring Boot reference](https://docs.spring.io/spring-boot/index.html) e [.NET, ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/) — equivalentes de implementação.

## Equivalências em Java e .NET

Java, .NET e Python podem materializar a mesma arquitetura. Spring Boot, ASP.NET Core e FastAPI oferecem HTTP e injeção de dependência. Drivers PostgreSQL protegem cada conexão com credenciais próprias. Clientes HTTP tratam timeout e respostas. Testes substituem somente a fronteira remota, não chamam internals do provedor.

Escolher um framework por familiaridade é aceitável; inferir estilo arquitetural a partir dele não é. A evidência relevante continua sendo a direção das dependências, a propriedade do estado, a autonomia de implantação necessária e o comportamento durante falhas.

## Continuidade

O próximo módulo aprofunda governança: como contratos, ownership, políticas e observabilidade sustentam vários serviços ao longo do tempo. Leve consigo a pergunta central deste módulo: qual é o menor grau de distribuição que preserva a autonomia necessária sem esconder custos?
