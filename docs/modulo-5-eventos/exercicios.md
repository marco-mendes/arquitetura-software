# Exercícios: decidir integrações assíncronas

As propostas usam o caso hospitalar e dados sintéticos. Não há resposta única: declare premissas, diferencie fato de hipótese e trate contrato, falha e operação como parte da decisão. Cada atividade produz um artefato autocontido, sem depender de configuração manual em um ambiente remoto.

## Recordar

### Nomear semântica e componentes

**Situação**

Uma equipe recebeu os nomes `ResultadoLaboratorialDisponibilizado.v1`, `GerarCobranca`, `hospital.events`, `billing.resultados.v1`, `hospital.events.dlx` e `billing.resultados.v1.dlq`, mas mistura intenção de domínio e elemento de transporte.

**Seu papel**

Você prepara um glossário de entrada para a equipe.

1\. A equipe usa evento, comando, mensagem, broker, mediator, fila, tópico e log distribuído de forma intercambiável em reuniões, e isso já gerou pelo menos uma discussão de projeto que não chegava a lugar nenhum porque duas pessoas falavam de coisas diferentes com a mesma palavra. Defina cada um dos oito termos numa frase curta, escrita de um jeito que alguém que nunca leu este módulo consiga usar para separar os oito conceitos sem confundir um pelo outro.

<details>
<summary>Ver resposta</summary>

Evento afirma um fato já ocorrido; comando pede uma ação a alguém; mensagem é o envelope técnico que transporta os dois. Broker distribui mensagens sem decidir regra de negócio; mediator coordena uma conversa entre participantes e assume essa decisão. Fila reparte trabalho pendente entre consumidores; tópico distribui a mesma publicação para múltiplos destinos independentes; log distribuído retém a sequência publicada e permite releituras em ritmos diferentes.
</details>

2\. Antes de você chegar, ninguém na equipe sabia dizer de cabeça se `ResultadoLaboratorialDisponibilizado.v1` era um evento ou um comando, nem se `hospital.events.dlx` era uma fila ou uma exchange — a distinção nunca tinha sido escrita em lugar nenhum. Classifique cada um dos seis nomes da situação (`ResultadoLaboratorialDisponibilizado.v1`, `GerarCobranca`, `hospital.events`, `billing.resultados.v1`, `hospital.events.dlx` e `billing.resultados.v1.dlq`) numa das categorias evento, comando, exchange de domínio, fila de trabalho, exchange de dead-letter ou fila de dead-letter, e diga que pista no próprio nome levou você a cada classificação.

<details>
<summary>Ver resposta</summary>

`ResultadoLaboratorialDisponibilizado.v1` é evento, pelo particípio e pela versão explícita. `GerarCobranca` é comando, pelo verbo no infinitivo pedindo uma ação. `hospital.events` é a exchange de domínio, pelo nome genérico do canal. `billing.resultados.v1` é a fila de trabalho de um consumidor específico. `hospital.events.dlx` é a exchange de dead-letter, pelo sufixo `.dlx`. `billing.resultados.v1.dlq` é a fila de dead-letter correspondente, pelo sufixo `.dlq`.
</details>

3\. O mesmo glossário precisa cobrir o vocabulário de confiabilidade que a equipe vai usar toda semana ao operar a fila em produção, sem o qual cada incidente vira uma discussão do zero sobre o que as palavras significam. Defina entrega pelo menos uma vez, idempotência, ordenação e dead-letter queue, e diga por que uma equipe acostumada só com filas tradicionais tende a tratar as duas primeiras como sinônimos.

<details>
<summary>Ver resposta</summary>

Entrega pelo menos uma vez admite repetição da mensagem; idempotência é a propriedade que faz repetir a mensagem não repetir o efeito de negócio. Ordenação exige declarar qual sequência importa e sob qual chave; dead-letter queue guarda mensagens rejeitadas para decisão controlada, sem apagá-las. Equipes acostumadas a filas tradicionais tratam as duas primeiras como sinônimos porque, numa fila simples sem múltiplos consumidores nem redelivery agressivo, a repetição raramente aparece — até o dia em que aparece.
</details>

4\. Um desenvolvedor júnior da equipe trata `GerarCobranca` como se fosse um fato já consumado: assim que a mensagem chega, ele processa a cobrança sem checar se ela foi de fato autorizada por outro serviço antes. Descreva a consequência prática dessa confusão entre comando e evento nesse cenário específico, e escreva a frase que você usaria para corrigir o entendimento dele.

<details>
<summary>Ver resposta</summary>

Tratar um comando como um evento já consumado pula a etapa de decisão que o comando deveria disparar: a cobrança sai sem que ninguém tenha verificado se ela era devida, e se a autorização vier a ser negada depois, o dinheiro já saiu. A correção: "`GerarCobranca` pede que você decida e aja; só publique o fato de que a cobrança ocorreu depois de ter decidido, nunca antes."
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

Um `set()` em memória existe só enquanto o processo está vivo: um reinício zera o histórico de `event_id` vistos, e uma segunda réplica começa com o próprio `set()` vazio, sem conhecimento do que a primeira já processou. `event_id` como chave primária numa tabela durável sobrevive a reinício e é compartilhada entre réplicas que apontam para o mesmo banco, porque a garantia passou a ser uma propriedade dos dados, não uma variável de um processo específico.
</details>

## Aplicar
### Recomendar a forma de propagar o resultado de exame

**Objetivo**

Recomendar uma entre quatro formas de propagar um fato para três consumidores independentes, declarando ganho, custo e a pré-condição que falta.

**Situação**

No hospital, o serviço de Exames grava o resultado no próprio banco e precisa avisar três destinos. Faturamento usa o resultado para compor a conta. Notificações avisa o paciente. Auditoria guarda o histórico para consulta posterior.

Hoje o serviço de Exames chama os três em sequência, dentro da mesma transação que grava o resultado. Na semana passada, o serviço de Notificações ficou lento e resultados deixaram de ser gravados. O time descobriu por reclamação de médico, e não por alarme.

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

Escreva em prosa, uma resposta por item. Não é preciso desenhar nada.

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

Faturamento parou de fechar contas. As reclamações chegaram pelo atendimento, e não por alarme.

Na véspera, o time de Resultados publicou uma versão nova do contrato do evento. O campo `unidade_medida`, que antes vinha sempre preenchido, passou a ser opcional.

Os sinais disponíveis são a idade da mensagem mais antiga na fila, a contagem de mensagens, o identificador de cada evento, os registros de log do consumidor e a versão do contrato publicada. Nenhum servidor ficou fora do ar no período, e o consumo de recursos das máquinas está normal.

Cinco fatos valem para a análise:

1. A fila saiu de dezenas para onze mil mensagens em quatro horas.
2. A fila de rejeitadas, normalmente vazia, tem trezentas mensagens.
3. Uma versão nova do contrato foi publicada na véspera, tornando um campo opcional.
4. Nenhum servidor ficou indisponível, e o uso de recursos está normal.
5. O problema foi descoberto por reclamação de usuário, e não por alarme.

**Seu papel**

Você conduz a investigação antes de qualquer correção. Reiniciar o consumidor é tentador e destruiria evidência.

**O que fazer**

Escreva em prosa, uma resposta por item.

1. Escreva duas hipóteses diferentes que explicam o crescimento da fila, e diga que sinal disponível separaria uma da outra.
2. O fato 3 tornou um campo opcional. Explique por que uma mudança que afrouxa uma regra pode quebrar um consumidor, em vez de facilitar a vida dele.
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

Escreva em prosa, uma resposta por item.

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

Escreva em prosa, uma resposta por item.

1. Escolha um dos três caminhos e defenda a escolha citando pelo menos duas das quatro restrições.
2. Sobre os dois caminhos que você não escolheu, escreva duas frases cada: o que ganhariam e o que custariam.
3. Descreva a ordem das etapas da sua proposta, dizendo o que cada uma das três equipes faz e em que momento. Deixe claro quando o consumidor antigo pode ser desligado da versão 1.
4. Explique o que acontece com o descarte de mensagem repetida enquanto os dois formatos coexistem, e como você impede que o mesmo resultado seja processado duas vezes.
5. Escreva o sinal que indicaria que a transição terminou e a versão antiga pode sair do ar.

**Evidência esperada**

O arquivo entregue traz o caminho escolhido com duas restrições citadas, os outros dois avaliados, a ordem das etapas com responsável por etapa, o tratamento da repetição durante a coexistência e o sinal de encerramento da transição.
