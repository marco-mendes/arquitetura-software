# Exercícios: tornar políticas governáveis

Tente responder antes de abrir cada feedback. Nas atividades avançadas, os nove campos tornam explícitos contexto, artefato e avaliação de uma decisão justificável. Cada entrega distingue política, arquivo declarativo, serviço que a recebe e saída que comprova o comportamento.

## Recordar

1. Defina governança de serviços em uma frase.

<details>
<summary>Ver resposta</summary>

É o conjunto de contratos, responsabilidades e políticas verificáveis que torna uma decisão repetível e revisável.
</details>

2. O que uma política de rate limiting protege e o que ela não decide?

<details>
<summary>Ver resposta</summary>

Protege a capacidade da borda contra volume excessivo; não decide autorização ou regra clínica do domínio.
</details>

3. Diferencie `correlation_id` de trace ID.

<details>
<summary>Ver resposta</summary>

`correlation_id` facilita a busca humana entre resposta e logs; trace ID identifica a árvore técnica de spans distribuídos.
</details>

4. Nomeie o arquivo da política de rota local.

<details>
<summary>Ver resposta</summary>

`laboratorios/plataforma-hospitalar/infra/kong/kong.yml`.
</details>

5. Que saída comprova o limite da oficina?

<details>
<summary>Ver resposta</summary>

Uma resposta HTTP `429 Too Many Requests` depois de mais chamadas que o limiar da janela.
</details>

## Compreender

1. Explique por que Kong não é sinônimo de governança.

<details>
<summary>Ver resposta</summary>

Kong implementa localmente políticas de borda; governança também inclui contrato, owner, versão, evidência e revisão, que sobrevivem à troca da ferramenta.
</details>

2. Por que uma regra de plano vencido deve permanecer em Elegibilidade?

<details>
<summary>Ver resposta</summary>

Ela depende de estado e exceções do domínio, que pertencem ao serviço; o gateway só medeia controles comuns de entrada.
</details>

3. Compare uma resposta `200` direta e uma `200` pelo gateway.

<details>
<summary>Ver resposta</summary>

A direta prova serviço e dado didático; a governada também prova a rota e a aplicação da política de borda, mas não autorização clínica.
</details>

4. Por que o trace não substitui um log estruturado?

<details>
<summary>Ver resposta</summary>

O trace mostra caminho e tempo causal; o log descreve evento e campos seguros. A investigação usa ambos com a mesma correlação.
</details>

5. O que a rastreabilidade permite afirmar com segurança?

<details>
<summary>Ver resposta</summary>

Que uma decisão publicada, sua configuração e uma execução observada podem ser relacionadas; ela não prova sozinha uma conclusão clínica ou de conformidade.
</details>

## Aplicar

### Publicar uma rota de resultado de exame

**Objetivo**

Preparar uma política inicial para Resultados que seja declarada, limitada e verificável.

**Situação**

Resultados contém dado de saúde, possui consumidor móvel autenticado, precisa suportar picos e mantém a decisão de vínculo clínico no serviço.

**Seu papel**

Você prepara a proposta de owner do serviço.

**Artefato que você irá usar**

Crie `<raiz-do-clone>/entregas/modulo-4/aplicar-resultados.md`, usando `docs/modulo-4-governanca/padroes-e-decisoes.md` e `laboratorios/plataforma-hospitalar/infra/kong/kong.yml` como referência, sem alterar o laboratório.

**Antes de executar**

Considere Kong DB-less, uma réplica local, Collector, Jaeger e a convenção `X-Correlation-ID`.

**Insumos disponíveis**

Contrato de Resultados, catálogo em Markdown e políticas da oficina.

**Como conduzir**

1. Registre owner, contrato, consumidores, dados e versão.
2. Proponha rota, chave, janela, consequência de `429` e fronteira de domínio.
3. Desenhe a propagação de `correlation_id` e trace.
4. Declare um gatilho de revisão do limite.

**Evidência esperada**

Política observada: limite de entrada; arquivo: `<raiz-do-clone>/entregas/modulo-4/aplicar-resultados.md`; serviço que a recebe: Resultados via gateway; saída: uma chamada automatizável com `429`, `X-Correlation-ID` e trace consultável.

**Entrega esperada**

Envie o arquivo com uma página, política, mapa de fluxo, hipótese e risco.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Catálogo e ownership explícitos | 20% | Evidência: dono e consumidor; insuficiente: API sem responsável. |
| Política de borda coerente | 25% | Evidência: regra declarada; insuficiente: política sem risco associado. |
| Regra de domínio preservada | 25% | Evidência: serviço decide regra; insuficiente: gateway decide domínio. |
| Evidência de correlação e trace | 20% | Evidência: identificador e trace; insuficiente: sinais não relacionados. |
| Condição de revisão | 10% | Evidência: limiar de revisão; insuficiente: política permanente sem gatilho. |

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

Considere três logs anonimizados, taxa de `5xx`, traces parciais e a política atual; não inclua dado clínico na entrega.

**Insumos disponíveis**

As amostras do caso e os arquivos declarativos indicados.

**Como conduzir**

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

Considere consumidores parcialmente identificados, suporte em horário comercial e meta de latência para consultas aceitas.

**Insumos disponíveis**

Pico, capacidade, risco de atraso e alternativas IP, credencial e fila.

**Como conduzir**

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

**Como conduzir**

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
