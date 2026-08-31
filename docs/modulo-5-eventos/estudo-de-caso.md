# Estudo de caso: resultado, faturamento e tempo de convergência

## Situação

O hospital rodava assim havia quase dois anos: ao receber um resultado do Laboratório, a capacidade Resultados chamava Faturamento diretamente, que chamava Notificações, numa cadeia síncrona dentro da mesma requisição HTTP. Funcionou enquanto o volume era baixo e as três equipes cabiam numa mesma reunião semanal.

O sintoma que forçou a revisão apareceu no atendimento ao cliente: pacientes ligando para perguntar por que o extrato do convênio mostrava duas cobranças para o mesmo exame. Nenhum alarme técnico tinha disparado antes disso. A investigação encontrou três problemas empilhados na mesma cadeia. Lentidão na cobrança atrasava a liberação do resultado na tela do médico, porque a chamada a Faturamento fazia parte do mesmo fluxo síncrono. Uma falha transitória em Notificações (um provedor de SMS fora do ar por sete minutos) fazia o Laboratório parecer indisponível, mesmo com o resultado já gravado. E a correção manual que um analista aplicava toda vez que uma chamada falhava e alguém reexecutava o job à mão foi exatamente o que produziu a cobrança duplicada.

Três pessoas participaram da decisão: a arquiteta responsável pela plataforma, o tech lead de Faturamento e o tech lead de Resultados. A primeira reação de alguém no comitê foi “bota tudo no Kafka”. A resposta não respondia a nenhuma das perguntas que importavam: contrato, ordem, forma de lidar com repetição ou operação de um cluster que ninguém no time tinha rodado antes. A decisão registrada foi RabbitMQ com uma fila de Faturamento: a necessidade comprovada era rotear uma unidade de trabalho, observar confirmações e DLQ; replay para muitos consumidores ainda era hipótese, sem um segundo consumidor concreto pedindo isso. Não é ranking: ActiveMQ, RabbitMQ ou Kafka só fazem sentido contra necessidades, topologia e capacidade operacional medidas.

## Decisão e consequências

Resultados publicou `ResultadoLaboratorialDisponibilizado.v1` em `hospital.events`, contendo referência, não laudo. Faturamento assumiu `billing.resultados.v1`, retry, store idempotente e uma dead-letter queue (DLQ, a fila que guarda mensagens rejeitadas em vez de descartá-las); nova capacidade poderá criar sua própria fila. A disponibilidade do resultado deixou de depender da cobrança: o médico passou a ver o resultado assim que Resultados publicasse, independente do estado de Faturamento.

Essa é consistência eventual: a interface pode informar resultado disponível e atualização administrativa pendente. Operação acompanha idade da mensagem, tamanho da fila, rejeição e DLQ. Fila vazia não prova efeito correto; fila crescente pede investigação de capacidade, dependência ou contrato. Nas primeiras duas semanas depois da migração, a equipe manteve um painel simples só com essas quatro métricas, porque não havia histórico suficiente para saber qual variação era normal.

## Incidente: duplicidade de entrega

Três semanas depois de entrar em produção, o padrão antigo reapareceu, e por um instante a equipe temeu ter recriado o mesmo bug. Faturamento gravou cobrança e caiu antes do ack. RabbitMQ redeliverou; `INSERT` sem chave única duplicaria o efeito. A diferença desta vez é que havia uma métrica nova para diagnosticar: `processed_events` mostrou duas tentativas para o mesmo `event_id`, e `billing_effects` mostrou uma linha só. A correção foi registrar tentativa e efeito na mesma transação, deduplicando por `event_id`. Desabilitar o redelivery ficou fora de cogitação: trocaria uma duplicidade visível por uma perda silenciosa, bem mais difícil de detectar.

Na segunda entrega, o handler aumenta tentativas, confirma a mensagem e não cria nova cobrança. Duas tentativas demonstram disponibilidade parcial; uma cobrança é o efeito que deve permanecer único.

## Incidente: evolução incompatível

Meses depois, um evento sem `result_reference` falhou na validação Pydantic, não recebeu ack e chegou à DLQ. A causa foi um deploy do time de Resultados que renomeou um campo interno sem revisar o contrato publicado — o tipo de erro que passa despercebido em testes unitários porque cada serviço testa o próprio lado do contrato, nunca os dois juntos. Inventar a referência ocultaria contrato quebrado. A equipe identificou o produtor pelo cabeçalho `type` da mensagem rejeitada, corrigiu a versão e decidiu a recuperação das mensagens com proteção de dados: republicar apenas depois de confirmar que o campo voltava a vir preenchido.

Para acrescentar referência administrativa mais tarde, a equipe escolhe campo opcional ou `v2` conforme a semântica, verifica consumidores e mede uma convivência temporária. A identidade usada para deduplicação não muda durante a transição.

## Quando Kafka vira extensão plausível

Um ano depois da migração, Auditoria pediu para reconstruir a sequência completa de um caso para prestação de contas a um convênio — o primeiro pedido real de replay independente que o comitê via desde a decisão original. Se Auditoria e outras capacidades futuras precisarem disso de forma recorrente e com retenção definida, Kafka passa a ser alternativa: tópicos, chave de partição, grupos, retenção e classificação de dados entram na decisão. Faturamento ainda deduplica efeito externo e escolhe ordem por exame ou conta. Um desenho híbrido de log para integração e fila para trabalho também exige owner, observabilidade e recuperação em cada ponte.

## Roteiro passo a passo: leia o caso como decisão arquitetural

Este roteiro usa os quatro episódios acima como matéria-prima. Siga a ordem: cada passo depende do anterior.

**Passo 1 — Separe fato de sintoma.** No texto da Situação, três problemas aparecem misturados: latência, falso indisponível e cobrança duplicada. Escreva os três em frases separadas e aponte, para cada um, se a causa estava na cadeia síncrona, na ausência de idempotência ou nas duas.

**Passo 2 — Reconstrua o critério de escolha do broker.** O comitê descartou “Kafka para tudo” sem descartar Kafka para sempre. Releia o parágrafo da decisão inicial e liste as duas condições que, se tivessem sido verdadeiras naquele momento, teriam justificado Kafka em vez de RabbitMQ.

**Passo 3 — Diagnostique o incidente de duplicidade sem olhar a resposta do texto.** Antes de reler a seção do incidente, escreva sua própria hipótese: o que a dupla observação de `processed_events` e `billing_effects` revela que uma única métrica de contagem de mensagens não revelaria? Só depois confira contra o texto.

**Passo 4 — Avalie a evolução incompatível pela raiz, não pelo sintoma.** O sintoma foi a mensagem na DLQ. A raiz foi um contrato alterado sem revisão cruzada entre times. Proponha um mecanismo, ferramenta ou processo, capaz de pegar essa mudança antes do deploy chegar à fila de produção.

**Passo 5 — Redija o gatilho de revisão para Kafka.** Use o pedido de Auditoria como âncora e escreva, em uma frase, a condição observável (não a intuição) que deveria abrir a discussão de migrar Auditoria para um log com retenção, mantendo Faturamento onde está.

**Passo 6 — Registre a decisão como ADR.** Responda: que atraso o usuário vê? Qual payload mínimo e qual efeito é único? O que acontece fora de ordem? Quem acompanha a DLQ e em quanto tempo? As quatro respostas juntas são o conteúdo mínimo do `ADR-005` do [incremento 5 do projeto integrador](../projeto-integrador/incrementos.md#incremento-5-colaboracao-orientada-por-eventos) sobre a mensageria escolhida.
