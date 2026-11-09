# Exercícios por Taxonomia de Bloom

Responda primeiro e abra “Ver resposta” somente depois da tentativa. Nas atividades de Aplicar, Analisar, Avaliar e Criar, siga o roteiro completo: ele apresenta o artefato, a condição de início, a evidência e os limites da prática antes de pedir uma decisão.

## Recordar

1\. Toda API tem três camadas fáceis de confundir: a **interface** (a porta oferecida), o **contrato** (as promessas observáveis) e a **implementação** (como elas são cumpridas). O que diferencia essas três?

<details markdown="1">
<summary>Ver resposta</summary>

Interface é a fronteira oferecida; contrato torna explícitas as promessas observáveis; implementação é o mecanismo que as cumpre. Um consumidor deveria depender somente do contrato, sem depender do framework ou do banco usados internamente.
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

6\. Um **API gateway** fica na borda, entre os consumidores e as APIs internas. Cite duas responsabilidades técnicas adequadas a ele e uma responsabilidade que **não** deveria ficar nele.

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

3\. O **WebSocket** mantém um canal aberto entre cliente e servidor. O que ele resolve e o que ele não resolve sozinho?

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

Os três parceiros paginam de jeitos diferentes:

| Parceiro | Como pagina |
| --- | --- |
| **A** | Devolve os horários ordenados por data e aceita pular um número de registros, informado pelo consumidor a cada chamada. |
| **B** | Aceita pular um número de registros e devolve os horários numa ordem própria, que muda entre uma chamada e outra. |
| **C** | Entrega um cursor próprio, uma marca opaca que o consumidor devolve para pedir a página seguinte. |

Enquanto o paciente rola a tela, horários são criados e cancelados o tempo inteiro. Pacientes relatam duas coisas: horários que aparecem duas vezes na lista e horários que existem mas nunca aparecem.

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

Os quatro fatos numerados, a tabela de paginação dos três parceiros e as três saídas estão descritos nesta página.

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

O que foi medido nos últimos três meses:

1. O tempo de resposta da operadora fica entre duzentos milissegundos e um segundo em metade dos pedidos, passa de dois segundos em cerca de cinco por cento deles e chega a vinte e cinco segundos no pior caso.
2. A operadora ficou indisponível seis vezes no período, por até dez minutos seguidos em cada uma.
3. O pico chega a doze mil pedidos de autorização por hora.
4. Cinco por cento dos pedidos são repetidos pelo sistema do hospital dois segundos depois da primeira chamada.

O que não foi medido:

5. Ninguém mediu quantos pedidos repetidos viram autorização duplicada hoje.
6. Ninguém mediu por quanto tempo uma decisão anterior continua válida para o mesmo beneficiário e procedimento.

Há ainda uma restrição de operação:

7. A equipe de operação trabalha em horário comercial, e ninguém acompanha a integração à noite.

As três propostas e as listas numeradas do que foi medido, do que não foi medido e da restrição de operação estão descritas nesta página.

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

O hospital vai expor, pela primeira vez, a consulta de elegibilidade de um beneficiário. Três públicos com necessidades diferentes vão consumir essa capacidade:

1. O aplicativo do paciente precisa de uma resposta curta e rápida, porque roda em rede móvel e mostra apenas se o beneficiário está apto.
2. O sistema interno de recepção precisa da resposta completa, com vigência, categoria do plano e motivo da recusa, para orientar o atendente.
3. Uma operadora parceira quer receber a mesma informação, e o contrato que ela mantém com outros hospitais usa XML sobre um envelope antigo, que o hospital não usa em lugar nenhum.

A restrição de execução também está definida:

4. A equipe tem quatro pessoas e três meses até a primeira entrega.

Três esboços estão sobre a mesa:

#### Esboço A

Um contrato único, com a resposta completa, servindo os três públicos. Quem precisa de menos ignora os campos que sobram.

#### Esboço B

Dois contratos sobre a mesma capacidade: um enxuto para o aplicativo e um completo para a recepção. A operadora consome o completo.

#### Esboço C

Dois contratos internos, como no esboço B, mais um adaptador dedicado que traduz para o envelope XML da operadora, isolado do resto.

As três necessidades de consumo numeradas de 1 a 3, a restrição de equipe e prazo no item 4 e os três esboços estão descritos nesta página.

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

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 2 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes: as simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

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

Qual especificação descreve caminhos, operações, parâmetros, corpos, respostas e schemas de uma API HTTP em YAML ou JSON?

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
- (d) Que a solicitação foi aceita para processamento, ainda sem decisão, e pode ser acompanhada no endereço informado.

#### Questão 10 [Média]

Uma equipe criou a rota POST /aprovarAutomaticamente com corpo em JSON e afirma que a API é REST. Como o módulo avalia essa afirmação?

- (a) Incorreta, porque a operação é coerente como RPC, mas usar JSON e HTTP não a torna REST.
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

Uma integração com o governo exige XML e SOAP. A equipe pergunta se a plataforma interna também precisa adotar XML. Qual é a orientação do módulo?

- (a) Sim, porque o formato do parceiro deve ser o formato canônico interno.
- (b) Não, porque usar SOAP com o parceiro não obriga a plataforma a adotar XML internamente, e a tradução deve ficar isolada do domínio.
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

- (a) A paginação pode repetir ou omitir itens, e um cursor opaco lida melhor com a mudança.
- (b) A paginação aumenta a latência, e a alternativa é retornar a coleção inteira.
- (c) A paginação impede o cache, e a alternativa é usar ETag em cada item.
- (d) A paginação quebra a idempotência do GET, e a alternativa é usar POST.

#### Questão 15 [Média]

O arquivo openapi.yaml do laboratório é válido sintaticamente. Por que o módulo usa também Spectral, Bruno e TestClient?

- (a) Porque o OpenAPI não aceita exemplos de requisição.
- (b) Porque as três ferramentas geram o código do servidor a partir do contrato.
- (c) Porque um contrato válido ainda pode ser fraco, e as três ferramentas examinam o documento, o consumo e a execução HTTP.
- (d) Porque o FastAPI exige essas ferramentas para iniciar.

### Questões difíceis

#### Questão 16 [Difícil]

Uma API pública precisa evoluir. Qual das mudanças abaixo tende a ser compatível com os consumidores existentes?

- (a) Tornar obrigatório um campo que antes era opcional.
- (b) Mudar a unidade de um campo numérico de reais para centavos.
- (c) Remover uma operação pouco usada.
- (d) Acrescentar um campo opcional, preservando o significado dos campos existentes.

#### Questão 17 [Difícil]

O cliente de um POST de autorização sofreu timeout e vai repetir a requisição. A equipe decide usar uma chave de idempotência. O que o módulo exige para que essa chave funcione?

- (a) Apenas gerar um UUID novo a cada tentativa.
- (b) Trocar POST por PUT, porque PUT é idempotente por definição.
- (c) Confiar na deduplicação automática do protocolo HTTP.
- (d) Definir escopo, retenção, comparação da requisição e a resposta para uma repetição divergente.

#### Questão 18 [Difícil]

Uma dependência externa responde lentamente, e a equipe propõe trocar REST por gRPC para resolver a latência. Como o módulo avalia a proposta?

- (a) Adequada, porque gRPC sempre reduz a latência total.
- (b) Adequada, porque gRPC elimina a necessidade de contrato.
- (c) Insuficiente, porque gRPC não resolve por si só a lentidão de uma dependência externa, e a escolha deve partir da força e da evidência.
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
- (b) Que expor uma API transforma nomes, formatos e regras em compromissos públicos, e mudar ou remover esse contrato afeta quem depende dele.
- (c) Que REST é inadequado para APIs públicas de grande escala.
- (d) Que ecossistemas de terceiros não dependem do contrato da API.
