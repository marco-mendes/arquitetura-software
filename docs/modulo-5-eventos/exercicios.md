# Exercícios: decidir integrações assíncronas

As propostas usam o caso hospitalar e dados sintéticos. Não há resposta única: declare premissas, diferencie fato de hipótese e trate contrato, falha e operação como parte da decisão. Cada atividade produz um artefato autocontido, sem depender de configuração manual em um ambiente remoto.

## Recordar

### Nomear semântica e componentes

**Situação**

Uma equipe recebeu os nomes `ResultadoLaboratorialDisponibilizado.v1`, `GerarCobranca`, `hospital.events`, `billing.resultados.v1`, `hospital.events.dlx` e `billing.resultados.v1.dlq`, mas mistura intenção de domínio e elemento de transporte.

**Seu papel**

Você prepara um glossário de entrada para a equipe.

**Insumos disponíveis**

As páginas do módulo, o código do laboratório e a topologia RabbitMQ local.

**Como conduzir**

1. Defina evento, comando, mensagem, broker, mediator, fila, tópico e log distribuído.
2. Relacione cada nome da situação a uma definição.
3. Defina entrega pelo menos uma vez, idempotência, ordenação e dead-letter queue.
4. Dê um exemplo de consequência se dois termos forem confundidos.

**Entrega esperada**

Um glossário de uma página com definição, exemplo hospitalar e limite de cada termo.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Precisão das definições | 35% |
| Relação entre domínio e infraestrutura | 35% |
| Limites e consequências identificados | 30% |

## Compreender

### Explicar a repetição sem prometer magia

**Situação**

Uma pessoa afirma que, se RabbitMQ confirmar a publicação, Faturamento nunca verá uma mensagem duas vezes. Outra propõe ignorar todos os redeliveries para evitar cobrança repetida.

**Seu papel**

Você explica o ciclo de falha e propõe linguagem correta para a equipe.

**Insumos disponíveis**

O diagrama de sequência do módulo, o store SQLite e os conceitos de confirmação e transação local.

**Como conduzir**

1. Descreva uma queda entre escrita local e confirmação ao broker.
2. Explique por que a repetição protege contra perda em vez de ser sempre defeito.
3. Diferencie tentativa, confirmação e efeito de negócio.
4. Explique por que `event_id` e uma restrição durável ajudam.

**Entrega esperada**

Uma explicação ilustrada com uma linha do tempo de duas tentativas e um efeito.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Sequência de falha coerente | 30% |
| Uso correto de idempotência | 35% |
| Distinção entre transporte e negócio | 35% |

## Aplicar

### Modelar uma reação administrativa

**Situação**

Além de Faturamento, a plataforma precisa atualizar uma projeção administrativa quando um resultado fica disponível. A projeção aceita alguns minutos de atraso, mas não pode contar o mesmo exame duas vezes. Ela não precisa receber conteúdo clínico.

**Seu papel**

Você desenha o contrato e a reação mínima para a nova capacidade.

**Insumos disponíveis**

O evento da oficina, a exchange `hospital.events`, referências sintéticas, uma tabela própria da projeção e a hipótese de que mensagens podem repetir e chegar atrasadas.

**Como conduzir**

1. Declare se a entrada é evento, comando ou consulta e justifique.
2. Escreva o payload mínimo, a identidade de deduplicação e a versão de contrato.
3. Defina fila ou tópico, owner e política de confirmação.
4. Mostre como um efeito será único após duas entregas iguais.
5. Declare o atraso aceitável e como a interface representa estado pendente.
6. Inclua uma condição que envia uma mensagem à DLQ.

**Entrega esperada**

Um contrato, diagrama de fluxo, pseudocódigo de consumidor e plano de evidências locais.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Semântica e ownership explícitos | 20% |
| Payload mínimo e versionamento | 20% |
| Idempotência verificável | 25% |
| Consistência eventual comunicada | 20% |
| Falha e DLQ tratadas | 15% |

## Analisar

### Investigar uma fila que cresce

**Situação**

Após uma mudança de contrato, a fila `billing.resultados.v1` cresce, a DLQ recebe mensagens e parte das cobranças fica pendente. A equipe possui idade da mensagem mais antiga, contagem por fila, amostras sintéticas de `event_id`, logs de validação e a versão publicada por Resultados. Não há evidência de indisponibilidade do broker.

**Seu papel**

Você analisa causas plausíveis sem concluir além das evidências.

**Insumos disponíveis**

As métricas descritas, os schemas de `v1` e uma mudança proposta que tornou uma referência obrigatória.

**Como conduzir**

1. Separe fatos, inferências e hipóteses.
2. Compare incompatibilidade de schema, capacidade insuficiente e dependência do consumidor.
3. Explique como cada hipótese apareceria em fila, DLQ e store de tentativas.
4. Proponha uma verificação reproduzível para reduzir incerteza.
5. Indique ação segura de contenção e a decisão que exigiria owner do contrato.
6. Declare o que não se pode deduzir apenas pela contagem de mensagens.

**Entrega esperada**

Um diagnóstico com linha do tempo, mapa de evidências, hipóteses alternativas e plano de investigação.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Separação de evidência e hipótese | 25% |
| Comparação de causas plausíveis | 25% |
| Uso dos sinais de fila e DLQ | 20% |
| Verificação segura proposta | 20% |
| Limites da conclusão | 10% |

## Avaliar

### Escolher fila ou log para novo consumidor

**Situação**

Qualidade quer recalcular indicadores de exames por mês; Faturamento precisa tratar uma unidade de trabalho por vez; ambos consomem fatos de resultados. A organização consegue operar um broker local hoje, mas a necessidade de reprocessamento histórico ainda é uma hipótese. A referência de resultado tem classificação sensível e não pode ser retida sem prazo e justificativa.

**Seu papel**

Você recomenda uma decisão inicial e condições objetivas de revisão.

**Insumos disponíveis**

O laboratório RabbitMQ, a descrição de tópicos e logs distribuídos, estimativa de volume mensal e owners de Faturamento e Qualidade.

**Como conduzir**

1. Compare fila RabbitMQ e log Kafka quanto a trabalho, leitura independente, replay, retenção e operação.
2. Avalie o que é requisito comprovado e o que ainda é hipótese.
3. Declare chave de ordenação necessária e o que ela não ordena.
4. Inclua idempotência para o efeito de Faturamento em ambas as alternativas.
5. Defina regra de retenção e proteção de referência antes de sugerir replay.
6. Registre gatilhos mensuráveis para reavaliar a escolha.

**Entrega esperada**

Um registro de decisão com alternativas, escolha, consequências, riscos, sinais e condição de retorno.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Comparação contextual das alternativas | 25% |
| Requisitos e hipóteses separados | 20% |
| Ordem, retenção e dados tratados | 20% |
| Idempotência ponta a ponta | 20% |
| Gatilhos de revisão mensuráveis | 15% |

## Criar

### Projetar evolução `v2` de resultado

**Situação**

Resultados precisa acrescentar uma classificação administrativa que alguns consumidores usarão. Um consumidor antigo só entende `ResultadoLaboratorialDisponibilizado.v1`; Faturamento não pode parar nem cobrar duas vezes. A nova classificação não deve revelar conteúdo clínico e a transição precisa ser observável.

**Seu papel**

Você cria um plano de evolução e convivência entre consumidores.

**Insumos disponíveis**

O contrato `v1`, lista de consumers, tópicos ou filas disponíveis, store idempotente e uma janela de transição definida pela equipe responsável.

**Como conduzir**

1. Classifique a mudança como compatível ou incompatível e justifique.
2. Defina `v2` ou campo opcional, exemplos sintéticos e owner do contrato.
3. Descreva publicação dupla ou adaptação, com início e fim observáveis.
4. Mantenha a chave de deduplicação através da transição.
5. Planeje validação, DLQ, métricas de consumidores e retorno seguro.
6. Registre como remover `v1` depois da migração confirmada.

**Entrega esperada**

Um pacote com contrato versionado, diagrama de convivência, plano de rollout, sinais e critérios de retirada.

**Critérios de avaliação**

| Critério | Peso |
| --- | ---: |
| Semântica da evolução | 20% |
| Compatibilidade e transição | 20% |
| Preservação de idempotência | 20% |
| Observabilidade e recuperação | 20% |
| Proteção de dados e ownership | 20% |
