# Conceitos

Dividir um sistema é escolher o que deve permanecer junto e o que pode evoluir separadamente. Pastas, classes e contêineres são mecanismos de implementação, enquanto a justificativa de uma fronteira vem do domínio e dos atributos de qualidade exigidos pelo negócio.

## Capacidade de negócio

Uma **capacidade de negócio** descreve algo que a organização sabe fazer para produzir um resultado, independentemente da tela ou da tecnologia usada hoje. “Verificar elegibilidade”, “agendar atendimento” e “solicitar exame” são capacidades do caso hospitalar. “Salvar no PostgreSQL” e “enviar JSON” são mecanismos técnicos e não descrevem nenhum resultado para o negócio.

As capacidades ajudam a evitar serviços recortados por camadas técnicas, como um serviço só de controladores ou um serviço só de acesso a banco. Um recorte útil reúne o comportamento, as regras e a informação necessários a um resultado, com um nome que costuma permanecer estável mesmo quando o processo muda. Ainda assim, um mapa de capacidades serve à análise estratégica e não define quais executáveis devem existir. Uma capacidade ampla pode conter vários contextos, assim como várias capacidades pequenas podem coexistir num mesmo contexto.

No caso hospitalar, Elegibilidade interpreta vínculo, vigência e regras da operadora. Exames conhece códigos, solicitações e estados do fluxo clínico. O segundo precisa da resposta do primeiro e não precisa conhecer as tabelas, os algoritmos ou os documentos internos usados para produzi-la.

## Bounded context

Em *Domain-Driven Design*, abordagem de modelagem proposta por Eric Evans, um ***bounded context*** delimita a parte do sistema em que um modelo e a sua linguagem possuem significado consistente. A palavra “situação” pode significar vigência cadastral em Elegibilidade e etapa operacional em Exames. Dentro de cada contexto, os termos, as invariantes e os responsáveis precisam ser claros. A passagem de um contexto para outro exige tradução explícita entre os dois modelos.

Um *bounded context* não é sinônimo de microsserviço, porque ele é antes de tudo uma fronteira semântica. Ele pode ser implementado como módulo de um monólito, como parte coesa de um macrosserviço ou como serviço implantável. Confundir o modelo lógico com a topologia física leva equipes a criar centenas de processos antes de existir necessidade operacional para eles.

Um bom limite permite responder às perguntas da lista abaixo sem consultar outra equipe.

- Qual resultado é produzido e para quem.
- Quais regras devem permanecer verdadeiras.
- Quem pode alterar os dados autoritativos.
- Qual contrato é oferecido aos consumidores.
- Quais mudanças deveriam ocorrer sem coordenação externa.

![Elegibilidade, Exames e Agendamento como capacidades de negócio com vocabulário, regras e dados autoritativos próprios. Setas de tradução intencional ligam os contextos sem tabelas compartilhadas.](../assets/images/m03-capacidades-contextos.png)

*Figura 1 — De capacidades de negócio a bounded contexts. Fonte: curso.*

**Leitura textual da figura:** Elegibilidade, Exames e Agendamento são capacidades de negócio representadas pelo seu vocabulário central. Elegibilidade trata de vínculo e vigência do plano segundo as regras da operadora, enquanto Exames trata de solicitações, códigos e estados do fluxo clínico. Agendamento trata de horários e profissionais disponíveis e da confirmação do atendimento ao paciente. Cada capacidade também é um *bounded context* com vocabulário, regras e dados autoritativos próprios, ligado aos vizinhos apenas por tradução intencional e sem tabela compartilhada. Na base, a figura registra que JSON, PostgreSQL e um *controller* são mecanismos técnicos que não constituem o resultado entregue pela organização.

## Coesão

**Coesão** é o grau em que os elementos de uma unidade contribuem para uma responsabilidade relacionada. Regras que mudam pelo mesmo motivo tendem a ficar juntas, como o cálculo de vigência e a interpretação da categoria do plano em Elegibilidade. Colocar nesse mesmo serviço o preparo de uma amostra laboratorial misturaria razões de mudança diferentes.

A alta coesão reduz a quantidade de contexto que uma pessoa precisa conhecer para alterar uma regra e favorece testes significativos. Ela não significa unidade minúscula, porque fragmentar cada função num processo próprio reduz a coesão do fluxo de negócio. Nesse cenário, uma alteração simples passa a exigir contratos, implantações e diagnósticos coordenados entre vários serviços.

As heurísticas úteis incluem o vocabulário compartilhado, as invariantes transacionais e o histórico de mudanças, além da propriedade da equipe e da necessidade de escalar. Nenhuma heurística decide sozinha, porque o histórico pode refletir uma organização antiga, uma transação pode ser redesenhada e a propriedade de uma equipe muda quando a organização se reestrutura.

## Acoplamento

**Acoplamento** é a dependência entre unidades de software. Ele não desaparece quando uma chamada de função é substituída por uma chamada HTTP, porque o acoplamento muda de forma e continua existindo.

- O **acoplamento de contrato** existe quando o consumidor depende dos campos, da semântica e dos códigos de resposta do provedor.
- O **acoplamento temporal** existe quando o consumidor precisa que o provedor esteja disponível no momento da chamada.
- O **acoplamento de dados** existe quando duas unidades dependem da mesma estrutura ou alteram a mesma informação.
- O **acoplamento de implantação** existe quando uma mudança exige publicar várias unidades em conjunto.
- O **acoplamento organizacional** existe quando equipes precisam negociar continuamente para entregar uma capacidade.

Uma dependência explícita e estável pode ser saudável. O problema é o acoplamento que impede a evolução das unidades ou torna as falhas imprevisíveis. No laboratório, Exames aceita acoplamento temporal com Elegibilidade, porque a solicitação espera uma resposta síncrona antes de ser gravada. Em compensação, Exames evita o acoplamento de dados, porque não lê a tabela do outro serviço.

![À esquerda, as regras de vigência, de plano e de operadora de Elegibilidade com alta coesão porque mudam pelo mesmo motivo. As quatro setas à direita partem de Exames e apontam para Elegibilidade, uma para cada forma de acoplamento descrita nesta seção.](../assets/images/m03-coesao-acoplamento.png)

*Figura 2 — Coesão dentro de uma capacidade e acoplamento entre capacidades. Fonte: curso.*

**Leitura textual da figura:** dentro de Elegibilidade, as regras de vigência e de plano têm alta coesão porque mudam pelo mesmo motivo. Entre Exames e Elegibilidade existem quatro setas, que representam o acoplamento de contrato e o temporal, além do acoplamento de dados e do de implantação. A figura termina com uma escala entre os extremos coeso e fragmentado. O risco cresce quando o desenho se aproxima do extremo fragmentado, em que muitos processos pequenos dependem uns dos outros.

## Fronteira lógica e fronteira física

Uma fronteira lógica controla as referências entre módulos, a linguagem de cada modelo e a propriedade dos dados. Uma fronteira física acrescenta a essas garantias um processo próprio, comunicação pela rede e implantação e falha independentes. A Figura 3 representa a progressão mais segura entre a fronteira lógica e a fronteira física de um serviço.

![A figura mostra quatro passos em que regras misturadas são separadas em módulos com interfaces e depois recebem dados com proprietário definido. Só então uma decisão pergunta se a autonomia física é necessária e leva a manter a implantação conjunta ou a extrair processo e contrato remoto.](../assets/images/m03-fronteira-logica-fisica.png)

*Figura 3 — Da fronteira lógica à fronteira física. Fonte: curso.*

**Leitura textual da figura:** as regras misturadas do primeiro passo são separadas em módulos com interfaces no segundo passo. Os dados desses módulos recebem um proprietário definido no terceiro passo. Só depois a figura chega à decisão sobre a necessidade de autonomia física. Se a resposta é negativa, a implantação conjunta é mantida. Se a resposta é positiva, um processo próprio é extraído com contrato remoto entre os serviços, cada um com o próprio banco. A frase final registra o critério de que a extração física só vale quando a autonomia obtida compensa o custo operacional.

Extrair um serviço cedo demais adiciona latência e serialização às chamadas entre módulos, além de exigir autenticação entre serviços, descoberta e telemetria. Extrair tarde demais pode manter equipes e ciclos de entrega presos uns aos outros. A arquitetura evolutiva preserva as duas opções com módulos que expõem APIs internas e testes de fronteira, o que torna uma extração futura menos custosa.

## Serviço e microsserviço

Um serviço é uma unidade que oferece capacidades por meio de um contrato e pode viver no mesmo processo do consumidor ou em outro processo. Um **microsserviço** é uma unidade implantável de maneira independente, alinhada a uma responsabilidade de negócio e dona do próprio estado. O prefixo “micro” não define limite de linhas de código ou de pessoas, porque o critério relevante é a autonomia combinada com coesão.

A independência é uma propriedade exigente. Quando cada alteração requer publicação coordenada, vários serviços escrevem no mesmo banco ou um fluxo só funciona quando dez respostas chegam, a topologia é distribuída e a autonomia é baixa. Equipes nessa situação chegam a um monólito distribuído, que acumula os custos da comunicação remota sem obter os benefícios do isolamento.

## Propriedade dos dados

A propriedade dos dados define quem é a autoridade para interpretar e alterar uma informação. **Banco por serviço** significa que somente o serviço proprietário acessa diretamente o seu armazenamento, enquanto os consumidores usam contratos, eventos ou réplicas projetadas para esse fim. O padrão não exige um servidor físico para cada processo, porque bancos, *schemas* ou credenciais separados oferecem graus diferentes de isolamento.

![Elegibilidade e Exames, cada um com seu contrato de API e seu banco protegido por um cadeado. Uma seta tracejada de acesso direto entre os bancos aparece bloqueada.](../assets/images/m03-propriedade-dados.png)

*Figura 4 — Fronteiras, contratos e dados. Fonte: curso.*

**Leitura textual da figura:** Elegibilidade e Exames são capacidades distintas da plataforma hospitalar. Cada uma oferece um contrato de API e mantém o próprio banco protegido. A seta tracejada que ligaria diretamente os dois bancos aparece bloqueada, porque o acesso direto violaria a propriedade dos dados. A única interação permitida passa pelo contrato HTTP ou por evento. Quando uma leitura precisa cruzar as duas capacidades, a figura lista como opções a composição por API e os eventos, além da réplica analítica e do modelo de leitura próprio. A frase final registra que cada serviço é autoridade sobre a informação que interpreta e altera.

No laboratório, dois PostgreSQL deixam a regra visível, porque a credencial de Exames conhece apenas o banco `exames` e a de Elegibilidade conhece apenas o banco `elegibilidade`. Cada banco fica numa rede interna própria, enquanto os dois processos compartilham somente a rede de aplicação necessária ao HTTP. Por isso, mesmo que Exames descubra o nome `elegibilidade-db`, ele não consegue resolvê-lo pela sua rede. Em ambientes maiores, o isolamento lógico no mesmo cluster equilibra custo e proteção quando as permissões e a responsabilidade são reais.

Compartilhar uma tabela parece conveniente para relatórios e transações e cria um contrato implícito entre os serviços. Uma alteração de coluna pode quebrar consumidores que o proprietário desconhece. Uma escrita externa pode violar invariantes que o proprietário deixou de controlar. Para a leitura integrada, a equipe avalia as alternativas descritas na Figura 4 e deixa explícitas a defasagem e a origem do dado.

## Persistência poliglota {#persistencia-como-decisao-de-fronteira}

**Persistência poliglota** significa escolher mecanismos de armazenamento diferentes quando a forma do dado e os seus acessos justificam essa escolha. Um exemplo é usar uma base relacional para regras transacionais, um mecanismo de busca para documentos e uma série temporal para medições. O conceito não significa dar um banco novo a cada serviço nem trocar de tecnologia por prestígio. Cada mecanismo adicional exige *backup* e segurança próprios, além de observabilidade, migrações e competência operacional da equipe.

A análise começa pela autoridade e pelo contrato, com as perguntas sobre quem escreve, quais invariantes precisam de transação e quais leituras podem ser projetadas. No exemplo, os dois PostgreSQL não demonstram poliglotismo e sim propriedade de dados. A decisão de persistência só muda quando as forças do domínio e da operação justificam o custo de um mecanismo adicional.

## Chamadas síncronas e falhas parciais

Numa chamada síncrona, o consumidor espera a resposta antes de continuar. O modelo é simples para fluxos que precisam de decisão imediata e oferece um caminho de erro direto ao consumidor. O custo é o acoplamento temporal, porque a disponibilidade percebida por Exames passa a depender da sua aplicação e do seu banco, da rede e também de Elegibilidade e do banco de Elegibilidade.

Uma **falha parcial** ocorre quando uma parte do sistema distribuído funciona e outra não. Exames pode estar saudável para consultar o próprio banco e incapaz de aceitar uma nova solicitação porque Elegibilidade parou. Retornar `503 Service Unavailable` com o código `dependencia_indisponivel` torna essa condição observável para o consumidor. Devolver um `500` genérico ou registrar a solicitação como concluída esconderia a semântica da falha.

O trecho abaixo é a saída do programa `demo_falha_parcial.py`, da pasta `codigo/oda-05` do [repositório das ODAs da disciplina](https://github.com/aulas-marco/odas-arquitetura-software), no momento em que Elegibilidade está fora do ar.

```text
Elegibilidade fora do ar
  GET /health        -> 200 {'status': 'ok', 'servico': 'exames'}
  POST /exames B-001 -> 503 {'codigo': 'dependencia_indisponivel'}
  solicitações gravadas em Exames: 1
```

O `GET /health` de Exames responde `200` porque o processo e o banco de Exames continuam saudáveis durante a parada de Elegibilidade. O `POST /exames` responde `503` porque a decisão de elegibilidade não está disponível. A contagem de solicitações gravadas permanece em 1, valor que corresponde a um pedido aceito antes da parada de Elegibilidade. O código completo e as outras situações da dependência estão na seção [Orçamento de falha das chamadas síncronas](padroes-e-decisoes.md#chamadas-sincronas-orcamento-de-falha). A [ODA 05](https://aulas-marco.github.io/odas-arquitetura-software/oda-05/) executa os mesmos programas num laboratório guiado.

O prazo de espera limita o tempo que o consumidor aguarda a resposta. A nova tentativa ajuda em falhas transitórias, embora aumente a carga sobre a dependência e exija idempotência da operação repetida. O disjuntor, conhecido como *circuit breaker*, interrompe as tentativas enquanto a dependência está instável. Uma resposta alternativa, chamada de *fallback*, precisa ser válida para o negócio além de conveniente para a técnica. No exemplo clínico, presumir elegibilidade positiva seria perigoso. Por isso, Exames falha de forma explícita com `503` e o código `dependencia_indisponivel`, que informa ao consumidor qual dependência está indisponível.
