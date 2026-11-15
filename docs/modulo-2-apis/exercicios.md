# Exercícios por Taxonomia de Bloom

Responda primeiro e abra “Ver resposta” somente depois da tentativa. Nas atividades dos níveis Aplicar, Analisar, Avaliar e Criar o roteiro completo antecede o pedido de decisão. O roteiro apresenta o artefato, a condição de início, a evidência e os limites da prática.

## Recordar

1\. O que diferencia a **interface**, o **contrato** e a **implementação**, as três camadas de uma API que costumam ser confundidas pelas equipes de desenvolvimento?

<details markdown="1">
<summary>Ver resposta</summary>

A interface é a fronteira oferecida ao consumidor e o contrato torna explícitas as promessas observáveis dessa fronteira. A implementação é o mecanismo que cumpre essas promessas. Um consumidor deveria depender somente do contrato, sem depender do *framework* ou do banco de dados usados internamente pelo provedor da API.

</details>

2\. Qual é a diferença fundamental de propósito entre os métodos `GET` e `POST` do protocolo HTTP, considerando que cada método HTTP tem um papel definido por convenção?

<details markdown="1">
<summary>Ver resposta</summary>

O método `GET` solicita a representação atual de um recurso sem a intenção de alterar o estado do servidor. O método `POST` normalmente cria algo novo ou dispara um processamento e, com isso, altera o estado do servidor HTTP.

</details>

3\. Por que uma API REST evita colocar o nome da ação na própria URL, como em `/criarPedido` ou `/listarPedidos`, preferindo formas como `POST /pedidos` e `GET /pedidos`?

<details markdown="1">
<summary>Ver resposta</summary>

O estilo REST organiza a API em torno de **recursos** nomeados por substantivos e deixa a ação a cargo do **método HTTP**. A repetição da ação na URL duplica a semântica e quebra a uniformidade que permite o tratamento genérico das requisições por ferramentas, *caches* e roteadores HTTP.

</details>

4\. O que significa dizer que uma operação de uma API HTTP é **idempotente**, considerando que em integrações entre sistemas a mesma chamada às vezes chega repetida ao servidor?

<details markdown="1">
<summary>Ver resposta</summary>

Uma operação idempotente é aquela em que a repetição da mesma intenção produz o mesmo efeito pretendido no servidor. A idempotência não exige que cada resposta seja idêntica e não cria deduplicação automática numa integração distribuída entre sistemas HTTP.

</details>

5\. Que artefato padronizado descreve por escrito os *paths*, as operações e os *schemas* de uma API HTTP com seus exemplos e respostas?

<details markdown="1">
<summary>Ver resposta</summary>

O artefato é um documento OpenAPI, que no laboratório corresponde ao contrato explícito gravado em `laboratorios/plataforma-hospitalar/contratos/openapi.yaml`.

</details>

6\. Cite duas responsabilidades técnicas adequadas ao ***API gateway*** que fica na borda da arquitetura entre os consumidores e as APIs internas e uma responsabilidade que **não** deveria ser atribuída a esse componente.

<details markdown="1">
<summary>Ver resposta</summary>

O roteamento, a terminação TLS e a autenticação técnica são responsabilidades possíveis do *gateway*. O limite de tráfego, a correlação e a telemetria também são responsabilidades adequadas a ele. A tradução de vocabulário do laboratório e as regras de elegibilidade não devem ser colocadas no *gateway* da API.

</details>

## Compreender

1\. Por que a operação `POST /aprovarAutomaticamente`, que usa JSON e HTTP, pode ser um RPC coerente e ainda assim não deve ser chamada de REST apenas por usar JSON e HTTP?

<details markdown="1">
<summary>Ver resposta</summary>

O RPC organiza a colaboração por operações nomeadas. O REST requer restrições e a semântica de recursos, representações e mensagens HTTP, de modo que uma URL acessada por HTTP não comprova essas propriedades do estilo REST.

</details>

2\. Em comparação com uma API de leitura com campos fixos, em que situação o GraphQL tende a ajudar mais o consumidor?

<details markdown="1">
<summary>Ver resposta</summary>

O GraphQL ajuda mais quando os consumidores precisam de combinações de campos e de relações muito variáveis. O provedor ainda precisa controlar o custo das consultas, a autorização por campo e o *cache*. O GraphQL não é a escolha automática para qualquer tela de aplicativo móvel.

</details>

3\. Considerando que o **WebSocket** mantém um canal aberto entre cliente e servidor, o que o WebSocket resolve e o que ele não resolve sozinho?

<details markdown="1">
<summary>Ver resposta</summary>

O WebSocket mantém um canal bidirecional persistente para atualização em tempo real entre cliente e servidor. Ele não garante entrega durável, reprocessamento e ordenação de negócio nem recuperação após desconexão, políticas que precisam ser projetadas fora do protocolo WebSocket.

</details>

4\. O laboratório usa **SOAP/TISS**, padrão de troca de dados das operadoras de saúde, enquanto a plataforma hospitalar usa o próprio vocabulário de negócio. Por que a tradução entre os dois vocabulários é mais apropriada num **adaptador** do que no ***gateway*** da plataforma hospitalar?

<details markdown="1">
<summary>Ver resposta</summary>

A tradução contém conhecimento da dependência externa e dos significados que ela atribui aos dados. O *gateway* pode aplicar políticas técnicas, enquanto o adaptador isola as mudanças externas e protege o domínio interno da plataforma contra o vocabulário SOAP/TISS.

</details>

## Aplicar
### Recomendar o estilo de entrega do resultado ao parceiro

**Objetivo**

Recomendar um entre quatro estilos de interação para entregar resultados de exame a uma operadora parceira, com a declaração do ganho, do custo e do fato que decide a escolha.

**Situação**

O hospital precisa entregar o resultado de exames a uma operadora de saúde parceira. O resultado é produzido pelo laboratório e fica pronto muito depois do pedido. A operadora usa esse resultado para liberar os procedimentos seguintes, de modo que o atraso tem consequência para o paciente.

Atualmente não existe integração entre as duas empresas. Um funcionário exporta uma planilha no fim do dia e a envia por correio eletrônico à operadora. A operadora reclama do atraso na entrega e o hospital reclama do retrabalho manual que a planilha exige.

A área de integração pediu uma recomendação de contrato antes de abrir o projeto.

A lista abaixo reúne os seis fatos apurados nas duas empresas.

1. O resultado fica pronto entre vinte minutos e seis horas depois do pedido, sem previsibilidade.
2. A operadora processa no máximo quatrocentos resultados por dia.
3. O contrato entre as empresas exige comprovar a entrega de cada resultado, com identificador e carimbo de tempo.
4. A operadora não mantém endereço público para receber chamadas de entrada e a área de segurança dela não pretende abrir um.
5. O hospital não opera fila nem *broker* atualmente e a equipe de infraestrutura tem uma pessoa.
6. Um atraso de até quinze minutos entre o resultado ficar pronto e chegar à operadora é aceitável.

A tabela abaixo descreve as quatro alternativas em avaliação.

| Alternativa | O que muda no contrato |
| --- | --- |
| **A. Consulta periódica** | O hospital expõe um recurso REST com os resultados prontos. A operadora consulta de tempos em tempos e marca o que já leu. |
| **B. Aceitação assíncrona** | A operadora registra o interesse num pedido e recebe `202` com `Location`. Consulta aquele protocolo depois, até o resultado aparecer. |
| **C. Chamada de retorno** | Quando o resultado fica pronto, o hospital chama um endereço da operadora e entrega o conteúdo. |
| **D. Mensageria** | O hospital publica cada resultado num tópico. A operadora consome no próprio ritmo, com reprocessamento possível. |

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação de contrato. A implementação fica com outra equipe, que espera de você a escolha e os riscos declarados.

**O que fazer**

Escreva em texto corrido uma resposta para cada item da lista abaixo, sem necessidade de diagramas.

1. Recomende uma das quatro alternativas em uma frase.
2. Escreva duas frases sobre cada uma das quatro alternativas, que indiquem o que ela resolve do problema descrito e o que ela exige em troca.
3. Na alternativa recomendada, diga o que a operadora recebe quando o resultado ainda não ficou pronto. Diga também onde fica registrada a comprovação de entrega que o fato 3 exige.
4. Aponte a alternativa que você descartaria de imediato e diga qual fato a elimina.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que levaria à troca de alternativa.

**Evidência esperada**

O artefato traz o quadro comparativo completo e a recomendação em uma frase. Ele também traz o contrato de erro escrito com código de status e identificador e a resposta sobre a comprovação de entrega. Por fim, registra a alternativa descartada com o fato que a elimina, o risco aceito e o sinal de revisão observável.

## Analisar
**Objetivo**

Explicar por que três contratos de consulta que funcionam isoladamente falham quando usados em conjunto e comparar as saídas possíveis.

**Situação**

Um sistema de agendamento hospitalar consulta a agenda de três parceiros diferentes para montar uma lista única de horários livres. A lista tem até quarenta mil horários futuros e o aplicativo do paciente carrega vinte por vez, conforme o paciente rola a tela.

A tabela abaixo descreve a forma de paginação de cada parceiro.

| Parceiro | Como pagina |
| --- | --- |
| **A** | Devolve os horários ordenados por data e aceita pular um número de registros, informado pelo consumidor a cada chamada. |
| **B** | Aceita pular um número de registros e devolve os horários numa ordem própria, que muda entre uma chamada e outra. |
| **C** | Entrega um cursor próprio, uma marca opaca que o consumidor devolve para pedir a página seguinte. |

Enquanto o paciente rola a tela, horários são criados e cancelados continuamente. Os pacientes relatam dois problemas, que são horários repetidos na lista e horários existentes que nunca aparecem nela.

A lista abaixo reúne os quatro fatos apurados.

1. O aplicativo pede vinte horários por vez e o paciente costuma rolar de cinco a dez páginas.
2. Criações e cancelamentos acontecem durante a navegação, em média quatro por minuto.
3. Os três parceiros respondem em menos de trezentos milissegundos.
4. Nenhum dos três aceita alterar o contrato antes de seis meses.

As três saídas em discussão estão descritas a seguir.

#### Saída A

O sistema busca a lista inteira dos três parceiros, monta a página no próprio lado e serve o aplicativo a partir dessa cópia.

#### Saída B

O sistema mantém a paginação de cada parceiro como está e passa a devolver, junto de cada horário, um identificador estável que o aplicativo usa para descartar repetição.

#### Saída C

O sistema adota um cursor próprio para o aplicativo e traduz internamente esse cursor para o mecanismo de cada parceiro, com o registro da posição de leitura de cada um.

Os quatro fatos numerados, a tabela de paginação dos três parceiros e as três saídas estão descritos nesta página.

**Seu papel**

Você conduz a análise antes de qualquer mudança de contrato. Nenhum parceiro aceitará mudar o próprio contrato nesta semana.

**O que fazer**

Escreva em texto corrido uma resposta para cada item da lista abaixo.

1. Explique por que o parceiro B produz horários repetidos e horários invisíveis, com a ligação entre o defeito e o fato 2.
2. Diga se o mesmo defeito aparece com o parceiro A e explique o motivo. Depois faça a mesma análise para o parceiro C.
3. Escreva duas frases sobre cada uma das três saídas, que indiquem o que ela resolve e o que ela exige em troca.
4. Recomende uma das três saídas e cite o fato que mais pesou na escolha.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que levaria à revisão dela.

**Evidência esperada**

O arquivo entregue explica o mecanismo do defeito além de nomeá-lo e distingue o comportamento dos três parceiros. Ele também traz o ganho e o custo das três saídas e registra o sinal de revisão como condição observável.

## Avaliar
**Objetivo**

Julgar três propostas de contrato para uma operação lenta e instável, com a declaração dos critérios antes da escolha e a identificação do que a evidência não alcança.

**Situação**

Um hospital consulta a operadora para autorizar procedimentos e recebe doze mil pedidos de autorização por hora no horário de pico.

A operadora tem tempo de resposta lento e irregular, que varia entre duzentos milissegundos e vinte e cinco segundos sem padrão definido. Duas vezes por mês, a operadora fica indisponível por até dez minutos seguidos.

O comportamento do consumidor agrava a situação. Cinco por cento dos pedidos são repetidos pelo próprio sistema do hospital dois segundos depois, quando a primeira chamada demora.

Três propostas chegaram ao comitê.

#### Proposta A

O hospital mantém a chamada aberta esperando a operadora responder, com um tempo limite de trinta segundos.

#### Proposta B

O hospital aceita o pedido, devolve imediatamente um protocolo e resolve a autorização em segundo plano. O consumidor consulta o protocolo depois.

#### Proposta C

O hospital aceita o pedido e devolve na hora a última decisão conhecida para aquele beneficiário e procedimento, quando existir, marcando a resposta como provisória.

A lista abaixo reúne o que foi medido nos últimos três meses.

1. O tempo de resposta da operadora fica entre duzentos milissegundos e um segundo em metade dos pedidos. Ele passa de dois segundos em cerca de cinco por cento deles e chega a vinte e cinco segundos no pior caso.
2. A operadora ficou indisponível seis vezes no período, por até dez minutos seguidos em cada uma.
3. O pico chega a doze mil pedidos de autorização por hora.
4. Cinco por cento dos pedidos são repetidos pelo sistema do hospital dois segundos depois da primeira chamada.

A lista abaixo reúne o que não foi medido.

5. Ninguém mediu quantos pedidos repetidos resultam hoje em autorização duplicada.
6. Ninguém mediu por quanto tempo uma decisão anterior continua válida para o mesmo beneficiário e procedimento.

Há ainda uma restrição de operação.

7. A equipe de operação trabalha em horário comercial e ninguém acompanha a integração à noite.

As três propostas e as listas numeradas do que foi medido, do que não foi medido e da restrição de operação estão descritas nesta página.

**Seu papel**

Você emite o parecer que o comitê vai discutir. O parecer pode aprovar uma proposta, recusar as três ou aprovar uma delas com condição.

**O que fazer**

Escreva em texto corrido uma resposta para cada item da lista abaixo.

1. Declare de três a cinco critérios de julgamento e diga qual pesa mais neste caso, com justificativa baseada no risco de errar.
2. Avalie as três propostas segundo os seus critérios, em um parágrafo por proposta, com o que cada uma protege e o que expõe.
3. A proposta C depende de uma medida que ninguém tem. Diga qual é essa medida e o que aconteceria se a equipe adotasse C sem ela.
4. Emita o parecer e escreva o contrato de resposta da proposta que você aprovar. O contrato deve indicar o que o consumidor recebe no caso de sucesso e o que recebe enquanto a decisão não existe.
5. Escreva a objeção mais forte contra o seu parecer e responda a ela.

**Evidência esperada**

O parecer traz critérios escritos antes da escolha e as três propostas julgadas segundo esses critérios. Ele também nomeia a medida ausente com a consequência de ignorá-la e descreve o contrato de resposta e uma objeção respondida.

## Criar
**Objetivo**

Propor o contrato inicial de uma capacidade que será consumida por três públicos diferentes, com a escolha entre três esboços e a declaração do que fica de fora.

**Situação**

O hospital vai expor pela primeira vez a consulta de elegibilidade de um beneficiário. A lista abaixo descreve os três públicos com necessidades diferentes que vão consumir essa capacidade.

1. O aplicativo do paciente precisa de uma resposta curta e rápida, porque é executado em rede móvel e mostra apenas se o beneficiário está apto.
2. O sistema interno de recepção precisa da resposta completa com vigência, categoria do plano e motivo da recusa para orientar o atendente.
3. Uma operadora parceira quer receber a mesma informação. O contrato que ela mantém com outros hospitais usa XML sobre um envelope antigo, que o hospital não usa em nenhum outro sistema.

A restrição de execução também está definida.

4. A equipe tem quatro pessoas e três meses até a primeira entrega.

Os três esboços em discussão estão descritos a seguir.

#### Esboço A

Um contrato único, com a resposta completa, servindo os três públicos. Quem precisa de menos ignora os campos que sobram.

#### Esboço B

Dois contratos sobre a mesma capacidade, sendo um enxuto para o aplicativo e um completo para a recepção. A operadora consome o contrato completo.

#### Esboço C

Dois contratos internos iguais aos do esboço B, acrescidos de um adaptador dedicado e isolado que traduz a resposta para o envelope XML da operadora.

As três necessidades de consumo numeradas de 1 a 3, a restrição de equipe e prazo no item 4 e os três esboços estão descritos nesta página.

**Seu papel**

Você propõe o contrato inicial. Esse contrato será a fronteira pública do hospital por vários anos e qualquer mudança posterior exige acordo com os consumidores existentes.

**O que fazer**

Escreva em texto corrido uma resposta para cada item da lista abaixo.

1. Escolha um dos três esboços e defenda a escolha com a citação de pelo menos duas das necessidades descritas.
2. Escreva duas frases sobre cada um dos dois esboços que você não escolheu, com o que ganhariam e o que custariam.
3. Descreva o que o consumidor recebe quando o beneficiário está apto, quando o beneficiário não tem cobertura para o procedimento e quando o identificador é desconhecido. Diga o que muda entre a segunda e a terceira situação.
4. A operadora usa um formato que o hospital não usa. Diga onde essa tradução deve ficar na sua proposta e o que aconteceria se ela fosse transferida para o contrato interno.
5. Escreva o sinal que indicaria que o contrato escolhido precisa evoluir. Diga também como você faria essa evolução sem quebrar os consumidores existentes.

**Evidência esperada**

O arquivo entregue traz o esboço escolhido com duas necessidades citadas e a avaliação dos outros dois esboços. Ele também descreve as três situações de resposta com a diferença entre elas explicada, justifica o lugar da tradução e apresenta um caminho de evolução compatível.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 2 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes. As questões simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

Na separação proposta pelo módulo, qual camada de uma API responde à pergunta "que promessa é observável?"

- (a) Interface.
- (b) Contrato.
- (c) Implementação.
- (d) Infraestrutura.

#### Questão 2 [Simples]

Qual método HTTP é, ao mesmo tempo, seguro e idempotente?

- (a) POST.
- (b) PATCH.
- (c) GET.
- (d) DELETE.

#### Questão 3 [Simples]

O que significa dizer que uma operação HTTP é idempotente?

- (a) Que repetir a mesma intenção produz o mesmo efeito pretendido no servidor, embora a resposta possa variar.
- (b) Que ela nunca altera o estado do servidor.
- (c) Que ela deduplica automaticamente qualquer transação distribuída.
- (d) Que ela sempre retorna o mesmo código de status e o mesmo corpo.

#### Questão 4 [Simples]

Em REST, o que é um recurso?

- (a) Uma tabela do banco de dados exposta pela API.
- (b) Um método HTTP aplicado a uma URL.
- (c) Um arquivo JSON armazenado no servidor.
- (d) Algo identificado por uma URI e manipulado por meio de representações.

#### Questão 5 [Simples]

Qual cabeçalho HTTP informa ao cliente onde acompanhar um recurso aceito, como em uma resposta 202 a POST /elegibilidades?

- (a) Location.
- (b) Content-Type.
- (c) Accept.
- (d) ETag.

#### Questão 6 [Simples]

Qual especificação descreve em YAML ou JSON os caminhos e as operações de uma API HTTP com seus parâmetros, corpos, respostas e schemas?

- (a) Protocol Buffers.
- (b) WSDL.
- (c) OpenAPI.
- (d) CloudEvents.

#### Questão 7 [Simples]

Entre as restrições REST definidas por Fielding, qual é opcional?

- (a) Cliente-servidor.
- (b) Sem estado.
- (c) Interface uniforme.
- (d) Código sob demanda.

#### Questão 8 [Simples]

Quais são as três capacidades de uma plataforma de APIs apresentadas no módulo?

- (a) Autenticação, autorização e auditoria.
- (b) Desenvolvimento, execução e engajamento.
- (c) Design, código e testes.
- (d) Cache, fila e banco de dados.

### Questões médias

#### Questão 9 [Média]

A API recebe POST /elegibilidades e responde 202 Accepted com o cabeçalho Location. O que essa resposta comunica ao consumidor?

- (a) Que a operadora já aprovou a elegibilidade e o recurso foi criado.
- (b) Que a solicitação foi rejeitada por dados inválidos.
- (c) Que o consumidor deve repetir a requisição até receber 200.
- (d) Que a solicitação foi aceita para processamento ainda sem decisão e pode ser acompanhada no endereço informado.

#### Questão 10 [Média]

Uma equipe criou a rota POST /aprovarAutomaticamente com corpo em JSON e afirma que a API é REST. Como o módulo avalia essa afirmação?

- (a) Incorreta, porque a operação é coerente como RPC, embora o uso de JSON e HTTP não a torne REST.
- (b) Correta, porque usa HTTP e JSON.
- (c) Correta, porque toda rota com verbo é REST.
- (d) Incorreta, porque POST não pode ser usado em APIs REST.

#### Questão 11 [Média]

Um aplicativo móvel precisa buscar exatamente os campos de álbuns, artistas e playlists em uma única consulta, com seleção variável a cada tela. Qual estilo atende melhor essa necessidade e qual cuidado o acompanha?

- (a) SOAP, com cuidado sobre a tradução do vocabulário do parceiro.
- (b) WebSocket, com cuidado sobre reconexão e ordenação.
- (c) GraphQL, com cuidado sobre custo, autorização e cache nos resolvers.
- (d) gRPC, com cuidado sobre a evolução da toolchain.

#### Questão 12 [Média]

Uma integração com o governo exige XML e SOAP e a equipe pergunta se a plataforma interna também precisa adotar XML. Qual é a orientação do módulo sobre o uso de XML na plataforma interna?

- (a) Sim, porque o formato do parceiro deve ser o formato canônico interno.
- (b) Não, porque usar SOAP com o parceiro não obriga a plataforma a adotar XML internamente e a tradução deve ficar isolada do domínio.
- (c) Sim, porque XML tem validação mais forte que JSON em qualquer cenário.
- (d) Não, porque SOAP está obsoleto e deve ser substituído pelo parceiro.

#### Questão 13 [Média]

O schema ErroAPI do laboratório usa codigo estável, mensagem legível e detalhes por campo. Qual problema esse desenho evita?

- (a) Que o servidor precise registrar logs de erro.
- (b) Que o consumidor dependa de texto livre para tratar o erro.
- (c) Que a API retorne códigos da família 5xx.
- (d) Que o contrato precise ser versionado.

#### Questão 14 [Média]

Uma coleção de agendamentos muda com frequência e é paginada por offset e limit. Qual risco o módulo aponta e qual alternativa sugere?

- (a) A paginação pode repetir ou omitir itens e um cursor opaco lida melhor com a mudança.
- (b) A paginação aumenta a latência e a alternativa é retornar a coleção inteira.
- (c) A paginação impede o cache e a alternativa é usar ETag em cada item.
- (d) A paginação quebra a idempotência do GET e a alternativa é usar POST.

#### Questão 15 [Média]

O arquivo openapi.yaml do laboratório é válido sintaticamente. Por que o módulo usa também Spectral, Bruno e TestClient?

- (a) Porque o OpenAPI não aceita exemplos de requisição.
- (b) Porque as três ferramentas geram o código do servidor a partir do contrato.
- (c) Porque um contrato válido ainda pode ser fraco e as três ferramentas examinam o documento, o consumo e a execução HTTP.
- (d) Porque o FastAPI exige essas ferramentas para iniciar.

### Questões difíceis

#### Questão 16 [Difícil]

Uma API pública precisa evoluir. Qual das mudanças abaixo tende a ser compatível com os consumidores existentes?

- (a) Tornar obrigatório um campo que antes era opcional.
- (b) Mudar a unidade de um campo numérico de reais para centavos.
- (c) Remover uma operação pouco usada.
- (d) Acrescentar um campo opcional, preservando o significado dos campos existentes.

#### Questão 17 [Difícil]

O cliente de um POST de autorização sofreu timeout e vai repetir a requisição, de modo que a equipe decide usar uma chave de idempotência. O que o módulo exige para que essa chave de idempotência funcione?

- (a) Apenas gerar um UUID novo a cada tentativa.
- (b) Trocar POST por PUT, porque PUT é idempotente por definição.
- (c) Confiar na deduplicação automática do protocolo HTTP.
- (d) Definir escopo, retenção, comparação da requisição e a resposta para uma repetição divergente.

#### Questão 18 [Difícil]

Uma dependência externa responde lentamente e a equipe propõe trocar REST por gRPC para resolver a latência. Como o módulo avalia a proposta?

- (a) Adequada, porque gRPC sempre reduz a latência total.
- (b) Adequada, porque gRPC elimina a necessidade de contrato.
- (c) Insuficiente, porque gRPC não resolve por si só a lentidão de uma dependência externa e a escolha deve partir da força e da evidência.
- (d) Insuficiente, porque gRPC só funciona com XML.

#### Questão 19 [Difícil]

Uma equipe quer substituir mensageria por WebSocket para notificar consumidores sobre resultados de exame, inclusive quando estiverem desconectados. Qual é a avaliação correta?

- (a) WebSocket não atende sozinho, porque manter o canal aberto não garante durabilidade de evento, que pede outro mecanismo.
- (b) WebSocket atende, porque mantém o canal aberto e garante a entrega.
- (c) WebSocket atende, porque é bidirecional e dispensa reconexão.
- (d) WebSocket não atende, porque só funciona entre servidores.

#### Questão 20 [Difícil]

No caso real do módulo, o Twitter abriu uma API, viu um ecossistema inteiro crescer sobre ela e depois a desligou três vezes. Qual princípio do módulo esse caso ilustra?

- (a) Que APIs públicas devem ser abertas sem qualquer contrato para estimular a adoção.
- (b) Que expor uma API transforma nomes, formatos e regras em compromissos públicos cuja mudança ou remoção afeta quem depende deles.
- (c) Que REST é inadequado para APIs públicas de grande escala.
- (d) Que ecossistemas de terceiros não dependem do contrato da API.
