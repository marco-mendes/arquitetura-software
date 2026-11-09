# Exercícios: tornar políticas governáveis

Tente responder antes de abrir cada feedback. Nas atividades avançadas, os nove campos tornam explícitos contexto, artefato e avaliação de uma decisão justificável. Cada entrega distingue política, arquivo declarativo, serviço que a recebe e saída que comprova o comportamento.

## Recordar

1\. Defina governança de serviços em uma frase.

<details>
<summary>Ver resposta</summary>

É o conjunto de contratos, responsabilidades e políticas verificáveis que torna uma decisão repetível e revisável.
</details>

2\. O que uma política de rate limiting protege e o que ela não decide?

<details>
<summary>Ver resposta</summary>

Protege a capacidade da borda contra volume excessivo; não decide autorização ou regra clínica do domínio.
</details>

3\. Diferencie `correlation_id` de trace ID.

<details>
<summary>Ver resposta</summary>

`correlation_id` facilita a busca humana entre resposta e logs; trace ID identifica a árvore técnica de spans distribuídos.
</details>

4\. Nomeie o arquivo da política de rota local.

<details>
<summary>Ver resposta</summary>

`laboratorios/plataforma-hospitalar/infra/kong/kong.yml`.
</details>

5\. Que saída comprova o limite da oficina?

<details>
<summary>Ver resposta</summary>

Uma resposta HTTP `429 Too Many Requests` depois de mais chamadas que o limiar da janela.
</details>

## Compreender

1\. Explique por que Kong não é sinônimo de governança.

<details>
<summary>Ver resposta</summary>

Kong implementa localmente políticas de borda; governança também inclui contrato, owner, versão, evidência e revisão, que sobrevivem à troca da ferramenta.
</details>

2\. Por que uma regra de plano vencido deve permanecer em Elegibilidade?

<details>
<summary>Ver resposta</summary>

Ela depende de estado e exceções do domínio, que pertencem ao serviço; o gateway só medeia controles comuns de entrada.
</details>

3\. Compare uma resposta `200` direta e uma `200` pelo gateway.

<details>
<summary>Ver resposta</summary>

A direta prova serviço e dado didático; a governada também prova a rota e a aplicação da política de borda, mas não autorização clínica.
</details>

4\. Por que o trace não substitui um log estruturado?

<details>
<summary>Ver resposta</summary>

O trace mostra caminho e tempo causal; o log descreve evento e campos seguros. A investigação usa ambos com a mesma correlação.
</details>

5\. O que a rastreabilidade permite afirmar com segurança?

<details>
<summary>Ver resposta</summary>

Que uma decisão publicada, sua configuração e uma execução observada podem ser relacionadas; ela não prova sozinha uma conclusão clínica ou de conformidade.
</details>

## Aplicar
### Recomendar onde aplicar a política de limite e correlação

**Objetivo**

Recomendar um entre quatro lugares para aplicar uma política de governança, declarando o que cada opção ganha, o que cobra e o que deixa descoberto.

**Situação**

Uma plataforma hospitalar tem seis serviços mantidos por três equipes. A diretoria de tecnologia aprovou duas políticas: toda chamada carrega um identificador de correlação que atravessa a cadeia inteira, e nenhum consumidor ultrapassa três chamadas por segundo por origem.

As políticas estão escritas e ninguém consegue provar que valem. Cada equipe entende a regra de um jeito, dois serviços já implementaram versões diferentes do limite, e o identificador de correlação se perde em algum lugar do meio da cadeia sem que ninguém saiba onde.

A diretoria pediu uma recomendação de onde a política deve morar.

Seis fatos foram apurados na plataforma:

1. Os seis serviços usam três linguagens diferentes.
2. A política precisa valer também nas chamadas entre serviços internos, e não apenas no tráfego que entra.
3. A operação de plataforma tem duas pessoas.
4. Uma auditoria externa exige provar, serviço por serviço, que o limite estava ativo numa data passada.
5. Não existe malha de serviços instalada, e instalar exigiria janela de manutenção nos seis serviços.
6. O tráfego que entra passa integralmente por um gateway já em produção.

As quatro alternativas em avaliação:

| Alternativa | Onde a política é aplicada |
| --- | --- |
| **A. Em cada serviço** | Cada equipe implementa o limite e a propagação no próprio código, seguindo a política escrita. |
| **B. Biblioteca compartilhada** | Uma biblioteca de chassi implementa a política, e todos os serviços a incorporam como dependência. |
| **C. Gateway de borda** | O gateway que já existe aplica o limite e injeta o identificador de correlação antes de rotear. |
| **D. Malha de serviços** | Um *sidecar* ao lado de cada serviço aplica a política, fora do código da aplicação. |

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação. As três equipes implementam depois, e esperam de você a escolha e o que ela deixa em aberto.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende uma das quatro alternativas para a plataforma, em uma frase.
2. Sobre cada uma das quatro, escreva duas frases: o que ela resolve do problema descrito e o que ela cobra em troca.
3. Nenhuma das quatro cobre tudo com o que a plataforma tem hoje. Diga o que a sua recomendação deixa descoberto e por que você aceita essa lacuna.
4. Aponte a alternativa que você descartaria de imediato e diga qual fato a derruba.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria rever a decisão.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, a lacuna declarada em relação às chamadas internas, o caminho de comprovação para a auditoria, a alternativa descartada com o fato que a derruba, o risco aceito e o sinal de revisão observável.

## Analisar
### Investigar uma cadeia sem correlação

**Objetivo**

Formar hipóteses sobre um incidente a partir dos sinais disponíveis, sem transformar ausência de dado em conclusão.

**Situação**

Na terça-feira à tarde, a recepção do hospital reportou que a consulta de elegibilidade estava falhando "às vezes". Ninguém soube dizer com que frequência.

Três registros guardam alguma coisa sobre aquele período:

- O log do gateway de borda mostra respostas `502` em cerca de dois por cento das chamadas.
- O log do serviço de Elegibilidade mostra erros de conexão com o banco, sem carimbo de tempo padronizado.
- O Jaeger mostra traces, e boa parte deles aparece com nomes de operação diferentes para o que parece ser a mesma rota.

O painel de latência média do gateway não mudou nada durante a tarde inteira.

Nenhum dos três registros carrega um identificador comum que permita seguir uma mesma chamada do começo ao fim.

Quatro fatos valem para a análise:

1. O gateway registrou `502` em cerca de dois por cento das chamadas da tarde.
2. O serviço de Elegibilidade registrou erros de conexão com o banco no mesmo período.
3. Os traces existem, e os nomes de operação variam para a mesma rota.
4. A latência média do gateway ficou estável do começo ao fim do período.

Os quatro fatos, a descrição dos três registros e a ausência de identificador comum estão nesta página.

**Seu papel**

Você conduz a investigação. A diretoria quer saber o que aconteceu, e a equipe quer saber o que medir para não passar por isso de novo.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Explique por que a latência média pode ficar estável enquanto dois por cento das chamadas falham, e diga que medida mostraria o problema que a média esconde.
2. Escreva duas hipóteses diferentes que explicariam os fatos 1 e 2 ao mesmo tempo, e diga o que distinguiria uma da outra.
3. O fato 3 impede um tipo de verificação. Diga qual, e explique por que nomes de operação inconsistentes atrapalham mais do que nomes feios.
4. Diga o que faltou para transformar esses três registros numa investigação de dez minutos, e onde esse elemento precisaria ser criado e propagado.
5. Aponte uma conclusão que os quatro fatos não sustentam, rotule-a como hipótese e diga que dado a confirmaria.

**Evidência esperada**

O arquivo entregue distingue medida agregada de medida por chamada, apresenta duas hipóteses com o dado que as separa, explica o efeito da inconsistência de nomes e registra a hipótese não sustentada com o dado que a confirmaria.

## Avaliar
### Escolher uma política de limite

**Objetivo**

Julgar quatro políticas de limite de tráfego contra critérios declarados, sabendo que todas prejudicam alguém.

**Situação**

Um portal parceiro passou a chamar a API de elegibilidade do hospital vinte vezes por segundo durante cinco minutos, três vezes ao dia. A capacidade atual do serviço é de oito chamadas por segundo antes que a fila comece a crescer.

Durante essas rajadas, o atendimento presencial do próprio hospital fica lento, porque usa a mesma API.

Vários hospitais da rede saem pelo mesmo proxy e, portanto, pelo mesmo endereço de origem visto pelo gateway, o que impede distinguir um hospital do outro pelo endereço de rede.

O parceiro tem contrato assinado e não pode simplesmente ser bloqueado.

Seis fatos valem para a decisão:

1. A capacidade atual é de oito chamadas por segundo, e o parceiro envia vinte por segundo durante cinco minutos.
2. O atendimento presencial usa a mesma API e degrada junto.
3. Vários hospitais compartilham o mesmo endereço de origem no gateway.
4. Existe contrato com o parceiro, e ele precisa continuar sendo atendido.
5. O gateway já identifica o portal parceiro e o atendimento presencial por credencial de cliente própria, mas os outros hospitais da rede ainda chamam a API sem credencial.
6. A infraestrutura permite multiplicar as instâncias do serviço em menos de um dia, e o banco de elegibilidade nunca foi testado acima de quinze chamadas por segundo.

Quatro políticas estão sobre a mesa:

#### Política A

Limite por endereço de origem, oito chamadas por segundo. O que passar disso recebe recusa imediata.

#### Política B

Limite por credencial de cliente, com cota separada para o parceiro e para o atendimento presencial.

#### Política C

Fila com espera: as chamadas acima da capacidade aguardam até dois segundos antes de serem atendidas ou recusadas.

#### Política D

Nenhum limite, e aumento da capacidade do serviço para trinta chamadas por segundo.

Os seis fatos e a descrição das quatro políticas estão nesta página.

**Seu papel**

Você recomenda a política que entra em vigor na segunda-feira, sabendo que ela será revista.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Declare de três a quatro critérios de julgamento e diga qual pesa mais, justificando pelo efeito sobre o atendimento presencial.
2. Avalie as quatro políticas contra os seus critérios, um parágrafo por política, dizendo quem é protegido e quem é prejudicado em cada uma.
3. O fato 3 atrapalha uma das quatro de forma direta. Diga qual e explique o mecanismo.
4. Recomende uma política e escreva o que o parceiro recebe quando ultrapassa o limite: código de resposta, informação devolvida e o que ele deve fazer em seguida.
5. Escreva o sinal observável que encerraria essa política temporária, e diga quem olha esse sinal.

**Evidência esperada**

O arquivo entregue traz critérios declarados, as quatro políticas julgadas com protegido e prejudicado nomeados, o efeito do endereço compartilhado explicado, a resposta ao parceiro descrita com código e orientação, e o sinal de encerramento com responsável.

## Criar
### Propor o mínimo de governança para uma capacidade nova

**Objetivo**

Propor o conjunto mínimo de governança para uma capacidade que nasce agora, escolhendo entre três níveis de exigência e defendendo o que fica de fora.

**Situação**

O hospital vai lançar a capacidade de Agendamento como serviço próprio, com equipe própria. A diretoria aprovou o serviço novo com uma condição: ele não pode nascer com o mesmo problema dos seis serviços que já estão no ar.

Seis fatos foram apurados no hospital:

1. Agendamento consulta Elegibilidade, reserva o horário e avisa Preparo de Sala, que pertence a outra equipe.
2. A API de Agendamento será pública para dois parceiros externos desde o primeiro dia.
3. Nenhum dos seis serviços no ar tem dono declarado por escrito, e a descoberta de quem responde por uma falha leva em média quarenta minutos.
4. A equipe de plataforma tem duas pessoas e opera um gateway em produção, que já aplica limite de tráfego e injeta identificador de correlação nas chamadas que entram.
5. Os serviços enviam traces para um Jaeger compartilhado, mas Preparo de Sala ainda descarta o identificador de correlação que recebe.
6. A esteira de integração compila e testa cada serviço sem nenhuma etapa que compare a implementação com o contrato publicado, e o hospital não tem registro de decisão arquitetural escrito nem sinal de saúde publicado por serviço.

Três níveis de exigência estão sobre a mesa:

#### Nível A

Dono declarado e contrato publicado. Nada mais é exigido para o lançamento.

#### Nível B

O nível A, mais identificador de correlação atravessando a cadeia e um limite de tráfego aplicado no gateway.

#### Nível C

O nível B, mais registro de decisão arquitetural obrigatório, verificação automática do contrato na esteira e sinal de saúde publicado por serviço.

Os seis fatos e os três níveis estão nesta página.

**Seu papel**

Você propõe o pacote de governança que acompanha o lançamento. O pacote precisa equilibrar dois riscos: exigências em excesso atrasam o lançamento, e exigências insuficientes repetem o problema que a diretoria mandou evitar.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três níveis e defenda a escolha, citando a condição imposta pela diretoria e o tamanho da equipe de plataforma.
2. Sobre os dois níveis que você não escolheu, escreva duas frases cada: o que ganhariam e o que custariam neste lançamento.
3. Para cada exigência do nível escolhido, diga em uma linha como alguém verifica que ela está valendo. Se alguma não puder ser verificada hoje, marque-a como intenção e diga o que falta.
4. O problema dos quarenta minutos é de descoberta de responsável. Diga qual exigência do seu nível ataca isso diretamente, e por quê.
5. Escreva o sinal que indicaria que o nível escolhido ficou insuficiente, e a exigência que você acrescentaria primeiro.

**Evidência esperada**

O arquivo entregue traz o nível escolhido com justificativa, os outros dois avaliados, uma forma de verificação para cada exigência mantida, a ligação explícita com o problema de descoberta de responsável e o sinal de reforço com a próxima exigência nomeada.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 4 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes: as simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

Como o módulo define governança em uma arquitetura distribuída?

- (a) Um comitê que aprova cada mudança antes da implantação.
- (b) O conjunto de decisões, responsabilidades e políticas verificáveis que torna a arquitetura repetível sem congelá-la.
- (c) Uma ferramenta de API gateway instalada na borda.
- (d) Um documento de padrões revisado uma vez por ano.

#### Questão 2 [Simples]

Qual das atividades abaixo pertence à governança em design-time?

- (a) Responder 429 quando o limite de chamadas é excedido.
- (b) Exportar spans do Collector para o Jaeger.
- (c) Revisar um contrato OpenAPI e uma convenção de versão.
- (d) Medir a taxa de respostas 5xx em produção.

#### Questão 3 [Simples]

Qual pergunta os logs respondem, segundo o módulo?

- (a) O que aconteceu neste evento?
- (b) Com que frequência e em que distribuição?
- (c) Por onde esta operação passou e onde esperou?
- (d) Qual indisponibilidade é aceitável?

#### Questão 4 [Simples]

Qual cabeçalho do padrão W3C carrega a relação entre os spans de um trace distribuído?

- (a) X-Correlation-ID.
- (b) Authorization.
- (c) Location.
- (d) traceparent.

#### Questão 5 [Simples]

O que é um SLO?

- (a) Um contrato jurídico com multa por indisponibilidade.
- (b) Um painel com todos os gráficos do serviço.
- (c) Uma meta operacional baseada em um indicador, como a proporção de consultas concluídas abaixo de 300 ms em uma janela.
- (d) Um log estruturado com nível de severidade.

#### Questão 6 [Simples]

Qual código HTTP o plugin de rate limiting do Kong devolve quando o limite é excedido?

- (a) 429 Too Many Requests.
- (b) 401 Unauthorized.
- (c) 503 Service Unavailable.
- (d) 500 Internal Server Error.

#### Questão 7 [Simples]

O que significa ownership de um serviço no catálogo?

- (a) Que o time recebe a culpa automática por qualquer incidente.
- (b) Que o time é dono do servidor físico onde o serviço roda.
- (c) Que apenas o time dono pode consumir a API.
- (d) Que existe alguém com autoridade e contexto para priorizar correção, evolução e retirada do serviço.

#### Questão 8 [Simples]

No laboratório, o Kong roda em modo DB-less. O que isso significa?

- (a) Que o Kong não encaminha requisições para serviços com banco de dados.
- (b) Que a configuração vem de um arquivo declarativo, kong.yml, sem banco de configuração nem painel.
- (c) Que o Kong guarda os logs apenas em memória.
- (d) Que o serviço de Elegibilidade não usa banco de dados.

### Questões médias

#### Questão 9 [Média]

A regra "um beneficiário não pode usar um plano vencido" deve ser aplicada no gateway ou no serviço de Elegibilidade?

- (a) No serviço, porque é uma política de domínio que depende do vocabulário e do estado da capacidade.
- (b) No gateway, porque toda política deve ficar na borda.
- (c) No gateway, porque reduz a duplicação de código.
- (d) Em nenhum dos dois, porque é responsabilidade do banco de dados.

#### Questão 10 [Média]

Uma equipe propõe usar o identificador do paciente como correlation ID, para facilitar a busca nos logs. Como o módulo avalia a proposta?

- (a) Adequada, porque o identificador já é único.
- (b) Adequada, desde que o identificador também vá para o traceparent.
- (c) Inadequada, porque o correlation ID deve ser gerado pelo banco de dados.
- (d) Inadequada, porque revela dado e gera cardinalidade inadequada, e um UUID sem semântica é suficiente.

#### Questão 11 [Média]

O rate limiting foi configurado em três chamadas por segundo por origem. Um colega afirma que, com isso, a autorização de acesso aos resultados de exame está resolvida. O que o módulo afirma?

- (a) Que a afirmação é correta, porque o limite impede acessos indevidos.
- (b) Que o limite deve ser reduzido para uma chamada por segundo para funcionar como autorização.
- (c) Que rate limiting é uma proteção contra abuso e não decide se uma pessoa tem direito a um recurso.
- (d) Que a autorização deve ser feita pelo Jaeger.

#### Questão 12 [Média]

Uma métrica de latência usa o identificador do paciente como rótulo. Qual problema o módulo aponta?

- (a) A métrica fica imprecisa porque o identificador muda.
- (b) Rótulos de cardinalidade ilimitada aumentam o custo e dificultam a consulta, e devem ser substituídos por categorias estáveis.
- (c) O identificador impede o cálculo de percentis.
- (d) Não há problema, porque métricas não são armazenadas.

#### Questão 13 [Média]

Qual é a diferença entre correlation ID e traceparent, segundo o módulo?

- (a) São o mesmo identificador com nomes diferentes.
- (b) O correlation ID é um identificador de busca compreensível entre logs e resposta, e o traceparent descreve a árvore de execução, com trace ID, span pai e sinalizadores.
- (c) O correlation ID só existe no gateway, e o traceparent só existe no banco.
- (d) O traceparent substitui o correlation ID em qualquer cenário.

#### Questão 14 [Média]

Uma política de versionamento foi publicada, e uma versão antiga da API vai ser retirada. O que, além de registrar a nova versão, o módulo exige?

- (a) Apenas um aviso por e-mail aos consumidores.
- (b) Que a versão antiga seja retirada imediatamente para evitar custo.
- (c) Que todas as versões sejam mantidas indefinidamente.
- (d) Que o catálogo aponte os consumidores, a política defina a depreciação e os logs mostrem o uso da versão antiga antes da retirada.

#### Questão 15 [Média]

No ADR do laboratório, a equipe decidiu usar Kong DB-less e rejeitou a configuração por API administrativa. Qual foi o motivo da rejeição?

- (a) A API administrativa é mais lenta.
- (b) A API administrativa não suporta rate limiting.
- (c) A API administrativa esconderia estado fora do repositório.
- (d) A API administrativa exige licença comercial.

### Questões difíceis

#### Questão 16 [Difícil]

A rota de Elegibilidade cumpre a meta de latência, mas recusa com 429 parte dos consumidores legítimos. Qual leitura o módulo propõe?

- (a) O indicador de latência isolado não descreve a qualidade, e os indicadores de sucesso, disponibilidade e proteção devem refletir o objetivo do recurso.
- (b) O serviço está saudável, porque o SLO de latência foi atendido.
- (c) O limite deve ser removido, porque consumidores legítimos nunca podem ser recusados.
- (d) A falha é do consumidor, que deve repetir até ser atendido.

#### Questão 17 [Difícil]

O orçamento de erro de um SLO está sendo consumido rapidamente, e o produto quer acrescentar uma nova dependência ao serviço. Qual é a orientação do módulo?

- (a) Acrescentar a dependência e revisar o SLO depois.
- (b) Priorizar a confiabilidade antes de acrescentar tráfego ou novas dependências.
- (c) Aumentar a meta do SLO para refletir o novo cenário.
- (d) Desativar os alertas até a entrega da nova funcionalidade.

#### Questão 18 [Difícil]

A autenticação técnica ocorre no gateway, e a autorização para ver um resultado específico de exame ocorre no serviço. Qual risco o módulo aponta nesse arranjo e como tratá-lo?

- (a) Nenhum risco, porque o gateway cobre a segurança inteira.
- (b) Duplicação de autenticação, tratada removendo a verificação do serviço.
- (c) Uma lacuna entre as duas partes, tratada documentando ambas e o comportamento de falha.
- (d) Latência excessiva, tratada movendo a autorização para o gateway.

#### Questão 19 [Difícil]

No caso Knight Capital, um servidor recebeu o código antigo do Power Peg e o sistema enviou 97 mensagens de erro antes da abertura do mercado, sem que ninguém agisse. Qual lição de governança o caso ilustra?

- (a) Que mensagens automáticas devem ser desativadas, porque geram ruído.
- (b) Que implantações em etapas são sempre mais arriscadas que implantações completas.
- (c) Que o problema foi exclusivamente técnico e não teria sido evitado por procedimentos.
- (d) Que um controle que existe apenas como artefato, sem ligação a uma ação automática e a uma pessoa responsável, não governa o comportamento em execução.

#### Questão 20 [Difícil]

Durante o incidente da Knight Capital, a equipe desinstalou o código novo dos sete servidores corretos, e o problema se espalhou para os oito. O que essa decisão revela sobre a governança da empresa?

- (a) Que a ausência de procedimento de resposta a incidentes levou a diagnóstico em produção com uma hipótese não verificada.
- (b) Que reverter uma implantação é sempre a resposta errada a um incidente.
- (c) Que o rate limiting teria impedido o problema.
- (d) Que o código novo era o defeito e a reversão foi correta, mas tardia.
