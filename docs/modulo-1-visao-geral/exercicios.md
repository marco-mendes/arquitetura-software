# Exercícios por Taxonomia de Bloom

Responda antes de abrir “Ver resposta”. Nas atividades seguintes, siga o roteiro e justifique escolhas pelas mesmas forças e limites.

## Recordar

1\. O que diferencia um componente de um conector?

<details>
<summary>Ver resposta</summary>

Componente concentra responsabilidade; conector descreve colaboração, como chamada HTTP, mensagem ou acesso a dados.
</details>

2\. Quais são os quatro estilos aprofundados nesta unidade?

<details>
<summary>Ver resposta</summary>

Camadas, Pipes and Filters, Microkernel e Monólito modular.
</details>

3\. Qual nome recebe uma condição assumida como verdadeira, mas que ainda pode precisar de revisão?

<details>
<summary>Ver resposta</summary>

Premissa; uma restrição já limita alternativas conhecidas.
</details>

4\. Quais seis partes tornam um cenário de atributo de qualidade observável?

<details>
<summary>Ver resposta</summary>

Fonte, estímulo, ambiente, artefato, resposta e medida.
</details>

5\. Qual estilo organiza transformações independentes encadeadas por um fluxo de dados?

<details>
<summary>Ver resposta</summary>

Pipes and Filters: filtro transforma; pipe transporta a saída ou rejeição.
</details>

6\. O que um ADR registra além da alternativa escolhida?

<details>
<summary>Ver resposta</summary>

Contexto, forças, alternativas, consequências, evidências e gatilho de revisão.
</details>

## Compreender

1\. “A aplicação será executada em Python 3.12.” Isso descreve estilo, padrão ou tecnologia?

<details>
<summary>Ver resposta</summary>

Tecnologia; ela não define responsabilidades ou conectores.
</details>

2\. A frase “as regras de negócio não podem importar adaptadores de persistência” impõe uma direção permitida de dependência entre módulos. Que nome se dá a esse tipo de regra, e qual estilo — Camadas ou Hexagonal — foi pensado para sustentá-la e permitir testá-la automaticamente?

<details>
<summary>Ver resposta</summary>

É uma regra de dependência: módulos de mais alto nível (negócio) não podem depender de detalhes de baixo nível (persistência). Tanto Camadas quanto Hexagonal foram desenhados para sustentar essa direção e permitir verificá-la de forma automatizada.
</details>

3\. Por que MVC não é simplesmente outro nome para qualquer aplicação web?

<details>
<summary>Ver resposta</summary>

MVC organiza requisição-resposta em controller, model e view; não resolve por si só domínio, eventos ou implantação.
</details>

4\. Quando uma camada é chamada de fechada?

<details>
<summary>Ver resposta</summary>

Quando a interação atravessa a camada imediatamente abaixo, sem atalho.
</details>

5\. Um filtro sem estado trata cada item de forma independente. Um filtro com estado guarda informação de itens anteriores. Que problema esse segundo tipo introduz, que o primeiro não tem?

<details>
<summary>Ver resposta</summary>

Ele passa a depender do que aconteceu antes, então é preciso declarar onde esse estado fica guardado, o que acontece se o processo reiniciar e como ele se comporta se dois itens chegarem ao mesmo tempo (concorrência).
</details>

6\. Por que um plugin que lê tabelas internas do núcleo não demonstra bem um microkernel?

<details>
<summary>Ver resposta</summary>

Porque depende de detalhes privados, aumenta acoplamento e incentiva core creep.
</details>

## Aplicar
### Recomendar um estilo para o motor de regras de reajuste

**Objetivo**

Recomendar um entre quatro estilos arquiteturais para um componente descrito, declarando o que cada um ganha, o que cobra e qual atributo de qualidade decide.

**Situação**

Uma operadora de saúde calcula o reajuste anual dos contratos coletivos. O cálculo aplica uma sequência de regras: índice legal do ano, faixa etária dos beneficiários, sinistralidade do contrato, descontos negociados e arredondamento contratual. Hoje tudo isso vive num único método de 900 linhas, dentro do serviço que emite o boleto.

Quando a lei muda o índice, alguém edita esse método. Quando um cliente grande negocia um desconto diferente, alguém acrescenta um `if`. O time perdeu a conta de quantas regras existem, e ninguém consegue dizer, olhando um cálculo pronto, quais regras foram aplicadas e em que ordem.

A diretoria pediu uma recomendação de estrutura antes da próxima virada de índice.

Seis fatos foram apurados na operadora:

1. O índice legal muda uma vez por ano; descontos negociados mudam várias vezes por ano.
2. A equipe tem seis pessoas e faz uma implantação por semana, com tudo junto.
3. A auditoria exige saber, para cada cálculo já emitido, quais regras foram aplicadas e em que ordem.
4. O volume é de alguns milhares de cálculos por dia, sem pico previsto.
5. Acrescentar uma regra hoje exige alterar o método e reimplantar o sistema inteiro.
6. Ninguém pediu para trocar uma regra com o sistema no ar.

As quatro alternativas em avaliação:

| Alternativa | O que muda na estrutura |
| --- | --- |
| **A. Camadas** | O cálculo vira um serviço de domínio na camada de negócio, chamado pela camada de aplicação. Uma classe por grupo de regras, todas dentro do mesmo serviço. |
| **B. Pipes and Filters** | Cada regra vira um filtro independente. O cálculo é a passagem do contrato por uma sequência de filtros, e cada filtro registra o que alterou. |
| **C. Microkernel** | Um núcleo estável executa o cálculo e consulta um registro de regras. Cada regra é um plugin que se declara ao núcleo por um contrato fixo. |
| **D. Monólito modular** | O motor de regras vira um módulo com fronteira verificada na esteira de integração, dentro da mesma implantação, com interface própria. |

**Seu papel**

Você é a pessoa arquiteta chamada para recomendar a estrutura. A equipe implementa depois, e espera de você a escolha, a justificativa e os riscos.

**O que fazer**

Escreva em texto corrido, uma resposta por item. Não é preciso desenhar nada.

1. Recomende um dos quatro estilos para a operadora, em uma frase.
2. Sobre cada um dos quatro, escreva duas frases: o que ele resolve do problema descrito e o que ele cobra em troca.
3. Diga qual dos seis fatos pesou mais na sua recomendação, e por quê.
4. Aponte o estilo que você descartaria de imediato e diga qual fato o derruba.
5. Escreva o que pode dar errado com a sua recomendação e o sinal que faria a operadora trocar de estilo. Data no calendário não vale como sinal.

**Evidência esperada**

O artefato traz o quadro comparativo completo, com ganho e custo declarados para os quatro estilos, a recomendação em uma frase, o cenário de qualidade com medida, o fato que sustenta a escolha, o risco aceito e o sinal de revisão como condição observável.

## Analisar
**Objetivo**

Decompor as forças de uma integração antes de comparar estruturas, e dizer o que cada estrutura resolve e o que ela cobra.

**Situação**

Uma rede de laboratórios recebe resultados de dezoito parceiros numa central. Cada parceiro envia no formato que já usa: uns mandam JSON, outros CSV, outros XML. São quatro milhões de registros por dia, com pico de seiscentos por segundo no fim da tarde, quando os laboratórios fecham o expediente.

O mesmo registro às vezes chega duas vezes, e às vezes chega horas atrasado. Os parceiros mudam o layout do arquivo cerca de uma vez por mês, quase sempre sem avisar antes.

Quando a central rejeita um registro, ela precisa dizer de qual parceiro veio, em que versão de layout, qual transformação falhou e por quê. Um lote precisa ser aceito em até vinte minutos.

Hoje tudo isso acontece num programa único que ninguém quer mais tocar.

Os seis fatos, as quatro estruturas e as exigências de rejeição e de prazo, todos descritos nesta página.

**Seu papel**

Você conduz a análise antes de qualquer decisão de estrutura. Separar o que é fato do que é suposição sua faz parte do trabalho.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Das seis exigências apuradas, escolha as três que mais restringem a estrutura e explique, em uma frase cada, por que restringem.
2. Sobre cada uma das quatro estruturas, escreva duas frases: o que ela resolve e o que ela cobra em troca.
3. A exigência 5 pede rastrear parceiro, versão, transformação e motivo em cada rejeição. Diga qual das quatro estruturas torna isso mais barato, e por quê.
4. Aponte a estrutura que você descartaria de imediato e diga qual fato a derruba.
5. Escreva uma afirmação sua que os seis fatos não sustentam, rotule-a como suposição e diga que dado a confirmaria. Se faltar algum dado que você considera necessário para julgar, escreva a pergunta que faria à central antes de fechar a análise.

**Evidência esperada**

O arquivo entregue liga cada exigência escolhida a uma consequência de estrutura, traz ganho e custo das quatro estruturas, e separa o que foi apurado do que você supôs, registrando o dado que confirmaria a suposição.

## Avaliar
**Objetivo**

Julgar duas propostas concorrentes com critérios declarados antes da escolha, dizendo o que a evidência disponível sustenta e o que ela não alcança.

**Situação**

Uma secretaria estadual consolida a disponibilidade de leitos de 45 hospitais num painel público. Alguns hospitais enviam JSON a cada trinta segundos; outros enviam CSV a cada cinco minutos. No horário de maior movimento chegam novecentas atualizações por minuto.

Os dados brigam entre si. O mesmo hospital às vezes manda a mesma atualização duas vezes, às vezes manda com atraso, e às vezes duas fontes do mesmo hospital discordam sobre quantos leitos estão livres. O painel precisa refletir a realidade em até sessenta segundos, e a auditoria precisa saber, para cada número exibido, de qual fonte ele veio, em que versão, que transformação sofreu e como o desempate foi feito.

Duas equipes apresentaram propostas.

#### Proposta A

Um caminho comum para todos os hospitais, com conectores finos na entrada e um modelo de dados único no meio. Toda regra de desempate vive num lugar só.

#### Proposta B

Um coletor por hospital, cada um com a própria regra de leitura e de desempate, gravando num repositório comum já no formato final.

As duas propostas, a amostra descrita e a lista do que foi medido e do que não foi, todos nesta página.

**Seu papel**

Você emite o parecer que o comitê vai ler. Pode aprovar uma proposta, recusar as duas ou adiar com uma condição escrita.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Declare de três a cinco critérios de julgamento e diga qual deles pesa mais para uma secretaria de saúde. Justifique o peso pelo risco de errar, e não por gosto técnico.
2. Avalie as duas propostas contra os seus critérios, um parágrafo por proposta, dizendo o que cada uma protege e o que ela expõe.
3. Para cada critério, diga se a evidência disponível permite julgar ou se falta medida. Quando faltar, nomeie a medida que falta.
4. Emita o parecer: aprovar uma, recusar as duas ou adiar. Se adiar, escreva a condição concreta que encerraria a espera.
5. Escreva a objeção mais forte contra o seu próprio parecer, e responda a ela.

**Evidência esperada**

O parecer traz critérios escritos antes da escolha, as duas propostas julgadas contra eles, a separação explícita entre o que a amostra sustenta e o que ninguém mediu, e uma objeção ao próprio parecer com resposta.

## Criar
**Objetivo**

Propor a estrutura inicial de uma plataforma nova, escolhendo entre três esboços e deixando registrado o que fica de fora por enquanto.

**Situação**

Um hospital de médio porte vai construir uma plataforma digital do zero. Na primeira fase, três coisas precisam funcionar: cadastrar o paciente, marcar um procedimento e emitir o comprovante que o paciente leva para casa.

O hospital tem seis pessoas na equipe de desenvolvimento, nenhuma com experiência em sistemas distribuídos. A diretoria quer a primeira versão no ar em quatro meses. O sistema atende cerca de duzentos atendimentos por dia, sem previsão de crescer nos próximos dois anos.

Duas coisas o hospital já sabe que vai querer depois, e não agora: integração com laboratórios externos e um aplicativo para o paciente.

As três funcionalidades da primeira fase, as restrições de equipe, prazo e volume, os dois planos futuros declarados e os três esboços, todos nesta página.

**Seu papel**

Você propõe a estrutura inicial. Outra equipe vai continuar o trabalho nos próximos meses, então a proposta precisa ser legível por quem não participou desta conversa.

**O que fazer**

Escreva em texto corrido, uma resposta por item.

1. Escolha um dos três esboços e defenda a escolha citando pelo menos duas restrições do hospital.
2. Sobre os dois esboços que você não escolheu, escreva duas frases cada: o que eles ganhariam e o que custariam a esta equipe, neste prazo.
3. Escreva um cenário de qualidade para a sua proposta, no formato estímulo, resposta esperada e medida. Um exemplo de forma, com números que não servem para este caso: "quando dez pessoas marcam ao mesmo tempo, a confirmação aparece em até dois segundos em nove de cada dez tentativas".
4. Diga o que fica explicitamente fora da primeira fase, e por quê.
5. Os dois planos futuros já são conhecidos. Escreva, para cada um, o sinal que indicaria que chegou a hora de mudar a estrutura escolhida.

**Evidência esperada**

O arquivo entregue traz o esboço escolhido com duas restrições citadas, os outros dois avaliados, um cenário de qualidade com medida observável, o escopo excluído com justificativa, e dois sinais de evolução ligados aos planos já conhecidos.

## Questões de múltipla escolha

As vinte questões a seguir formam a atividade de fixação da Unidade 1 no Canvas e cobrem o conteúdo das páginas deste módulo. Cada questão tem uma única alternativa correta e traz o nível de dificuldade entre colchetes: as simples verificam definições, as médias aplicam os conceitos a uma situação e as difíceis pedem análise de alternativas e consequências.

### Questões simples

#### Questão 1 [Simples]

O que define um estilo arquitetural?

- (a) Um conjunto de frameworks e linguagens recomendados para um tipo de sistema.
- (b) Uma forma conhecida de organizar elementos, conectores e restrições sobre o que pode depender de quê.
- (c) A sequência de etapas obrigatórias do processo de desenvolvimento de software.
- (d) O diagrama de implantação que mostra servidores, redes e bancos de dados.

#### Questão 2 [Simples]

Como se chama o anti-padrão do estilo em camadas em que a requisição atravessa as camadas sem que nenhuma delas decida, valide ou transforme algo?

- (a) Core creep.
- (b) Estado compartilhado invisível.
- (c) Sumidouro.
- (d) Monólito distribuído.

#### Questão 3 [Simples]

Entre os quatro tipos canônicos de filtro do estilo Pipes and Filters, qual avalia os dados contra um critério e descarta os que não passam?

- (a) Producer.
- (b) Transformer.
- (c) Consumer.
- (d) Tester.

#### Questão 4 [Simples]

No estilo Microkernel, o que caracteriza o anti-padrão core creep?

- (a) O núcleo acumula condicionais particulares e lógica que pertence aos plugins.
- (b) Os plugins passam a se comunicar diretamente entre si, sem o núcleo.
- (c) O registro de plugins exige reinicialização a cada alteração.
- (d) Um plugin é implantado como serviço externo na nuvem.

#### Questão 5 [Simples]

O que afirma a Lei de Conway, citada na discussão do estilo em camadas?

- (a) Sistemas tendem a aumentar sua complexidade a cada nova versão.
- (b) A latência de uma requisição cresce com o número de camadas atravessadas.
- (c) Organizações produzem arquiteturas que espelham sua estrutura de comunicação.
- (d) Toda decisão arquitetural deve ser registrada antes da implementação.

#### Questão 6 [Simples]

Qual é a diferença entre uma camada fechada e uma camada aberta?

- (a) A camada fechada não pode ser testada, e a camada aberta pode ser testada em isolamento.
- (b) A camada fechada obriga a passagem pela camada adjacente, e a camada aberta permite um atalho deliberado.
- (c) A camada fechada roda em servidor próprio, e a camada aberta roda no mesmo processo.
- (d) A camada fechada contém regras de negócio, e a camada aberta contém apenas infraestrutura.

#### Questão 7 [Simples]

Segundo a definição de Kamil Grzybek adotada no módulo, o que é um monólito?

- (a) Um sistema com exatamente uma unidade de implantação.
- (b) Um sistema escrito em uma única linguagem de programação.
- (c) Um sistema sem separação de camadas ou módulos.
- (d) Um sistema com um único banco de dados compartilhado por todas as equipes.

#### Questão 8 [Simples]

O que é um ADR (Architecture Decision Record)?

- (a) Um diagrama C4 de contexto que mostra o sistema e seus usuários.
- (b) Um relatório de testes de desempenho anexado a cada versão.
- (c) Uma lista de requisitos funcionais aprovada pelo cliente.
- (d) Um documento versionado com contexto, forças, alternativas, decisão, consequências, evidências e revisão.

### Questões médias

#### Questão 9 [Média]

Em uma API organizada em controller, serviço e repositório, cerca de 85% das requisições passam pelo serviço sem que ele valide, decida ou transforme qualquer dado. Segundo a regra prática de Richards e Ford, o que essa medição indica?

- (a) Que o estilo em camadas provavelmente não é o adequado para esse sistema.
- (b) Que o sistema precisa de mais uma camada para separar melhor as responsabilidades.
- (c) Que as camadas devem ser distribuídas em servidores separados para reduzir latência.
- (d) Que o repositório deve ser substituído por acesso direto ao banco no controller.

#### Questão 10 [Média]

O faturamento hospitalar precisa validar documentos, normalizar códigos, enriquecer os dados do convênio e publicar o resultado, registrando o lote, a etapa e a causa de cada rejeição. Qual estilo atende melhor essa necessidade?

- (a) Microkernel, com um plugin por convênio.
- (b) Pipes and Filters, com uma etapa por transformação.
- (c) Camadas, com uma camada por tipo de documento.
- (d) Monólito modular, com um módulo por etapa.

#### Questão 11 [Média]

Um sistema tributário calcula impostos com regras que variam por estado, mas o fluxo de cálculo é o mesmo. A equipe quer incluir um novo estado sem alterar o código central. Qual estilo atende esse requisito e como?

- (a) Camadas, acrescentando uma camada de regras para o novo estado.
- (b) Pipes and Filters, inserindo um filtro Tester por estado.
- (c) Monólito modular, criando um módulo que lê as tabelas do módulo fiscal.
- (d) Microkernel, registrando um novo plugin para o estado selecionado pelo núcleo.

#### Questão 12 [Média]

Em um monólito modular, o módulo Faturamento passou a consultar diretamente a tabela de agendamentos do módulo Agenda, porque a pasta vizinha estava a um import de distância. Qual regra do estilo foi violada?

- (a) A regra de que módulos devem rodar em processos separados.
- (b) A regra de que cada módulo deve usar um banco físico próprio.
- (c) A regra de que um módulo consome outro apenas pela API pública, e cada conjunto de dados tem um único escritor.
- (d) A regra de que módulos só podem se comunicar por eventos assíncronos.

#### Questão 13 [Média]

Um filtro de um pipeline de logs conta as ocorrências de erro em uma variável interna e usa essa contagem para decidir o que emitir. Qual é o problema e qual é a correção recomendada no módulo?

- (a) Excesso de filtros, corrigido pela fusão de todas as etapas em uma só.
- (b) Core creep, corrigido pela criação de um plugin de contagem.
- (c) Sumidouro, corrigido pela inclusão de uma camada de serviço.
- (d) Estado compartilhado invisível, corrigido por um mecanismo externo declarado, como um state store.

#### Questão 14 [Média]

Uma equipe separou apresentação, negócios e dados em três servidores, mas as responsabilidades continuam misturadas entre as camadas. O que o módulo afirma sobre essa situação?

- (a) Distribuir camadas fisicamente não resolve um acoplamento lógico mal definido.
- (b) A separação física resolve o acoplamento, porque cada servidor é implantado de forma independente.
- (c) O sistema passou a ser uma arquitetura de microsserviços.
- (d) A latência de rede compensa o acoplamento, porque obriga contratos explícitos.

#### Questão 15 [Média]

Por que aplicar o princípio aberto-fechado (OCP) na fronteira com os dados permite trocar MySQL por PostgreSQL sem alterar o serviço de negócio?

- (a) Porque os dois bancos usam a mesma linguagem SQL e dispensam qualquer adaptação.
- (b) Porque o serviço de negócio acessa o banco por meio do controller.
- (c) Porque a camada de negócios depende de uma abstração de repositório, e a implementação concreta fica na infraestrutura.
- (d) Porque o OCP proíbe mudanças em qualquer camada depois da primeira versão.

### Questões difíceis

#### Questão 16 [Difícil]

Uma equipe avalia extrair um módulo de um monólito modular para um serviço separado. Qual conjunto de evidências justifica essa extração segundo o módulo?

- (a) A equipe quer experimentar uma tecnologia nova e o módulo é pequeno o suficiente para isso.
- (b) Mudanças que exigem coordenação frequente entre módulos, incidentes que atravessam fronteiras, um módulo que domina os recursos do processo ou cadências de mudança muito diferentes, todos medidos.
- (c) O código do módulo cresceu e a pasta ficou difícil de navegar.
- (d) Microsserviços são o padrão de mercado e a extração antecipa uma necessidade futura.

#### Questão 17 [Difícil]

Um sistema precisa de alta elasticidade e de implantação independente por equipe. Considerando as avaliações de 1 a 5 apresentadas no módulo, qual conclusão é coerente?

- (a) Camadas é adequado, porque tem custo geral 5 e simplicidade 5.
- (b) Monólito modular é adequado, porque tem desempenho 4 e modularidade 4.
- (c) Pipes and Filters é adequado, porque tem testabilidade 5 e modularidade 5.
- (d) Camadas e monólito modular têm elasticidade 1, e esses requisitos apontam para a decomposição em serviços.

#### Questão 18 [Difícil]

Na Triagem hospitalar organizada em Microkernel, um plugin de uma unidade passou a editar dados internos do núcleo, e o núcleo ganhou uma regra específica para essa unidade. Qual é a leitura correta da situação?

- (a) A situação é esperada, porque plugins podem controlar o estado interno quando a unidade exige.
- (b) A fronteira entre núcleo e plugins precisa ser revista, porque o plugin deve conhecer apenas capacidades públicas e regra por unidade pertence ao plugin.
- (c) O problema é de desempenho e deve ser resolvido com plugins fora do processo.
- (d) O estilo deve ser trocado por Pipes and Filters, porque a triagem é um fluxo de dados.

#### Questão 19 [Difícil]

Em uma arquitetura em camadas fechadas, a equipe propõe abrir uma camada para uma consulta de leitura muito frequente. Em que condição essa abertura é defensável?

- (a) Sempre que reduzir o volume de código, independentemente de medição.
- (b) Nunca, porque qualquer camada aberta destrói o estilo em camadas.
- (c) Quando houver evidência de custo, contrato e teste para o atalho, sem contornar regra de negócio, e a decisão for registrada em um ADR.
- (d) Quando equipes diferentes forem responsáveis pelas duas camadas envolvidas.

#### Questão 20 [Difícil]

A Shopify mantém um grande monólito Ruby on Rails com centenas de implantações por dia. Qual lição arquitetural o módulo extrai desse caso?

- (a) Que o monólito modular escala em código e em equipe quando as fronteiras são verificadas continuamente por ferramenta na integração contínua.
- (b) Que monólitos só funcionam em equipes pequenas e com poucas implantações.
- (c) Que a migração para microsserviços é inevitável quando o código passa de certo tamanho.
- (d) Que a separação em pastas é suficiente para manter os módulos independentes.
