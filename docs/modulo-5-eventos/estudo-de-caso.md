# Estudo de caso: resultado, faturamento e tempo de convergência

## Situação

Inicialmente, ao disponibilizar um resultado, Laboratório chamava Faturamento, que chamava Notificação. Lentidão na cobrança atrasava o fluxo clínico; falha transitória fazia parecer que o resultado não existia; repetição manual produziu cobrança duplicada. Responsabilidades e falhas estavam na mesma cadeia.

“Kafka para tudo” não respondia sobre contrato, ordem, dados ou operação. A primeira decisão foi RabbitMQ com uma fila de Faturamento: a necessidade comprovada era rotear uma unidade de trabalho, observar confirmações e DLQ; replay para muitos consumidores ainda era hipótese. Não é ranking: ActiveMQ, RabbitMQ ou Kafka só fazem sentido contra necessidades, topologia e capacidade operacional medidas.

## Decisão e consequências

Resultados publicou `ResultadoLaboratorialDisponibilizado.v1` em `hospital.events`, contendo referência, não laudo. Faturamento assumiu `billing.resultados.v1`, retry, store idempotente e DLQ; nova capacidade poderá criar sua própria fila. A disponibilidade do resultado deixou de depender da cobrança.

Essa é consistência eventual: a interface pode informar resultado disponível e atualização administrativa pendente. Operação acompanha idade da mensagem, tamanho da fila, rejeição e DLQ. Fila vazia não prova efeito correto; fila crescente pede investigação de capacidade, dependência ou contrato.

## Incidente: duplicidade de entrega

Faturamento gravou cobrança e caiu antes do ack. RabbitMQ redeliverou; `INSERT` sem chave única duplicaria o efeito. A correção foi registrar tentativa e efeito na mesma transação, deduplicando por `event_id`, não desabilitar redelivery.

Na segunda entrega, o handler aumenta tentativas, confirma a mensagem e não cria nova cobrança. Duas tentativas demonstram disponibilidade parcial; uma cobrança é o efeito que deve permanecer único.

## Incidente: evolução incompatível

Um evento sem `result_reference` falhou na validação Pydantic, não recebeu ack e chegou à DLQ. Inventar a referência ocultaria contrato quebrado. A equipe identifica o produtor, corrige a versão e decide a recuperação das mensagens com proteção de dados.

Para acrescentar referência administrativa, a equipe escolhe campo opcional ou `v2` conforme a semântica, verifica consumidores e mede uma convivência temporária. A identidade usada para deduplicação não muda durante a transição.

## Quando Kafka vira extensão plausível

Se Analytics, Qualidade e novos consumidores precisarem de replay independente por retenção definida, Kafka passa a ser alternativa: tópicos, chave de partição, grupos, retenção e classificação de dados entram na decisão. Faturamento ainda deduplica efeito externo e escolhe ordem por exame ou conta. Um desenho híbrido de log para integração e fila para trabalho também exige owner, observabilidade e recuperação em cada ponte.

## Perguntas para a decisão

Que atraso o usuário vê? Qual payload mínimo e qual efeito é único? O que acontece fora de ordem? Quem acompanha a DLQ e em quanto tempo? Responder transforma escolha de broker em arquitetura verificável.
