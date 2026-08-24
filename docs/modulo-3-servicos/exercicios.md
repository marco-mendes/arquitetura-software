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
### Recomendar a fronteira entre laudos e notificações

**Objetivo**

Recomendar uma entre quatro arquiteturas propostas para a clínica, sustentando a escolha nos fatos apurados e declarando o que cada alternativa ganha e o que cobra.

**Situação**

Uma clínica de diagnóstico por imagem roda tudo num sistema único: um processo, um banco, uma implantação. Duas coisas acontecem ali dentro. **Laudos** recebe o resultado técnico do equipamento, registra a assinatura do médico radiologista e publica o documento no portal do paciente. **Notificações** avisa o paciente por SMS e por e-mail depois que o laudo foi publicado.

As duas funcionalidades leem e escrevem as mesmas tabelas, e nenhuma tabela tem dono declarado. A tabela `laudo` carrega, lado a lado, o conteúdo clínico e o controle de envio, nas colunas `sms_enviado_em` e `tentativas_envio`. O mesmo trecho de código que publica o documento também dispara o aviso, dentro da mesma transação.

Na semana passada o provedor de SMS ficou lento. A publicação de laudos travou junto, e o plantão levou quarenta minutos para descobrir que o problema não estava no laudo. A diretoria pediu uma recomendação para a próxima reunião.

Seis fatos foram apurados na clínica e valem para a decisão:

1. Uma equipe só mantém o sistema inteiro.
2. A implantação é semanal, com tudo junto.
3. Assinatura e publicação acontecem na mesma transação local, e precisam continuar assim.
4. Um atraso de até cinco minutos no aviso ao paciente é aceitável para a clínica.
5. O volume é estável, sem pico previsto para os próximos meses.
6. Não existe fila, *broker* ou serviço separado no ambiente hoje.

Os termos necessários para responder:

| Termo | Definição em uma linha |
| --- | --- |
| Dono do dado | quem tem autoridade para interpretar e alterar a informação; os demais pedem por interface |
| Fronteira lógica | módulos com interface e propriedade definidas dentro do mesmo processo |
| Fronteira física | processo, rede e implantação separados, com falha independente |
| Acoplamento temporal | uma unidade só conclui o próprio trabalho depois que outra responde |

As quatro alternativas em avaliação:

| Alternativa | O que muda no desenho |
| --- | --- |
| **A. Tempo limite no envio** | Nada de estrutura. A chamada ao provedor de SMS ganha tempo limite curto e o erro é registrado. Uma implantação, um banco, mesma transação. |
| **B. Módulos com dono declarado** | Laudos e Notificações viram módulos separados no mesmo processo, cada um dono das próprias tabelas. A publicação continua chamando a notificação de forma direta e síncrona. |
| **C. Módulos com entrega adiada** | Como a B, e a publicação passa a apenas registrar o aviso numa tabela de pendências do módulo de Notificações. Um processo em segundo plano envia depois. Uma implantação só. |
| **D. Notificações como serviço** | Notificações vira processo próprio, com banco próprio, recebendo os avisos por um *broker* novo no ambiente. |

Os seis fatos apurados, as quatro alternativas descritas e as referências de padrões e decisões do módulo.

**Seu papel**

Você é a pessoa arquiteta convidada a recomendar um caminho. A equipe da clínica implementa depois, e espera de você a escolha e a justificativa, com os riscos declarados.

**O que fazer**

Escreva em prosa, uma resposta por item. Não é preciso desenhar nada.

1. Recomende uma das quatro alternativas para a clínica, em uma frase.
2. Sobre cada uma das quatro, escreva duas frases: o que ela resolve do incidente da semana passada e o que ela cobra em troca.
3. As alternativas B e C separam a propriedade dos dados do mesmo jeito. Explique o que só a C resolve.
4. Aponte a alternativa que você descartaria de imediato e diga qual fato a derruba.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria a clínica trocar de alternativa. Data no calendário não vale como sinal.

**Evidência esperada**

O artefato traz o quadro comparativo completo, com ganho e custo declarados para cada uma das quatro alternativas, a recomendação escrita em uma frase, o fato que sustenta a escolha, o risco aceito e o sinal de revisão como condição observável.

## Analisar
### Diagnosticar a rede de clínicas

**Objetivo**

Explicar o mecanismo por trás de cada sintoma relatado, separando o que é fato apurado do que é inferência sua, e comparar duas correções propostas.

**Situação**

Uma rede de clínicas separou seu sistema em quatro serviços há dois anos: **Cadastro**, **Agenda**, **Atendimento** e **Faturamento**. Cada um roda no próprio processo, com repositório próprio e esteira de implantação própria. No papel, são quatro microsserviços.

A cada consulta registrada, Atendimento chama Cadastro, depois Agenda, depois Faturamento, em sequência, e só responde ao usuário quando as três voltam.

Os quatro processos apontam para o mesmo *schema* PostgreSQL, com as mesmas credenciais. Acrescentar um campo no cadastro do paciente, no mês passado, exigiu quatro implantações coordenadas na mesma janela de sábado.

O painel de cada equipe mostra 99,9% de disponibilidade, e mesmo assim o fluxo de atendimento acumulou incidentes o suficiente para virar pauta na diretoria. Ninguém fez a conta que explica o painel: quatro chamadas síncronas em série, cada uma com 99,9%, entregam 99,6% no fluxo inteiro, o que significa cerca de 35 horas indisponíveis por ano contra as 9 horas que cada equipe promete isoladamente.

Sete fatos foram apurados na rede. Trate cada um como dado verificado:

1. Setenta por cento das mudanças em Cadastro e em Atendimento são publicadas juntas.
2. Agenda recebe dez vezes mais carga entre 07h e 09h, quando os pacientes chegam.
3. Faturamento pertence a outro time, com fila de trabalho e prioridades próprias.
4. Cadastro válido é obrigatório para registrar o atendimento.
5. Faturamento não precisa confirmar nada enquanto o usuário espera a resposta.
6. Não existe evento, idempotência nem repetição automática em lugar nenhum.
7. Os quatro processos usam o mesmo *schema* e as mesmas credenciais.

Cinco tipos de acoplamento aparecem nesta análise, e as definições abaixo bastam para respondê-la:

| Tipo | O que significa |
| --- | --- |
| de contrato | o consumidor depende de campos, semântica e códigos de resposta do provedor |
| temporal | o consumidor só conclui o próprio trabalho se o provedor responder agora |
| de dados | duas unidades dependem da mesma estrutura ou alteram a mesma informação |
| de implantação | uma mudança obriga a publicar várias unidades na mesma janela |
| organizacional | duas equipes precisam negociar continuamente para entregar uma capacidade |

Duas correções estão sobre a mesa, e a diretoria quer sua leitura sobre as duas:

#### Correção 1 — consolidar Cadastro e Atendimento

Os dois viram um serviço só, com transação local, banco próprio e uma esteira. Agenda e Faturamento continuam separados como estão hoje.

#### Correção 2 — tirar Faturamento do caminho crítico

Os quatro processos continuam existindo. Atendimento passa a responder ao usuário assim que Cadastro e Agenda confirmam, e o aviso a Faturamento sai depois, fora da espera.

Os sete fatos, o mapa de chamadas, a conta de disponibilidade, as definições de acoplamento e as duas correções propostas, todos nesta página.

**Seu papel**

Você lidera a análise antes de qualquer reestruturação. Nenhuma linha de código será alterada esta semana; a diretoria quer entender o problema antes de autorizar trabalho.

**O que fazer**

Escreva em prosa, um parágrafo por resposta. Sempre que afirmar algo, diga se está apoiado num dos sete fatos ou se é inferência sua.

1. Três sintomas foram relatados: um campo novo exigiu quatro implantações coordenadas, Cadastro e Atendimento saem sempre juntos, e Atendimento espera Faturamento para responder. Explique o mecanismo de cada um e diga que tipo de acoplamento ele revela.
2. Explique por que quatro painéis marcando 99,9% convivem com um fluxo de 99,6%, e diga o que essa conta revela sobre medir disponibilidade serviço por serviço.
3. Um dos quatro processos tem razão legítima para continuar separado mesmo depois da reestruturação. Identifique qual, e sustente com o fato que dá essa razão.
4. Compare as duas correções propostas: o que cada uma resolve, o que ela deixa em pé e qual fato apurado sustenta cada avaliação. Se recomendar as duas, diga em que ordem e por quê.
5. Hoje, quando Faturamento está fora do ar e alguém registra um atendimento, Atendimento devolve um erro genérico. Explique que informação essa resposta esconde e diga qual resposta seria honesta em cada uma das duas correções.
6. Aponte uma conclusão sua que os sete fatos não sustentam, rotule-a como hipótese e diga qual dado a confirmaria.

**Evidência esperada**

O texto explica o mecanismo de cada sintoma em vez de apenas nomeá-lo, associa cada afirmação a um fato ou a uma inferência declarada, compara as duas correções com ganho e limite de cada uma, e traz a resposta de falha parcial escrita com o comportamento que o usuário observa.

## Avaliar
### Decidir a resposta à indisponibilidade da autorização

**Objetivo**

Julgar quatro respostas possíveis a uma indisponibilidade externa, usando critérios que você mesmo pondera, e defender a escolha diante de um risco clínico.

**Situação**

Uma rede de clínicas depende de um provedor externo de autorizações. Antes de executar um procedimento, a clínica consulta esse provedor por uma chamada HTTP e recebe autorizado ou negado. Não existe evento nem aviso de mudança, e a resposta pode variar de um dia para o outro conforme a situação do beneficiário.

O provedor fica indisponível por até quinze minutos, algumas vezes por mês, sem hora marcada. Nesses períodos, hoje, a clínica simplesmente para de receber solicitações.

Duas coisas são inaceitáveis para a rede, e elas puxam em direções opostas. Executar um procedimento sem autorização válida cria risco clínico e prejuízo financeiro, porque a operadora pode recusar o pagamento depois. Perder a solicitação do paciente também é inaceitável, porque ele já está na clínica e vai embora sem atendimento.

O comitê de arquitetura se reúne na quinta-feira para decidir.

Cinco restrições valem para a decisão:

1. Cada solicitação já nasce com um identificador único gerado pela clínica.
2. A rede aceita manter uma solicitação em estado pendente por até trinta minutos.
3. A comunicação com o provedor é consulta HTTP; ele não notifica mudanças.
4. A equipe de operação trabalha em horário comercial, sem plantão noturno.
5. Não existe transação distribuída entre a clínica e o provedor, e não haverá.

As quatro alternativas em avaliação:

#### A. Falha explícita

Enquanto o provedor não responde, a clínica recusa a solicitação e informa que o sistema de autorização está indisponível. O paciente é orientado a voltar, ou a recepção anota em papel.

#### B. Recepção pendente

A clínica aceita a solicitação, guarda como pendente e responde que a autorização está em análise. Quando o provedor volta, o sistema consulta e resolve cada pendência, avisando a recepção do resultado.

#### C. Autorização em cache

A clínica guarda a última resposta conhecida de cada beneficiário e a reutiliza durante a indisponibilidade, dentro de uma janela definida por ela.

#### D. Faixa de risco

A clínica aceita e executa na hora apenas os procedimentos de uma lista curta previamente acordada com a operadora, de baixo custo e baixo risco. Todos os demais entram como pendentes, como na alternativa B.

As cinco restrições, as duas condições inaceitáveis e as quatro alternativas descritas, todas nesta página.

**Seu papel**

Você é a pessoa arquiteta que apresenta a recomendação ao comitê. A decisão será registrada e cobrada depois, então o que você declarar como custo aceito precisa estar escrito.

**O que fazer**

Escreva em prosa. O comitê vai ler o documento antes da reunião, então cada resposta precisa se sustentar sozinha.

1. Antes de comparar, declare os critérios que você vai usar e diga qual deles pesa mais nesta decisão. Justifique a ponderação pelo risco do domínio, e não por preferência técnica.
2. Avalie as quatro alternativas contra os seus critérios, uma por parágrafo, dizendo o que cada uma protege e o que ela expõe.
3. Recomende uma delas e escreva, em uma frase, o que a clínica está aceitando ao segui-la.
4. Descreva os estados pelos quais uma solicitação passa na sua recomendação, e diga o que a recepção enxerga em cada estado.
5. Explique como o identificador único da restrição 1 impede que uma repetição vire procedimento duplicado.
6. Uma das quatro é inaceitável para esta rede. Diga qual, e sustente com uma das duas condições inaceitáveis da situação.
7. Escreva o sinal observável que levaria a rede a rever a decisão, e diga quem olharia esse sinal, dado que não há plantão noturno.

**Evidência esperada**

O documento traz critérios declarados e ponderados antes da comparação, as quatro alternativas avaliadas contra esses critérios, a recomendação com o custo aceito escrito em uma frase, a tabela de estados com o que a recepção observa, e o sinal de revisão com o responsável por observá-lo.

## Criar
### Propor a arquitetura inicial do agendamento

**Objetivo**

Propor a arquitetura de uma capacidade nova, escolhendo entre três topologias esboçadas e defendendo a escolha com as restrições dadas.

**Situação**

A plataforma hospitalar vai ganhar uma capacidade nova: **Agendamento**. Quando um paciente marca um procedimento, o agendamento precisa fazer três coisas, nesta ordem.

Primeiro, consultar **Elegibilidade**, que já existe e responde por HTTP se o beneficiário pode usar o plano. Segundo, reservar o horário na agenda do equipamento, garantindo que ninguém mais ocupe aquele intervalo. Terceiro, avisar **Preparo de Sala**, que pertence a outra equipe e cuida de material, higienização e equipe de apoio.

Três coisas diferenciam essas partes. A agenda muda o tempo inteiro e recebe picos concentrados no início da manhã. Elegibilidade é estável e raramente muda. Preparo de Sala tem outro dono, outro ritmo de entrega, e tolera receber o aviso com até dois minutos de atraso.

O paciente precisa ver a confirmação da reserva em até três segundos.

Cinco restrições valem para a proposta:

1. A resposta ao paciente sai em até três segundos.
2. O identificador da solicitação é gerado pelo consumidor, e chega pronto.
3. PostgreSQL está disponível e é a base padrão da plataforma.
4. Mensageria é permitida, e não existe nenhum *broker* instalado hoje.
5. No máximo três unidades implantáveis novas podem existir neste semestre.

As três topologias esboçadas:

#### A. Agendamento como módulo

Agendamento nasce como módulo dentro de um serviço existente, chamando Elegibilidade por HTTP e Preparo de Sala por HTTP, tudo dentro da mesma requisição do paciente.

#### B. Agendamento como serviço, avisos síncronos

Agendamento vira serviço próprio com banco próprio. Continua chamando Elegibilidade e Preparo de Sala por HTTP, e só confirma ao paciente depois que os dois responderem.

#### C. Agendamento como serviço, aviso adiado

Agendamento vira serviço próprio com banco próprio. Consulta Elegibilidade por HTTP, reserva o horário, confirma ao paciente, e registra o aviso a Preparo de Sala numa tabela de saída processada logo depois.

As cinco restrições, as três capacidades descritas, as diferenças de ritmo entre elas e as três topologias, todas nesta página.

**Seu papel**

Você é a pessoa arquiteta responsável pela proposta inicial. Ela será discutida com as três equipes envolvidas e precisa começar simples, sem fechar portas que a rede vá querer abrir depois.

**O que fazer**

Escreva em prosa, com um título por resposta. A proposta é um documento de decisão; o detalhe técnico fica para a equipe que implementa.

1. Escolha uma das três topologias e defenda a escolha usando pelo menos três das cinco restrições, citando cada uma pelo número.
2. Explique o que as outras duas topologias custariam, uma por parágrafo, para deixar registrado que foram consideradas.
3. Diga quem é o dono de cada dado que aparece na história: a reserva de horário, a resposta de elegibilidade e o estado do preparo de sala. Justifique cada dono.
4. Descreva o caminho de sucesso do agendamento em texto corrido, do pedido do paciente até a confirmação, indicando onde a resposta de três segundos é gasta.
5. Descreva três falhas parciais e o que o paciente vê em cada uma: Elegibilidade fora do ar, horário já ocupado por outra pessoa entre a consulta e a reserva, e Preparo de Sala fora do ar. Para cada uma, diga se a reserva permanece válida.
6. A restrição 4 permite mensageria e não a entrega instalada. Diga se a sua proposta precisa dela agora, e o que aconteceria se a equipe adotasse um *broker* apenas para este caso.
7. Escreva dois sinais observáveis que levariam a rede a mudar a topologia escolhida, um na direção de mais separação e outro na direção de menos.

**Evidência esperada**

O documento traz a topologia escolhida com pelo menos três restrições citadas pelo número, as outras duas avaliadas e descartadas, um dono declarado para cada dado, o caminho de sucesso descrito com o orçamento de tempo, três falhas parciais com o que o paciente observa e o destino da reserva, e dois sinais de mudança em direções opostas.
