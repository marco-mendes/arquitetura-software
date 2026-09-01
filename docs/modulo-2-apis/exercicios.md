# Exercícios por Taxonomia de Bloom

Responda primeiro e abra “Ver resposta” somente depois da tentativa. Nas atividades de Aplicar, Analisar, Avaliar e Criar, siga o roteiro completo: ele apresenta o artefato, a condição de início, a evidência e os limites da prática antes de pedir uma decisão.

## Recordar

1\. Toda API tem três camadas fáceis de confundir: a **interface** (a porta oferecida), o **contrato** (as promessas observáveis) e a **implementação** (como elas são cumpridas). O que diferencia essas três?

<details markdown="1">
<summary>Ver resposta</summary>

Interface é a fronteira oferecida; contrato torna explícitas as promessas observáveis; implementação é o mecanismo que as cumpre. Um consumidor deveria depender do contrato, e não do framework ou banco usados internamente.
</details>

2\. Os métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`...) têm papéis diferentes por convenção. Qual é a diferença fundamental de propósito entre `GET` e `POST`?

<details markdown="1">
<summary>Ver resposta</summary>

`GET` solicita a representação atual de um recurso, sem a intenção de alterar estado no servidor. `POST` normalmente cria algo novo ou dispara um processamento, alterando o estado do servidor.
</details>

3\. Por que uma API REST evita colocar o nome da ação na própria URL — como `/criarPedido` ou `/listarPedidos` — e prefere algo como `POST /pedidos` e `GET /pedidos`?

<details markdown="1">
<summary>Ver resposta</summary>

Porque REST organiza a API em torno de **recursos** (substantivos) e deixa a ação a cargo do **verbo HTTP**. Repetir a ação na URL duplica a semântica e quebra a uniformidade que permite tratamento genérico por ferramentas, cache e roteamento.
</details>

4\. Em integrações, a mesma chamada às vezes chega repetida. O que significa dizer que uma operação é **idempotente**?

<details markdown="1">
<summary>Ver resposta</summary>

Repetir a mesma intenção produz o mesmo efeito pretendido no servidor. Isso não exige que cada resposta seja idêntica nem cria deduplicação automática em uma integração distribuída.
</details>

5\. Existe um formato padrão para descrever por escrito os paths, operações, schemas, exemplos e respostas de uma API HTTP. Que artefato é esse?

<details markdown="1">
<summary>Ver resposta</summary>

Um documento OpenAPI. No laboratório, o contrato explícito está em `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`.
</details>

6\. Um **API gateway** fica na borda, entre os consumidores e as APIs internas. Cite duas responsabilidades técnicas adequadas a ele — e uma que **não** deveria ficar nele.

<details markdown="1">
<summary>Ver resposta</summary>

Roteamento, terminação TLS, autenticação técnica, limite de tráfego, correlação e telemetria são responsabilidades possíveis. Tradução de vocabulário do laboratório e regras de elegibilidade não devem ser despejadas no gateway.
</details>

## Compreender

1\. Uma operação `POST /aprovarAutomaticamente` usa JSON e HTTP. Por que ela pode ser um RPC coerente, mas não deve ser chamada de REST só por causa disso?

<details markdown="1">
<summary>Ver resposta</summary>

RPC organiza a colaboração por operações nomeadas. REST requer restrições e semântica de recursos, representações e mensagens HTTP; uma URL com HTTP não comprova essas propriedades.
</details>

2\. Comparado a uma API de leitura com campos fixos, quando o GraphQL tende a ajudar mais?

<details markdown="1">
<summary>Ver resposta</summary>

Quando consumidores precisam de combinações de campos e relações muito variáveis. Ainda é necessário controlar custo das consultas, autorização por campo e cache; não é a escolha automática para qualquer tela móvel.
</details>

3\. O **WebSocket** mantém um canal aberto entre cliente e servidor. O que ele resolve, e o que ele não resolve sozinho?

<details markdown="1">
<summary>Ver resposta</summary>

Ele mantém um canal bidirecional persistente para atualização em tempo real. Não garante entrega durável, reprocessamento, ordenação de negócio ou recuperação após desconexão; essas políticas precisam ser projetadas.
</details>

4\. O laboratório fala **SOAP/TISS** (o padrão de troca das operadoras) e a plataforma usa o próprio vocabulário. Por que traduzir entre os dois é mais apropriado num **adaptador** do que no **gateway**?

<details markdown="1">
<summary>Ver resposta</summary>

Porque a tradução contém conhecimento da dependência e de seus significados. O gateway pode aplicar políticas técnicas; o adaptador isola mudanças externas e protege o domínio interno da plataforma.
</details>

## Aplicar
### Recomendar o estilo de entrega do resultado ao parceiro

**Objetivo**

Recomendar um entre quatro estilos de interação para entregar resultados de exame a uma operadora parceira, declarando ganho, custo e o fato que decide.

**Situação**

O hospital precisa entregar o resultado de exames a uma operadora de saúde parceira. O resultado nasce no laboratório e fica pronto muito depois do pedido. A operadora usa esse resultado para liberar procedimentos seguintes, então o atraso tem consequência para o paciente.

Hoje não existe integração. Alguém exporta uma planilha no fim do dia e envia por correio eletrônico. A operadora reclama do atraso e o hospital reclama do retrabalho.

A área de integração pediu uma recomendação de contrato antes de abrir o projeto.

Seis fatos foram apurados nas duas empresas:

1. O resultado fica pronto entre vinte minutos e seis horas depois do pedido, sem previsibilidade.
2. A operadora processa no máximo quatrocentos resultados por dia.
3. O contrato entre as empresas exige comprovar a entrega de cada resultado, com identificador e carimbo de tempo.
4. A operadora não mantém endereço público para receber chamadas de entrada, e a área de segurança dela não pretende abrir um.
5. O hospital não opera fila nem *broker* hoje, e a infraestrutura tem uma pessoa.
6. Um atraso de até quinze minutos entre o resultado ficar pronto e chegar à operadora é aceitável.

As quatro alternativas em avaliação:

| Alternativa | O que muda no contrato |
| --- | --- |
| **A. Consulta periódica** | O hospital expõe um recurso REST com os resultados prontos. A operadora consulta de tempos em tempos e marca o que já leu. |
| **B. Aceitação assíncrona** | A operadora registra o interesse num pedido e recebe `202` com `Location`. Consulta aquele protocolo depois, até o resultado aparecer. |
| **C. Chamada de retorno** | Quando o resultado fica pronto, o hospital chama um endereço da operadora e entrega o conteúdo. |
| **D. Mensageria** | O hospital publica cada resultado num tópico. A operadora consome no próprio ritmo, com reprocessamento possível. |

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação de contrato. A implementação fica com outra equipe, que espera de você a escolha e os riscos declarados.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende uma das quatro alternativas, em uma frase.
2. Sobre cada uma das quatro, escreva duas frases: o que ela resolve do problema descrito e o que ela cobra em troca.
3. Na alternativa recomendada, diga o que a operadora recebe quando o resultado ainda não ficou pronto, e onde fica registrada a comprovação de entrega que o fato 3 exige.
4. Aponte a alternativa que você descartaria de imediato e diga qual fato a derruba.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria trocar de alternativa.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, o contrato de erro escrito com código de status e identificador, a resposta sobre comprovação de entrega, a alternativa descartada com o fato que a derruba, o risco aceito e o sinal de revisão observável.

## Analisar
**Objetivo**

Explicar por que três contratos de consulta que funcionam isoladamente quebram quando usados juntos, e comparar as saídas possíveis.

**Situação**

Um sistema de agendamento hospitalar consulta a agenda de três parceiros diferentes para montar uma lista única de horários livres. São até quarenta mil horários futuros, e o aplicativo do paciente carrega vinte por vez, conforme ele rola a tela.

Os três parceiros paginam de jeitos diferentes. O parceiro A devolve os horários ordenados por data e aceita pular um número de registros. O parceiro B devolve na ordem que quiser, e a ordem muda entre uma chamada e outra. O parceiro C entrega um cursor próprio, uma marca opaca que o consumidor devolve para pedir a página seguinte.

Enquanto o paciente rola a tela, horários são criados e cancelados o tempo inteiro. Pacientes relatam duas coisas: horários que aparecem duas vezes na lista, e horários que existem e nunca aparecem.

Quatro fatos foram apurados:

1. O aplicativo pede vinte horários por vez, e o paciente costuma rolar de cinco a dez páginas.
2. Criações e cancelamentos acontecem durante a navegação, em média quatro por minuto.
3. Os três parceiros respondem em menos de trezentos milissegundos.
4. Nenhum dos três aceita alterar o contrato antes de seis meses.

Três saídas estão sobre a mesa:

#### Saída A

O sistema busca a lista inteira dos três parceiros, monta a página no próprio lado e serve o aplicativo a partir dessa cópia.

#### Saída B

O sistema mantém a paginação de cada parceiro como está e passa a devolver, junto de cada horário, um identificador estável que o aplicativo usa para descartar repetição.

#### Saída C

O sistema adota um cursor próprio para o aplicativo e, por baixo, traduz esse cursor para o mecanismo de cada parceiro, guardando a posição de leitura de cada um.

Os quatro fatos, o comportamento de paginação dos três parceiros e as três saídas, todos descritos nesta página.

**Seu papel**

Você conduz a análise antes de qualquer mudança de contrato. Nenhum parceiro será convencido a mudar nesta semana.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Explique por que o parceiro B produz horários repetidos e horários invisíveis, ligando o defeito ao fato 2.
2. Diga se o mesmo defeito aparece com o parceiro A, e por quê. Depois faça o mesmo para o parceiro C.
3. Sobre cada uma das três saídas, escreva duas frases: o que ela resolve e o que ela cobra em troca.
4. Recomende uma das três e cite o fato que mais pesou na escolha.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria revê-la.

**Evidência esperada**

O arquivo entregue explica o mecanismo do defeito em vez de apenas nomeá-lo, distingue o comportamento dos três parceiros, traz ganho e custo das três saídas e registra o sinal de revisão como condição observável.

## Avaliar
**Objetivo**

Julgar três propostas de contrato para uma operação lenta e instável, declarando critérios antes de escolher e nomeando o que a evidência não alcança.

**Situação**

Um hospital consulta a operadora para autorizar procedimentos. No horário de pico chegam doze mil pedidos de autorização por hora.

A operadora é lenta e irregular: responde entre duzentos milissegundos e vinte e cinco segundos, sem padrão. Duas vezes por mês fica indisponível por até dez minutos seguidos.

O comportamento do consumidor piora o quadro. Cinco por cento dos pedidos são repetidos pelo próprio sistema do hospital dois segundos depois, quando a primeira chamada demora.

Três propostas chegaram ao comitê.

#### Proposta A

O hospital mantém a chamada aberta esperando a operadora responder, com um tempo limite de trinta segundos.

#### Proposta B

O hospital aceita o pedido, devolve imediatamente um protocolo e resolve a autorização em segundo plano. O consumidor consulta o protocolo depois.

#### Proposta C

O hospital aceita o pedido e devolve na hora a última decisão conhecida para aquele beneficiário e procedimento, quando existir, marcando a resposta como provisória.

O que se sabe e o que não se sabe:

1. A distribuição de tempo de resposta da operadora foi medida por três meses.
2. A frequência de indisponibilidade foi medida no mesmo período.
3. Ninguém mediu quantos pedidos repetidos viram autorização duplicada hoje.
4. Ninguém mediu por quanto tempo uma decisão anterior continua válida.
5. A equipe de operação trabalha em horário comercial.

As três propostas, os números de volume e de tempo de resposta, e a lista do que foi medido e do que não foi, todos nesta página.

**Seu papel**

Você emite o parecer que o comitê vai discutir. Pode aprovar uma proposta, recusar todas ou aprovar com condição.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Declare de três a cinco critérios de julgamento e diga qual pesa mais neste caso, justificando pelo risco de errar.
2. Avalie as três propostas contra os seus critérios, um parágrafo por proposta, dizendo o que cada uma protege e o que expõe.
3. A proposta C depende de uma medida que ninguém tem. Diga qual é, e o que aconteceria se a equipe adotasse C sem ela.
4. Emita o parecer e escreva o contrato de resposta da proposta que você aprovar: o que o consumidor recebe no caso de sucesso, e o que recebe enquanto a decisão não existe.
5. Escreva a objeção mais forte contra o seu parecer e responda a ela.

**Evidência esperada**

O parecer traz critérios escritos antes da escolha, as três propostas julgadas contra eles, a medida ausente nomeada com a consequência de ignorá-la, o contrato de resposta descrito e uma objeção respondida.

## Criar
**Objetivo**

Propor o contrato inicial de uma capacidade que será consumida por três públicos diferentes, escolhendo entre três esboços e declarando o que fica de fora.

**Situação**

O hospital vai expor, pela primeira vez, a consulta de elegibilidade de um beneficiário. Três públicos vão consumir essa capacidade, e eles querem coisas diferentes.

O aplicativo do paciente precisa de uma resposta curta e rápida, porque roda em rede móvel e mostra apenas se o beneficiário está apto.

O sistema interno de recepção precisa da resposta completa, com vigência, categoria do plano e motivo da recusa, para orientar o atendente.

Uma operadora parceira quer receber a mesma informação, e o contrato que ela mantém com outros hospitais usa XML sobre um envelope antigo, que o hospital não usa em lugar nenhum.

A equipe tem quatro pessoas e três meses até a primeira entrega.

Três esboços estão sobre a mesa:

#### Esboço A

Um contrato único, com a resposta completa, servindo os três públicos. Quem precisa de menos ignora os campos que sobram.

#### Esboço B

Dois contratos sobre a mesma capacidade: um enxuto para o aplicativo e um completo para a recepção. A operadora consome o completo.

#### Esboço C

Dois contratos internos, como no esboço B, mais um adaptador dedicado que traduz para o envelope XML da operadora, isolado do resto.

As três necessidades de consumo, a restrição de equipe e prazo e os três esboços, todos nesta página.

**Seu papel**

Você propõe o contrato inicial. Ele será a fronteira pública do hospital por vários anos, e mudá-lo depois exige combinar com quem já consome.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três esboços e defenda a escolha citando pelo menos duas das necessidades descritas.
2. Sobre os dois esboços que você não escolheu, escreva duas frases cada: o que ganhariam e o que custariam.
3. Descreva o que o consumidor recebe em três situações: beneficiário apto, beneficiário sem cobertura para o procedimento e identificador desconhecido. Diga o que muda entre a segunda e a terceira.
4. A operadora usa um formato que o hospital não usa. Diga onde essa tradução deve morar na sua proposta, e o que aconteceria se ela vazasse para o contrato interno.
5. Escreva o sinal que indicaria que o contrato escolhido precisa evoluir, e diga como você faria essa evolução sem quebrar quem já consome.

**Evidência esperada**

O arquivo entregue traz o esboço escolhido com duas necessidades citadas, os outros dois avaliados, as três situações de resposta descritas com a diferença entre elas explicada, o lugar da tradução justificado e um caminho de evolução compatível.
