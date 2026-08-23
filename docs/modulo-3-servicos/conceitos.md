# Conceitos: do negócio à fronteira

Dividir um sistema é escolher o que deve permanecer junto e o que pode evoluir separadamente. Pastas, classes e contêineres são mecanismos; a justificativa vem do domínio e dos atributos de qualidade.

## Capacidade de negócio

Uma **capacidade de negócio** descreve algo que a organização sabe fazer para produzir um resultado, independentemente da tela ou tecnologia atual. “Verificar elegibilidade”, “agendar atendimento” e “solicitar exame” são capacidades. “Salvar no PostgreSQL” e “enviar JSON” são mecanismos técnicos.

Capacidades ajudam a evitar serviços recortados por camadas como “serviço de controladores” ou “serviço de banco”. Um recorte útil reúne comportamento, regras e informação necessários a um resultado. O nome costuma ser estável mesmo quando o processo muda. Ainda assim, um mapa de capacidades é uma lente estratégica, não um gerador automático de executáveis. Uma capacidade ampla pode conter vários contextos; várias capacidades pequenas podem coexistir no mesmo contexto.

No caso hospitalar, elegibilidade interpreta vínculo, vigência e regras da operadora. Exames conhece códigos, solicitações e estados do fluxo clínico. O segundo precisa da resposta do primeiro, mas não precisa conhecer tabelas, algoritmos ou documentos internos usados para produzi-la.

## Bounded context

Em Domain-Driven Design, um **bounded context** delimita onde um modelo e sua linguagem possuem significado consistente. A palavra “situação” pode significar vigência cadastral em Elegibilidade e etapa operacional em Exames. Dentro de cada contexto, termos, invariantes e responsáveis devem ser claros. Entre contextos, existe tradução explícita.

Bounded context não é sinônimo de microsserviço. Ele é primeiro uma fronteira semântica. Pode ser implementado como módulo em um monólito, como parte coesa de um macrosserviço ou como serviço implantável. Confundir modelo lógico com topologia física leva a centenas de processos antes de existir necessidade operacional.

Um bom limite permite responder:

- qual resultado é produzido e para quem;
- quais regras devem permanecer verdadeiras;
- quem pode alterar os dados autoritativos;
- qual contrato é oferecido a consumidores;
- quais mudanças deveriam ocorrer sem coordenação externa.

![Três capacidades de negócio — Elegibilidade, Exames e Agendamento — cada uma com seu próprio vocabulário, regras e dados autoritativos; setas de tradução intencional ligam os contextos, nunca tabelas compartilhadas.](../assets/images/m03-capacidades-contextos.png)

*Figura 1 — De capacidades de negócio a bounded contexts. Fonte: curso.*

**Leitura textual da figura:** Elegibilidade, Exames e Agendamento são capacidades de negócio, cada uma resumida por seu vocabulário central (vínculo/vigência/regras; solicitação/códigos/estados; horários/profissionais/confirmação). Cada uma também é um bounded context: vocabulário próprio, regras próprias e dados autoritativos próprios. Entre contextos vizinhos existe apenas tradução intencional, nunca uma tabela compartilhada. Na base, a figura reforça que capacidade de negócio não é tecnologia: JSON, PostgreSQL e um controller são mecanismos, não o resultado que a organização entrega.

## Coesão

**Coesão** é o grau em que elementos de uma unidade contribuem para uma responsabilidade relacionada. Regras que mudam pelo mesmo motivo tendem a ficar juntas. Em Elegibilidade, calcular vigência e interpretar categoria do plano possuem alta coesão. Colocar ali o preparo de uma amostra laboratorial mistura razões de mudança.

Alta coesão reduz a quantidade de contexto mental para alterar uma regra e favorece testes significativos. Ela não significa unidade minúscula. Fragmentar cada função em um processo pode reduzir a coesão do fluxo de negócio: uma alteração simples passa a exigir contratos, implantações e diagnósticos coordenados.

Heurísticas úteis incluem observar vocabulário compartilhado, invariantes transacionais, histórico de mudanças, propriedade da equipe e necessidade de escalar. Nenhuma heurística decide sozinha. O histórico pode refletir uma organização antiga; uma transação pode ser redesenhada; uma equipe pode mudar.

## Acoplamento

**Acoplamento** é a dependência entre unidades. Ele não desaparece quando trocamos uma chamada de função por HTTP. Apenas muda de forma. Alguns tipos importantes são:

- **de contrato:** consumidor depende de campos, semântica e códigos de resposta;
- **temporal:** consumidor precisa que o provedor esteja disponível agora;
- **de dados:** duas unidades dependem da mesma estrutura ou alteram a mesma informação;
- **de implantação:** uma mudança exige publicar várias unidades em conjunto;
- **organizacional:** equipes precisam negociar continuamente para entregar uma capacidade.

Uma dependência explícita e estável pode ser saudável. O problema é o acoplamento que impede evolução ou torna falhas imprevisíveis. No laboratório, Exames aceita acoplamento temporal com Elegibilidade: a solicitação espera uma resposta síncrona. Em compensação, evita acoplamento de dados: Exames não lê a tabela do outro serviço.

![À esquerda, três regras de Elegibilidade (vigência, plano, regras) com alta coesão porque mudam pelo mesmo motivo. À direita, Exames com quatro setas de acoplamento — contrato, temporal, dados e implantação — apontando para Elegibilidade.](../assets/images/m03-coesao-acoplamento.png)

*Figura 2 — Coesão dentro de uma capacidade, acoplamento entre capacidades. Fonte: curso.*

**Leitura textual da figura:** dentro de Elegibilidade, vigência, plano e regras têm alta coesão porque mudam pelo mesmo motivo. Entre Exames e Elegibilidade existem quatro formas de acoplamento — de contrato, temporal, de dados e de implantação —, cada uma representada por uma seta própria. A figura fecha com um espectro entre "coeso" e "fragmentado": uma dependência explícita e estável pode ser saudável; o risco cresce quando o desenho se aproxima do extremo fragmentado, com muitos processos pequenos dependendo uns dos outros.

## Fronteira lógica e fronteira física

Uma fronteira lógica controla referências, linguagem e propriedade. Uma fronteira física acrescenta processo, rede, implantação e falha independentes. A progressão mais segura costuma ser:

![Quatro passos: regras misturadas viram módulos com interfaces, depois dados com proprietário definido; só então uma decisão pergunta se autonomia física é necessária, levando a manter implantação conjunta ou extrair processo e contrato remoto.](../assets/images/m03-fronteira-logica-fisica.png)

*Figura 3 — Da fronteira lógica à fronteira física. Fonte: curso.*

**Leitura textual da figura:** regras misturadas (1) são separadas em módulos com interfaces (2), cujos dados recebem um proprietário definido (3). Só depois disso a figura chega a uma decisão — "autonomia física é necessária?" — que, se não, mantém a implantação conjunta, e, se sim, extrai um processo próprio com contrato remoto (API) entre serviço e serviço, cada um com seu próprio banco. A frase final resume o critério: a extração física só vale quando sua autonomia paga o custo operacional.

Extrair cedo demais adiciona latência, serialização, autenticação entre serviços, descoberta, telemetria e recuperação. Extrair tarde demais pode manter equipes e ciclos de entrega presos. A arquitetura evolutiva mantém opções: módulos com APIs internas e testes de fronteira tornam uma futura extração menos traumática.

## Serviço e microsserviço

“Serviço” é uma unidade que oferece capacidades por um contrato. Pode viver no mesmo processo ou em outro. Um **microsserviço** é uma unidade implantável de maneira independente, alinhada a uma responsabilidade de negócio e dona de seu estado. “Micro” não fornece um limite de linhas ou pessoas. O sinal relevante é autonomia com coesão, não tamanho arbitrário.

Independência é uma propriedade exigente. Se toda alteração requer publicação coordenada, se vários serviços escrevem o mesmo banco ou se um fluxo só funciona quando dez respostas chegam, a topologia é distribuída, mas a autonomia é baixa. Equipes podem acabar com um monólito distribuído: custos remotos sem benefícios de isolamento.

## Propriedade dos dados

Propriedade responde quem é autoridade para interpretar e alterar uma informação. **Banco por serviço** significa que somente o serviço proprietário acessa diretamente seu armazenamento. Consumidores usam contratos, eventos ou réplicas explicitamente projetadas. Não significa obrigatoriamente um servidor físico para cada processo. Bancos, schemas ou credenciais podem oferecer graus diferentes de isolamento.

![Elegibilidade e Exames, cada um com seu contrato de API e seu banco protegido por um cadeado; uma seta tracejada de acesso direto entre os bancos aparece bloqueada.](../assets/images/m03-propriedade-dados.png)

*Figura 4 — Fronteiras, contratos e dados. Fonte: curso.*

**Leitura textual da figura:** Elegibilidade e Exames são capacidades distintas da plataforma hospitalar. Cada uma oferece um contrato de API e mantém seu próprio banco protegido; a seta tracejada que ligaria diretamente os dois bancos aparece bloqueada, porque o acesso direto violaria a propriedade dos dados. A única interação permitida passa pelo contrato HTTP ou por evento. Quando uma leitura precisa cruzar as duas capacidades, as opções listadas são composição por API, eventos, réplica analítica ou um modelo de leitura próprio — nunca uma consulta direta ao banco alheio. A frase final resume a regra: cada serviço é autoridade sobre a informação que interpreta e altera.

No laboratório, dois PostgreSQL deixam a regra visível: a credencial de Exames conhece apenas o banco `exames`; Elegibilidade conhece apenas `elegibilidade`. Cada banco fica em uma rede interna própria; ambos os processos compartilham somente a rede de aplicação necessária ao HTTP. Portanto, mesmo que Exames descubra o alias `elegibilidade-db`, ele não consegue resolvê-lo pela sua rede. Em ambientes maiores, isolamento lógico no mesmo cluster pode equilibrar custo e proteção, desde que permissões e responsabilidade sejam reais.

Compartilhar uma tabela parece conveniente para relatórios e transações, porém cria contrato implícito. Uma alteração de coluna pode quebrar consumidores desconhecidos; uma escrita externa pode violar invariantes; o proprietário deixa de controlar evolução. Para leitura integrada, avalie composição por API, eventos, réplica analítica ou modelo de leitura, sempre deixando defasagem e origem explícitas.

## Persistência como decisão de fronteira

**Persistência poliglota** significa escolher mecanismos de armazenamento diferentes quando a forma do dado e seus acessos justificam isso: por exemplo, uma base relacional para regras transacionais, uma busca para documentos e uma série temporal para medições. Não significa dar um banco novo a cada serviço nem trocar de tecnologia por prestígio. Cada mecanismo acrescenta backup, segurança, observabilidade, migração e competência operacional.

Comece pela autoridade e pelo contrato: quem escreve, quais invariantes precisam de transação e quais leituras podem ser projetadas. No exemplo, os dois PostgreSQL não demonstram poliglotismo; demonstram propriedade de dados. A decisão de persistência só muda quando as forças do domínio e da operação pagam o seu custo.

## Chamadas síncronas e falhas parciais

Em uma chamada síncrona, o consumidor espera a resposta. É simples para fluxos que precisam de decisão imediata e oferece um caminho de erro direto. O custo é acoplamento temporal: a disponibilidade percebida por Exames depende de sua própria aplicação, seu banco, a rede, Elegibilidade e o banco de Elegibilidade.

Uma **falha parcial** ocorre quando uma parte distribuída funciona e outra não. Exames pode estar saudável para consultar seu banco enquanto não consegue aceitar nova solicitação porque Elegibilidade parou. Retornar `503 Service Unavailable` com `dependencia_indisponivel` torna essa condição observável. Devolver `500` genérico ou registrar como se a solicitação tivesse sido concluída esconderia a semântica.

Timeouts limitam espera; repetição pode ajudar falhas transitórias, mas amplia carga e exige idempotência; circuit breaker interrompe tentativas quando a dependência está instável; fallback precisa ser válido para o negócio, não apenas tecnicamente conveniente. No exemplo clínico, presumir elegibilidade positiva seria perigoso. Falhar de forma explícita é a decisão didática.
