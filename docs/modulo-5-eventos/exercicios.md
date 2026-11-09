# Exercícios: decidir integrações assíncronas

As propostas usam o caso hospitalar e dados sintéticos. Não há resposta única: declare premissas, diferencie fato de hipótese e trate contrato, falha e operação como parte da decisão. Cada atividade produz um artefato autocontido, sem depender de configuração manual em um ambiente remoto.

## Recordar

### Nomear semântica e componentes

**Situação**

Você acabou de entrar como arquiteta numa equipe que está migrando a integração entre Resultados e Faturamento de chamadas diretas para mensageria. Ao herdar o código e as conversas já em andamento, você encontra seis nomes espalhados pelo repositório, sem nenhum glossário que diga o que cada um significa: `ResultadoLaboratorialDisponibilizado.v1`, `GerarCobranca`, `hospital.events`, `billing.resultados.v1`, `hospital.events.dlx` e `billing.resultados.v1.dlq`. Numa reunião recente, dois desenvolvedores gastaram dez minutos discutindo se `GerarCobranca` era algo que já tinha acontecido ou um pedido para alguém fazer algo. A discussão só terminou porque o horário da reunião acabou, sem que nenhum dos dois tivesse convencido o outro.

**Seu papel**

Você prepara um glossário curto, que vai virar a referência oficial da equipe a partir de agora.

1\. Qual é a diferença essencial entre um broker e um mediator?

<details>
<summary>Ver resposta</summary>

Um broker distribui mensagens entre produtor e consumidor sem decidir nada sobre a ordem ou o sentido de negócio do fluxo; ele só roteia. Um mediator conhece o processo inteiro, decide a sequência dos passos e coordena os participantes — assume, de propósito, a decisão que o broker se recusa a tomar.
</details>

2\. Como se nomeia corretamente um evento? E um comando? Dê um exemplo de cada, usando o domínio da situação acima.

<details>
<summary>Ver resposta</summary>

Um evento é nomeado no particípio passado, porque afirma um fato já ocorrido: `ResultadoLaboratorialDisponibilizado` segue esse padrão. Um comando é nomeado no infinitivo ou como uma ordem direta, porque pede uma ação a alguém: `GerarCobranca` segue esse padrão. Nomear um comando no particípio (como se já tivesse acontecido) é exatamente o tipo de erro que gerou a discussão de dez minutos da situação.
</details>

3\. Classifique cada um dos seis nomes da situação (`ResultadoLaboratorialDisponibilizado.v1`, `GerarCobranca`, `hospital.events`, `billing.resultados.v1`, `hospital.events.dlx` e `billing.resultados.v1.dlq`) numa das categorias evento, comando, exchange de domínio, fila de trabalho, exchange de dead-letter ou fila de dead-letter.

<details>
<summary>Ver resposta</summary>

`ResultadoLaboratorialDisponibilizado.v1` é evento, pelo particípio e pela versão explícita. `GerarCobranca` é comando, pelo verbo no infinitivo pedindo uma ação. `hospital.events` é a exchange de domínio, pelo nome genérico do canal. `billing.resultados.v1` é a fila de trabalho de um consumidor específico. `hospital.events.dlx` é a exchange de dead-letter, pelo sufixo `.dlx`. `billing.resultados.v1.dlq` é a fila de dead-letter correspondente, pelo sufixo `.dlq`.
</details>

4\. Defina, numa frase cada, entrega pelo menos uma vez, idempotência, ordenação e dead-letter queue.

<details>
<summary>Ver resposta</summary>

Entrega pelo menos uma vez admite que a mesma mensagem chegue mais de uma vez. Idempotência é a propriedade que faz repetir a mensagem não repetir o efeito de negócio. Ordenação exige declarar qual sequência importa e sob qual chave. Dead-letter queue é a fila que guarda mensagens rejeitadas para decisão controlada, sem apagá-las.
</details>

## Compreender

### Explicar a repetição sem prometer magia

**Situação**

Uma pessoa afirma que, se RabbitMQ confirmar a publicação, Faturamento nunca verá uma mensagem duas vezes. Outra propõe ignorar todos os redeliveries para evitar cobrança repetida.

**Seu papel**

Você explica o ciclo de falha e propõe linguagem correta para a equipe.

1\. Descreva, em uma sequência de passos concreta, o que acontece quando o consumidor de Faturamento grava o efeito de uma cobrança no SQLite e o processo cai antes de confirmar a mensagem ao RabbitMQ. Explique o que o broker faz a seguir com aquela mensagem e por que ele não tem nenhuma forma de saber que o efeito já havia sido registrado do outro lado.

<details>
<summary>Ver resposta</summary>

O consumidor recebe a mensagem, grava a linha em `billing_effects` e cai antes de enviar o ack ao RabbitMQ. Da perspectiva do broker, a mensagem nunca foi confirmada, então ela permanece disponível e é reentregue quando o consumidor volta ao ar. O broker não tem acesso ao SQLite do consumidor: ele só sabe se recebeu ou não uma confirmação, e por isso reentrega por precaução em vez de assumir que o trabalho foi concluído.
</details>

2\. A pessoa da situação, que propôs ignorar todos os redeliveries, está tentando resolver um problema real com a ferramenta errada. Explique por que a entrega repetida é uma consequência necessária de garantir que nenhuma mensagem se perca diante de falhas ambíguas como a do item anterior, e diga o que a equipe perderia de fato se simplesmente desligasse o redelivery em vez de tratar a repetição.

<details>
<summary>Ver resposta</summary>

O broker não consegue distinguir "o consumidor processou e a confirmação se perdeu na rede" de "o consumidor nunca processou": as duas situações parecem idênticas do lado de fora. Reentregar é a escolha segura porque assume o cenário mais caro, que é perder trabalho, em vez do cenário mais raro, que é duplicar uma confirmação. Desligar o redelivery trocaria duplicidade visível, que a idempotência resolve, por perda silenciosa de resultados de exame, que nenhum mecanismo do laboratório detecta.
</details>

3\. No log do consumidor de Faturamento aparece a linha `processed=False attempts=2` para um `event_id` que já tinha gerado efeito antes, mas a tabela `billing_effects` mostra só uma linha de cobrança para essa mesma identidade. Um colega, olhando só a linha do log, conclui que há um bug porque "a mensagem foi processada duas vezes". Usando esse log e essa tabela como evidência, diferencie tentativa, confirmação e efeito de negócio, e explique por que a conclusão do colega está errada.

<details>
<summary>Ver resposta</summary>

Tentativa é cada vez que o consumidor viu a mensagem e registrou isso em `processed_events`; confirmação é o ack enviado ao broker, que encerra a entrega daquela cópia específica; efeito de negócio é a linha em `billing_effects`, que só existe na primeira vez. O colega confundiu tentativa com efeito: `attempts=2` conta quantas vezes o consumidor viu aquele `event_id`, contagem que cresce a cada entrega repetida, enquanto `billing_effects` registra o efeito de negócio, que a mesma transação garante existir uma única vez. A tabela com uma única linha é exatamente a evidência de que o sistema funcionou como projetado.
</details>

4\. Alguém na equipe propõe resolver a duplicidade guardando os `event_id` já vistos num `set()` em memória, dentro do próprio processo Python do consumidor, em vez de gravar cada tentativa no SQLite. Explique por que essa alternativa falha na primeira vez que o serviço reinicia ou que uma segunda réplica do consumidor entra no ar, e diga o que ter `event_id` como chave primária durável resolve que o `set()` em memória não resolve.

<details>
<summary>Ver resposta</summary>

Um `set()` em memória existe só enquanto o processo está vivo: um reinício zera o histórico de `event_id` vistos, e uma segunda réplica começa com o próprio `set()` vazio, sem conhecimento do que a primeira já processou. `event_id` como chave primária numa tabela durável sobrevive a reinício e é compartilhada entre réplicas que apontam para o mesmo banco, porque a garantia passou a ser uma propriedade dos dados persistidos, independente do processo que está em execução.
</details>

## Aplicar
### Recomendar a forma de propagar o resultado de exame

**Objetivo**

Recomendar uma entre quatro formas de propagar um fato para três consumidores independentes, declarando ganho, custo e a pré-condição que falta.

**Situação**

No hospital, o serviço de Exames grava o resultado no próprio banco e precisa avisar três destinos. Faturamento usa o resultado para compor a conta. Notificações avisa o paciente. Auditoria guarda o histórico para consulta posterior.

Hoje o serviço de Exames chama os três em sequência, dentro da mesma transação que grava o resultado. Na semana passada, o serviço de Notificações ficou lento e resultados deixaram de ser gravados. O time descobriu o problema por reclamação de médico, porque nenhum alarme disparou.

A liderança técnica pediu uma recomendação antes de acrescentar o quarto consumidor, já solicitado por Compliance.

Seis fatos foram apurados no hospital:

1. Quando a regra de retenção legal muda, a Auditoria precisa reprocessar os últimos noventa dias.
2. Faturamento não pode perder nenhum resultado; Notificações pode perder sem dano relevante.
3. O serviço de Exames grava o resultado no próprio banco antes de avisar qualquer destino.
4. Hoje, se um dos avisos falha, a gravação do resultado é desfeita junto.
5. Um consumidor novo é pedido a cada dois meses, em média.
6. Nenhum dos três consumidores trata mensagem repetida hoje.

As quatro alternativas em avaliação:

| Alternativa | Como o fato chega aos destinos |
| --- | --- |
| **A. Chamada síncrona** | Exames chama os três destinos e só conclui quando todos responderem. |
| **B. Uma fila por destino** | Exames publica em três filas, uma por consumidor, cada uma com seu dono. |
| **C. Tópico compartilhado** | Exames publica um evento num tópico. Os três consomem de forma independente, cada um no próprio ritmo. |
| **D. Tópico com registro de saída** | Como a C, e a publicação passa por uma tabela de saída gravada na mesma transação do resultado, com retenção que permite reprocessar. |

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação. A equipe implementa depois, e espera de você a escolha, a pré-condição obrigatória e o risco aceito.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende uma das quatro alternativas, em uma frase.
2. Sobre cada uma das quatro, escreva duas frases: o que ela resolve do problema descrito e o que ela cobra em troca.
3. O fato 1 e o fato 2 pedem coisas diferentes. Diga como a sua recomendação atende aos dois.
4. O fato 6 diz que nenhum consumidor trata mensagem repetida. Diga o que acontece se a equipe ligar a sua recomendação antes de resolver isso.
5. Aponte a alternativa que você descartaria de imediato, diga qual fato a derruba, e escreva o sinal que faria rever a decisão.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, a resposta para os fatos 1 e 2, a pré-condição de idempotência nomeada com a consequência de ignorá-la, a alternativa descartada com o fato que a derruba, o risco aceito e o sinal de revisão observável.

## Analisar
### Investigar uma fila que cresce

**Objetivo**

Formar hipóteses sobre o crescimento de uma fila a partir dos sinais disponíveis, sem transformar uma contagem em diagnóstico.

**Situação**

Na quinta-feira de manhã, o time de plantão percebeu que a fila `billing.resultados.v1` passou de algumas dezenas de mensagens para onze mil em quatro horas. A fila de mensagens rejeitadas, que costuma ficar vazia, tinha trezentas.

Faturamento parou de fechar contas. As reclamações chegaram pelo atendimento, porque nenhum alarme disparou.

Na véspera, o time de Resultados publicou uma versão nova do contrato do evento. O campo `unidade_medida`, que antes vinha sempre preenchido, passou a ser opcional.

Os sinais disponíveis são a idade da mensagem mais antiga na fila, a contagem de mensagens, o identificador de cada evento, os registros de log do consumidor e a versão do contrato publicada. Nenhum servidor ficou fora do ar no período, e o consumo de recursos das máquinas está normal.

Cinco fatos valem para a análise:

1. A fila saiu de dezenas para onze mil mensagens em quatro horas.
2. A fila de rejeitadas, normalmente vazia, tem trezentas mensagens.
3. Uma versão nova do contrato foi publicada na véspera, tornando um campo opcional.
4. Nenhum servidor ficou indisponível, e o uso de recursos está normal.
5. O problema foi descoberto por reclamação de usuário, sem que nenhum alarme disparasse.

**Seu papel**

Você conduz a investigação antes de qualquer correção. Reiniciar o consumidor é tentador e destruiria evidência.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escreva duas hipóteses diferentes que explicam o crescimento da fila, e diga que sinal disponível separaria uma da outra.
2. O fato 3 tornou um campo opcional. Explique por que uma mudança que afrouxa uma regra pode quebrar um consumidor.
3. Diga a diferença entre a fila principal crescer e a fila de rejeitadas crescer, e o que cada um dos dois sinais indica sobre onde está o defeito.
4. O fato 5 é um problema em si. Diga qual sinal, se estivesse sendo observado, teria avisado a equipe antes do usuário, e por quê.
5. Aponte uma conclusão que os cinco fatos não sustentam, rotule-a como hipótese e diga que dado a confirmaria.

**Evidência esperada**

O arquivo entregue apresenta duas hipóteses com o sinal que as separa, explica o efeito de afrouxar um campo obrigatório, distingue o significado das duas filas, nomeia o alarme ausente e registra a hipótese não sustentada com o dado que a confirmaria.

## Avaliar
### Escolher o mecanismo de entrega para um consumidor novo

**Objetivo**

Julgar três mecanismos de entrega contra critérios declarados, considerando que os dois consumidores existentes têm necessidades opostas.

**Situação**

Dois sistemas já consomem os resultados de exame do hospital. Faturamento processa um resultado por vez, e não pode perder nenhum. Notificações avisa o paciente, e perder um aviso ocasional é tolerável.

Agora entra um terceiro. A área de Qualidade quer recalcular indicadores mensais e, sempre que a definição de um indicador muda, precisa reprocessar os últimos três meses de resultados desde o começo.

O hospital opera hoje um servidor de mensageria com filas tradicionais, em que a leitura remove a mensagem. Ninguém no time operou um sistema de log com retenção.

A equipe de plataforma tem duas pessoas.

Três mecanismos estão sobre a mesa, e as descrições abaixo bastam para julgá-los.

O primeiro é uma fila dedicada à Qualidade, alimentada em paralelo às filas que já existem. A leitura remove a mensagem, como nas outras.

O segundo é um log com retenção de noventa dias, no qual a leitura não remove nada e cada consumidor guarda a própria posição. Os três consumidores migrariam para ele.

O terceiro é uma fila dedicada à Qualidade, como o primeiro, somada a uma cópia dos resultados guardada em banco pela própria Qualidade, para servir de base ao reprocessamento.

Quatro fatos valem para a decisão:

1. A Qualidade precisa reler três meses inteiros quando um indicador muda.
2. Faturamento não pode perder nenhum resultado; Notificações pode.
3. A equipe opera filas hoje e nunca operou log com retenção.
4. A equipe de plataforma tem duas pessoas, sem plantão noturno.

**Seu papel**

Você emite o parecer sobre como atender a Qualidade sem prejudicar os dois consumidores que já funcionam.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Declare de três a quatro critérios de julgamento e diga qual pesa mais, justificando pelo risco de errar.
2. Avalie os três mecanismos contra os seus critérios, um parágrafo por mecanismo, dizendo o que cada um resolve e o que cobra.
3. O fato 1 elimina um dos três de forma direta. Diga qual e explique por quê.
4. Emita o parecer e diga o que acontece com os dois consumidores atuais na sua escolha: eles precisam mudar, e se sim, o quê.
5. Escreva a objeção mais forte contra o seu parecer, considerando o fato 3, e responda a ela.

**Evidência esperada**

O parecer traz critérios escritos antes da escolha, os três mecanismos julgados contra eles, a eliminação justificada pelo requisito de releitura, o impacto declarado sobre os consumidores atuais e uma objeção respondida.

## Criar
### Propor a evolução do contrato de resultado

**Objetivo**

Propor uma mudança de contrato que atenda ao consumidor novo sem parar os que já funcionam, escolhendo entre três caminhos.

**Situação**

O evento `ResultadoLaboratorialDisponibilizado` circula no hospital há dois anos, na versão 1. Três sistemas o consomem.

A área de Compliance pediu um campo novo: uma classificação administrativa do resultado, que só ela vai usar. Os outros dois consumidores não têm interesse nesse campo e não querem mexer no código.

Um dos consumidores é um sistema antigo, mantido por um fornecedor externo. Ele só entende a versão 1, e qualquer alteração no formato faz o processamento dele falhar. A próxima janela de mudança desse fornecedor é daqui a oito meses.

Faturamento consome o mesmo evento e não pode parar em nenhum momento.

Todos os consumidores usam o identificador do evento para descartar mensagem repetida, e esse mecanismo precisa continuar funcionando durante a transição.

A mudança será executada por três equipes: a de Resultados, que publica o evento e controla o formato emitido, a de Faturamento, que mantém o consumidor que não pode parar, e a de Compliance, que vai consumir o campo novo. O fornecedor externo do sistema antigo não faz parte dessas três equipes e só altera o próprio sistema na janela de mudança prevista para daqui a oito meses.

Três caminhos estão sobre a mesa, e as descrições abaixo bastam para escolher.

O primeiro acrescenta o campo novo na própria versão 1, como campo opcional. Um só formato continua existindo.

O segundo publica uma versão 2 em paralelo à versão 1. A origem passa a emitir os dois formatos, e cada consumidor escolhe qual assina.

O terceiro publica só a versão 2 e coloca um tradutor no caminho do consumidor antigo, convertendo a versão 2 de volta para o formato que ele entende.

Quatro restrições valem para a proposta:

1. O consumidor antigo só entende a versão 1 e tem janela de mudança em oito meses.
2. Faturamento não pode parar em nenhum momento da transição.
3. O descarte de mensagem repetida depende do identificador do evento e precisa continuar funcionando.
4. Só a área de Compliance vai usar o campo novo.

**Seu papel**

Você propõe o caminho de evolução. A proposta será executada por três equipes diferentes, e precisa dizer o que cada uma faz e em que ordem.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três caminhos e defenda a escolha citando pelo menos duas das quatro restrições.
2. Sobre os dois caminhos que você não escolheu, escreva duas frases cada: o que ganhariam e o que custariam.
3. Descreva a ordem das etapas da sua proposta, dizendo o que cada uma das três equipes faz e em que momento. Deixe claro quando o consumidor antigo pode ser desligado da versão 1.
4. Explique o que acontece com o descarte de mensagem repetida enquanto os dois formatos coexistem, e como você impede que o mesmo resultado seja processado duas vezes.
5. Escreva o sinal que indicaria que a transição terminou e a versão antiga pode sair do ar.

**Evidência esperada**

O arquivo entregue traz o caminho escolhido com duas restrições citadas, os outros dois avaliados, a ordem das etapas com responsável por etapa, o tratamento da repetição durante a coexistência e o sinal de encerramento da transição.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 5 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes: as simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

Qual é a diferença entre um evento e um comando?

- (a) O evento descreve um fato de domínio no passado, e o comando expressa uma intenção dirigida a um destinatário que pode aceitar ou rejeitar.
- (b) O evento é síncrono, e o comando é assíncrono.
- (c) O evento é transportado por fila, e o comando é transportado por tópico.
- (d) Não há diferença, os dois termos são sinônimos.

#### Questão 2 [Simples]

Qual é a forma correta de nomear um evento, segundo o módulo?

- (a) GerarCobranca, com verbo no infinitivo.
- (b) ProcessarPedidoAgora, com verbo no imperativo.
- (c) PedidoRealizado.v1, com verbo no particípio e linguagem do domínio.
- (d) PedidoService.publish, com o nome da classe que publica.

#### Questão 3 [Simples]

O que diferencia um broker de um mediator?

- (a) O broker só funciona com Kafka, e o mediator só funciona com RabbitMQ.
- (b) O broker roteia e entrega sem decidir a ordem do processo, e o mediator conhece o processo e decide a ordem das etapas.
- (c) O broker guarda regra de negócio, e o mediator apenas encaminha mensagens.
- (d) O broker é síncrono, e o mediator é assíncrono.

#### Questão 4 [Simples]

O que é uma dead-letter queue (DLQ)?

- (a) Uma fila que apaga automaticamente as mensagens inválidas.
- (b) Uma fila de alta prioridade para mensagens urgentes.
- (c) Uma fila que reentrega mensagens indefinidamente até o sucesso.
- (d) Uma fila que recebe mensagens rejeitadas e as mantém visíveis para inspeção.

#### Questão 5 [Simples]

Em um log distribuído, como o Kafka, o que é o offset?

- (a) O tempo máximo de retenção das mensagens.
- (b) O número de partições de um tópico.
- (c) O identificador único de cada evento.
- (d) A posição de leitura de cada consumidor, que indica até onde ele já leu.

#### Questão 6 [Simples]

O que significa idempotência no consumidor de eventos?

- (a) Que aplicar a mesma ocorrência mais de uma vez tem o mesmo efeito de negócio observável que aplicá-la uma única vez.
- (b) Que o consumidor nunca recebe a mesma mensagem duas vezes.
- (c) Que o consumidor processa as mensagens na ordem exata de publicação.
- (d) Que o broker garante entrega exatamente uma vez.

#### Questão 7 [Simples]

O que distingue um tópico de uma fila?

- (a) O tópico guarda as mensagens para sempre, e a fila guarda por um dia.
- (b) O tópico copia a mesma publicação para filas distintas com critérios de assinatura próprios, e a fila reparte o trabalho entre réplicas de um consumidor.
- (c) O tópico só aceita comandos, e a fila só aceita eventos.
- (d) O tópico exige mediator, e a fila exige broker.

#### Questão 8 [Simples]

Qual garantia de entrega admite repetição da mesma mensagem e exige consumidor idempotente?

- (a) No máximo uma vez.
- (b) Exatamente uma vez em qualquer escopo.
- (c) Pelo menos uma vez.
- (d) Entrega ordenada global.

### Questões médias

#### Questão 9 [Média]

Um consumidor de Faturamento recebe o evento, grava a cobrança e cai antes de confirmar a mensagem ao broker. O que acontece e como o módulo trata a situação?

- (a) A mensagem se perde, e a cobrança deve ser refeita manualmente.
- (b) O broker descarta a mensagem, porque a cobrança já existe.
- (c) O broker volta a entregar a mensagem, e o consumidor usa o event_id para não criar uma segunda cobrança.
- (d) O produtor detecta a falha e cancela a cobrança.

#### Questão 10 [Média]

Uma equipe guarda os event_id já processados em um cache na memória do processo. Por que o módulo considera essa solução insuficiente?

- (a) Porque o cache é lento demais para mensageria.
- (b) Porque reinício, réplica diferente e expiração permitem duplicidade, e a deduplicação deve ficar no banco do consumidor, na mesma transação do efeito.
- (c) Porque o event_id não é único.
- (d) Porque o broker já garante que não haverá repetição.

#### Questão 11 [Média]

O evento de resultado de exame carrega apenas result_reference, sem incluir o laudo. Qual é a principal razão dessa escolha no domínio clínico?

- (a) Controlar o acesso, para que o evento entregue internamente não vire um atalho em torno da autorização de leitura.
- (b) Reduzir o tamanho da mensagem, que tem limite rígido no broker.
- (c) Garantir a ordenação dos eventos.
- (d) Eliminar a necessidade de consultar a origem.

#### Questão 12 [Média]

Depois do evento de pedido, Crédito pode aprovar um limite e Notificação pode preparar um aviso, sem que uma reação dependa da outra. Qual padrão é adequado?

- (a) Mediator, porque toda reação precisa de coordenação central.
- (b) Chamada síncrona em cadeia, para garantir a ordem.
- (c) Transação distribuída entre Crédito e Notificação.
- (d) Broker, porque nenhuma reação precisa comandar a outra e cada serviço reage de forma independente.

#### Questão 13 [Média]

Após o pedido ser publicado, a tela de status mostra confirmação enquanto Faturamento ainda não criou a cobrança. Como o módulo chama essa situação, e o que ela exige da equipe?

- (a) Inconsistência permanente, corrigida por rollback.
- (b) Consistência eventual, que exige decidir como informar o estado pendente, quanto tempo é aceitável, como reprocessar e quem investiga atrasos.
- (c) Falha de entrega, que exige reiniciar o broker.
- (d) Consistência forte, que dispensa qualquer tratamento.

#### Questão 14 [Média]

Uma equipe precisa que dois grupos independentes leiam a mesma sequência de eventos em ritmos diferentes, e que um deles possa reprocessar um trecho já lido. Qual modelo de canal atende esse requisito?

- (a) Fila de trabalho com confirmação destrutiva.
- (b) Mediator com orquestração central.
- (c) Chamada HTTP síncrona com repetição.
- (d) Log distribuído com retenção e offset por consumidor.

#### Questão 15 [Média]

Um evento chega com um campo obrigatório ausente. O que o consumidor deve fazer, segundo o desenho da oficina?

- (a) Rejeitar a mensagem sem confirmá-la como faturada, enviando-a à DLQ para inspeção.
- (b) Confirmar a mensagem como sucesso e registrar um aviso.
- (c) Reentregar a mensagem indefinidamente até o produtor corrigir.
- (d) Completar o campo com um valor padrão e seguir.

### Questões difíceis

#### Questão 16 [Difícil]

Um serviço grava o pedido no banco e, em seguida, publica o evento no broker. Qual problema essa sequência cria, e qual padrão o módulo recomenda?

- (a) Problema de ordenação, resolvido com uma partição única.
- (b) Problema de latência, resolvido com payload completo.
- (c) Problema de dupla escrita, resolvido pelo outbox, que grava a mudança e a intenção de publicação na mesma transação local.
- (d) Problema de autorização, resolvido com DLQ.

#### Questão 17 [Difícil]

No Kafka, a equipe escolheu pedido_id como chave de partição. O que essa escolha garante e o que ela não garante?

- (a) Garante a ordem global de todos os eventos da loja.
- (b) Garante entrega exatamente uma vez, mas não garante ordem.
- (c) Garante a ordem dos eventos do mesmo pedido em uma partição, mas não ordena eventos de pedidos diferentes.
- (d) Garante que cada pedido seja processado por um único consumidor para sempre, mas não garante retenção.

#### Questão 18 [Difícil]

Uma equipe quer mudar a unidade do campo valor de reais para centavos em um evento já publicado, sem alterar o nome nem o tipo. Como o módulo avalia a mudança?

- (a) Compatível, porque o parse continua funcionando.
- (b) Compatível, desde que o consumidor use esquema estrito.
- (c) Incompatível apenas para consumidores escritos em outra linguagem.
- (d) Pode quebrar o negócio sem quebrar o parse, e uma ruptura de semântica pede nova versão no nome, com transição documentada.

#### Questão 19 [Difícil]

A DLQ de Faturamento acumula centenas de mensagens há semanas, sem alerta e sem responsável definido. Qual é a leitura do módulo?

- (a) A DLQ está funcionando como trilha de auditoria geral.
- (b) A DLQ virou armazenamento silencioso de falhas, porque sem owner, alerta e procedimento de decisão ela não preserva evidência útil.
- (c) A DLQ deve ser reprocessada automaticamente em loop até esvaziar.
- (d) A DLQ corrige o schema automaticamente com o tempo.

#### Questão 20 [Difícil]

No caso real do módulo, o LinkedIn substituiu uma cadeia de chamadas síncronas por um log distribuído que deu origem ao Kafka. Que propriedades do log justificam essa troca, segundo o módulo?

- (a) Retenção, leitura não destrutiva e leitura simultânea por vários grupos independentes, sem que a origem conheça os consumidores.
- (b) Ordem global e ausência de repetição garantidas para todos os eventos.
- (c) Eliminação da necessidade de idempotência nos consumidores.
- (d) Consistência forte imediata entre todos os sistemas.
