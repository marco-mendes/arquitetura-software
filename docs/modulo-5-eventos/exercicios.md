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

<details>
<summary>Ver resposta</summary>

Evento afirma fato; comando pede ação; mensagem transporta. Broker distribui; mediator coordena. Fila reparte trabalho; tópico copia; log retém leituras.
</details>

2. Relacione cada nome da situação a uma definição.

<details>
<summary>Ver resposta</summary>

`ResultadoLaboratorialDisponibilizado.v1` é evento; `GerarCobranca`, comando. A exchange publica; a fila trabalha; DLX e DLQ recebem rejeições.
</details>

3. Defina entrega pelo menos uma vez, idempotência, ordenação e dead-letter queue.

<details>
<summary>Ver resposta</summary>

Entrega pode repetir; idempotência contém o efeito. Ordem exige chave e fronteira. DLQ guarda rejeições para decisão controlada.
</details>

4. Dê um exemplo de consequência se dois termos forem confundidos.

<details>
<summary>Ver resposta</summary>

Confundir ack com cobrança permite nova cobrança após queda e redelivery.
</details>

**Entrega esperada**

Um glossário de uma página com definição, exemplo hospitalar e limite de cada termo.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Precisão das definições | 35% | Evidência: termo e exemplo; insuficiente: definição circular. |
| Relação entre domínio e infraestrutura | 35% | Evidência: fato separado do transporte; insuficiente: broker tratado como domínio. |
| Limites e consequências identificados | 30% | Evidência: limite descrito; insuficiente: mecanismo sem consequência. |

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

<details>
<summary>Ver resposta</summary>

O consumidor grava no SQLite, cai antes do ack e recebe o mesmo `event_id` novamente.
</details>

2. Explique por que a repetição protege contra perda em vez de ser sempre defeito.

<details>
<summary>Ver resposta</summary>

Sem reentrega, confirmação perdida pode virar trabalho perdido; idempotência contém a repetição.
</details>

3. Diferencie tentativa, confirmação e efeito de negócio.

<details>
<summary>Ver resposta</summary>

Tentativa é processamento visto; ack encerra entrega; cobrança é efeito. Duas tentativas podem produzir uma cobrança.
</details>

4. Explique por que `event_id` e uma restrição durável ajudam.

<details>
<summary>Ver resposta</summary>

`event_id` une tentativas; restrição única durável bloqueia efeito repetido após reinício ou réplica.
</details>

**Entrega esperada**

Uma explicação ilustrada com uma linha do tempo de duas tentativas e um efeito.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Sequência de falha coerente | 30% | Evidência: tentativas ordenadas; insuficiente: falha sem sequência. |
| Uso correto de idempotência | 35% | Evidência: efeito único; insuficiente: duplicação tratada como impossível. |
| Distinção entre transporte e negócio | 35% | Evidência: mensagem e efeito separados; insuficiente: entrega confundida com cobrança. |

## Aplicar

### Modelar uma reação administrativa

**Objetivo**

Projetar uma reação administrativa que permaneça explicável diante de atraso, repetição e rejeição.

**Situação**

A plataforma precisa atualizar projeção administrativa quando um resultado fica disponível. Aceita atraso de minutos, mas não conta o mesmo exame duas vezes nem recebe conteúdo clínico.

**Seu papel**

Você desenha contrato e reação mínima.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/compose.eventos.yml`, `<raiz-do-clone>/laboratorios/plataforma-hospitalar/src/hospital/eventos/publicador.py` e `<raiz-do-clone>/laboratorios/plataforma-hospitalar/src/hospital/eventos/consumidor.py`; definem contrato, filas e deduplicação.

**Antes de executar**

Crie `<raiz-do-clone>/entregas/modulo-5/`. O estado inicial é Compose parado e laboratório imutável; confirme exchange, fila e `event_id`.

**O que fazer**

1. Crie `<raiz-do-clone>/entregas/modulo-5/aplicar-projecao-administrativa.md` e declare se a entrada é evento, comando ou consulta.
2. Copie para o documento um payload sintético mínimo, a versão `v1` e a chave `event_id`; não copie resultado clínico.
3. Desenhe `hospital.events`, fila própria, owner e confirmação após persistência.
4. Simule duas entregas do mesmo `event_id` e um registro.
5. Declare atraso, estado pendente e DLQ.
6. Se faltar `event_id` ou o contrato falhar, rejeite na DLQ.

**Evidência esperada**

Payload `v1`, duas entradas de `event_id`, saída com um `INSERT` e rejeição com nome da DLQ verificam deduplicação sem RabbitMQ.

**Entrega esperada**

Um contrato, diagrama de fluxo, pseudocódigo de consumidor e plano de evidências locais em `<raiz-do-clone>/entregas/modulo-5/aplicar-projecao-administrativa.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Semântica e ownership explícitos | 20% | Evidência: fato e dono; insuficiente: evento sem responsabilidade. |
| Payload mínimo e versionamento | 20% | Evidência: campos necessários e versão; insuficiente: dado excessivo sem justificativa. |
| Idempotência verificável | 25% | Evidência: repetição testada; insuficiente: chave apenas citada. |
| Consistência eventual comunicada | 20% | Evidência: estado pendente explicado; insuficiente: atraso escondido. |
| Falha e DLQ tratadas | 15% | Evidência: rejeição e destino; insuficiente: mensagem perdida sem sinal. |

## Analisar

### Investigar uma fila que cresce

**Objetivo**

Formar hipóteses operacionais sem transformar uma contagem de fila em diagnóstico definitivo.

**Situação**

Após mudança de contrato, `billing.resultados.v1` cresce, a DLQ recebe mensagens e cobranças pendem. Há idade da mensagem, contagem, `event_id` sintético, logs e versão publicada; não há indisponibilidade do broker.

**Seu papel**

Você analisa causas plausíveis sem concluir além das evidências.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/compose.eventos.yml` para `billing.resultados.v1` e `.dlq`, e `<raiz-do-clone>/laboratorios/plataforma-hospitalar/src/hospital/eventos/consumidor.py` para validação e tentativas. Registre métricas e schema `v1` em `<raiz-do-clone>/entregas/modulo-5/analisar-fila-crescente.md`.

**Antes de executar**

O estado inicial é documental: Compose parado, fila e DLQ sintéticas, diagnóstico inexistente. Crie-o, marque observação/hipótese e não altere mensagens reais.

**O que fazer**

1. Escreva uma linha do tempo que separe fatos, inferências e hipóteses.
2. Compare schema, capacidade e dependência nos sinais de fila, DLQ e tentativas.
3. Descreva a saída esperada de cada hipótese.
4. Proponha verificação com payload sintético, sem alterar Compose.
5. Registre uma contenção segura e a decisão que exige owner do contrato.
6. Se o sinal for ambíguo, preserve amostras e peça captura ao owner; não reprocesse.

**Evidência esperada**

Tabela de hipóteses e saídas (`aceita`, `DLQ` ou `tentativa`), payload sintético e verificação segura; contagem isolada não confirma causa.

**Entrega esperada**

Um diagnóstico com linha do tempo, mapa de evidências, hipóteses alternativas e plano de investigação em `<raiz-do-clone>/entregas/modulo-5/analisar-fila-crescente.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Separação de evidência e hipótese | 25% | Evidência: fonte marcada; insuficiente: hipótese vira observação. |
| Comparação de causas plausíveis | 25% | Evidência: causas contrastadas; insuficiente: causa única assumida. |
| Uso dos sinais de fila e DLQ | 20% | Evidência: atraso e rejeição lidos; insuficiente: fila vista sem contexto. |
| Verificação segura proposta | 20% | Evidência: teste sintético; insuficiente: produção alterada para investigar. |
| Limites da conclusão | 10% | Evidência: incerteza declarada; insuficiente: conclusão definitiva cedo. |

## Avaliar

### Escolher fila ou log para novo consumidor

**Objetivo**

Registrar uma decisão proporcional a requisitos de trabalho, replay, retenção e capacidade de operação.

**Situação**

Qualidade recalcula indicadores mensais; Faturamento trata uma unidade por vez; ambos consomem resultados. Há broker local, mas replay histórico é hipótese. A referência sensível exige prazo e justificativa de retenção.

**Seu papel**

Você recomenda uma decisão inicial e condições objetivas de revisão.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/compose.eventos.yml` (RabbitMQ) e `<raiz-do-clone>/docs/modulo-5-eventos/padroes-e-decisoes.md` (Kafka/ActiveMQ). Crie `<raiz-do-clone>/entregas/modulo-5/avaliar-fila-ou-log.md`.

**Antes de executar**

O estado inicial não tem broker adicional: Faturamento/Qualidade são fatos; crescimento/replay, hipóteses. Abra o ADR e separe-as.

**O que fazer**

1. Preencha uma tabela que compare RabbitMQ, Kafka e ActiveMQ quanto a trabalho, leitura independente, replay, retenção, interoperabilidade e operação.
2. Marque requisito comprovado ou hipótese em cada linha.
3. Declare a chave de ordenação e o que ela não ordena.
4. Escreva como Faturamento mantém um efeito idempotente nas duas alternativas finalistas.
5. Defina retenção e proteção da referência antes de sugerir replay.
6. Registre dois gatilhos mensuráveis de revisão; se a estimativa de retenção não estiver disponível, mantenha replay como hipótese e não o aprove.

**Evidência esperada**

ADR com tabela, escolha, ordem, retenção, idempotência, sinais e gatilhos; a saída nomeia o dado faltante para replay.

**Entrega esperada**

Um registro de decisão com alternativas, escolha, consequências, riscos, sinais e condição de retorno em `<raiz-do-clone>/entregas/modulo-5/avaliar-fila-ou-log.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação contextual das alternativas | 25% | Evidência: contexto por opção; insuficiente: tecnologia escolhida por fama. |
| Requisitos e hipóteses separados | 20% | Evidência: hipótese rotulada; insuficiente: requisito inventado. |
| Ordem, retenção e dados tratados | 20% | Evidência: regra de cada aspecto; insuficiente: ordem global presumida. |
| Idempotência ponta a ponta | 20% | Evidência: efeito externo considerado; insuficiente: deduplicação apenas no broker. |
| Gatilhos de revisão mensuráveis | 15% | Evidência: limiar definido; insuficiente: revisar quando necessário. |

## Criar

### Projetar evolução `v2` de resultado

**Objetivo**

Planejar uma mudança de contrato que mantenha consumidores em funcionamento e preserve a deduplicação.

**Situação**

Resultados precisa acrescentar uma classificação administrativa que alguns consumidores usarão. Um consumidor antigo só entende `ResultadoLaboratorialDisponibilizado.v1`; Faturamento não pode parar nem cobrar duas vezes. A nova classificação não deve revelar conteúdo clínico e a transição precisa ser observável.

**Seu papel**

Você cria um plano de evolução e convivência entre consumidores.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/src/hospital/eventos/publicador.py`, `<raiz-do-clone>/laboratorios/plataforma-hospitalar/src/hospital/eventos/consumidor.py` e `<raiz-do-clone>/laboratorios/plataforma-hospitalar/tests/test_event_idempotency.py`. Escreva em `<raiz-do-clone>/entregas/modulo-5/criar-evolucao-v2.md`.

**Antes de executar**

O estado inicial é `ResultadoLaboratorialDisponibilizado.v1` imutável, consumidores só `v1` e Compose parado. Declare owner e janela; não altere laboratório.

**O que fazer**

1. Classifique a mudança como compatível ou incompatível e justifique com o contrato `v1` nomeado.
2. Escreva `v2` ou campo opcional, exemplos sintéticos e owner do contrato.
3. Desenhe publicação dupla ou adaptação, com início, métrica e fim observáveis.
4. Mantenha `event_id`: duas versões produzem uma cobrança.
5. Planeje validação, DLQ, métricas de consumidores e retorno seguro.
6. Se qualquer consumidor não confirmar compatibilidade na janela, prolongue `v1`, não retire a fila e registre o retorno; só então defina a remoção de `v1`.

**Evidência esperada**

Contrato `v1`/`v2`, diagrama, saída `uma cobrança`, métrica, DLQ e critério numérico para retirar `v1` ou retornar.

**Entrega esperada**

Um pacote com contrato versionado, diagrama de convivência, plano de rollout, sinais e critérios de retirada em `<raiz-do-clone>/entregas/modulo-5/criar-evolucao-v2.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Semântica da evolução | 20% | Evidência: mudança nomeada; insuficiente: versão sem significado. |
| Compatibilidade e transição | 20% | Evidência: convivência descrita; insuficiente: consumidor antigo ignorado. |
| Preservação de idempotência | 20% | Evidência: mesma chave mantida; insuficiente: nova versão duplica efeito. |
| Observabilidade e recuperação | 20% | Evidência: sinal e retorno; insuficiente: rollout sem monitoramento. |
| Proteção de dados e ownership | 20% | Evidência: dono e minimização; insuficiente: dado circula sem necessidade. |
