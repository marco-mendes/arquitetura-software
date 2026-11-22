# Exercícios

As questões usam o caso do módulo, a plataforma de uma rede hospitalar fictícia que atende pacientes de planos de saúde. Nesse caso, o serviço de Exames registra os pedidos de exame feitos pelos médicos e consulta o serviço de Elegibilidade para saber se o paciente tem cobertura do plano antes de gravar cada pedido.

As questões dos níveis recordar e compreender têm uma resposta comentada, que deve ser aberta depois da tentativa de resposta. As atividades dos quatro níveis seguintes da taxonomia de Bloom não têm gabarito. Elas usam campos padronizados que tornam explícitos o contexto, a entrega e a forma de avaliar uma decisão justificável.

## Recordar

1\. Explique por que a expressão "verificar elegibilidade" descreve uma capacidade de negócio enquanto "salvar no PostgreSQL" descreve um mecanismo técnico e dê outro exemplo hospitalar de cada tipo.

<details>
<summary>Ver resposta</summary>

Uma capacidade de negócio é definida pelo resultado que produz para alguém, independentemente da tecnologia usada. A expressão "salvar no PostgreSQL" descreve a forma de persistir um dado e não indica o resultado entregue pela organização. "Agendar atendimento" e "solicitar exame" são exemplos de capacidades de negócio do caso hospitalar. "Enviar JSON" e "consultar cache" são exemplos de mecanismos técnicos, que podem ser trocados por outros mecanismos sem alterar o nome da capacidade atendida.

</details>

2\. Identifique o erro de raciocínio de uma equipe que decide transformar Elegibilidade e Exames em microsserviços imediatamente porque os dois são *bounded contexts* diferentes.

<details>
<summary>Ver resposta</summary>

A equipe confunde fronteira semântica com topologia física. Um *bounded context* delimita a parte do sistema em que um modelo e a sua linguagem têm significado consistente, delimitação que independe da forma de implantação. Um *bounded context* pode ser implementado como módulo de um monólito, como parte de um macrosserviço ou como serviço implantável. A extração física só se justifica quando há necessidade comprovada de autonomia de implantação, de escala ou de falha independente. Tratar cada fronteira lógica como um serviço separado cria processos, redes e trabalho de operação antes de existir benefício demonstrado.

</details>

3\. Escolha duas das cinco formas de acoplamento entre serviços descritas no módulo e explique com um exemplo a dependência que cada uma cria entre os serviços.

<details>
<summary>Ver resposta</summary>

As cinco formas de acoplamento estão descritas na tabela.

| Forma | Dependência criada |
| --- | --- |
| De contrato | O consumidor depende de campos, semântica e códigos de resposta do provedor. A mudança de um campo pode quebrar o consumidor |
| Temporal | O consumidor precisa que o provedor esteja disponível no momento da chamada, como numa chamada síncrona |
| De dados | Duas unidades dependem da mesma estrutura de armazenamento ou alteram a mesma informação |
| De implantação | Uma mudança obriga a publicar várias unidades em conjunto |
| Organizacional | Equipes precisam negociar continuamente para entregar uma única capacidade |

No laboratório da Oficina de ferramentas, Exames aceita acoplamento temporal com Elegibilidade porque espera a resposta sobre a cobertura do paciente antes de gravar o pedido de exame. Exames evita o acoplamento de dados, porque não lê diretamente a tabela de Elegibilidade.

</details>

4\. Uma pessoa desenvolvedora de Faturamento precisa de um relatório e faz uma consulta SQL direta nas tabelas do banco de Elegibilidade, sem passar pelo contrato de API. Indique a regra de propriedade de dados violada pela consulta e o acoplamento oculto que ela cria.

<details>
<summary>Ver resposta</summary>

A consulta viola o banco por serviço, regra segundo a qual somente o serviço proprietário acessa diretamente o próprio armazenamento. Os demais consumidores devem usar contrato, evento ou réplica projetada. A consulta direta cria um acoplamento de dados oculto, porque Faturamento passa a depender da estrutura interna das tabelas de Elegibilidade sem nenhum contrato que declare essa dependência. Uma mudança de coluna feita por Elegibilidade pode quebrar o relatório sem aviso, o que retira do proprietário o controle sobre a evolução do próprio *schema*.

</details>

5\. Indique a característica que distingue o monólito modular, o macrosserviço e o microsserviço como formas de implantação, considerando que o tamanho do código não é essa característica.

<details>
<summary>Ver resposta</summary>

A característica que distingue as três formas é a autonomia física de implantação e de falha. No monólito modular, os módulos têm fronteiras lógicas claras e são publicados e falham juntos numa única unidade implantável. No macrosserviço, algumas fronteiras já correspondem a processos separados que agrupam mais de uma capacidade por unidade. No microsserviço, cada unidade implantável corresponde a uma responsabilidade de negócio, é dona do próprio estado e pode ser publicada e falhar de forma independente. O prefixo "micro" não corresponde a nenhum limite de linhas de código ou de pessoas.

</details>

6\. Indique o nome da situação em que Exames continua respondendo a consultas ao próprio banco e passa a recusar novas solicitações porque Elegibilidade está fora do ar e explique por que ela não deve ser tratada apenas como queda do sistema.

<details>
<summary>Ver resposta</summary>

A situação se chama falha parcial, em que uma parte do sistema distribuído continua saudável enquanto outra parte indisponível impede a conclusão de uma capacidade específica. Tratar a situação como queda do sistema esconde a informação de que o consumidor precisa para agir, como saber se pode repetir o pedido ou se o problema está no próprio pedido. Por isso, a resposta deve expor a causa real com o status `503` e o código `dependencia_indisponivel`. Um `500` genérico trataria a falha da dependência como erro interno de Exames.

</details>

7\. Descreva o que acontece com Exames quando uma chamada síncrona sem prazo de espera aguarda sem limite a resposta de Elegibilidade lenta e explique o papel do prazo de espera, conhecido como *timeout*, nessa situação.

<details>
<summary>Ver resposta</summary>

Sem prazo de espera, a requisição de Exames aguarda indefinidamente a resposta de Elegibilidade e mantém ocupados a *thread*, a conexão e os demais recursos alocados para a chamada. Quando isso se repete em várias solicitações simultâneas, a lentidão de Elegibilidade se propaga e pode esgotar os recursos de Exames. O prazo de espera limita o tempo que Exames aguarda antes de tratar a chamada como falha, o que restringe o problema à operação que depende de Elegibilidade.

</details>

8\. O banco de Elegibilidade está replicado em dois datacenters da rede hospitalar. O enlace entre eles fica indisponível por três minutos, período em que as duas réplicas continuam atendendo sem comunicação entre si. Nesse intervalo, o sistema pode recusar escritas para manter uma visão única e atual do dado ou continuar aceitando escritas nas duas réplicas com risco de divergência. Indique o nome que o teorema CAP dá a essa interrupção de comunicação e as duas propriedades entre as quais ela obriga a escolher.

<details>
<summary>Ver resposta</summary>

O teorema CAP chama essa interrupção de partição, situação em que mensagens entre nós ou grupos de nós são perdidas ou atrasadas. Durante os três minutos de partição, a escolha é entre consistência e disponibilidade. A consistência recusa ou atrasa operações para preservar uma visão única e atual do dado. A disponibilidade mantém cada réplica respondendo com a possibilidade de divergência entre elas. Depois que o enlace volta, a escolha descrita pelo CAP deixa de existir e as decisões entre latência e consistência passam a ser descritas por outros modelos. Por isso, o CAP não é uma escolha permanente de duas das três letras e não justifica dado desatualizado numa integração comum, que exige um mecanismo e uma promessa de convergência declarados.

</details>

9\. O fluxo de Agendamento tem três etapas, cada uma com transação local no próprio banco. A Agenda reserva o horário, a Autorização autoriza o procedimento e o Preparo de Sala reserva a sala. As duas primeiras etapas confirmam e a terceira falha, sem nenhuma transação abrangente capaz de desfazer as duas etapas confirmadas. Indique o nome da ação que uma SAGA executa para neutralizar o efeito das etapas anteriores e as duas formas de coordenação da sequência descritas no módulo.

<details>
<summary>Ver resposta</summary>

A ação é a compensação, uma operação definida pelo domínio que neutraliza o efeito de uma etapa já confirmada. Neste exemplo, as compensações liberam o horário reservado e cancelam a autorização. A coreografia coordena a sequência por eventos, aos quais cada participante reage. A orquestração usa um componente que conhece a sequência inteira e conduz cada passo. A compensação acrescenta um fato novo à história do fluxo e também pode falhar. Outros participantes podem ter observado o estado intermediário, por isso o desenho da SAGA declara estados explícitos e comandos idempotentes, além da política de repetição e da trilha de auditoria.

</details>

10\. Em Laudos, a assinatura de um laudo exige validar regras clínicas antes de gravar, enquanto a tela que lista os laudos do mês precisa apenas de uma lista pronta para leitura. A equipe separou as duas operações em classes e interfaces distintas, mantidas no mesmo processo e no mesmo banco PostgreSQL. Indique os dois modelos que o CQRS separa e diga se essa separação dentro de um único banco já conta como CQRS.

<details>
<summary>Ver resposta</summary>

Os dois modelos são o de comando e o de consulta. Os comandos expressam uma intenção e preservam as invariantes de negócio, enquanto as consultas oferecem uma projeção adequada a quem lê. A separação feita em Laudos já conta como CQRS, porque o padrão não exige dois bancos nem mensageria ou *event sourcing* e pode começar com objetos e interfaces distintos no mesmo processo e no mesmo banco. O custo aparece no passo seguinte, quando um modelo de leitura materializado passa a exigir atualização e monitoramento e introduz defasagem e necessidade de reconstrução. Esse modelo materializado só se justifica quando a assimetria entre leitura e escrita, a complexidade dos modelos ou a escala compensam esse custo.

</details>

## Compreender

1\. Explique por que mover duas funções para processos diferentes não reduz automaticamente o acoplamento entre elas.

<details>
<summary>Ver resposta</summary>

A separação de duas funções em processos diferentes mantém a dependência entre elas e muda a sua forma. A chamada de função em memória passa a ser um contrato de rede, com serialização, latência e disponibilidade envolvidas. Se as duas partes continuam mudando pelos mesmos motivos e precisam ser implantadas juntas, os acoplamentos de contrato, temporal e de implantação continuam altos. A distribuição acrescenta o custo da rede e da coordenação remota e não entrega autonomia de implantação, porque as duas partes continuam sendo publicadas juntas.

</details>

2\. Descreva como serviços pequenos demais podem prejudicar a coesão de uma capacidade.

<details>
<summary>Ver resposta</summary>

Coesão é o grau em que os elementos de uma unidade contribuem para uma mesma responsabilidade. Por isso, as regras que mudam pelo mesmo motivo tendem a ficar juntas na mesma unidade. Quando um serviço é dividido em partes menores do que esse conjunto de regras, uma alteração simples de negócio passa a exigir mudanças em vários serviços ao mesmo tempo. Cada um desses serviços tem contrato, esteira de implantação e falha próprios. O resultado é mais coordenação, mais componentes sujeitos a falha e mais contexto necessário para entender uma mudança que deveria ser única.

</details>

3\. Explique se o uso de bancos PostgreSQL diferentes pelos dois serviços do laboratório garante sozinho a proteção da propriedade dos dados e indique o que mais precisa ser verdade para essa proteção existir.

<details>
<summary>Ver resposta</summary>

A separação física não garante a proteção sozinha. A propriedade dos dados define quem tem autoridade para interpretar e alterar uma informação e corresponde a uma regra de acesso e de responsabilidade, independente do local em que o banco está gravado. Bancos, *schemas* ou instâncias separados só protegem a propriedade quando acompanhados de isolamento de rede e de credenciais que impedem a conexão direta de outro serviço. No laboratório da Oficina de ferramentas, a credencial de Exames conhece apenas o banco `exames` e a rede interna de cada banco não é alcançável pelo outro processo. Sem essas permissões, dois bancos separados fisicamente podem ser acessados por qualquer serviço que conheça a *string* de conexão, o que reduz a propriedade a uma convenção sem aplicação.

</details>

4\. Faturamento mantém uma réplica projetada dos dados de Elegibilidade, alimentada pelos eventos que Elegibilidade publica. A promessa é de consistência eventual, em que a réplica chega ao mesmo estado da origem quando não há novas escritas. Essa promessa não define como nem quando a convergência acontece, o que depende das **regras de convergência** listadas abaixo.

- O identificador associa cada evento ao registro correto.
- A ordenação garante a ordem de aplicação quando ela altera o resultado.
- A idempotência impede que o mesmo evento aplicado duas vezes produza o efeito duas vezes.
- A política de repetição trata mensagens perdidas ou atrasadas.
- A reconciliação detecta e corrige a divergência restante.

Escolha três dessas regras e descreva, para cada uma, o que acontece com a réplica de Faturamento quando ela falta.

<details>
<summary>Ver resposta</summary>

- Sem identificador, a réplica cria linhas duplicadas para a mesma pessoa ou atualiza a linha errada, sem como saber qual é a versão corrente.
- Sem ordenação, um evento antigo que chega atrasado sobrescreve um evento mais recente, de modo que uma elegibilidade cancelada volta a aparecer como válida.
- Sem idempotência, a mesma mensagem entregue duas vezes aplica o efeito duas vezes e a réplica acumula um estado que nunca existiu na origem.
- Sem política de repetição, uma mensagem perdida nunca chega à réplica, que fica defasada por tempo indeterminado.
- Sem reconciliação, nenhuma das divergências anteriores é detectada e Faturamento opera sobre dados incorretos sem nenhum sinal de alerta.

A consistência eventual descreve o resultado desejado, enquanto as regras de convergência são os mecanismos que produzem esse resultado.

</details>

5\. Descreva um cenário da plataforma hospitalar em que o monólito modular seja a forma preferível e outro em que microsserviços com implantação independente sejam necessários. Em cada cenário, indique o fato que decide a escolha, considerando que o tamanho do código não é esse fato.

<details>
<summary>Ver resposta</summary>

O monólito modular tende a ser preferível quando as mudanças em duas capacidades acontecem juntas e compartilham uma mesma transação. Um exemplo é a assinatura e a publicação de um laudo, que precisam ser consistentes no mesmo instante e são alteradas pela mesma equipe. Nesse caso, as fronteiras lógicas são úteis e a separação em processos acrescentaria apenas rede e coordenação.

Os microsserviços passam a se justificar quando duas capacidades têm equipes diferentes, cargas de trabalho distintas ou ciclos de mudança e de risco que não deveriam bloquear um ao outro. Um exemplo é a Agenda, que recebe picos de carga e muda com frequência. O Preparo de Sala pertence a outra equipe, tolera alguns minutos de atraso e não deveria ser publicado de novo a cada mudança da Agenda.

Nos dois cenários, a escolha depende da autonomia de implantação e de falha necessária e do padrão de evolução conjunta das capacidades.

</details>

6\. Explique por que uma compensação de SAGA não apaga fatos já observados.

<details>
<summary>Ver resposta</summary>

Uma compensação de SAGA cria um fato novo que neutraliza o efeito de negócio de uma etapa anterior, sem desfazer o que outras partes do sistema já observaram. Se uma solicitação de exame já foi confirmada e notificada, o cancelamento posterior não significa que ela nunca existiu. Quem recebeu a confirmação pode ter agido com base nela, enquanto as mensagens de cancelamento podem chegar duplicadas ou fora de ordem. Por isso, o desenho da SAGA declara estados explícitos, comandos idempotentes e uma trilha de auditoria que mantém os eventos anteriores registrados ao lado da compensação.

</details>

7\. Uma equipe quer introduzir SAGA e CQRS no fluxo de Agendamento com o argumento de que os sistemas distribuídos usam os dois padrões. Indique o problema que cada padrão resolveria e explique por que a adoção de um não implica a necessidade do outro.

<details>
<summary>Ver resposta</summary>

A SAGA resolveria a coordenação de uma mudança que atravessa várias transações locais, situação em que a falha de uma etapa posterior exige compensar as etapas anteriores. A reserva de horário seguida da autorização do procedimento e do preparo de um recurso é um exemplo dessa situação. O CQRS resolveria a assimetria entre a escrita por comandos que preservam invariantes e a leitura por consultas que podem exigir uma projeção de alto volume. Um fluxo pode precisar de SAGA sem precisar separar leitura e escrita, assim como pode precisar de CQRS sem nenhuma coordenação entre transações. A adoção dos dois padrões sem uma necessidade demonstrada para cada um acrescenta componentes, estados e formas de falha sem benefício para o fluxo.

</details>

## Aplicar
### Recomendar a fronteira entre laudos e notificações

**Objetivo**

Recomendar uma entre quatro arquiteturas propostas para a clínica, com a escolha sustentada nos fatos apurados e o benefício e o custo de cada alternativa declarados.

**Situação**

Uma clínica de diagnóstico por imagem opera com um sistema único, executado num só processo, com um só banco e uma só implantação. O sistema contém duas funcionalidades principais. **Laudos** recebe o resultado técnico do equipamento, registra a assinatura do médico radiologista e publica o documento no portal do paciente. **Notificações** avisa o paciente por SMS e por e-mail depois que o laudo é publicado.

As duas funcionalidades leem e escrevem as mesmas tabelas, sem dono declarado para nenhuma delas. A tabela `laudo` contém o conteúdo clínico e o controle de envio nas colunas `sms_enviado_em` e `tentativas_envio`. O mesmo trecho de código que publica o documento também dispara o aviso ao paciente dentro da mesma transação.

Na semana anterior, a lentidão do provedor de SMS também paralisou a publicação de laudos. A equipe de plantão levou quarenta minutos para descobrir que o problema estava no provedor de SMS. A diretoria pediu uma recomendação de arquitetura para a reunião seguinte, com prazo de uma semana.

A lista abaixo reúne os fatos apurados na clínica que valem para a decisão de arquitetura.

1. Uma equipe só mantém o sistema inteiro.
2. A implantação é semanal, com tudo junto.
3. Assinatura e publicação acontecem na mesma transação local e precisam continuar assim.
4. Um atraso de até cinco minutos no aviso ao paciente é aceitável para a clínica.
5. O volume é estável, sem pico previsto para os próximos meses.
6. Não existe fila, *broker* ou serviço separado no ambiente hoje.

A tabela define os termos necessários para responder à atividade.

| Termo | Definição em uma linha |
| --- | --- |
| Dono do dado | quem tem autoridade para interpretar e alterar a informação, enquanto os demais consumidores pedem a informação por interface |
| Fronteira lógica | módulos com interface e propriedade definidas dentro do mesmo processo |
| Fronteira física | processo, rede e implantação separados, com falha independente |
| Acoplamento temporal | uma unidade só conclui o próprio trabalho depois que outra responde |

A tabela descreve as alternativas em avaliação pela clínica.

| Alternativa | O que muda no desenho |
| --- | --- |
| **A. Prazo de espera no envio** | A estrutura não muda. A chamada ao provedor de SMS recebe um prazo de espera curto e o erro é registrado, com uma implantação, um banco e a mesma transação. |
| **B. Módulos com dono declarado** | Laudos e Notificações passam a ser módulos separados no mesmo processo, cada um dono das próprias tabelas. A publicação continua chamando a notificação de forma direta e síncrona. |
| **C. Módulos com entrega adiada** | Mesma separação da alternativa B, com a publicação apenas registrando o aviso numa tabela de pendências do módulo de Notificações. Um processo em segundo plano envia o aviso depois, com uma única implantação. |
| **D. Notificações como serviço** | Notificações passa a ser um processo próprio com banco próprio e recebe os avisos por um *broker* novo no ambiente. |

Os fatos, os termos e as alternativas descritos nesta página são suficientes para responder a todos os itens da atividade.

**Seu papel**

Você é a pessoa arquiteta convidada a recomendar um caminho. A equipe da clínica implementa a solução depois e espera de você a escolha e a justificativa, com os riscos declarados.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende uma das quatro alternativas para a clínica, em uma frase.
2. Escreva duas frases sobre cada uma das quatro alternativas, com o que ela resolve do incidente da semana anterior e o custo que ela impõe.
3. As alternativas B e C separam a propriedade dos dados do mesmo jeito. Explique o que só a C resolve.
4. Aponte a alternativa que você descartaria de imediato e diga qual fato a derruba.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria a clínica trocar de alternativa. Data no calendário não vale como sinal.

**Evidência esperada**

O artefato traz o quadro comparativo completo, com benefício e custo declarados para cada uma das quatro alternativas. Também traz a recomendação em uma frase com o fato que a sustenta, além do risco aceito e do sinal de revisão descrito como condição observável.

## Analisar
### Diagnosticar a rede de clínicas

**Objetivo**

Explicar o mecanismo de cada sintoma relatado com a separação entre fato apurado e inferência própria, além de comparar duas correções propostas.

**Situação**

Uma rede de clínicas separou o seu sistema há dois anos nos serviços **Cadastro**, **Agenda**, **Atendimento** e **Faturamento**. Cada serviço roda no próprio processo, com repositório e esteira de implantação próprios, o que corresponde formalmente a quatro microsserviços.

A cada consulta registrada, Atendimento chama em sequência Cadastro, Agenda e Faturamento e só responde ao usuário quando os três serviços retornam.

Os quatro processos usam o mesmo *schema* PostgreSQL com as mesmas credenciais. No mês anterior, a inclusão de um campo no cadastro do paciente exigiu quatro implantações coordenadas na mesma janela de sábado.

O painel de cada equipe mostra 99,9% de disponibilidade, enquanto o fluxo de atendimento acumulou incidentes suficientes para entrar na pauta da diretoria. Quatro chamadas síncronas em série com 99,9% de disponibilidade cada resultam em 99,6% no fluxo completo. Esse valor corresponde a 35 horas de indisponibilidade por ano. Cada equipe promete isoladamente cerca de 9 horas de indisponibilidade por ano.

Os fatos abaixo foram apurados na rede e devem ser tratados como dados verificados.

1. Setenta por cento das mudanças em Cadastro e em Atendimento são publicadas juntas.
2. Agenda recebe dez vezes mais carga entre 07h e 09h, quando os pacientes chegam.
3. Faturamento pertence a outro time, com fila de trabalho e prioridades próprias.
4. Cadastro válido é obrigatório para registrar o atendimento.
5. Faturamento não precisa confirmar nada enquanto o usuário espera a resposta.
6. Não existe evento, idempotência nem repetição automática em lugar nenhum.
7. Os quatro processos usam o mesmo *schema* e as mesmas credenciais.

A tabela define as formas de acoplamento usadas nesta análise.

| Tipo | O que significa |
| --- | --- |
| de contrato | o consumidor depende de campos, semântica e códigos de resposta do provedor |
| temporal | o consumidor só conclui o próprio trabalho se o provedor responder agora |
| de dados | duas unidades dependem da mesma estrutura ou alteram a mesma informação |
| de implantação | uma mudança obriga a publicar várias unidades na mesma janela |
| organizacional | duas equipes precisam negociar continuamente para entregar uma capacidade |

A diretoria pediu uma avaliação das duas correções propostas a seguir.

#### Correção 1. Consolidação de Cadastro e Atendimento

Cadastro e Atendimento passam a formar um único serviço, com transação local, banco próprio e uma única esteira de implantação. Agenda e Faturamento continuam separados como estão hoje.

#### Correção 2. Retirada de Faturamento do caminho crítico

Os quatro processos continuam existindo. Atendimento passa a responder ao usuário assim que Cadastro e Agenda confirmam, enquanto o aviso a Faturamento é enviado depois da resposta.

Os fatos, o mapa de chamadas e a conta de disponibilidade estão nesta página, assim como as definições de acoplamento e as duas correções propostas.

**Seu papel**

Você lidera a análise antes de qualquer reestruturação. Nenhuma linha de código será alterada nesta semana, porque a diretoria quer entender o problema antes de autorizar o trabalho.

**O que fazer**

Escreva em texto corrido, um parágrafo por resposta. Sempre que afirmar algo, diga se está apoiado num dos sete fatos ou se é inferência sua.

1. Explique o mecanismo de cada sintoma relatado e diga que tipo de acoplamento ele revela. Os sintomas são as quatro implantações coordenadas para um campo novo e a publicação conjunta de Cadastro e Atendimento, além da espera de Atendimento por Faturamento.
2. Explique por que quatro painéis com 99,9% convivem com um fluxo de 99,6% e diga o que essa conta revela sobre a medição de disponibilidade serviço por serviço.
3. Identifique o processo que tem razão legítima para continuar separado mesmo depois da reestruturação e sustente a escolha com o fato que dá essa razão.
4. Compare as duas correções propostas quanto ao que cada uma resolve, ao problema que ela mantém e ao fato apurado que sustenta cada avaliação. Se recomendar as duas, diga em que ordem e por quê.
5. Hoje, quando Faturamento está fora do ar e alguém registra um atendimento, Atendimento devolve um erro genérico. Explique que informação essa resposta esconde e diga qual resposta seria honesta em cada uma das duas correções.
6. Aponte uma conclusão sua que os sete fatos não sustentam, rotule-a como hipótese e diga qual dado a confirmaria.

**Evidência esperada**

O texto explica o mecanismo de cada sintoma e associa cada afirmação a um fato ou a uma inferência declarada. O texto também compara as duas correções com o benefício e o limite de cada uma e descreve a resposta de falha parcial pelo comportamento que o usuário observa.

## Avaliar
### Decidir a resposta à indisponibilidade da autorização

**Objetivo**

Julgar quatro respostas possíveis a uma indisponibilidade externa com critérios ponderados por você mesmo e defender a escolha diante de um risco clínico.

**Situação**

Uma rede de clínicas depende de um provedor externo de autorizações. Antes de executar um procedimento, a clínica consulta esse provedor por uma chamada HTTP e recebe autorizado ou negado. Não existe evento nem aviso de mudança, enquanto a resposta pode variar de um dia para o outro conforme a situação do beneficiário.

O provedor fica indisponível por até quinze minutos, algumas vezes por mês, sem hora marcada. Nesses períodos, hoje, a clínica simplesmente para de receber solicitações.

A rede considera inaceitáveis duas condições, de modo que reduzir o risco de uma delas tende a aumentar o risco da outra. Executar um procedimento sem autorização válida cria risco clínico e prejuízo financeiro, porque a operadora pode recusar o pagamento depois. Perder a solicitação do paciente também é inaceitável, porque ele já está na clínica e vai embora sem atendimento.

O comitê de arquitetura se reúne na quinta-feira para decidir.

As restrições abaixo valem para a decisão do comitê.

1. Cada solicitação já nasce com um identificador único gerado pela clínica.
2. A rede aceita manter uma solicitação em estado pendente por até trinta minutos.
3. A comunicação com o provedor é feita por consulta HTTP, sem notificação de mudanças.
4. A equipe de operação trabalha em horário comercial, sem plantão noturno.
5. A rede não tem nem pretende criar uma transação distribuída entre a clínica e o provedor.

As alternativas em avaliação estão descritas abaixo.

#### A. Falha explícita

Enquanto o provedor não responde, a clínica recusa a solicitação e informa que o sistema de autorização está indisponível. O paciente é orientado a voltar, ou a recepção anota em papel.

#### B. Recepção pendente

A clínica aceita a solicitação, guarda como pendente e responde que a autorização está em análise. Quando o provedor volta, o sistema consulta e resolve cada pendência, avisando a recepção do resultado.

#### C. Autorização em cache

A clínica guarda a última resposta conhecida de cada beneficiário e a reutiliza durante a indisponibilidade, dentro de uma janela definida por ela.

#### D. Faixa de risco

A clínica aceita e executa na hora apenas os procedimentos de uma lista curta previamente acordada com a operadora, de baixo custo e baixo risco. Todos os demais entram como pendentes, como na alternativa B.

As cinco restrições, as duas condições inaceitáveis e as quatro alternativas descritas estão nesta página.

**Seu papel**

Você é a pessoa arquiteta que apresenta a recomendação ao comitê. A decisão será registrada e cobrada depois, então o que você declarar como custo aceito precisa estar escrito.

**O que fazer**

Escreva em texto corrido. O comitê vai ler o documento antes da reunião, então cada resposta precisa se sustentar sozinha.

1. Antes de comparar, declare os critérios que você vai usar e diga qual deles pesa mais nesta decisão. Justifique a ponderação pelo risco do domínio, sem recorrer a preferência técnica.
2. Avalie as quatro alternativas contra os seus critérios, uma por parágrafo, dizendo o que cada uma protege e o que ela expõe.
3. Recomende uma delas e escreva, em uma frase, o que a clínica está aceitando ao segui-la.
4. Descreva os estados pelos quais uma solicitação passa na sua recomendação e diga o que a recepção enxerga em cada estado.
5. Explique como o identificador único da restrição 1 impede que uma repetição vire procedimento duplicado.
6. Indique a alternativa inaceitável para esta rede e sustente a resposta com uma das duas condições inaceitáveis da situação.
7. Escreva o sinal observável que levaria a rede a rever a decisão e diga quem acompanharia esse sinal, considerando que não há plantão noturno.

**Evidência esperada**

O documento traz critérios declarados e ponderados antes da comparação e as quatro alternativas avaliadas contra esses critérios. Também traz a recomendação com o custo aceito escrito em uma frase e a tabela de estados com o que a recepção observa. O documento termina com o sinal de revisão e o papel responsável por acompanhá-lo, considerando a ausência de plantão noturno.

## Criar
### Propor a arquitetura inicial do agendamento

**Objetivo**

Propor a arquitetura de uma capacidade nova, escolhendo entre três topologias esboçadas e defendendo a escolha com as restrições dadas.

**Situação**

A plataforma hospitalar vai ganhar uma capacidade nova: **Agendamento**. Quando um paciente marca um procedimento, o agendamento precisa fazer três coisas, nesta ordem.

O primeiro passo consulta **Elegibilidade**, que já existe e responde por HTTP se o beneficiário pode usar o plano. O segundo passo reserva o horário na agenda do equipamento, de modo que ninguém mais ocupe aquele intervalo. O terceiro passo avisa **Preparo de Sala**, serviço de outra equipe que cuida de material e higienização, além da equipe de apoio.

A agenda muda com frequência e recebe picos de carga concentrados no início da manhã. Elegibilidade é estável e raramente muda. Preparo de Sala tem outro dono e outro ritmo de entrega e tolera receber o aviso com até dois minutos de atraso.

O paciente precisa ver a confirmação da reserva em até três segundos.

As restrições abaixo valem para a proposta.

1. A resposta ao paciente sai em até três segundos.
2. O identificador da solicitação é gerado pelo consumidor e chega pronto.
3. PostgreSQL está disponível e é a base padrão da plataforma.
4. Mensageria é permitida, embora nenhum *broker* esteja instalado hoje.
5. No máximo três unidades implantáveis novas podem existir neste semestre.

As topologias esboçadas para o Agendamento estão descritas abaixo.

#### A. Agendamento como módulo

Agendamento nasce como módulo dentro de um serviço existente, chamando Elegibilidade por HTTP e Preparo de Sala por HTTP, tudo dentro da mesma requisição do paciente.

#### B. Agendamento como serviço com avisos síncronos

Agendamento passa a ser um serviço próprio com banco próprio. Continua chamando Elegibilidade e Preparo de Sala por HTTP e só confirma ao paciente depois que os dois responderem.

#### C. Agendamento como serviço com aviso adiado

Agendamento passa a ser um serviço próprio com banco próprio. O serviço consulta Elegibilidade por HTTP, reserva o horário e confirma ao paciente, depois de registrar o aviso a Preparo de Sala numa tabela de saída processada logo depois.

As cinco restrições, as três capacidades descritas, as diferenças de ritmo entre elas e as três topologias estão nesta página.

**Seu papel**

Você é a pessoa arquiteta responsável pela proposta inicial. Ela será discutida com as três equipes envolvidas e precisa começar simples, sem fechar portas que a rede vá querer abrir depois.

**O que fazer**

Escreva em texto corrido, com um título por resposta. A proposta é um documento de decisão, enquanto o detalhe técnico fica a cargo da equipe que implementa.

1. Escolha uma das três topologias e defenda a escolha usando pelo menos três das cinco restrições, citando cada uma pelo número.
2. Explique o que as outras duas topologias custariam, uma por parágrafo, para deixar registrado que foram consideradas.
3. Indique o dono da reserva de horário, da resposta de elegibilidade e do estado do preparo de sala e justifique cada dono.
4. Descreva o caminho de sucesso do agendamento em texto corrido, do pedido do paciente até a confirmação, indicando onde a resposta de três segundos é gasta.
5. Descreva o que o paciente vê em três falhas parciais e diga, para cada uma, se a reserva permanece válida. As falhas são Elegibilidade fora do ar, horário ocupado por outra pessoa entre a consulta e a reserva e Preparo de Sala fora do ar.
6. A restrição 4 permite mensageria sem que exista um *broker* instalado. Diga se a sua proposta precisa de mensageria agora e o que aconteceria se a equipe adotasse um *broker* apenas para este caso.
7. Escreva dois sinais observáveis que levariam a rede a mudar a topologia escolhida, um na direção de mais separação e outro na direção de menos.

**Evidência esperada**

O documento traz a topologia escolhida com pelo menos três restrições citadas pelo número e as outras duas topologias avaliadas e descartadas. Também traz um dono declarado para cada dado e o caminho de sucesso descrito com o orçamento de tempo. O documento descreve ainda três falhas parciais com o que o paciente observa e o destino da reserva, além de dois sinais de mudança em direções opostas.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 3 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes. As questões simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

O que é uma capacidade de negócio?

- (a) Algo que a organização sabe fazer para produzir um resultado, independentemente da tela ou da tecnologia atual.
- (b) Um mecanismo técnico, como salvar no PostgreSQL ou enviar JSON.
- (c) Um microsserviço implantado de forma independente.
- (d) Uma tabela do banco de dados compartilhada entre equipes.

#### Questão 2 [Simples]

Em *Domain-Driven Design*, o que delimita um *bounded context*?

- (a) O conjunto de servidores em que um serviço é implantado.
- (b) A área em que um modelo e sua linguagem têm significado consistente.
- (c) O número máximo de linhas de código de um microsserviço.
- (d) O grupo de tabelas acessadas por uma mesma transação.

#### Questão 3 [Simples]

Qual tipo de acoplamento ocorre quando o consumidor precisa que o provedor esteja disponível no momento da chamada?

- (a) De contrato.
- (b) De dados.
- (c) Temporal.
- (d) Organizacional.

#### Questão 4 [Simples]

O que significa o padrão banco por serviço?

- (a) Que cada serviço precisa de um servidor físico de banco de dados próprio.
- (b) Que cada serviço deve usar uma tecnologia de banco diferente.
- (c) Que todos os serviços escrevem em um banco central com tabelas separadas por prefixo.
- (d) Que somente o serviço proprietário acessa diretamente o seu armazenamento, enquanto os demais usam contratos, eventos ou réplicas projetadas.

#### Questão 5 [Simples]

Como o módulo define uma falha parcial?

- (a) Uma falha em que uma parte do sistema distribuído funciona e outra não.
- (b) Uma falha que afeta apenas uma parte dos usuários por erro de interface.
- (c) Uma falha corrigida automaticamente por repetição.
- (d) Uma falha que ocorre apenas durante a implantação.

#### Questão 6 [Simples]

O que é uma SAGA?

- (a) Uma transação ACID distribuída entre vários bancos.
- (b) Um padrão que separa modelos de leitura e de escrita.
- (c) Um log imutável de eventos usado para reconstruir o estado.
- (d) Uma sequência de transações locais coordenadas, com ações compensatórias quando uma etapa posterior falha.

#### Questão 7 [Simples]

O que o padrão CQRS separa?

- (a) O banco de dados de produção e o de testes.
- (b) O código do serviço e o código do gateway.
- (c) Os modelos de comando e de consulta.
- (d) As equipes de desenvolvimento e de operação.

#### Questão 8 [Simples]

O que faz o padrão estrangulador, em inglês *strangler fig*?

- (a) Interrompe chamadas a uma dependência instável depois de um número de falhas.
- (b) Encaminha gradualmente partes de uma interface antiga para uma implementação nova, preservando o contrato.
- (c) Reúne capacidades transversais, como logs e autenticação, em uma base comum.
- (d) Divide o banco de dados em partições por cliente.

### Questões médias

#### Questão 9 [Média]

No laboratório, Exames chama Elegibilidade de forma síncrona antes de gravar uma solicitação e não lê a tabela de Elegibilidade. Quais acoplamentos Exames aceita e evita?

- (a) Aceita acoplamento temporal e evita acoplamento de dados.
- (b) Aceita acoplamento de dados e evita acoplamento temporal.
- (c) Aceita acoplamento de implantação e evita acoplamento de contrato.
- (d) Evita todos os tipos de acoplamento por usar HTTP.

#### Questão 10 [Média]

Elegibilidade parou e Exames não consegue aceitar novas solicitações. Qual resposta o módulo considera adequada para tornar essa condição observável?

- (a) 500 genérico, para não expor detalhes internos.
- (b) 503 Service Unavailable com o código dependencia_indisponivel.
- (c) 201, registrando a solicitação como concluída e corrigindo depois.
- (d) 200 com elegibilidade positiva presumida.

#### Questão 11 [Média]

Uma organização tem dezenas de serviços, cada alteração exige publicação coordenada e vários serviços escrevem no mesmo banco. Como o módulo classifica essa situação?

- (a) Como uma arquitetura de microsserviços madura.
- (b) Como um monólito modular.
- (c) Como um monólito distribuído, com custos remotos sem os benefícios do isolamento.
- (d) Como um macrosserviço bem delimitado.

#### Questão 12 [Média]

A palavra "situação" significa vigência cadastral em Elegibilidade e etapa operacional em Exames. O que o módulo recomenda?

- (a) Unificar o termo em um modelo único para toda a organização.
- (b) Proibir o uso da palavra nos dois serviços.
- (c) Compartilhar a tabela de situações entre os dois serviços.
- (d) Manter cada significado dentro do seu *bounded context* e fazer tradução explícita entre os contextos.

#### Questão 13 [Média]

Um relatório gerencial precisa combinar dados de Elegibilidade e de Exames. Qual abordagem respeita a propriedade dos dados?

- (a) Dar ao serviço de relatório credenciais de leitura nos dois bancos.
- (b) Fazer JOIN entre as tabelas dos dois serviços em uma visão compartilhada.
- (c) Usar composição por API, eventos, réplica analítica ou modelo de leitura com defasagem e origem declaradas.
- (d) Copiar manualmente as tabelas para o banco de Exames toda noite, sem registro.

#### Questão 14 [Média]

Uma equipe quer adotar persistência poliglota e dar um tipo de banco diferente a cada serviço novo. Como o módulo avalia a proposta?

- (a) Adequada, porque cada serviço deve ter tecnologia própria.
- (b) Inadequada, porque persistência poliglota significa escolher mecanismos diferentes apenas quando a forma do dado e seus acessos justificam o custo operacional.
- (c) Adequada, porque bancos diferentes eliminam o acoplamento de dados.
- (d) Inadequada, porque o padrão banco por serviço proíbe mais de uma tecnologia na organização.

#### Questão 15 [Média]

Uma equipe propõe usar CQRS e afirma que precisa de dois bancos de dados e de mensageria para isso. O que o módulo afirma?

- (a) Que CQRS não exige dois bancos, mensageria ou *event sourcing*, porque a separação pode começar em objetos e interfaces no mesmo processo.
- (b) Que CQRS exige dois bancos e dispensa a mensageria.
- (c) Que CQRS exige *event sourcing*.
- (d) Que CQRS só funciona com SAGA orquestrada.

### Questões difíceis

#### Questão 16 [Difícil]

Como o módulo interpreta o teorema CAP em um sistema distribuído real?

- (a) Como a escolha permanente de duas entre três propriedades, feita pelo fornecedor do banco.
- (b) Como a garantia de que sistemas com consistência e disponibilidade não sofrem partições.
- (c) Como uma justificativa para qualquer dado desatualizado em integrações.
- (d) Como uma decisão sobre o comportamento durante uma partição, entre recusar ou atrasar operações e responder aceitando possível divergência.

#### Questão 17 [Difícil]

Durante uma partição, um sistema aceita escritas e duas réplicas recebem alterações concorrentes no registro de um paciente, cuja versão válida deve ser decidida por critério clínico. Qual estratégia de resolução é a única capaz de acertar nesse caso?

- (a) Última escrita vence, pelo carimbo de tempo.
- (b) Tipos de dados que convergem por construção, conhecidos como CRDTs.
- (c) Descartar as duas versões e restaurar o último backup.
- (d) Função de mesclagem do domínio, com regra explícita definida pela aplicação.

#### Questão 18 [Difícil]

Em uma SAGA, o passo de autorizar procedimento falhou depois que a agenda já havia sido reservada e confirmada. Qual afirmação descreve corretamente a compensação?

- (a) A compensação desfaz a reserva como se ela nunca tivesse existido, igual a um rollback ACID.
- (b) A compensação é dispensável, porque a SAGA garante atomicidade entre os serviços.
- (c) A compensação é uma ação de negócio que neutraliza o efeito da reserva, pode falhar e não apaga estados intermediários já observados.
- (d) A compensação deve ser executada pelo banco de dados, sem regra de negócio.

#### Questão 19 [Difícil]

Um fluxo de agendamento tem muitas ramificações e a equipe de suporte precisa saber, em um único lugar, em que estado está cada agendamento. Qual forma de coordenação da SAGA é mais indicada e qual custo ela traz?

- (a) Coreografia, ao custo de concentrar a lógica em um componente central.
- (b) Orquestração, ao custo de manter um componente que se torna dependência de todos os passos.
- (c) Coreografia, ao custo de exigir transação distribuída.
- (d) Orquestração, ao custo de eliminar as operações compensatórias.

#### Questão 20 [Difícil]

No estudo de caso do módulo, a equipe precisava de consistência forte nas regras de elegibilidade, que estavam espalhadas em vários serviços. Qual decisão o módulo descreve e por quê?

- (a) Reunir as regras fortemente relacionadas em um macrosserviço, recuperando uma transação local e deixando a consistência eventual só onde a defasagem era aceitável.
- (b) Introduzir uma SAGA orquestrada, porque é o padrão para consistência forte entre serviços.
- (c) Adotar CQRS com dois bancos, porque separa leitura e escrita.
- (d) Replicar o banco de elegibilidade em todos os serviços consumidores.
