# Estudo de caso: quando a fragmentação supera a autonomia

Este caso usa a mesma plataforma hospitalar do laboratório e do exemplo arquitetural deste módulo — mas numa fase anterior. Antes de chegar ao desenho de dois processos que você viu em Elegibilidade e Exames, a equipe já tinha tentado "ir direto para microsserviços" em Elegibilidade, e foi longe demais.

Depois de uma meta corporativa de "migrar para microsserviços", a capacidade Elegibilidade — que interpreta vínculo, vigência e regras da operadora, como você viu em [conceitos](conceitos.md) — foi dividida em processos separados: cadastro de beneficiário, vínculo com a operadora, vigência do plano, categoria de plano, regra contratual, procedimento e rede credenciada. A capacidade vizinha, Autorização, virou mais quatro processos: protocolo, decisão de autorização, notificação e auditoria. Ao final, eram onze processos, cada um com seu próprio repositório e pipeline de implantação — mas mantidos por uma única equipe.

## Sintomas

Adicionar uma nova regra de autorização exigia alterar contratos de quatro processos e implantar seis deles na mesma janela. Vínculo, vigência e categoria de plano nunca eram escalados separadamente — sempre recebiam a mesma carga, porque sempre respondiam à mesma pergunta de negócio. Em incidentes, a equipe precisava correlacionar logs de vários processos só para descobrir que um campo tinha mudado de significado em algum deles. Uma tela de atendimento fazia oito chamadas sequenciais e mostrava um erro genérico sempre que qualquer uma delas atrasava.

Havia muitos contêineres, mas pouca autonomia real. O desenho tinha as quatro formas de acoplamento que você viu em [conceitos](conceitos.md#acoplamento): de implantação (mudar uma regra exigia publicar várias unidades juntas), temporal (a tela dependia de oito respostas síncronas), de contrato (cada processo expunha uma fatia do mesmo assunto) e organizacional (a mesma equipe negociava consigo mesma sem parar). A separação física — vários processos, vários deploys — tinha acontecido antes de existir uma separação semântica estável.

## Diagnóstico por capacidades

A equipe mapeou linguagem, regras, mudanças conjuntas e propriedade dos dados de cada processo. Vínculo, vigência, categoria de plano e regra contratual sempre participavam da mesma decisão — "este beneficiário está elegível?" — e mudavam sob as mesmas políticas: esse conjunto formava, na prática, um único bounded context, o mesmo **Elegibilidade** que você já conhece. Protocolo e decisão de autorização formavam outro bounded context, **Autorização**. Auditoria recebia fatos dos dois, mas não deveria controlar o fluxo principal de nenhum deles.

Esse mapa não obrigava a manter três (ou onze) processos separados. Ele apenas mostrava três fronteiras lógicas. A partir daí, a equipe comparou alternativas:

- manter os onze processos e investir em mais automação de implantação não corrigiria a fronteira incoerente — só tornaria mais barato operar um desenho errado;
- reunir tudo em um único processo reduziria a rede, mas misturaria autoridades que deveriam ficar separadas (Elegibilidade decidindo por Autorização, por exemplo);
- consolidar os processos que sempre mudavam juntos em um **macrosserviço** — uma unidade implantável que ainda agrupa mais de uma capacidade, mas já é um processo próprio, com módulos internos — preservaria os limites lógicos e reduziria a coordenação entre times;
- extrair Auditoria de forma assíncrona (por eventos) poderia isolar uma carga com comportamento bem diferente do restante, sem afetar o caminho síncrono de decisão.

## Decisão

A equipe consolidou vínculo, vigência, categoria de plano e regra contratual num único macrosserviço, chamado Elegibilidade. Internamente, módulos e testes de arquitetura (equivalentes ao ArchUnit ou ao Spring Modulith mencionados em [conceitos](conceitos.md#equivalencias-em-java-e-net)) impediram que um módulo acessasse diretamente as tabelas de outro. O banco permaneceu sob uma única credencial do macrosserviço, com schemas internos definidos pela própria equipe. Autorização continuou como outro processo, consumindo Elegibilidade por uma API documentada — nunca acessando essas tabelas diretamente.

Auditoria passou a receber eventos, mas só depois que a equipe definiu identificador de negócio, prazo de retenção e o que fazer com uma mensagem repetida. A mudança não foi feita para "usar eventos" — foi feita para que uma indisponibilidade do lado analítico não bloqueasse o atendimento ao paciente. O fluxo que precisava de decisão imediata (a própria autorização) continuou síncrono.

## Consequências observadas

O número de implantações coordenadas caiu, porque mudanças que sempre andavam juntas voltaram a viver na mesma unidade. A latência percebida também caiu, porque várias chamadas de rede internas viraram chamadas de função dentro do mesmo processo. Por outro lado, o impacto de uma implantação do macrosserviço Elegibilidade cresceu — uma falha ali agora afeta vínculo, vigência, categoria de plano e regra contratual ao mesmo tempo. Por isso, testes, liberação gradual e plano de rollback passaram a receber mais atenção.

A equipe não declarou sucesso pelo número de serviços que existiam antes e depois. Ela acompanhou: a frequência de implantação independente de cada unidade, o tempo médio para diagnosticar um incidente, a taxa de erro nas chamadas entre Elegibilidade e Autorização, e quantas mudanças ainda atravessavam a fronteira entre as duas.

## Discussão de consistência

Antes da consolidação, processos diferentes escreviam pedaços de estado que, juntos, deveriam formar uma única decisão de elegibilidade — mas não havia transação nem compensação entre eles. Uma falha no meio do caminho deixava registros contraditórios. A equipe cogitou introduzir uma **SAGA** (a coordenação de transações locais com compensação que você viu em [padrões e decisões](padroes-e-decisoes.md)), mas primeiro perguntou se a distribuição continuava sendo necessária. Ao reunir as regras fortemente relacionadas num único macrosserviço, ela conseguiu manter consistência local, numa única transação de banco — e não precisou mais de SAGA para decidir elegibilidade.

Para o fluxo que restou entre Elegibilidade e Autorização, a chamada síncrona continuou sendo uma escolha deliberada: nenhuma autorização é registrada sem uma resposta válida de Elegibilidade.

Um painel gerencial também precisava cruzar autorizações com dados agregados de várias fontes. Em vez de consultar diretamente os bancos operacionais, ele passou a receber uma projeção própria, atualizada por eventos — a mesma ideia de **CQRS** (separar o modelo de leitura do modelo de escrita) que você viu em [padrões e decisões](padroes-e-decisoes.md), aplicada só onde a necessidade existia. O painel passou a mostrar, de forma explícita, a defasagem dessa projeção. A equipe não separou leitura e escrita do resto do sistema — só desse painel.

## Evidência para revisar a decisão

A consolidação deveria ser revista se equipes diferentes passassem a ser donas de partes do macrosserviço, se uma das regras precisasse de um ciclo de implantação isolado, se as cargas de vínculo/vigência e de regra contratual divergissem de forma relevante, ou se a unidade voltasse a impedir entregas independentes. Também deveria ser revista se a projeção do painel gerencial parasse de atender ao prazo que o negócio precisa. Uma boa decisão arquitetural carrega dentro de si os sinais que a tornariam obsoleta.

O caso ensina que consolidar não é fracassar, e distribuir não é modernizar. O objetivo é sempre alinhar coesão do código, propriedade dos dados, padrão de comunicação e desenho das equipes. Um macrosserviço pode ser uma etapa estável ou um estágio de transição; um monólito modular pode ser o destino certo; microsserviços continuam fazendo sentido em fronteiras específicas — como Elegibilidade e Exames continuam sendo dois processos no exemplo deste módulo, porque ali a autonomia observada compensa o custo de rede.

## Netflix e Uber como consequências, não como receitas

Relatos públicos sobre a Netflix costumam destacar a escala de entrega e a necessidade de isolar mudanças e falhas entre muitas equipes. Relatos sobre a Uber mostram como diferentes domínios, volumes e operações geográficas podem justificar fronteiras bem mais granulares. Nenhum dos dois casos é um argumento para copiar a topologia de um fornecedor: são empresas com histórico, equipes, dados e obrigações operacionais muito diferentes dos de um hospital.

Use os dois casos como perguntas de consequência, não como modelo a copiar: que carga precisa escalar separadamente? Que falha precisa ficar contida sem derrubar o resto? Qual contrato precisa continuar estável durante uma migração? E, sobretudo, como a equipe volta atrás se a fronteira escolhida não entregar a autonomia prometida? Uma extração reversível começa por módulos, contratos, telemetria e dados com dono definido; um **padrão de estrangulamento** (migrar uma rota de cada vez para o novo desenho, mantendo a rota antiga viva até a troca ser segura) só funciona se existir uma fonte de verdade única e um plano para desligar o caminho antigo.

## Perguntas para revisar o caso

Responda antes de seguir para os exercícios do módulo:

1. Qual das quatro formas de acoplamento (implantação, temporal, contrato, organizacional) você acha que mais atrasava a equipe no dia a dia, e por quê?
2. O mapa de capacidades encontrou três bounded contexts (Elegibilidade, Autorização, Auditoria) dentro de onze processos. O que, no texto, permitiu à equipe enxergar esses três limites em vez de simplesmente contar processos?
3. Por que consolidar vínculo, vigência, categoria de plano e regra contratual num único macrosserviço não é o mesmo que reunir Elegibilidade, Autorização e Auditoria inteiras num único processo?
4. A equipe só introduziu eventos para Auditoria depois de definir identificador, retenção e comportamento de repetição. O que aconteceria se ela tivesse introduzido mensageria sem essas três decisões?
5. Escolha um dos quatro sinais de revisão listados no final do caso. Que dado, especificamente, a equipe precisaria observar para saber que esse sinal apareceu?

## Equivalências em Java e .NET

Uma consolidação em Java pode usar módulos Maven ou Gradle, pacotes organizados por domínio e ArchUnit para impedir referências proibidas entre eles; Spring Modulith acrescenta verificação de módulos e eventos internos. Em .NET, projetos separados por módulo, modificadores de visibilidade e testes de dependência cumprem um papel semelhante.

Em ambos os ecossistemas, a consolidação precisa preservar os contratos externos durante a migração. Um roteador pode encaminhar chamadas antigas para o novo macrosserviço enquanto os consumidores são atualizados aos poucos. O padrão de estrangulamento é uma estratégia de transição — não uma razão para manter duas fontes de verdade funcionando indefinidamente.
