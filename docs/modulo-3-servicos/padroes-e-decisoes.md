# Padrões e decisões: escolher o grau de distribuição

Arquitetura de serviços não oferece uma escada em que microsserviços ocupam o último degrau. Existem formas diferentes de empacotar limites lógicos. A escolha deve ligar forças do contexto a consequências verificáveis.

## Monólito modular, macrosserviços e microsserviços

Um **monólito modular** possui uma unidade de implantação, mas separa o código em módulos com interfaces e dependências controladas. Uma transação local pode atravessar módulos sob regras explícitas. Ele simplifica operação e depuração; exige disciplina para impedir referências arbitrárias e um banco sem proprietário.

Um **macrosserviço** é uma unidade implantável maior que reúne capacidades fortemente relacionadas. O termo é útil para sair da falsa dicotomia entre um sistema inteiro e dezenas de serviços minúsculos. Pode corresponder a uma área de negócio mantida por uma equipe, com módulos internos fortes. Reduz viagens de rede e coordenação operacional, mas uma implantação afeta uma superfície maior.

Um **microsserviço** busca autonomia de implantação, operação e dados em uma responsabilidade coesa. Favorece escalabilidade seletiva, isolamento de mudanças e ownership quando esses benefícios existem. Cobra automação de entrega, contratos, observabilidade, segurança de rede, capacidade de resposta a incidentes e tratamento de falhas parciais.

| Aspecto | Monólito modular | Macrosserviço | Microsserviço |
| --- | --- | --- | --- |
| Implantação | uma para o sistema | uma por conjunto amplo | uma por limite menor |
| Chamada dominante | local | local e remota | remota entre limites |
| Transação | local com maior alcance | local dentro do conjunto | local por proprietário |
| Operação | menor variedade | intermediária | maior variedade |
| Autonomia | lógica | por área ampla | física e organizacional |
| Risco típico | erosão dos módulos | unidade crescer sem revisão | monólito distribuído |

Comece perguntando se há necessidade de implantação independente, escalabilidade diferente, isolamento regulatório, tecnologias especializadas ou equipes com ownership real. Sem essas forças, a fronteira interna costuma preservar mais simplicidade.

## Banco por serviço como proteção da autoridade

O padrão banco por serviço protege invariantes e evolução. Cada serviço decide schema, migrações e regras de escrita. Outro serviço não faz `SELECT`, `JOIN` ou `UPDATE` direto. A proteção deve ser concreta: credenciais distintas, permissões mínimas e testes arquiteturais.

“Por serviço” descreve propriedade, não necessariamente uma máquina. Opções incluem schemas separados no mesmo PostgreSQL, bancos separados no mesmo servidor ou instâncias separadas. O isolamento cresce junto com custo operacional. O laboratório escolhe dois contêineres PostgreSQL e dois schemas homônimos para que a violação seja evidente.

Consultas que atravessam limites podem ser resolvidas por composição síncrona, cópias orientadas a eventos, plataforma analítica ou modelo materializado. Cada alternativa troca frescor, disponibilidade, complexidade e custo. Não use acesso compartilhado como atalho silencioso.

## Consistência local e consistência entre serviços

Dentro de um serviço, uma transação ACID pode preservar invariantes locais. Entre serviços, não existe rollback automático de todas as decisões. É preciso definir quando o usuário considera o fluxo aceito, quais estados intermediários são legítimos e como detectar ou reparar divergências.

Consistência forte é útil quando uma leitura precisa refletir a escrita mais recente. Consistência eventual permite uma janela de defasagem, desde que o domínio aceite isso, a janela seja observável e haja convergência. **Consistência eventual não significa** ausência de regras; exige identidade, ordem quando necessária, idempotência, repetição e reconciliação.

## CAP sem o triângulo simplista

O teorema CAP trata um armazenamento distribuído quando existe partição de comunicação. Consistência, nesse modelo, aproxima-se de uma visão única e atual; disponibilidade exige resposta de cada nó não falho; tolerância à partição reconhece mensagens perdidas ou atrasadas entre grupos. Em uma rede sujeita a partições, o sistema precisa decidir entre recusar ou atrasar operações para preservar consistência, ou responder aceitando possível divergência.

Portanto, **CAP se torna uma decisão durante uma partição**, não uma classificação cotidiana em que um produto escolhe livremente duas letras. Fora da partição, latência e consistência ainda geram decisões descritas por outros modelos. Também não devemos usar CAP para justificar qualquer dado desatualizado em uma integração: é necessário especificar mecanismo e promessa.

## SAGA

Uma **SAGA** coordena uma sequência de transações locais. Cada etapa confirma seu próprio estado; se uma etapa posterior falha, ações compensatórias semanticamente adequadas tentam neutralizar efeitos anteriores. Coordenação pode ser coreografada por eventos ou orquestrada por um componente que conhece a sequência.

**SAGA não é uma transação ACID distribuída**. Uma compensação não apaga o passado e pode falhar. Cancelar uma solicitação não equivale a ela nunca ter existido; mensagens podem duplicar; outros participantes podem ter observado estados intermediários. O desenho precisa declarar estados, comandos idempotentes, políticas de repetição, intervenção operacional e trilha de auditoria.

No caso hospitalar, uma SAGA poderia coordenar reservar agenda, autorizar procedimento e preparar recurso. Ela não é necessária para o laboratório de dois passos: Exames consulta Elegibilidade antes de gravar localmente. Introduzir um orquestrador ali aumentaria componentes sem demonstrar benefício.

## CQRS

**CQRS** separa modelos de comando e consulta quando eles possuem necessidades realmente diferentes. Comandos expressam intenção e preservam invariantes; consultas oferecem projeções adequadas a leitura. **CQRS não exige dois bancos**, mensageria ou Event Sourcing. A separação pode começar em objetos e interfaces dentro do mesmo processo.

Um modelo de leitura materializado pode reduzir composições remotas e atender consultas de alto volume, mas cria atualização, defasagem, reconstrução e monitoramento. Por isso, **não aplique CQRS por padrão**. Use quando a assimetria entre leitura e escrita, a complexidade dos modelos ou a escala justificarem a duplicação e sua governança.

CQRS e SAGA resolvem problemas diferentes. SAGA coordena mudança distribuída; CQRS separa responsabilidades de ler e escrever. Eles podem coexistir, mas nenhum depende automaticamente do outro.

## Chamadas síncronas: orçamento de falha

Antes de adicionar uma chamada, documente timeout, política de repetição, idempotência, propagação de identidade, códigos de erro e telemetria. Uma cadeia de cinco serviços pode produzir latência acumulada e disponibilidade inferior à de cada participante. Paralelismo reduz tempo em alguns casos, porém não elimina dependências.

No laboratório, Exames usa timeout de dois segundos e converte indisponibilidade de Elegibilidade em `503`. Não repete automaticamente porque a consulta é rápida, mas uma tempestade de repetições durante queda poderia piorar recuperação. O contrato diferencia beneficiário desconhecido, inelegível, resposta inválida e dependência fora do ar.

## Registro de decisão

Uma decisão defensável registra contexto, alternativas, forças, consequência e sinal de revisão. Exemplo: “Manter Elegibilidade e Exames em processos distintos porque possuem propriedade de dados e ritmos de mudança diferentes; aceitar chamada síncrona porque a decisão é necessária antes da escrita; revisar se indisponibilidade conjunta ou volume ultrapassarem metas”. Essa formulação é superior a “usar microsserviços porque escala”.

## Equivalências em Java e .NET

SAGA pode ser implementada com máquinas de estado e mensageria em qualquer ecossistema, mas bibliotecas não removem a necessidade de compensações de domínio. Java oferece Spring Transaction para transações locais, Resilience4j para timeout e circuit breaker e Spring Modulith para reforçar módulos. .NET oferece transações locais, `IHttpClientFactory`, políticas de resiliência e soluções de mensageria compatíveis.

CQRS pode ser apenas a separação entre handlers de comando e serviços de consulta. MediatR é comum em .NET; padrões equivalentes podem ser construídos com interfaces Spring em Java. Em ambos, banco por serviço deve ser protegido por usuários e permissões PostgreSQL, não apenas por convenção de código.
