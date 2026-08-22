# Exercícios: decidir antes de distribuir

Tente responder antes de abrir cada feedback. Nas atividades avançadas não há gabarito: os nove campos tornam explícitos o contexto, a entrega e a forma de avaliar uma decisão justificável.

## Recordar

1\. Uma capacidade de negócio descreve algo que a organização sabe fazer para produzir um resultado. "Verificar elegibilidade" é uma capacidade; "salvar no PostgreSQL" não é. Por quê? Dê outro exemplo hospitalar de capacidade e um de mecanismo técnico.

<details>
<summary>Ver resposta</summary>

Capacidade de negócio é definida pelo resultado que ela produz para alguém, independentemente da tecnologia usada para produzi-lo; "salvar no PostgreSQL" descreve como um dado é persistido, não que resultado a organização entrega. Exemplos de capacidade: "agendar atendimento", "solicitar exame". Exemplo de mecanismo técnico: "enviar JSON", "consultar cache" — eles podem mudar sem que a capacidade que servem mude de nome.
</details>

2\. Uma equipe decide que, como Elegibilidade e Exames são bounded contexts diferentes, cada um precisa virar um microsserviço imediatamente. Que erro de raciocínio essa equipe está cometendo?

<details>
<summary>Ver resposta</summary>

A equipe está confundindo fronteira semântica com topologia física. Bounded context delimita onde um modelo e sua linguagem têm significado consistente — é uma decisão sobre significado, não sobre implantação. Um bounded context pode viver como módulo dentro de um monólito, como parte de um macrosserviço ou como um serviço implantável; a extração física só se justifica quando há necessidade comprovada de autonomia, escala ou falha independentes. Tratar toda fronteira lógica como um serviço separado cria processos, redes e operação antes de existir qualquer benefício demonstrado.
</details>

3\. O módulo descreve cinco formas de acoplamento entre serviços: de contrato, temporal, de dados, de implantação e organizacional. Escolha duas delas e explique, com um exemplo, o que cada uma faz um serviço depender do outro.

<details>
<summary>Ver resposta</summary>

São cinco: acoplamento de contrato (o consumidor depende de campos, semântica e códigos de resposta expostos pelo provedor — mudar um campo pode quebrar quem consome); acoplamento temporal (o consumidor precisa que o provedor esteja disponível no momento da chamada, como numa chamada síncrona); acoplamento de dados (duas unidades dependem da mesma estrutura de armazenamento ou alteram a mesma informação); acoplamento de implantação (uma mudança obriga a publicar várias unidades juntas); e acoplamento organizacional (equipes precisam negociar continuamente para entregar uma única capacidade). Exemplo do laboratório: Exames aceita acoplamento temporal com Elegibilidade — espera uma resposta síncrona —, mas evita acoplamento de dados, porque não lê a tabela do outro serviço diretamente.
</details>

4\. Uma pessoa desenvolvedora de Faturamento precisa de um relatório e decide fazer uma consulta SQL direta nas tabelas do banco de Elegibilidade, sem passar pelo contrato de API. Qual regra de propriedade de dados essa consulta viola, e que acoplamento oculto ela cria?

<details>
<summary>Ver resposta</summary>

Ela viola banco por serviço: a regra de que somente o serviço proprietário acessa diretamente o próprio armazenamento, e qualquer outro consumidor deve passar por contrato, evento ou réplica projetada. A consulta direta cria um acoplamento de dados oculto — Faturamento passa a depender da estrutura interna das tabelas de Elegibilidade, que nenhum contrato declara e ninguém revisa. Uma mudança de coluna feita por Elegibilidade, sem saber que Faturamento a lê, pode quebrar o relatório sem aviso; o proprietário perde o controle sobre a evolução do próprio esquema.
</details>

5\. O módulo compara monólito modular, macrosserviço e microsserviço como formas de implantação. O que muda entre elas não é o tamanho do código — é outra coisa. O que é?

<details>
<summary>Ver resposta</summary>

O que muda é a autonomia física de implantação e de falha, não o volume de linhas ou de pessoas. No monólito modular, os módulos têm fronteiras lógicas claras, mas publicam e falham juntos, numa única unidade implantável. No macrosserviço, algumas fronteiras já viram processos separados, mas ainda agrupam mais de uma capacidade por unidade. No microsserviço, cada unidade implantável está alinhada a uma única responsabilidade de negócio e é dona do próprio estado, podendo publicar e falhar de forma independente das demais. "Micro" não é uma medida de tamanho: é um sinal de autonomia com coesão.
</details>

6\. Exames continua respondendo consultas ao próprio banco, mas passa a recusar novas solicitações porque Elegibilidade está fora do ar. Que nome se dá a essa situação, e por que ela não deveria ser tratada apenas como "o sistema caiu"?

<details>
<summary>Ver resposta</summary>

Chama-se falha parcial: uma parte do sistema distribuído continua saudável enquanto outra parte, indisponível, impede que uma capacidade específica seja concluída. Tratar isso como "o sistema caiu" esconde informação que o consumidor precisa para agir — ele não sabe se pode tentar de novo, se deve esperar ou se o problema é seu. Por isso a resposta deveria expor a causa real, como um `503` com o código `dependencia_indisponivel`, em vez de um `500` genérico que trata falha de dependência como se fosse erro interno do próprio Exames.
</details>

7\. Uma chamada síncrona sem timeout está esperando a resposta de Elegibilidade, que ficou lenta. O que acontece com Exames enquanto essa espera não tem limite, e que papel um timeout cumpre nessa situação?

<details>
<summary>Ver resposta</summary>

Sem timeout, a requisição de Exames fica presa esperando indefinidamente a resposta de Elegibilidade — a thread, conexão ou recurso alocado para essa chamada continua ocupado, e se isso se repetir em várias solicitações simultâneas, a lentidão de Elegibilidade se propaga e pode esgotar os recursos de Exames também. Um timeout limita quanto tempo Exames espera antes de desistir e tratar a chamada como falha, contendo o problema em vez de deixar que a lentidão de uma dependência derrube quem depende dela.
</details>

8\. O banco de Elegibilidade está replicado em dois data centers da rede hospitalar. O enlace entre eles cai por três minutos: as duas réplicas continuam de pé e atendendo, mas param de conversar entre si. Nesse intervalo, o sistema pode recusar escritas para manter uma visão única e atual do dado, ou seguir aceitando escritas nas duas pontas correndo o risco de divergir. Que nome o teorema CAP dá a essa interrupção de comunicação, e entre quais duas propriedades ela obriga a escolher?

<details>
<summary>Ver resposta</summary>

O nome é partição — o CAP trata de um armazenamento distribuído justamente quando mensagens entre nós ou grupos de nós são perdidas ou atrasadas. Durante os três minutos de partição, a escolha é entre consistência (recusar ou atrasar operações para preservar uma visão única e atual) e disponibilidade (cada réplica não falha continua respondendo, aceitando possível divergência). Restabelecido o enlace, CAP deixa de estar em jogo: latência e consistência continuam gerando decisões, mas descritas por outros modelos. Por isso CAP não é uma escolha livre entre duas de três letras que um produto faz a qualquer momento, nem serve para justificar qualquer dado desatualizado numa integração comum — ali é preciso nomear o mecanismo e a promessa reais.
</details>

9\. O fluxo de Agendamento tem três etapas, cada uma gravando no próprio banco, em transações locais separadas: reservar o horário na Agenda, autorizar o procedimento e pedir o preparo da sala. As duas primeiras confirmam; a terceira falha. Não existe nenhuma transação abrangente capaz de desfazer as duas que já foram confirmadas. Como se chama a ação que uma SAGA aciona para neutralizar o efeito dessas etapas anteriores, e quais são as duas formas de coordenar a sequência descritas no módulo?

<details>
<summary>Ver resposta</summary>

A ação é a compensação: ações compensatórias, semanticamente adequadas ao domínio, que neutralizam o efeito das etapas já confirmadas — liberar o horário reservado e cancelar a autorização, neste exemplo. As duas formas de coordenação são a coreografia, em que cada participante reage aos eventos que os outros publicam, e a orquestração, em que um componente conhece toda a sequência e a conduz. Compensar não é desfazer: a compensação é um novo fato na história, pode ela mesma falhar, e outros participantes podem já ter observado o estado intermediário — por isso o desenho precisa declarar estados explícitos, comandos idempotentes, política de repetição e trilha de auditoria.
</details>

10\. Em Laudos, assinar um laudo exige validar regras clínicas antes de gravar; já a tela que lista os laudos do mês só precisa de uma lista pronta para leitura. A equipe separou as duas coisas em classes e interfaces distintas, mas ambas continuam no mesmo processo e no mesmo banco PostgreSQL. Quais são os dois modelos que o CQRS separa, e uma separação feita assim, dentro de um único banco, já conta como CQRS?

<details>
<summary>Ver resposta</summary>

Os dois modelos são o de comando e o de consulta: comandos expressam intenção e precisam preservar invariantes de negócio; consultas existem para oferecer uma projeção adequada a quem lê. E sim, a separação de Laudos já conta como CQRS — o padrão não exige dois bancos, nem mensageria, nem Event Sourcing, e pode começar exatamente assim, como objetos e interfaces distintos dentro do mesmo processo e do mesmo banco. O que cobra caro é o passo seguinte: um modelo de leitura materializado atende consultas de alto volume, mas traz atualização, defasagem, reconstrução e monitoramento. Só vale introduzi-lo quando a assimetria entre leitura e escrita, a complexidade dos modelos ou a escala justificarem esse custo.
</details>

## Compreender

1\. Explique por que mover duas funções para processos diferentes não reduz automaticamente acoplamento.

<details>
<summary>Ver resposta</summary>

Separar duas funções em processos diferentes não elimina a dependência entre elas — ela só muda de forma: o que antes era uma chamada de função na memória vira um contrato de rede, com serialização, latência e disponibilidade envolvidas. Se as duas partes continuam mudando pelas mesmas razões e precisam ser implantadas juntas para uma alteração funcionar, o acoplamento de contrato, temporal e de implantação continua alto — só que agora com o custo adicional de rede e coordenação remota, sem o benefício de autonomia que a distribuição prometia.
</details>

2\. Descreva como alta coesão pode ser prejudicada por serviços pequenos demais.

<details>
<summary>Ver resposta</summary>

Coesão é o grau em que os elementos de uma unidade contribuem para uma mesma responsabilidade; regras que mudam pelo mesmo motivo tendem a pertencer junto. Quando um serviço é fatiado em pedaços menores que essas regras relacionadas, uma alteração simples de negócio passa a exigir mudar vários serviços ao mesmo tempo — cada um com seu próprio contrato, pipeline de implantação e possibilidade de falha isolada. O resultado é o oposto da autonomia que a distribuição buscava: mais coordenação, mais superfícies de falha e mais contexto mental para entender o que deveria ser uma única mudança coesa.
</details>

3\. Dois serviços do laboratório usam dois PostgreSQL diferentes, um para cada um. Isso já garante, por si só, que a propriedade dos dados está protegida? O que mais precisa ser verdade além da separação física?

<details>
<summary>Ver resposta</summary>

Não garante sozinho. Propriedade responde quem tem autoridade para interpretar e alterar uma informação — é uma regra de acesso e de responsabilidade, não uma questão de onde o arquivo do banco está gravado. A separação física (bancos, schemas ou instâncias distintas) só protege a propriedade quando vem acompanhada de isolamento de rede e de credenciais que realmente impedem o outro serviço de conectar diretamente — como no laboratório, em que a credencial de Exames só conhece o banco `exames`, e a rede interna de cada banco não é alcançável pelo outro processo. Sem essas permissões reais, dois bancos fisicamente separados ainda podem ser acessados livremente por qualquer serviço que descubra a string de conexão, e a propriedade continua sendo apenas uma convenção não aplicada.
</details>

4\. Faturamento mantém uma réplica projetada do dado de Elegibilidade, alimentada pelos eventos que Elegibilidade publica. A promessa é de consistência eventual: sem novas escritas, a réplica acaba chegando ao mesmo estado da origem. Só que essa promessa não diz como nem quando isso acontece — quem faz acontecer são as **regras de convergência**, um conjunto de decisões explícitas de desenho: o identificador que amarra cada evento ao mesmo registro; a ordenação, quando a ordem de aplicação altera o resultado; a idempotência, para que o mesmo evento aplicado duas vezes não produza o efeito duas vezes; a política de repetição, para mensagens perdidas ou atrasadas; e a reconciliação, para detectar e corrigir a divergência que sobrar. Escolha três dessas regras e diga, para cada uma, o que acontece com a réplica de Faturamento se ela faltar.

<details>
<summary>Ver resposta</summary>

Sem identificador, os eventos não podem ser amarrados ao mesmo registro: a réplica cria linhas duplicadas para a mesma pessoa, ou atualiza a linha errada, e não há como saber qual é a versão corrente. Sem ordenação, um evento antigo que chega atrasado sobrescreve um mais recente — uma elegibilidade cancelada volta a aparecer como válida. Sem idempotência, a mesma mensagem reentregue aplica o efeito duas vezes, e a réplica acumula um estado que nunca existiu na origem. Sem política de repetição, uma mensagem perdida simplesmente nunca chega, e a réplica fica defasada para sempre — "eventual" passa a significar "nunca". Sem reconciliação, nenhuma das divergências acima é detectada: Faturamento segue operando sobre dado errado sem sinal nenhum. O que as cinco têm em comum é revelar que consistência eventual, sozinha, não resolve nada: ela nomeia o resultado desejado, e as regras de convergência são o que o produz.
</details>

5\. Dê um cenário da plataforma hospitalar em que o monólito modular seja a forma preferível, e outro em que microsserviços, com implantação independente, sejam realmente necessários. Em cada cenário, diga qual fato decide a escolha — lembrando que não é o tamanho do código.

<details>
<summary>Ver resposta</summary>

Monólito modular tende a ser preferível quando as mudanças em duas capacidades costumam acontecer juntas e compartilham uma mesma transação — por exemplo, assinar um laudo e publicá-lo, que precisam ser consistentes no mesmo instante e são alteradas pela mesma equipe. Aqui as fronteiras lógicas valem a pena, mas separar em processos só acrescentaria rede e coordenação.

Microsserviços, com implantação e falha independentes, passam a se justificar quando duas capacidades têm equipes diferentes, cargas de trabalho muito distintas ou ciclos de mudança e de risco que não deveriam bloquear um ao outro — por exemplo, Agenda, que recebe picos e muda com frequência, e Preparo de Sala, de outra equipe, que tolera alguns minutos de atraso e não deveria ser publicada de novo toda vez que Agenda muda.

Em ambos os casos, o que decide é a autonomia necessária de implantação e de falha, mais o padrão de coevolução entre as capacidades — nunca o volume de linhas.
</details>

6\. Explique por que uma compensação de SAGA não apaga fatos já observados.

<details>
<summary>Ver resposta</summary>

Uma compensação de SAGA cria um novo fato que neutraliza o efeito de negócio de uma etapa anterior — ela não volta o tempo nem apaga o que já foi observado por outras partes do sistema. Se uma solicitação de exame já foi confirmada e notificada, cancelá-la depois não significa que ela nunca existiu: quem recebeu a confirmação já pode ter agido com base nela, e mensagens de cancelamento podem chegar duplicadas ou fora de ordem. É por isso que o desenho de uma SAGA precisa declarar estados explícitos, comandos idempotentes e uma trilha de auditoria — a compensação é mais um evento na história, não um apagador dela.
</details>

7\. Uma equipe quer introduzir tanto SAGA quanto CQRS no fluxo de Agendamento só porque "qualquer sistema distribuído sério usa os dois". Que problema real cada um resolveria, e por que adotar um não implica precisar do outro?

<details>
<summary>Ver resposta</summary>

SAGA resolveria o problema de coordenar uma mudança que atravessa múltiplas transações locais — por exemplo, reservar horário, autorizar procedimento e preparar um recurso, em que uma falha numa etapa posterior exige compensar as anteriores. CQRS resolveria um problema diferente: a assimetria entre como o sistema escreve (comandos, que precisam preservar invariantes) e como ele lê (consultas, que podem exigir uma projeção otimizada e de alto volume). Um fluxo pode precisar de SAGA sem nenhuma necessidade de separar leitura e escrita, e pode precisar de CQRS sem nenhuma coordenação distribuída entre transações — adotar os dois por hábito, sem uma necessidade concreta demonstrada para cada um, só adiciona componentes, estados e novas formas de falhar que ninguém pediu.
</details>

## Aplicar

### Delimitar o fluxo de laudos

**Objetivo**

Propor uma primeira fronteira lógica que preserve a transação clínica e permita notificação atrasada.

**Situação**

Uma clínica possui um sistema único. Laudos recebe o resultado técnico, aplica assinatura profissional e publica o documento; Notificações envia aviso depois da publicação. Ambos usam tabelas sem proprietário e a equipe quer melhorar limites sem distribuir agora.

**Seu papel**

Você é a pessoa arquiteta responsável pela proposta inicial.

**Artefato que você irá usar**

Crie `entregas/modulo-3/aplicar-laudos.md`, a partir da raiz do clone, e use as descrições de `docs/modulo-3-servicos/conceitos.md` e `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Crie o diretório `entregas/modulo-3/`; o estado inicial é sem serviços iniciados e sem alteração do laboratório. Considere uma equipe, implantação semanal conjunta, transação local para assinatura/publicação, atraso aceitável de cinco minutos para avisos e volume estável.

**Insumos disponíveis**

As capacidades, restrições e referências indicadas acima.

**Como conduzir**

**O que fazer**

1. Nomeie contexts e termos centrais.
2. Aloque tabelas e operações a um proprietário.
3. Desenhe interfaces internas e dependências permitidas.
4. Indique um evento interno e sua semântica.
5. Escolha a forma de implantação inicial e um sinal de revisão.
6. Se uma fronteira não puder ser justificada pelos fatos, mantenha-a no monólito e registre a hipótese a medir.

**Evidência esperada**

O artefato mostra capacidade, regra, dono do dado, direção de dependência e a razão contextual da escolha.

**Entrega esperada**

Envie o arquivo `entregas/modulo-3/aplicar-laudos.md` com uma página, um mapa de contexto, duas guardas automatizáveis, uma suposição e um risco.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Limites alinhados às capacidades e invariantes | 30% | Evidência: capacidade e regra; insuficiente: limite técnico arbitrário. |
| Propriedade de dados explícita | 25% | Evidência: dono do dado; insuficiente: banco compartilhado sem regra. |
| Dependências e contratos coerentes | 20% | Evidência: direção e contrato; insuficiente: acesso direto oculto. |
| Decisão ligada aos insumos | 15% | Evidência: insumo citado; insuficiente: decisão sem contexto. |
| Riscos e sinais de revisão | 10% | Evidência: risco e sinal; insuficiente: revisão sem condição. |

## Analisar

### Diagnosticar um monólito distribuído

**Objetivo**

Separar fatos, inferências e hipóteses ao analisar dependências que parecem serviços autônomos.

**Situação**

Cadastro, Agenda, Atendimento e Faturamento usam o mesmo schema. Atendimento chama os três em sequência; uma mudança de campo exige quatro implantações. Cada serviço anuncia 99,9% de disponibilidade, mas o fluxo tem incidentes frequentes.

**Seu papel**

Você lidera a análise antes de qualquer reestruturação.

**Artefato que você irá usar**

Crie `entregas/modulo-3/analisar-monolito-distribuido.md` a partir da raiz do clone; use a tabela comparativa de `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Registre como fatos que 70% das mudanças em Cadastro e Atendimento ocorrem juntas, Agenda escala dez vezes nos horários de entrada, Faturamento pertence a outro time, cadastro válido é obrigatório e faturamento não precisa confirmar no caminho crítico. Não há eventos nem idempotência.

**Insumos disponíveis**

Mapa de chamadas e fatos declarados na situação.

**Como conduzir**

**O que fazer**

1. Classifique os acoplamentos.
2. Identifique dependências críticas dispensáveis.
3. Relacione coevolução e escala a limites candidatos.
4. Compare duas alternativas de consolidação ou extração.
5. Modele uma falha parcial visível ao consumidor.

**Evidência esperada**

Saída: o texto associa cada conclusão a fato, inferência ou hipótese.

**Entrega esperada**

Envie `entregas/modulo-3/analisar-monolito-distribuido.md`, com no máximo duas páginas e dois diagramas (atual e candidato).

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Classificação precisa dos acoplamentos | 25% | Evidência: tipo e causa; insuficiente: dependência genérica. |
| Uso consistente dos dados do caso | 25% | Evidência: fatos referenciados; insuficiente: dado inventado. |
| Comparação de alternativas | 20% | Evidência: consequências contrastadas; insuficiente: opção só listada. |
| Análise de falha parcial | 20% | Evidência: parte saudável e falha; insuficiente: sistema tratado como inteiro. |
| Separação entre fato e hipótese | 10% | Evidência: hipótese rotulada; insuficiente: suposição como fato. |

## Avaliar

### Escolher consistência para autorização prévia

**Objetivo**

Escolher uma resposta à indisponibilidade que preserve a regra clínica e não esconda seus custos.

**Situação**

Uma rede quer receber solicitações durante até quinze minutos de indisponibilidade do provedor de autorizações. A autorização pode mudar a qualquer momento; executar sem ela é arriscado e perder a solicitação também é inaceitável.

**Seu papel**

Você participa do comitê que decide entre falha explícita, recepção pendente, cache ou outro desenho fundamentado.

**Artefato que você irá usar**

Crie `entregas/modulo-3/avaliar-autorizacao.md`, a partir da raiz do clone, usando CAP, SAGA e CQRS conforme explicados em `docs/modulo-3-servicos/padroes-e-decisoes.md`.

**Antes de executar**

Considere identificador único por solicitação, estado pendente aceito por até trinta minutos, consulta HTTP sem eventos do provedor, equipe operacional em horário comercial e ausência de transação distribuída.

**Insumos disponíveis**

As garantias e limitações declaradas na situação.

**Como conduzir**

**O que fazer**

1. Defina recebimento e execução.
2. Compare três alternativas por segurança, disponibilidade, consistência e operação.
3. Avalie SAGA e CQRS apenas se resolverem uma necessidade concreta.
4. Escolha, declare estados, timeout, repetição, idempotência e sinal de revisão.

**Evidência esperada**

A decisão mostra por que a promessa de consistência protege o risco do domínio e como a equipe observará pendências.

**Entrega esperada**

Envie `entregas/modulo-3/avaliar-autorizacao.md` com contexto, alternativas, decisão, consequências, fluxo de estados e plano de observação.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Critérios ligados ao risco do domínio | 30% | Evidência: risco orienta critério; insuficiente: critério técnico solto. |
| Comparação equilibrada | 25% | Evidência: custo e ganho; insuficiente: padrão sem contraste. |
| Tratamento de estados e falhas | 20% | Evidência: transição e falha; insuficiente: fluxo só feliz. |
| Uso criterioso de SAGA e CQRS | 15% | Evidência: necessidade justifica padrão; insuficiente: sigla sem problema. |
| Revisão e observação | 10% | Evidência: sinal e revisão; insuficiente: monitoramento sem decisão. |

## Criar

### Projetar uma evolução verificável

**Objetivo**

Desenhar uma evolução mínima para Agendamento que declare fronteiras, falhas e gatilhos de mudança.

**Situação**

A plataforma hospitalar ganhará Agendamento: consulta Elegibilidade, reserva horário e pede preparo de sala. Agenda muda com frequência e recebe picos; Preparo de Sala pertence a outra equipe e aceita dois minutos de atraso.

**Seu papel**

Você cria uma proposta que comece simples e continue verificável ao evoluir.

**Artefato que você irá usar**

Crie o diretório `entregas/modulo-3/criar-agendamento/` a partir da raiz do clone e entregue `proposta.md`, `fluxo-nominal.md` e `falhas-parciais.md`; use os contratos de `laboratorios/plataforma-hospitalar/` apenas como referência, sem alterar o código.

**Antes de executar**

Considere resposta inicial em três segundos, identificador fornecido pelo consumidor, PostgreSQL disponível, mensageria permitida porém não instalada e no máximo três novas unidades implantáveis neste semestre.

**O que fazer**

1. Modele capacidades, contexts, comandos, consultas e proprietários.
2. Escolha a implantação inicial.
3. Desenhe o fluxo nominal e três falhas parciais.
4. Declare consistência, compensações, contratos, idempotência e telemetria.
5. Planeje duas etapas com gatilhos de extração ou consolidação e testes de contrato, fronteira e recuperação.

**Evidência esperada**

Saída: cada componente tem proprietário, contrato verificável e consequência para falha e atraso.

**Entrega esperada**

Envie `entregas/modulo-3/criar-agendamento/` com dois diagramas, registro de decisão, tabela de estados, contratos de exemplo, estratégia de testes e roteiro de evolução.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Coerência entre domínio, dados e implantação | 25% | Evidência: mesmos limites; insuficiente: topologia contradiz domínio. |
| Falhas e consistência explícitas | 25% | Evidência: falha e efeito; insuficiente: consistência presumida. |
| Contratos e verificações executáveis | 20% | Evidência: teste ou comando; insuficiente: contrato sem verificação. |
| Evolução orientada por sinais | 15% | Evidência: sinal aciona mudança; insuficiente: evolução sem gatilho. |
| Viabilidade operacional | 15% | Evidência: recursos considerados; insuficiente: componente sem operação possível. |
