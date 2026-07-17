# Exercícios: decidir antes de distribuir

As atividades percorrem a Taxonomia de Bloom. Use o vocabulário do módulo e declare premissas. Nas atividades avançadas, o caso, os insumos, a condução, a entrega e os critérios estão completos; não há solução canônica nem resposta embutida.

## Recordar

1. Defina capacidade de negócio e dê um exemplo hospitalar.
2. Diferencie bounded context de microsserviço em duas frases.
3. Liste quatro formas de acoplamento apresentadas no módulo.
4. Explique o que banco por serviço proíbe.
5. Nomeie as três formas de implantação comparadas.
6. Defina falha parcial.
7. Indique o papel de timeout em uma chamada síncrona.
8. Declare a condição em que CAP força uma escolha.
9. Resuma SAGA sem usar a expressão “rollback global”.
10. Resuma CQRS sem pressupor bancos separados.

## Compreender

1. Explique por que mover duas funções para processos diferentes não reduz automaticamente acoplamento.
2. Descreva como alta coesão pode ser prejudicada por serviços pequenos demais.
3. Compare propriedade de dados com localização física do banco.
4. Explique por que `503 dependencia_indisponivel` comunica melhor a falha do laboratório do que um `500` genérico.
5. Mostre por que consistência eventual ainda exige regras de convergência.
6. Dê um cenário em que monólito modular seja preferível e outro em que implantação independente seja necessária.
7. Explique por que uma compensação de SAGA não apaga fatos já observados.
8. Descreva a diferença de propósito entre SAGA e CQRS.

## Aplicar

### Delimitar o fluxo de laudos

**Situação**

Uma clínica possui um sistema único. O módulo de Laudos recebe o resultado técnico, aplica assinatura do profissional e publica o documento. O módulo de Notificações envia aviso depois da publicação. Ambos usam tabelas sem proprietário. A equipe quer melhorar os limites sem distribuir imediatamente.

**Seu papel**

Você atua como arquiteto responsável por propor uma primeira separação lógica executável.

**Insumos disponíveis**

Capacidades “emitir laudo” e “notificar disponibilidade”; uma equipe; implantação semanal conjunta; uma transação local protege assinatura e publicação; notificações podem atrasar cinco minutos; volume estável.

**Como conduzir**

1. Nomeie os bounded contexts e seus termos centrais.
2. Aloque tabelas e operações a um proprietário.
3. Desenhe interfaces internas e dependências permitidas.
4. Indique um evento interno possível e sua semântica.
5. Escolha monólito modular, macrosserviço ou microsserviços para a primeira etapa.
6. Registre um sinal que justificaria revisar a forma de implantação.

**Entrega esperada**

Uma página com mapa de contexto, direção das dependências, decisão de implantação e duas guardas automatizáveis. Inclua uma suposição e um risco.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Limites alinhados às capacidades e invariantes | 30% | Evidência: capacidade e regra; insuficiente: limite técnico arbitrário. |
| Propriedade de dados explícita | 25% | Evidência: dono do dado; insuficiente: banco compartilhado sem regra. |
| Dependências e contratos coerentes | 20% | Evidência: direção e contrato; insuficiente: acesso direto oculto. |
| Decisão ligada aos insumos | 15% | Evidência: insumo citado; insuficiente: decisão sem contexto. |
| Riscos e sinais de revisão | 10% | Evidência: risco e sinal; insuficiente: revisão sem condição. |

## Analisar

### Diagnosticar um monólito distribuído

**Situação**

Uma plataforma possui serviços Cadastro, Agenda, Atendimento e Faturamento. Todos acessam o mesmo schema. Para abrir atendimento, a API chama Cadastro, Agenda e Faturamento em sequência. Uma mudança de campo exige quatro implantações. A disponibilidade mensal individual é 99,9%, mas o fluxo tem incidentes frequentes.

**Seu papel**

Você lidera a análise de dependências antes de qualquer reestruturação.

**Insumos disponíveis**

Mapa de chamadas: Atendimento → Cadastro → Agenda → Faturamento. Histórico: 70% das mudanças em Cadastro e Atendimento ocorrem juntas; Agenda escala dez vezes em horários de entrada; Faturamento pertence a outro time; o fluxo exige cadastro válido, mas não precisa confirmar faturamento imediatamente. Não há eventos nem idempotência.

**Como conduzir**

1. Classifique acoplamento temporal, de dados, de contrato, implantação e organização.
2. Identifique quais dependências estão no caminho crítico sem necessidade declarada.
3. Relacione coevolução e escalabilidade aos limites possíveis.
4. Compare pelo menos duas alternativas de consolidação ou extração.
5. Modele uma falha parcial e a resposta visível ao consumidor.
6. Explique que evidência adicional mudaria sua análise.

**Entrega esperada**

Um diagnóstico de até duas páginas, acompanhado por diagrama atual e diagrama candidato. Não implemente. Faça distinção entre fato fornecido, inferência e hipótese.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Classificação precisa dos acoplamentos | 25% | Evidência: tipo e causa; insuficiente: dependência nomeada genericamente. |
| Uso consistente dos dados do caso | 25% | Evidência: fatos referenciados; insuficiente: dado inventado. |
| Comparação de alternativas | 20% | Evidência: consequências contrastadas; insuficiente: opção apenas listada. |
| Análise de falha parcial | 20% | Evidência: parte saudável e falha; insuficiente: sistema tratado como inteiro. |
| Separação entre fato e hipótese | 10% | Evidência: hipótese rotulada; insuficiente: suposição como fato. |

## Avaliar

### Escolher consistência para autorização prévia

**Situação**

Uma rede de diagnóstico quer continuar recebendo solicitações durante indisponibilidade de até quinze minutos do provedor de autorizações. A autorização pode mudar a qualquer momento. Executar procedimento sem autorização gera risco operacional; perder uma solicitação também é inaceitável. Hoje, a API responde erro e o usuário reenvia manualmente.

**Seu papel**

Você participa do comitê que precisa escolher entre falha explícita, recepção pendente, cache de decisão ou outro desenho fundamentado.

**Insumos disponíveis**

Meta: nenhuma execução sem autorização válida. Solicitações possuem identificador único. Operadores aceitam estado “pendente” por até trinta minutos. O provedor oferece consulta HTTP, mas não publica eventos. Há equipe operacional em horário comercial. Não existe transação distribuída com o provedor.

**Como conduzir**

1. Defina o momento em que uma solicitação é considerada recebida e quando pode ser executada.
2. Compare ao menos três alternativas por segurança, disponibilidade, consistência e operação.
3. Avalie se SAGA descreve alguma sequência e quais compensações seriam possíveis.
4. Avalie se CQRS resolveria um problema concreto ou apenas adicionaria modelos.
5. Escolha uma alternativa e registre condições de revisão.
6. Declare estados intermediários, timeout, repetição e idempotência.

**Entrega esperada**

Um registro de decisão arquitetural com contexto, alternativas, decisão, consequências, fluxo de estados e plano de observação. Não há exigência de um padrão específico.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Critérios ligados ao risco do domínio | 30% | Evidência: risco orienta critério; insuficiente: critério técnico solto. |
| Comparação equilibrada das alternativas | 25% | Evidência: custo e ganho; insuficiente: padrão escolhido sem contraste. |
| Tratamento de estados e falhas | 20% | Evidência: transição e falha; insuficiente: fluxo só feliz. |
| Uso criterioso de SAGA e CQRS | 15% | Evidência: necessidade justifica padrão; insuficiente: sigla sem problema. |
| Condições de revisão e observação | 10% | Evidência: sinal e revisão; insuficiente: monitoramento sem decisão. |

## Criar

### Projetar uma evolução verificável

**Situação**

O hospital integrador ampliará a plataforma com Agendamento. Essa capacidade consulta Elegibilidade, reserva um horário e solicita preparo de sala. Elegibilidade já existe como no laboratório. Agenda muda com frequência e recebe picos; Preparo de Sala é operado por outra equipe e aceita processamento em até dois minutos.

**Seu papel**

Você criará uma proposta que possa começar simples e evoluir sem esconder propriedade ou falhas.

**Insumos disponíveis**

Contratos atuais de Elegibilidade; meta de resposta inicial em três segundos; identificador de solicitação fornecido pelo consumidor; PostgreSQL disponível; mensageria é permitida, mas ainda não está instalada; a equipe consegue operar no máximo três novas unidades implantáveis neste semestre.

**Como conduzir**

1. Modele capacidades, bounded contexts, comandos, consultas e proprietários.
2. Escolha unidades de implantação para a primeira versão.
3. Desenhe fluxo nominal e ao menos três falhas parciais.
4. Declare consistência de cada estado e eventual compensação.
5. Defina contratos mínimos, idempotência e telemetria.
6. Crie um plano em duas etapas com gatilhos mensuráveis para extração ou consolidação.
7. Especifique testes de contrato, fronteira e recuperação.

**Entrega esperada**

Um pacote autocontido com dois diagramas, registro de decisão, tabela de estados, contratos de exemplo, estratégia de testes e roteiro de evolução. Limite-se aos componentes necessários para justificar a arquitetura.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Coerência entre domínio, dados e implantação | 25% | Evidência: mesmos limites; insuficiente: topologia contradiz domínio. |
| Fluxos de falha e consistência explícitos | 25% | Evidência: falha e efeito; insuficiente: consistência presumida. |
| Contratos e verificações executáveis | 20% | Evidência: teste ou comando; insuficiente: contrato sem verificação. |
| Evolução orientada por sinais | 15% | Evidência: sinal aciona mudança; insuficiente: evolução sem gatilho. |
| Viabilidade operacional dentro dos insumos | 15% | Evidência: recursos considerados; insuficiente: componente sem operação possível. |
