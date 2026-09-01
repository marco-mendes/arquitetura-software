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
