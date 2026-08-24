# Exercícios: tornar políticas governáveis

Tente responder antes de abrir cada feedback. Nas atividades avançadas, os nove campos tornam explícitos contexto, artefato e avaliação de uma decisão justificável. Cada entrega distingue política, arquivo declarativo, serviço que a recebe e saída que comprova o comportamento.

## Recordar

1\. Defina governança de serviços em uma frase.

<details>
<summary>Ver resposta</summary>

É o conjunto de contratos, responsabilidades e políticas verificáveis que torna uma decisão repetível e revisável.
</details>

2\. O que uma política de rate limiting protege e o que ela não decide?

<details>
<summary>Ver resposta</summary>

Protege a capacidade da borda contra volume excessivo; não decide autorização ou regra clínica do domínio.
</details>

3\. Diferencie `correlation_id` de trace ID.

<details>
<summary>Ver resposta</summary>

`correlation_id` facilita a busca humana entre resposta e logs; trace ID identifica a árvore técnica de spans distribuídos.
</details>

4\. Nomeie o arquivo da política de rota local.

<details>
<summary>Ver resposta</summary>

`laboratorios/plataforma-hospitalar/infra/kong/kong.yml`.
</details>

5\. Que saída comprova o limite da oficina?

<details>
<summary>Ver resposta</summary>

Uma resposta HTTP `429 Too Many Requests` depois de mais chamadas que o limiar da janela.
</details>

## Compreender

1\. Explique por que Kong não é sinônimo de governança.

<details>
<summary>Ver resposta</summary>

Kong implementa localmente políticas de borda; governança também inclui contrato, owner, versão, evidência e revisão, que sobrevivem à troca da ferramenta.
</details>

2\. Por que uma regra de plano vencido deve permanecer em Elegibilidade?

<details>
<summary>Ver resposta</summary>

Ela depende de estado e exceções do domínio, que pertencem ao serviço; o gateway só medeia controles comuns de entrada.
</details>

3\. Compare uma resposta `200` direta e uma `200` pelo gateway.

<details>
<summary>Ver resposta</summary>

A direta prova serviço e dado didático; a governada também prova a rota e a aplicação da política de borda, mas não autorização clínica.
</details>

4\. Por que o trace não substitui um log estruturado?

<details>
<summary>Ver resposta</summary>

O trace mostra caminho e tempo causal; o log descreve evento e campos seguros. A investigação usa ambos com a mesma correlação.
</details>

5\. O que a rastreabilidade permite afirmar com segurança?

<details>
<summary>Ver resposta</summary>

Que uma decisão publicada, sua configuração e uma execução observada podem ser relacionadas; ela não prova sozinha uma conclusão clínica ou de conformidade.
</details>

## Aplicar

### Recomendar onde aplicar a política de limite e correlação

**Objetivo**

Recomendar um entre quatro lugares para aplicar uma política de governança, declarando o que cada opção ganha, o que cobra e o que deixa descoberto.

**Situação**

Uma plataforma hospitalar tem seis serviços mantidos por três equipes. A diretoria de tecnologia aprovou duas políticas: toda chamada carrega um identificador de correlação que atravessa a cadeia inteira, e nenhum consumidor ultrapassa três chamadas por segundo por origem.

As políticas estão escritas e ninguém consegue provar que valem. Cada equipe entende a regra de um jeito, dois serviços já implementaram versões diferentes do limite, e o identificador de correlação se perde em algum lugar do meio da cadeia sem que ninguém saiba onde.

A diretoria pediu uma recomendação de onde a política deve morar.

**Seu papel**

Você é a pessoa arquiteta responsável pela recomendação. As três equipes implementam depois, e esperam de você a escolha e o que ela deixa em aberto.

**Artefato que você irá usar**

Crie `entregas/modulo-4/aplicar-onde-mora-a-politica.md`, a partir da raiz do clone, e use as comparações de `docs/modulo-4-governanca/padroes-e-decisoes.md`.

**Antes de executar**

Crie o diretório `entregas/modulo-4/`; o estado inicial é sem serviços iniciados e sem alteração do laboratório.

Seis fatos foram apurados na plataforma:

1. Os seis serviços usam três linguagens diferentes.
2. A política precisa valer também nas chamadas entre serviços internos, e não apenas no tráfego que entra.
3. A operação de plataforma tem duas pessoas.
4. Uma auditoria externa exige provar, serviço por serviço, que o limite estava ativo numa data passada.
5. Não existe malha de serviços instalada, e instalar exigiria janela de manutenção nos seis serviços.
6. O tráfego que entra passa integralmente por um gateway já em produção.

As quatro alternativas em avaliação:

| Alternativa | Onde a política é aplicada |
| --- | --- |
| **A. Em cada serviço** | Cada equipe implementa o limite e a propagação no próprio código, seguindo a política escrita. |
| **B. Biblioteca compartilhada** | Uma biblioteca de chassi implementa a política, e todos os serviços a incorporam como dependência. |
| **C. Gateway de borda** | O gateway que já existe aplica o limite e injeta o identificador de correlação antes de rotear. |
| **D. Malha de serviços** | Um *sidecar* ao lado de cada serviço aplica a política, fora do código da aplicação. |

**O que fazer**

1. Recomende **uma** das quatro alternativas para a plataforma agora, em uma frase.
2. Preencha o quadro comparativo, uma linha por alternativa. A primeira vem resolvida como modelo.

    | Alternativa | O que resolve | O que cobra | Fato decisivo |
    | --- | --- | --- | --- |
    | A. Em cada serviço | alcança também as chamadas internas, sem infraestrutura nova | seis implementações para manter e seis provas independentes para a auditoria | fato 4, que multiplica o custo de comprovação |
    | B. Biblioteca compartilhada | | | |
    | C. Gateway de borda | | | |
    | D. Malha de serviços | | | |

3. Nomeie explicitamente o que a sua recomendação **deixa descoberto** em relação ao fato 2, e diga como a auditoria do fato 4 seria atendida mesmo assim.
4. Aponte a alternativa que você descartaria de imediato e nomeie o fato apurado que a derruba.
5. Declare o risco que a sua recomendação aceita e escreva o sinal observável que levaria a rever a decisão.
6. Se a política recomendada não puder ser verificada com dados sintéticos no laboratório, registre-a como hipótese e nomeie o teste pendente.

**Evidência esperada**

O artefato traz o quadro comparativo completo, a recomendação em uma frase, a lacuna declarada em relação às chamadas internas, o caminho de comprovação para a auditoria, a alternativa descartada com o fato que a derruba, o risco aceito e o sinal de revisão observável.

**Entrega esperada**

Envie `entregas/modulo-4/aplicar-onde-mora-a-politica.md` com no máximo uma página, contendo o quadro comparativo, a recomendação, a lacuna declarada, o risco aceito e o sinal de revisão.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação com ganho e custo nas quatro alternativas | 30% | Evidência: as duas colunas preenchidas para as quatro; insuficiente: opção listada sem custo. |
| Lacuna declarada em vez de escondida | 25% | Evidência: o que fica descoberto, nomeado; insuficiente: recomendação apresentada como cobertura total. |
| Recomendação sustentada por fato apurado | 20% | Evidência: fato citado pelo número; insuficiente: escolha por preferência de ferramenta. |
| Caminho de comprovação para a auditoria | 15% | Evidência: onde o registro fica e como é consultado; insuficiente: "os logs mostram". |
| Risco aceito e sinal de revisão | 10% | Evidência: consequência e condição observável; insuficiente: prazo no calendário. |

## Analisar

### Diagnosticar uma cadeia sem correlação

**Objetivo**

Separar fatos, inferências e hipóteses ao investigar uma cadeia sem correlação consistente.

**Situação**

Gateway registra `502`, Elegibilidade registra erro de banco e Jaeger contém traces sem nome consistente; a média de latência permanece estável.

**Seu papel**

Você conduz a análise do incidente sem afirmar causalidade além da evidência.

**Artefato que você irá usar**

Crie `<raiz-do-clone>/entregas/modulo-4/analisar-correlacao.md`, usando `docs/modulo-4-governanca/conceitos.md`, `laboratorios/plataforma-hospitalar/infra/kong/kong.yml` e `laboratorios/plataforma-hospitalar/src/hospital/telemetria.py`.

**Antes de executar**

O estado inicial reúne três logs anonimizados, taxa de `5xx`, traces parciais e a política atual; não inclua dado clínico na entrega.

**Insumos disponíveis**

As amostras do caso e os arquivos declarativos indicados.

**O que fazer**

1. Separe fato, inferência e hipótese.
2. Mapeie lacunas de `correlation_id` e `traceparent`.
3. Compare duas causas plausíveis e uma mudança mínima.
4. Declare o dado que confirmaria ou enfraqueceria cada hipótese.

**Evidência esperada**

Política: contexto; artefatos: `laboratorios/plataforma-hospitalar/infra/kong/kong.yml` e `laboratorios/plataforma-hospitalar/src/hospital/telemetria.py`; serviços: Kong e Elegibilidade. Kong extrai e injeta o `traceparent` W3C; o middleware de Elegibilidade extrai o contexto e cria o span filho. `infra/observabilidade/otel-collector.yml` recebe sinais OTLP, processa em lote e exporta ao Jaeger; não propaga `traceparent`. Saída: trace e log correlacionados, ou lacuna registrada.

**Entrega esperada**

Envie o arquivo com linha do tempo, mapa de evidências e plano de investigação seguro.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Separação de fato e hipótese | 25% | Evidência: hipótese rotulada; insuficiente: inferência como fato. |
| Leitura integrada dos sinais | 25% | Evidência: sinais correlacionados; insuficiente: métrica isolada conclui causa. |
| Hipóteses alternativas | 20% | Evidência: mais de uma causa; insuficiente: primeira hipótese tratada certa. |
| Mudança verificável proposta | 20% | Evidência: efeito esperado; insuficiente: mudança sem prova. |
| Limites da conclusão | 10% | Evidência: limite declarado; insuficiente: diagnóstico definitivo sem dados. |

## Avaliar

### Escolher uma política de limite

**Objetivo**

Recomendar uma política temporária que proteja capacidade e explicite seu impacto.

**Situação**

Um portal parceiro atinge 20 chamadas por segundo por cinco minutos; a capacidade atual é oito por segundo e hospitais compartilham proxy.

**Seu papel**

Você recomenda a decisão e suas condições de evolução.

**Artefato que você irá usar**

Crie `<raiz-do-clone>/entregas/modulo-4/avaliar-limite.md`, usando `docs/modulo-4-governanca/exemplo-arquitetural.md` e `laboratorios/plataforma-hospitalar/infra/kong/kong.yml`.

**Antes de executar**

O estado inicial considera consumidores parcialmente identificados, suporte em horário comercial e meta de latência para consultas aceitas.

**Insumos disponíveis**

Pico, capacidade, risco de atraso e alternativas IP, credencial e fila.

**O que fazer**

1. Compare as três estratégias por proteção, justiça e operação.
2. Declare resposta `429`, SLO, sinal de revisão e comunicação a consumidores.
3. Proponha experimento reversível e plano de retorno.

**Evidência esperada**

Política observada: rate limiting; arquivo: `infra/kong/kong.yml`; serviço que a recebe: Kong diante de Elegibilidade; entrega: `<raiz-do-clone>/entregas/modulo-4/avaliar-limite.md`; saída: série controlada de chamadas com `429` e decisão registrada sobre o impacto.

**Entrega esperada**

Envie o arquivo com alternativas, decisão, consequências, evidências e retorno.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação equilibrada | 25% | Evidência: ganhos e custos; insuficiente: uma opção idealizada. |
| Vínculo com capacidade e risco | 25% | Evidência: risco justifica decisão; insuficiente: mecanismo sem contexto. |
| SLO e sinais operacionais | 20% | Evidência: meta e sinal; insuficiente: número sem ação. |
| Reversibilidade | 15% | Evidência: plano de retorno; insuficiente: alteração irreversível sem avaliação. |
| Comunicação a consumidores | 15% | Evidência: impacto comunicado; insuficiente: mudança sem destinatário. |

## Criar

### Desenhar o mínimo de governança para agenda

**Objetivo**

Criar um pacote inicial de decisão para Agenda que continue verificável ao evoluir.

**Situação**

Agenda consulta Elegibilidade, reserva horário e informa preparo de sala; terá owner próprio, API pública e integração com duas equipes.

**Seu papel**

Você cria a proposta que começa localmente sem depender de memória informal.

**Artefato que você irá usar**

Crie `<raiz-do-clone>/entregas/modulo-4/criar-agenda/` e entregue nele `adr.md`, `politica.yml`, `sinais.md` e `teste.md`, usando `laboratorios/plataforma-hospitalar/infra/compose.governanca.yml` apenas como referência.

**Antes de executar**

Considere dados sintéticos, confirmação inicial em três segundos e no máximo três novas unidades implantáveis no semestre.

**Insumos disponíveis**

Contrato de Elegibilidade, Compose da oficina e as restrições declaradas.

**O que fazer**

1. Defina catálogo, classificação de dados, contrato e estratégia de versão.
2. Separe políticas de gateway, serviço e domínio.
3. Modele logs, métricas conceituais, trace, `correlation_id`, SLO e orçamento de erro.
4. Planeje testes de rota, limite e propagação, além de dois gatilhos de revisão.

**Evidência esperada**

Política observada: rota, correlação e limite; arquivo: `<raiz-do-clone>/entregas/modulo-4/criar-agenda/politica.yml`; serviço que a recebe: Agenda através do gateway; saída: roteiro reproduzível com resposta de rota, `429`, `X-Correlation-ID` e consulta de trace.

**Entrega esperada**

Envie os quatro arquivos com ADR, diagrama, configuração ilustrativa, plano de sinais e roteiro de teste.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Coerência entre ownership e contrato | 20% | Evidência: dono mantém contrato; insuficiente: responsabilidade dividida sem regra. |
| Separação de políticas | 20% | Evidência: borda e domínio separados; insuficiente: política clínica no gateway. |
| Observabilidade verificável | 20% | Evidência: consulta reproduzível; insuficiente: sinal sem como verificar. |
| SLO contextualizado | 15% | Evidência: usuário e janela; insuficiente: meta sem contexto. |
| Testes reproduzíveis | 15% | Evidência: comando e resultado; insuficiente: procedimento não repetível. |
| Gatilhos de evolução | 10% | Evidência: sinal de mudança; insuficiente: evolução sem condição. |
