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

Três lugares registram alguma coisa. O gateway de borda mostra respostas `502` em cerca de dois por cento das chamadas daquele período. O serviço de Elegibilidade registra erros de conexão com o banco, sem carimbo de tempo padronizado. O Jaeger mostra traces, e boa parte deles aparece com nomes de operação diferentes para o que parece ser a mesma rota.

O painel de latência média do gateway não mudou nada durante a tarde inteira.

Nenhum dos três registros carrega um identificador comum que permita seguir uma mesma chamada do começo ao fim.

Quatro fatos valem para a análise:

1. O gateway registrou `502` em cerca de dois por cento das chamadas da tarde.
2. O serviço de Elegibilidade registrou erros de conexão com o banco no mesmo período.
3. Os traces existem, e os nomes de operação variam para a mesma rota.
4. A latência média do gateway ficou estável do começo ao fim do período.

Os quatro fatos, a descrição dos três registros e a ausência de identificador comum, todos nesta página.

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

Há uma complicação. Vários hospitais da rede saem pelo mesmo proxy, e portanto pelo mesmo endereço de origem visto pelo gateway. Distinguir quem é quem pelo endereço de rede não funciona.

O parceiro tem contrato assinado e não pode simplesmente ser bloqueado.

Quatro fatos valem para a decisão:

1. Capacidade atual de oito chamadas por segundo; o parceiro pede vinte durante cinco minutos.
2. O atendimento presencial usa a mesma API e degrada junto.
3. Vários hospitais compartilham o mesmo endereço de origem no gateway.
4. Existe contrato com o parceiro, e ele precisa continuar sendo atendido.

Quatro políticas estão sobre a mesa:

#### Política A

Limite por endereço de origem, oito chamadas por segundo. O que passar disso recebe recusa imediata.

#### Política B

Limite por credencial de cliente, com cota separada para o parceiro e para o atendimento presencial.

#### Política C

Fila com espera: as chamadas acima da capacidade aguardam até dois segundos antes de serem atendidas ou recusadas.

#### Política D

Nenhum limite, e aumento da capacidade do serviço para trinta chamadas por segundo.

Os quatro fatos, a descrição das quatro políticas e o contrato com o parceiro, todos nesta página.

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

O hospital vai lançar a capacidade de Agendamento como serviço próprio, com equipe própria. Ela consulta Elegibilidade, reserva o horário e avisa Preparo de Sala, que pertence a outra equipe.

A API de Agendamento será pública para dois parceiros externos desde o primeiro dia.

O hospital já tem seis serviços no ar, e nenhum deles tem dono declarado por escrito. Quando algo quebra, a descoberta de quem responde leva em média quarenta minutos.

A diretoria aprovou o serviço novo com uma condição: ele não pode nascer com o mesmo problema dos outros seis.

A equipe de plataforma tem duas pessoas e já opera um gateway em produção.

Três níveis de exigência estão sobre a mesa:

#### Nível A

Dono declarado e contrato publicado. Nada mais é exigido para o lançamento.

#### Nível B

O nível A, mais identificador de correlação atravessando a cadeia e um limite de tráfego aplicado no gateway.

#### Nível C

O nível B, mais registro de decisão arquitetural obrigatório, verificação automática do contrato na esteira e sinal de saúde publicado por serviço.

O histórico dos seis serviços, o tamanho da equipe de plataforma, a exposição externa desde o primeiro dia e os três níveis, todos nesta página.

**Seu papel**

Você propõe o pacote de governança que acompanha o lançamento. Exigir demais atrasa o serviço; exigir de menos repete o problema que a diretoria mandou evitar.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três níveis e defenda a escolha, citando a condição imposta pela diretoria e o tamanho da equipe de plataforma.
2. Sobre os dois níveis que você não escolheu, escreva duas frases cada: o que ganhariam e o que custariam neste lançamento.
3. Para cada exigência do nível escolhido, diga em uma linha como alguém verifica que ela está valendo. Se alguma não puder ser verificada hoje, marque-a como intenção e diga o que falta.
4. O problema dos quarenta minutos é de descoberta de responsável. Diga qual exigência do seu nível ataca isso diretamente, e por quê.
5. Escreva o sinal que indicaria que o nível escolhido ficou insuficiente, e a exigência que você acrescentaria primeiro.

**Evidência esperada**

O arquivo entregue traz o nível escolhido com justificativa, os outros dois avaliados, uma forma de verificação para cada exigência mantida, a ligação explícita com o problema de descoberta de responsável e o sinal de reforço com a próxima exigência nomeada.
