# Estudo de caso

O estudo de caso usa a plataforma hospitalar do laboratório e do exemplo arquitetural deste módulo numa fase anterior ao desenho com dois processos de Elegibilidade e Exames. Nessa fase, a equipe dividiu a capacidade Elegibilidade em mais processos do que a capacidade comportava, depois de uma meta corporativa de migração para microsserviços.

A capacidade Elegibilidade interpreta vínculo, vigência e regras da operadora, como descreve a página de [Conceitos](conceitos.md). Ela foi dividida em sete processos. Os três primeiros tratavam de cadastro de beneficiário, vínculo com a operadora e vigência do plano. Os outros quatro tratavam de categoria de plano, regra contratual, procedimento e rede credenciada. A capacidade vizinha de Autorização foi dividida em quatro processos para protocolo, decisão de autorização, notificação e auditoria. Os onze processos tinham repositório e esteira de implantação próprios e eram mantidos por uma única equipe.

## Sintomas

A inclusão de uma nova regra de autorização exigia alterar os contratos de quatro processos e implantar seis deles na mesma janela. Vínculo, vigência e categoria de plano nunca eram escalados separadamente, porque recebiam sempre a mesma carga ao responder à mesma pergunta de negócio. Em incidentes, a equipe precisava correlacionar os logs de vários processos para descobrir que um campo tinha mudado de significado em um deles. A tela de atendimento fazia oito chamadas sequenciais e mostrava um erro genérico quando qualquer uma delas atrasava.

Os onze processos rodavam em contêineres separados e tinham pouca autonomia real. O desenho apresentava as formas de acoplamento descritas na seção [Acoplamento](conceitos.md#acoplamento) da página de conceitos, analisadas na primeira pergunta ao final desta página. A separação física em vários processos e várias implantações tinha sido feita antes de existir uma separação semântica estável entre as capacidades.

## Diagnóstico por capacidades

A equipe mapeou a linguagem, as regras, as mudanças conjuntas e a propriedade dos dados de cada processo. Vínculo, vigência, categoria de plano e regra contratual participavam sempre da mesma decisão sobre a elegibilidade do beneficiário e mudavam sob as mesmas políticas da operadora. Esse conjunto formava um único *bounded context*, o mesmo contexto **Elegibilidade** do exemplo arquitetural. Protocolo e decisão de autorização formavam outro *bounded context*, chamado **Autorização**. Auditoria recebia fatos dos dois contextos e não deveria controlar o fluxo principal de nenhum deles.

O mapa mostrava três fronteiras lógicas e não determinava quantos processos deveriam existir. A equipe comparou as quatro alternativas descritas na lista seguinte.

- Manter os onze processos e investir em automação de implantação reduziria o custo de operar o desenho e manteria a fronteira incoerente entre os processos.
- Reunir tudo num único processo reduziria as chamadas de rede e misturaria autoridades que deveriam ficar separadas, como a decisão de Autorização tomada dentro de Elegibilidade.
- Consolidar num **macrosserviço** os processos que sempre mudavam juntos preservaria os limites lógicos e reduziria a coordenação de implantação. O macrosserviço é uma unidade implantável própria que agrupa mais de uma capacidade em módulos internos.
- Extrair Auditoria para um fluxo assíncrono por eventos isolaria uma carga com comportamento diferente sem afetar o caminho síncrono da decisão de autorização.

## Decisão

A equipe consolidou vínculo, vigência, categoria de plano e regra contratual num único macrosserviço chamado Elegibilidade. Dentro dele, módulos e testes de arquitetura impedem que um módulo acesse diretamente as tabelas de outro módulo. O banco ficou sob uma única credencial do macrosserviço, com *schemas* internos definidos pela própria equipe. Autorização continuou como outro processo e consome Elegibilidade por uma API documentada, sem acesso direto às tabelas de Elegibilidade.

Auditoria passou a receber eventos depois que a equipe definiu o identificador de negócio, o prazo de retenção e o tratamento de mensagens repetidas. A mudança teve como objetivo impedir que uma indisponibilidade do lado analítico bloqueasse o atendimento ao paciente. O fluxo que precisava de decisão imediata, que é a própria autorização, continuou síncrono.

## Consequências observadas

O número de implantações coordenadas caiu, porque as mudanças que sempre ocorriam juntas passaram a ficar na mesma unidade implantável. A latência percebida também caiu, porque várias chamadas de rede internas foram substituídas por chamadas de função dentro do mesmo processo. Em contrapartida, uma implantação do macrosserviço Elegibilidade passou a afetar ao mesmo tempo as quatro regras consolidadas. Por isso, a equipe passou a dar mais atenção aos testes, à liberação gradual e ao plano de *rollback*.

A equipe avaliou o resultado por indicadores operacionais e não pela contagem de serviços antes e depois da consolidação. Os indicadores acompanhados foram a frequência de implantação independente de cada unidade e o tempo médio de diagnóstico de incidentes. A equipe também acompanhou a taxa de erro nas chamadas entre Elegibilidade e Autorização e a quantidade de mudanças que ainda atravessavam a fronteira entre as duas.

## Discussão de consistência

Antes da consolidação, processos diferentes escreviam partes de um estado que deveria formar uma única decisão de elegibilidade, sem transação nem compensação entre eles. Uma falha no meio do fluxo deixava registros contraditórios em bancos diferentes. A equipe considerou introduzir uma **SAGA**, padrão de coordenação de transações locais com compensação descrito na página [Padrões e decisões](padroes-e-decisoes.md#saga). Antes disso, avaliou se a distribuição ainda era necessária. A reunião das regras fortemente relacionadas num único macrosserviço permitiu manter a consistência local numa única transação de banco, o que eliminou a necessidade de SAGA para decidir a elegibilidade.

No fluxo entre Elegibilidade e Autorização, a chamada síncrona continuou como escolha deliberada, porque nenhuma autorização pode ser registrada sem uma resposta válida de Elegibilidade.

Um painel gerencial precisava cruzar autorizações com dados agregados de várias fontes. O painel passou a ler uma projeção própria atualizada por eventos, sem consultar diretamente os bancos operacionais. Essa solução aplica o **CQRS**, padrão de separação entre modelo de leitura e modelo de escrita descrito na seção [CQRS](padroes-e-decisoes.md#cqrs), somente no painel que tinha essa necessidade. O painel passou a mostrar de forma explícita a defasagem da projeção em relação aos bancos operacionais.

## Evidência para revisar a decisão

A consolidação deve ser revista nas situações listadas abaixo.

1. Equipes diferentes passam a ser donas de partes do macrosserviço.
2. Uma das regras passa a precisar de um ciclo de implantação isolado.
3. As cargas de vínculo e vigência e a carga de regra contratual divergem de forma relevante.
4. A unidade volta a impedir entregas independentes.
5. A projeção do painel gerencial deixa de atender ao prazo exigido pelo negócio.

O caso mostra que consolidar processos pode corrigir uma fragmentação excessiva e que a distribuição de um sistema não é um objetivo em si. A decisão precisa alinhar a coesão do código, a propriedade dos dados, o padrão de comunicação e a organização das equipes. Um macrosserviço pode ser um desenho estável ou um estágio de transição. Um monólito modular também pode ser o desenho final adequado ao contexto. Microsserviços continuam adequados em fronteiras específicas, como Elegibilidade e Exames no exemplo deste módulo, em que a autonomia observada compensa o custo das chamadas de rede.

A consolidação também precisa preservar os contratos externos durante a migração. Um roteador pode encaminhar as chamadas antigas para o novo macrosserviço enquanto os consumidores são atualizados aos poucos. Esse roteador aplica o padrão estrangulador, descrito na página [Padrões e decisões](padroes-e-decisoes.md#chassi-e-estrangulador-evoluir-sem-reescrever-no-escuro), que exige uma única fonte de verdade em cada etapa e uma data para desligar o caminho antigo.

## Netflix e Uber como fonte de perguntas

Relatos públicos sobre a Netflix destacam a escala de entrega e a necessidade de isolar mudanças e falhas entre muitas equipes. Relatos sobre a Uber mostram como domínios, volumes e operações geográficas diferentes justificam fronteiras mais granulares. Os dois casos não servem de argumento para copiar a topologia de outra empresa, porque cada empresa tem histórico, equipes e obrigações operacionais diferentes dos de um hospital.

Os dois casos servem para formular perguntas sobre consequências, apresentadas na lista seguinte.

- Qual carga precisa escalar separadamente das demais.
- Qual falha precisa ficar contida sem interromper o restante do sistema.
- Qual contrato precisa continuar estável durante uma migração.
- Como a equipe reverte a extração se a fronteira escolhida não entregar a autonomia esperada.

Uma extração reversível começa por módulos, contratos, telemetria e dados com proprietário definido. O padrão estrangulador, que migra uma rota de cada vez e mantém a rota antiga ativa até a troca ser segura, depende de uma fonte de verdade única e de um plano para desligar o caminho antigo.

## Perguntas para revisar o caso

Cada pergunta retoma o conceito necessário e indica a página em que ele foi apresentado, de modo que a resposta possa ser elaborada sem sair desta página. As respostas devem ser elaboradas antes dos exercícios do módulo.

### Forma de acoplamento que mais atrasava a equipe {#1-qual-forma-de-acoplamento-mais-atrasava-a-equipe}

O **acoplamento** é a dependência entre unidades de software e continua existindo quando uma chamada de função é substituída por uma chamada HTTP, como descreve a seção [Acoplamento](conceitos.md#acoplamento). O desenho de onze processos apresentava as quatro formas de acoplamento da tabela.

| Forma | Dependência criada entre as unidades | Ocorrência neste caso |
| --- | --- | --- |
| De implantação | Uma mudança exige publicar várias unidades em conjunto | Uma nova regra de autorização obrigava a implantar seis processos na mesma janela |
| Temporal | O consumidor precisa que o provedor esteja disponível no momento da chamada | A tela de atendimento fazia oito chamadas sequenciais e mostrava erro quando uma delas atrasava |
| De contrato | O consumidor depende de campos, semântica e códigos de resposta do provedor | Cada processo expunha uma parte do mesmo assunto, e uma regra nova alterava o contrato de quatro deles |
| Organizacional | Equipes precisam negociar continuamente para entregar uma capacidade | Uma única equipe mantinha os onze processos e coordenava cada mudança entre eles |

Escolha a forma de acoplamento que mais atrasava o trabalho da equipe e justifique a escolha com o sintoma da coluna da direita.

### Critério que revelou um único bounded context {#2-qual-criterio-revelou-que-quatro-processos-eram-um-unico-bounded-context}

Um ***bounded context*** é o limite dentro do qual um modelo e a sua linguagem têm significado consistente, como descreve a seção [Bounded context](conceitos.md#bounded-context). A contagem de processos não revela esse limite, porque os onze processos do caso correspondiam a três contextos. Para encontrar os três contextos, a equipe aplicou a cada processo os critérios de linguagem e de regras, além dos critérios de mudanças conjuntas e de propriedade dos dados.

| Critério observado | Pergunta respondida pelo critério |
| --- | --- |
| Linguagem | Os mesmos termos têm o mesmo significado nos dois processos? |
| Regras | As regras mudam sob a mesma política? |
| Mudanças conjuntas | Quando um processo muda, o outro tende a mudar junto? |
| Propriedade dos dados | Quem tem autoridade para interpretar e alterar a informação? |

Com base na seção "Diagnóstico por capacidades", indique qual dos quatro critérios mostrou de forma mais direta que as quatro regras consolidadas formavam um único *bounded context*. Transcreva a frase do caso que sustenta a escolha.

### Consolidação que preserva as fronteiras {#3-por-que-uma-consolidacao-preserva-as-fronteiras-e-a-outra-nao}

Um **macrosserviço** é uma unidade implantável própria que agrupa mais de uma capacidade em módulos internos e ocupa a posição intermediária entre o monólito modular e o microsserviço, como descreve a página [Padrões e decisões](padroes-e-decisoes.md#monolito-modular-macrosservicos-e-microsservicos). A equipe comparou as duas consolidações da tabela, que reúnem elementos de naturezas diferentes.

| Alternativa | Elementos reunidos |
| --- | --- |
| Escolhida | Vínculo, vigência, categoria de plano e regra contratual, que pertencem ao mesmo *bounded context*, Elegibilidade |
| Descartada | Elegibilidade, Autorização e Auditoria completas, que são três *bounded contexts* com autoridade sobre decisões diferentes |

Explique em uma ou duas frases por que a primeira alternativa preserva os limites encontrados pelo mapa de capacidades. Indique também quais autoridades a segunda alternativa misturaria.

### Regras definidas antes da mensageria {#4-por-que-definir-as-tres-regras-antes-de-ligar-a-mensageria}

Auditoria passou a receber os fatos por eventos e deixou de ser chamada dentro do atendimento. A consistência eventual exige regras de convergência, como descreve a seção [Consistência local e consistência entre serviços](padroes-e-decisoes.md#consistencia-local-e-consistencia-entre-servicos). Entre essas regras estão a identidade dos registros e a idempotência, além da repetição controlada e da reconciliação, de onde vêm as decisões tomadas pela equipe antes de ligar a mensageria.

| Decisão tomada antes | Garantia obtida |
| --- | --- |
| Identificador de negócio | Cada evento pode ser associado ao atendimento correto, mesmo quando chega fora de ordem |
| Prazo de retenção | A equipe sabe até quando o fato precisa ficar disponível e quando pode ser descartado |
| Comportamento de repetição | A mesma mensagem entregue duas vezes não produz o efeito duas vezes |

Escolha uma das três decisões e descreva o registro que a trilha de auditoria passaria a conter se a equipe tivesse ligado a mensageria sem ela.

### Dado que torna visível um sinal de revisão {#5-que-dado-tornaria-visivel-um-sinal-de-revisao}

A seção "Evidência para revisar a decisão" lista cinco sinais que indicariam a necessidade de rever a consolidação. Um sinal só pode ser acompanhado quando corresponde a um dado concreto que a equipe consegue observar. O sinal 3, por exemplo, aparece na comparação das requisições por minuto entre os módulos ao longo de algumas semanas. Escolha outro sinal da lista e indique o dado que a equipe precisaria acompanhar para detectar esse sinal.

As respostas preparam a decisão registrada em ADR no [incremento 3 do projeto integrador](../projeto-integrador/incrementos.md#incremento-3-limites-de-servicos-dados-e-coordenacao), que trata da escolha entre consolidar e distribuir e da evidência que sustenta essa escolha.
