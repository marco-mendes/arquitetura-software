# Exercícios por Taxonomia de Bloom

Responda antes de abrir “Ver resposta”. Nas atividades seguintes, siga o roteiro e justifique escolhas pelas mesmas forças e limites.

## Recordar

1. O que diferencia um componente de um conector?

<details>
<summary>Ver resposta</summary>

Componente concentra responsabilidade; conector descreve colaboração, como chamada HTTP, mensagem ou acesso a dados.
</details>

2. Quais são os quatro estilos aprofundados nesta unidade?

<details>
<summary>Ver resposta</summary>

Camadas, Pipes and Filters, Microkernel e Monólito modular.
</details>

3. Qual nome recebe uma condição assumida como verdadeira, mas que ainda pode precisar de revisão?

<details>
<summary>Ver resposta</summary>

Premissa; uma restrição já limita alternativas conhecidas.
</details>

4. Quais seis partes tornam um cenário de atributo de qualidade observável?

<details>
<summary>Ver resposta</summary>

Fonte, estímulo, ambiente, artefato, resposta e medida.
</details>

5. Qual estilo organiza transformações independentes encadeadas por um fluxo de dados?

<details>
<summary>Ver resposta</summary>

Pipes and Filters: filtro transforma; pipe transporta a saída ou rejeição.
</details>

6. O que um ADR registra além da alternativa escolhida?

<details>
<summary>Ver resposta</summary>

Contexto, forças, alternativas, consequências, evidências e gatilho de revisão.
</details>

## Compreender

1. “A aplicação será executada em Python 3.12.” Isso descreve estilo, padrão ou tecnologia?

<details>
<summary>Ver resposta</summary>

Tecnologia; ela não define responsabilidades ou conectores.
</details>

2. “As regras de negócio não podem importar adaptadores de persistência.” O que a frase declara?

<details>
<summary>Ver resposta</summary>

Uma regra de dependência que Camadas ou Hexagonal pode sustentar e testar.
</details>

3. Por que MVC não é simplesmente outro nome para qualquer aplicação web?

<details>
<summary>Ver resposta</summary>

MVC organiza requisição-resposta em controller, model e view; não resolve por si só domínio, eventos ou implantação.
</details>

4. Quando uma camada é chamada de fechada?

<details>
<summary>Ver resposta</summary>

Quando a interação atravessa a camada imediatamente abaixo, sem atalho.
</details>

5. O que torna um filtro com estado mais delicado que um filtro sem estado?

<details>
<summary>Ver resposta</summary>

Ele depende de contexto entre itens; declare onde o estado vive, como recupera e como trata concorrência.
</details>

6. Por que um plugin que lê tabelas internas do núcleo não demonstra bem um microkernel?

<details>
<summary>Ver resposta</summary>

Porque depende de detalhes privados, aumenta acoplamento e incentiva core creep.
</details>

## Aplicar

**Objetivo**

Executar o comparador didático de estilos e explicar por que sua saída é uma evidência parcial, não uma decisão automática.

**Situação**

Uma capacidade administrativa possui validação comum e etapa opcional por unidade; a regra varia mensalmente.

**Seu papel**

Você transforma a necessidade em forças verificáveis e interpreta a execução.

**Artefato que você irá usar**

Em `laboratorios/plataforma-hospitalar`, `src/hospital/estilos.py` compara quatro estilos por forças, limites e evidências. `tests/test_estilos.py` verifica o comparador. Não há dados reais ou conexão externa.

**Insumos disponíveis**

Use o código, seus testes, a [oficina](oficina-de-ferramentas.md) e o [template de ADR](../referencia/template-adr.md).

**Antes de executar**

Abra o terminal em `laboratorios/plataforma-hospitalar`. Siga a preparação da [oficina](oficina-de-ferramentas.md) até existir `.venv` e `python --version` e `python -m pytest --version` funcionarem. Leia os dois arquivos: o comparador recebe prioridades e retorna uma lista; não mede produção.

**Como conduzir**

Verifique o ambiente, registre a execução e só então argumente.

**O que fazer**

1. Crie `evidencias` na raiz do laboratório.
2. Execute `python -m pytest tests/test_estilos.py -q` e guarde a saída em `evidencias/testes-estilos.txt` conforme a oficina.
3. Crie `evidencias/comparacao.py` para prioridades `modificabilidade` e `extensibilidade`; importe e imprima `comparar_estilos`.
4. Registre primeira alternativa, força, limite, evidência e um cenário com estímulo, resposta e medida.
5. Copie o [template de ADR](../referencia/template-adr.md) para `evidencias/ADR-001-estilo-inicial.md` e registre alternativas, consequência e revisão.

**Evidência esperada**

`3 passed`, script, saída e ADR. Microkernel pode surgir primeiro, mas a tabela não substitui o limite de compatibilidade de plugins.

**Entrega esperada**

Entregue `evidencias` e um parágrafo sobre o que o comparador não mede.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Execução reproduzível | 25% | Evidência: comando, saída e cenário; insuficiência: arquivo sem contexto. |
| Cenário de qualidade | 25% | Evidência: estímulo, resposta e medida; insuficiência: qualidade vaga. |
| Comparação responsável | 30% | Evidência: força e limite ligados; insuficiência: tabela tratada como oráculo. |
| Decisão revisável | 20% | Evidência: consequência e gatilho; insuficiência: ADR sem revisão. |

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

Crie `analise-integracao` com `forcas.md`, `alternativas.md` e `fluxo.md`. Leia [conceitos](conceitos.md). Aqui, executar é elaborar e revisar arquivos, não iniciar uma API.

**Como conduzir**

Comece pelas forças; o diagrama é consequência da decomposição.

**O que fazer**

1. Em `forcas.md`, classifique throughput, variação, ordenação, deduplicação, rastreabilidade e operação.
2. Escreva três cenários mensuráveis.
3. Em `alternativas.md`, modele duas decomposições e nomeie componentes, conectores e estado.
4. Compare os quatro estilos por ganho, limite e evidência.
5. Em `fluxo.md`, desenhe Mermaid e uma falha parcial, ambos com leitura textual.
6. Registre três hipóteses e experimentos.

**Evidência esperada**

Os arquivos tratam repetição, atraso e rejeição; o diagrama identifica produtor, conector e registro de rejeição.

**Entrega esperada**

Entregue os três arquivos, com até mil palavras e uma lacuna de medição.

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

Use planilha ou Markdown. A proposta A mantém conectores, modelo canônico e sequência na mesma implantação; B usa coletor por parceiro e processador comum. Há seis pessoas, uma equipe operacional e amostra sintética de mil atualizações, cinquenta repetições, vinte atrasos e cinco contradições; não há medições de carga, custo ou inclusão.

**Insumos disponíveis**

Use propostas, amostra, equipe e [padrões e decisões](padroes-e-decisoes.md). Ausência de medida delimita a conclusão.

**Antes de executar**

Crie `parecer.md` com “critério”, “medida”, “evidência”, “lacuna” e “impacto”. Não escolha antes dos critérios.

**Como conduzir**

Preencha a tabela antes da conclusão.

**O que fazer**

1. Crie critérios para atualização, formato, repetição, atraso, auditoria e operação.
2. Marque evidência disponível, ausente ou contraditória.
3. Relacione cada proposta a estilos possíveis e consequências.
4. Recomende, rejeite ou adie com condição de revisão.
5. Descreva duas experiências e a objeção mais forte.

**Evidência esperada**

O parecer distingue desconhecido de medido.

**Entrega esperada**

Entregue `parecer.md` com tabela, recomendação, incertezas, objeção e experiências.

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

Crie `baseline-inicial` com `cenarios`, `modelos`, `decisoes` e `evidencias`. Prepare a [oficina](oficina-de-ferramentas.md) e confirme `3 passed` no teste de estilos.

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

Entregue `baseline-inicial` com `README.md` de leitura.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Delimitação e cenários | 20% | Evidência: escopo e medida; insuficiência: cenário vago. |
| Alternativas comparáveis | 20% | Evidência: consequências para todas; insuficiência: comparação desigual. |
| Modelos compreensíveis | 20% | Evidência: nomes e texto; insuficiência: modelos contraditórios. |
| Decisão rastreável | 20% | Evidência: ADR e revisão; insuficiência: decisão solta. |
| Evidência reproduzível | 15% | Evidência: comando e saída; insuficiência: resultado sem contexto. |
| Organização da entrega | 5% | Evidência: README orienta; insuficiência: arquivos sem vínculo. |
