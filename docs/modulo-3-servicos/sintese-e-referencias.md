# Síntese e referências

A arquitetura de serviços começa pela definição de responsabilidades e só depois trata da rede. A capacidade de negócio ajuda a reconhecer resultados estáveis da organização, enquanto o *bounded context* delimita a linguagem e o modelo de cada parte do sistema. A coesão mantém juntas as regras que mudam pelo mesmo motivo. A análise de acoplamento expõe as dependências de contrato, de tempo e de dados, além das dependências de implantação e de organização.

Monólito modular, macrosserviço e microsserviço são alternativas legítimas de empacotamento dos limites lógicos. A forma distribuída precisa de uma razão concreta, como autonomia de equipe e de implantação ou escala distinta entre capacidades. Isolamento regulatório e necessidade tecnológica também são razões aceitas. Na ausência dessas razões, módulos fortes num único processo preservam as opções futuras com menor carga operacional.

O banco por serviço protege a autoridade de cada serviço sobre os próprios dados. Os consumidores integram por contrato, evento ou projeção e não acessam a tabela de outro serviço. A chamada síncrona é apropriada quando a resposta é necessária imediatamente e cria acoplamento temporal com o provedor. O prazo de espera e o erro explícito tornam as falhas parciais controláveis. A nova tentativa, a resposta alternativa e o disjuntor dependem da semântica da operação, como mostram os programas da ODA 05.

A consistência entre serviços requer estados intermediários legítimos e mecanismos de reconciliação. O teorema CAP explica a escolha de comportamento durante uma partição e não funciona como rótulo universal de um produto. A pergunta útil sobre um armazenamento é o que ele faz quando os nós deixam de se comunicar, porque a resposta do fornecedor se torna restrição do desenho de quem o adota. Quando a escolha é continuar respondendo, a resolução de conflitos usa o carimbo de tempo, uma estrutura que converge por construção ou uma regra de mesclagem do domínio. A SAGA coordena transações locais com compensações que também podem falhar e declara passos, compensações e coordenação por coreografia ou orquestração. O CQRS separa os modelos de comando e de consulta quando a assimetria entre leitura e escrita justifica a duplicação. Nenhum dos dois padrões é requisito para adotar microsserviços, como mostram os programas da ODA 06 executados num único processo.

## Lista de verificação da decisão {#checklist-de-decisao}

- O limite corresponde a linguagem, invariantes e capacidade reconhecíveis?
- Há um proprietário para cada dado e somente ele escreve?
- Existe necessidade comprovada de implantação independente?
- Chamadas síncronas têm prazo de espera, códigos de erro e telemetria definidos?
- Estados intermediários e modelo de consistência são aceitáveis ao negócio?
- A equipe consegue operar a quantidade de unidades proposta?
- Existem testes de contrato e fronteira sem dependência de detalhes internos dos serviços?
- A decisão registra sinais para consolidar ou extrair no futuro?

## Referências fundamentais e oficiais

- Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) — síntese pública de bounded context e outros padrões de modelagem.
- Martin Fowler, [BoundedContext](https://martinfowler.com/bliki/BoundedContext.html) e [UbiquitousLanguage](https://martinfowler.com/bliki/UbiquitousLanguage.html) — o problema do modelo único numa organização grande, com o exemplo do medidor de energia elétrica.
- Chris Richardson, [Decompose by business capability](https://microservices.io/patterns/decomposition/decompose-by-business-capability.html) — capacidade de negócio como critério para definir serviços.
- Martin Fowler e James Lewis, [Microservices](https://martinfowler.com/articles/microservices.html) — caracterização influente do estilo e de suas consequências.
- Martin Fowler, [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) — argumento para estabilizar limites antes de distribuir.
- Microsoft Azure Architecture Center, [CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) e [Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga) — descrições, forças e limitações.
- AWS Prescriptive Guidance, [Database per service](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-persistence/database-per-service.html) — propriedade e alternativas de persistência.
- Seth Gilbert e Nancy Lynch, [Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services](https://dl.acm.org/doi/10.1145/564585.564601) — formulação e prova formal relacionadas a CAP.
- Eric Brewer, [CAP twelve years later: how the "rules" have changed](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/) — o próprio autor desmontando a leitura de "duas de três letras" e situando CAP no intervalo da partição.
- Hector Garcia-Molina e Kenneth Salem, [Sagas](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) — artigo de 1987 que propôs a SAGA para transações de longa duração com compensações.
- Michael Nygard, [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/) — livro que descreveu o disjuntor e os padrões de estabilidade de chamadas entre sistemas.
- Martin Fowler, [CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) — estados fechado, aberto e meio-aberto do disjuntor com exemplo de implementação.
- Marc Brooker, [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) — prazo de espera, nova tentativa e espera exponencial na experiência da Amazon.
- Martin Fowler, [CQRS](https://martinfowler.com/bliki/CQRS.html) — separação entre modelo de comando e modelo de consulta com os riscos da adoção sem necessidade.
- Chris Richardson, [Saga pattern](https://microservices.io/patterns/data/saga.html) — passos, compensações e a comparação entre coreografia e orquestração.
- Marc Shapiro et al., [Conflict-free replicated data types](https://inria.hal.science/inria-00609399) — fundamento das estruturas que convergem independentemente da ordem de aplicação.
- PostgreSQL, [documentação atual](https://www.postgresql.org/docs/current/) — *schemas* e *roles*, transações e operação.
- Docker, [Compose file reference](https://docs.docker.com/reference/compose-file/) e [control startup order](https://docs.docker.com/compose/how-tos/startup-order/) — definição oficial de serviços, dependências e health checks.
- FastAPI, [documentação oficial](https://fastapi.tiangolo.com/) — aplicações, dependências e testes HTTP.
- Python, [guia de ambientes e plataformas](https://docs.python.org/3/using/index.html) — instalação nos sistemas usados na oficina.

## Framework e estilo arquitetural {#o-que-nao-decide-a-arquitetura}

Escolher um *framework* por familiaridade é uma decisão aceitável que não define o estilo arquitetural do sistema. A evidência relevante continua sendo a direção das dependências, a propriedade do estado, a autonomia de implantação necessária e o comportamento durante falhas.

## Continuidade

O próximo módulo trata da governança, que reúne os contratos, as políticas e a observabilidade necessários para sustentar vários serviços ao longo do tempo. A pergunta central deste módulo continua válida no Módulo 4, porque cada decisão de governança depende do menor grau de distribuição que preserva a autonomia necessária sem esconder custos.
