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

**Seu papel**

Você é a pessoa arquiteta chamada para recomendar a estrutura. A equipe implementa depois, e espera de você a escolha, a justificativa e os riscos.

**Artefato que você irá usar**

Crie `entregas/unidade-1/aplicar-motor-de-regras.md`, a partir da raiz do repositório `arquitetura-software`, e use as descrições de estilos em `docs/modulo-1-visao-geral/padroes-e-decisoes.md`.

**Antes de executar**

Crie o diretório `entregas/unidade-1/`; o estado inicial é sem execução de laboratório e sem alteração dos exemplos do repositório.

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

**O que fazer**

1. Recomende **um** dos quatro estilos para a operadora agora, em uma frase.
2. Preencha o quadro comparativo, uma linha por alternativa. A primeira vem resolvida como modelo.

    | Alternativa | O que resolve | O que cobra | Fato decisivo |
    | --- | --- | --- | --- |
    | A. Camadas | organiza a dependência e separa o cálculo da emissão | o método continua sendo um bloco só; nada torna visível a sequência de regras aplicada | fato 3, que continua sem resposta |
    | B. Pipes and Filters | | | |
    | C. Microkernel | | | |
    | D. Monólito modular | | | |

3. Nomeie o atributo de qualidade que decide a sua recomendação e escreva um cenário para ele com estímulo, resposta e medida.
4. Aponte a alternativa que você descartaria de imediato e nomeie o fato apurado que a derruba.
5. Declare o risco que a sua recomendação aceita, isto é, o que pode dar errado e a operadora escolheu conviver com isso.
6. Escreva o sinal observável que levaria a operadora a trocar de estilo. Data no calendário não é sinal.
7. Se algum fato necessário para decidir não estiver na lista, registre a pergunta que você faria antes de assinar a recomendação.

**Evidência esperada**

O artefato traz o quadro comparativo completo, com ganho e custo declarados para os quatro estilos, a recomendação em uma frase, o cenário de qualidade com medida, o fato que sustenta a escolha, o risco aceito e o sinal de revisão como condição observável.

**Entrega esperada**

Envie `entregas/unidade-1/aplicar-motor-de-regras.md` com no máximo uma página, contendo o quadro comparativo, a recomendação, o cenário de qualidade, a alternativa descartada, o risco aceito e o sinal de revisão.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação com ganho e custo nos quatro estilos | 30% | Evidência: as duas colunas preenchidas para os quatro; insuficiente: estilo descrito sem custo declarado. |
| Recomendação sustentada por fato apurado | 25% | Evidência: fato citado pelo número; insuficiente: preferência técnica sem base no caso. |
| Cenário de qualidade com medida | 15% | Evidência: estímulo, resposta e medida; insuficiente: adjetivo como "flexível" sem medida. |
| Alternativa descartada com motivo | 15% | Evidência: fato que a derruba; insuficiente: descarte por gosto. |
| Risco aceito e sinal de revisão | 15% | Evidência: consequência nomeada e condição observável; insuficiente: prazo no calendário. |

## Analisar

**Objetivo**

Decompor uma integração de dados em forças, etapas, fronteiras e hipóteses antes de escolher uma organização.

**Situação**

Uma rede de laboratórios possui dezoito parceiros que enviam JSON, CSV ou XML para uma central. Há quatro milhões de registros por dia, pico de seiscentos por segundo, mudanças mensais de layout, repetições e atrasos. Cada rejeição precisa indicar origem, versão, transformação e motivo; lote aceito em até vinte minutos.

**Seu papel**

Você separa fatos, premissas e hipóteses antes de defender estrutura.

**Artefato que você irá usar**

Use o enunciado, [atributos de qualidade](../referencia/atributos-de-qualidade.md) e Mermaid. Considere três exemplos por formato, duas repetições, um atraso e duas versões; use códigos fictícios.

**Insumos disponíveis**

O enunciado fornece volume, formatos, mudança e prazo; Mermaid registra componentes e conectores sem instalar mensageria.

**Antes de executar**

No terminal aberto na raiz do repositório `arquitetura-software`, crie `entregas/unidade-1/analise-integracao/` com `forcas.md`, `alternativas.md` e `fluxo.md`. Leia [conceitos](conceitos.md). Aqui, executar é elaborar e revisar arquivos, não iniciar uma API.

**Condição inicial verificável**

A pasta `entregas/unidade-1/analise-integracao` existe, contém os três arquivos vazios e `fluxo.md` abre em editor com Mermaid.

**Como conduzir**

Comece pelas forças; o diagrama é consequência da decomposição.

**O que fazer**

1. Em `entregas/unidade-1/analise-integracao/forcas.md`, classifique throughput, variação, ordenação, deduplicação, rastreabilidade e operação.
2. Escreva três cenários mensuráveis.
3. Em `alternativas.md`, modele duas decomposições e nomeie componentes, conectores e estado.
4. Compare os quatro estilos por ganho, limite e evidência.
5. Em `fluxo.md`, desenhe Mermaid e uma falha parcial, ambos com leitura textual.
6. Registre três hipóteses e experimentos.

**Evidência esperada**

Os arquivos tratam repetição, atraso e rejeição; o diagrama identifica produtor, conector e registro de rejeição.

**Entrega esperada**

Entregue `entregas/unidade-1/analise-integracao/` com os três arquivos, até mil palavras e uma lacuna de medição.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Decomposição de forças e etapas | 25% | Evidência: força ligada a etapa; insuficiência: lista isolada. |
| Comparação simétrica | 30% | Evidência: mesmas forças e limites; insuficiência: favorecimento sem contraste. |
| Coerência de modelos | 25% | Evidência: elementos e texto concordam; insuficiência: seta sem leitura. |
| Hipóteses verificáveis | 20% | Evidência: hipótese com experimento; insuficiência: suposição como fato. |

## Avaliar

**Objetivo**

Avaliar propostas concorrentes com critérios mensuráveis, evidência incompleta e uma recomendação que possa ser revisada.

**Situação**

Uma secretaria consolida disponibilidade de leitos de 45 hospitais. Há JSON a cada 30 segundos, CSV a cada cinco minutos, pico de 900 atualizações por minuto, repetições, atrasos e contradições. O painel atualiza em 60 segundos; auditoria explica fonte, versão, transformação e desempate.

**Seu papel**

Você pode recomendar, rejeitar ou propor experimento limitado; não há resposta aprovada.

**Artefato que você irá usar**

Use `<raiz-do-clone>/entregas/unidade-1/avaliacao-leitos/parecer.md`. A mantém conectores e modelo comum; B usa coletor por parceiro. Há equipe e amostra de atualizações, cinquenta repetições, vinte atrasos e cinco contradições; não há medições de carga, custo ou inclusão.

**Insumos disponíveis**

Use propostas, amostra, equipe e [padrões e decisões](padroes-e-decisoes.md). Ausência de medida delimita a conclusão.

**Antes de executar**

No terminal aberto na raiz do repositório `arquitetura-software`, crie `entregas/unidade-1/avaliacao-leitos/parecer.md` com “critério”, “medida”, “evidência”, “lacuna” e “impacto”. Não escolha antes dos critérios.

**Condição inicial verificável**

A pasta `entregas/unidade-1/avaliacao-leitos` existe e `parecer.md` contém a tabela vazia. A amostra do enunciado está disponível; não inicie software adicional.

**Como conduzir**

Preencha a tabela antes da conclusão.

**O que fazer**

1. Crie critérios para atualização, formato, repetição, atraso, auditoria e operação.
2. Marque evidência disponível, ausente ou contraditória.
3. Relacione cada proposta a estilos possíveis e consequências.
4. Recomende, rejeite ou adie com condição de revisão.
5. Descreva duas experiências e a objeção mais forte.
6. Se uma medida necessária estiver ausente, adie a recomendação e registre a experiência que produziria essa medida.

**Evidência esperada**

O parecer distingue desconhecido de medido.

**Entrega esperada**

Entregue `entregas/unidade-1/avaliacao-leitos/parecer.md` com tabela, recomendação, incertezas, objeção e experiências.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Critérios anteriores à escolha | 20% | Evidência: tabela anterior; insuficiência: critério criado depois. |
| Uso honesto de evidências | 25% | Evidência: lacuna declarada; insuficiência: estimativa como medida. |
| Consequências comparadas | 25% | Evidência: ganhos e custos; insuficiência: somente benefício. |
| Recomendação revisável | 20% | Evidência: condição e gatilho; insuficiência: conclusão absoluta. |
| Experimentos alinhados | 10% | Evidência: responde à incerteza; insuficiência: atividade sem pergunta. |

## Criar

**Objetivo**

Criar uma baseline arquitetural inicial para a plataforma hospitalar que outra equipe consiga ler, executar e revisar nos próximos encontros.

**Situação**

O grupo iniciará o [incremento 1](../projeto-integrador/incrementos.md#incremento-1-estrutura-e-decisoes-iniciais) sem antecipar APIs, serviços, eventos ou infraestrutura.

**Seu papel**

Você garante consistência entre cenários, modelos, decisão e evidência.

**Artefato que você irá usar**

Use o contexto integrador, [atributos de qualidade](../referencia/atributos-de-qualidade.md), [template de ADR](../referencia/template-adr.md), Mermaid e `laboratorios/plataforma-hospitalar`.

**Insumos disponíveis**

O projeto fornece domínio; referências estruturam cenários e ADR; Mermaid registra modelos; laboratório produz evidência limitada.

**Antes de executar**

No terminal aberto na raiz do repositório `arquitetura-software`, crie `entregas/unidade-1/baseline-inicial/` com `cenarios`, `modelos`, `decisoes` e `evidencias`. Prepare a [oficina](oficina-de-ferramentas.md) e confirme `3 passed` no teste de estilos.

**Condição inicial verificável**

As quatro subpastas existem em `entregas/unidade-1/baseline-inicial`, e `cd laboratorios/plataforma-hospitalar` seguido do teste termina com `3 passed`.

**Como conduzir**

Produza e conecte cada artefato; revise contradições ao final.

**O que fazer**

1. Delimite sistema, atores, externos e fora de escopo em `cenarios/escopo.md`.
2. Escreva três cenários mensuráveis em `cenarios/qualidade.md`.
3. Compare três alternativas em `decisoes/alternativas.md`.
4. Modele estrutura e sequência com leitura textual em `modelos/`.
5. Crie `decisoes/ADR-001.md` com decisão, consequências e revisão.
6. Salve o teste e sua interpretação em `evidencias/`.
7. Confira se ADR, modelos e cenários usam os mesmos nomes.

**Evidência esperada**

Cadeia legível de escopo → cenário → alternativas → modelos → ADR → teste interpretado.

**Entrega esperada**

Entregue `entregas/unidade-1/baseline-inicial/` com `README.md` de leitura.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Delimitação e cenários | 20% | Evidência: escopo e medida; insuficiência: cenário vago. |
| Alternativas comparáveis | 20% | Evidência: consequências para todas; insuficiência: comparação desigual. |
| Modelos compreensíveis | 20% | Evidência: nomes e texto; insuficiência: modelos contraditórios. |
| Decisão rastreável | 20% | Evidência: ADR e revisão; insuficiência: decisão solta. |
| Evidência reproduzível | 15% | Evidência: comando e saída; insuficiência: resultado sem contexto. |
| Organização da entrega | 5% | Evidência: README orienta; insuficiência: arquivos sem vínculo. |
