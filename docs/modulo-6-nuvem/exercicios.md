# Exercícios: decidir e operar capacidade

As atividades usam a plataforma hospitalar e dados sintéticos. Não existe resposta única: declare contexto, limite e evidência necessária. Não inclua identificadores de pacientes, credenciais ou informação clínica em capturas e entregas.

## Recordar

### Nomear fronteiras de serviço

**Situação**

Uma equipe usa “nuvem”, “Kubernetes” e “PaaS” como sinônimos ao discutir a API de elegibilidade.

**Seu papel**

Você prepara um glossário de revisão.

**Insumos disponíveis**

As páginas do módulo e os manifests do laboratório.

**Como conduzir**

1. Defina IaaS, PaaS, SaaS e on-premise.

<details>
<summary>Ver resposta</summary>

IaaS entrega infraestrutura virtualizada; PaaS entrega runtime operado; SaaS entrega produto configurável; on-premise mantém infraestrutura sob maior responsabilidade interna. Nenhum modelo elimina o owner de dados, configuração e continuidade.
</details>

2. Diferencie região, zona, contêiner, imagem e orquestração.

<details>
<summary>Ver resposta</summary>

Região e zona delimitam localização e falha; imagem é o pacote versionado; contêiner é sua execução; orquestração reconcilia execuções com o estado declarado.
</details>

3. Explique readiness, liveness, elasticidade, resiliência e rollback. Para cada termo, relacione uma decisão ou arquivo do caso.

<details>
<summary>Ver resposta</summary>

Readiness controla tráfego, liveness permite reiniciar processo travado, elasticidade ajusta capacidade, resiliência mede continuidade e rollback retorna uma revisão compatível. Os manifests e a oficina fornecem as evidências locais.
</details>

**Entrega esperada**

Uma tabela de duas colunas: definição curta e exemplo/limite hospitalar.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Definições precisas | 50% | Evidência: definição e exemplo; insuficiente: termo apenas repetido. |
| Relação com o caso | 30% | Evidência: exemplo hospitalar; insuficiente: exemplo sem contexto. |
| Limites explicitados | 20% | Evidência: limite declarado; insuficiente: nuvem tratada como solução total. |

## Compreender

### Explicar probes sem analogia enganosa

**Situação**

Alguém propõe usar a mesma chamada ao banco para liveness e readiness porque “se o banco cair, a API morreu”.

**Seu papel**

Você explica o efeito dessa proposta a quem opera o cluster.

**Insumos disponíveis**

Os endpoints `/health/live` e `/health/ready`, a definição de Service e o Deployment.

**Como conduzir**

1. Descreva o que acontece quando readiness falha.

<details>
<summary>Ver resposta</summary>

O Pod pode continuar em execução, mas o Service deixa de encaminhar tráfego a ele; isso não confirma que a regra de negócio está correta.
</details>

2. Descreva o que acontece quando liveness falha e quando a dependência compartilhada está indisponível.

<details>
<summary>Ver resposta</summary>

Falha de liveness permite reinício do contêiner. Se uma dependência remota cai, usá-la como liveness pode reiniciar todas as réplicas e ampliar o incidente; ela deve orientar readiness ou degradação conforme o contrato.
</details>

3. Diferencie processo vivo, pronto para tráfego e resposta de negócio correta. Explique por que reiniciar todas as réplicas pode piorar o incidente.

<details>
<summary>Ver resposta</summary>

Vivo significa processo executando; pronto significa elegível ao tráfego; correto requer validação de negócio. Reinícios coletivos removem capacidade enquanto a dependência externa ainda está indisponível.
</details>

**Entrega esperada**

Uma sequência de no máximo 400 palavras e um diagrama de estado simples.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Semântica correta de probes | 40% | Evidência: readiness e liveness distintos; insuficiente: probes equivalentes. |
| Cenário de falha coerente | 35% | Evidência: falha e reação; insuficiente: reinício sem causa. |
| Limites reconhecidos | 25% | Evidência: dependência externa citada; insuficiente: probe promete recuperação total. |

## Aplicar

### Preparar uma implantação local reproduzível

**Objetivo**

Demonstrar implantação local descartável com evidências.

**Situação**

Outro grupo precisa demonstrar a API sem provedor remoto, usando Docker, kind, kubectl e o laboratório.

**Seu papel**

Você produz o roteiro operacional mínimo.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/Dockerfile`, `infra/kind/cluster.yaml`, `infra/k8s/deployment.yaml` e `infra/k8s/service.yaml`. Eles definem imagem, cluster, réplicas e probes.

**Antes de executar**

O estado inicial não usa `hospital-local`, não aplicou manifests e mira `kind-hospital-local`. Crie `<raiz-do-clone>/entregas/modulo-6/`; confirme versões e contexto. Não use cluster compartilhado.

**O que fazer**

1. Registre no roteiro as versões e o contexto esperado `kind-hospital-local`.
2. Em `<raiz-do-clone>/laboratorios/plataforma-hospitalar`, construa `hospital-api:1.0.0`, crie `hospital-local` por `infra/kind/cluster.yaml` e carregue a imagem.
3. Faça dry-run, aplique namespace/manifests e acompanhe rollout.
4. Faça port-forward para `127.0.0.1:18080`, consulte `/health/ready` e guarde pods/endpoints com duas réplicas.
5. Salve em `<raiz-do-clone>/entregas/modulo-6/aplicar-implantacao-local.md` e remova o cluster.
6. Se kind, Docker ou porta falhar, não use outro cluster: rode o teste de manifests e registre o desvio.

**Evidência esperada**

Versões/contexto, imagem, `2/2` réplicas, `200` de `/health/ready`, endpoints e limpeza. Na contingência, teste de manifests substitui o cluster.

**Entrega esperada**

Um roteiro por plataforma, saída esperada e checklist de evidências em `<raiz-do-clone>/entregas/modulo-6/aplicar-implantacao-local.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Reprodutibilidade e contexto seguro | 25% | Evidência: versões e dados sintéticos; insuficiente: passo depende de máquina oculta. |
| Sequência de imagem, cluster e apply | 25% | Evidência: ordem registrada; insuficiente: recursos aplicados sem namespace. |
| Evidência observável | 25% | Evidência: saída ou status; insuficiente: implantação sem prova. |
| Limpeza e contingência | 25% | Evidência: remoção limitada; insuficiente: comando global perigoso. |

<!-- Compatibilidade editorial: **Insumos disponíveis** e **Como conduzir** foram substituídos pelos campos auto-contidos acima. -->

## Analisar

### Investigar uma atualização que não termina

**Objetivo**

Separar sinal, hipótese e contenção sem tocar em ambiente compartilhado.

**Situação**

Após mudança de imagem, há `ImagePullBackOff`, duas réplicas antigas, revisão anterior e readiness; sem alteração de banco.

**Seu papel**

Você conduz a análise sem assumir que cada erro é “Kubernetes”.

**Artefato que você irá usar**

Use `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/k8s/deployment.yaml` e `infra/kind/cluster.yaml`. Registre pods, describe e histórico em `<raiz-do-clone>/entregas/modulo-6/analisar-rollout-bloqueado.md`.

**Antes de executar**

O estado inicial tem duas réplicas antigas prontas, imagem nova ausente e sem alteração de banco. Use saídas sintéticas ou `kind-hospital-local`; não altere Deployment compartilhado.

**O que fazer**

1. Escreva linha do tempo: fatos, inferências e hipóteses.
2. Compare `ImagePullBackOff`, tag, credencial e readiness.
3. Relacione `maxUnavailable: 0` a impacto, não correção.
4. Defina condição e saídas para rollback.
5. Proponha teste de imagem/manifest no pipeline.
6. Se sinais não distinguirem causa, preserve revisão e peça saída faltante; não faça rollback.

**Evidência esperada**

Linha do tempo, `ImagePullBackOff`, revisão, saídas antes/depois e barreira executável; se insuficiente, registre “rollback não executado”.

**Entrega esperada**

Uma linha do tempo, tabela de hipóteses/evidências e plano de contenção em `<raiz-do-clone>/entregas/modulo-6/analisar-rollout-bloqueado.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Separação entre fato e hipótese | 25% | Evidência: hipótese rotulada; insuficiente: suposição como incidente confirmado. |
| Diagnóstico diferencial | 25% | Evidência: causas comparadas; insuficiente: primeiro sintoma define causa. |
| Uso correto de rollout e rollback | 25% | Evidência: estado e retorno; insuficiente: rollback usado sem falha observada. |
| Prevenção verificável | 25% | Evidência: controle testável; insuficiente: recomendação sem teste. |

<!-- Compatibilidade editorial: **Insumos disponíveis** e **Como conduzir** foram substituídos pelos campos auto-contidos acima. -->

## Avaliar

### Escolher uma plataforma para uma nova capacidade

**Objetivo**

Justificar modelo de serviço por responsabilidade, dados, custo e operação.

**Situação**

O hospital criará portal de consultas: poucas APIs, equipe pequena, residência de dados, picos previsíveis e possível SaaS de mensagens; cluster não é competência consolidada.

**Seu papel**

Você recomenda IaaS, PaaS, Kubernetes gerenciado ou integração prioritária com SaaS, com condições de revisão.

**Artefato que você irá usar**

Use `<raiz-do-clone>/docs/modulo-6-nuvem/conceitos.md`, `<raiz-do-clone>/docs/modulo-6-nuvem/padroes-e-decisoes.md` e `<raiz-do-clone>/docs/referencia/template-adr.md`, além da estimativa sintética de picos, requisitos de disponibilidade, contrato de dados, capacidade da equipe e custo mensal. Escreva em `<raiz-do-clone>/entregas/modulo-6/avaliar-plataforma.md`.

**Antes de executar**

O estado inicial não tem provedor/cluster: residência, picos e equipe são fatos. Crie o ADR; AWS, iFood e Taco Bell são apenas comparações.

**O que fazer**

1. Compare IaaS, PaaS, Kubernetes gerenciado e SaaS por responsabilidade, elasticidade, recuperação, custo e lock-in.
2. Marque fato/hipótese, região, zonas e exportação.
3. Registre decisão, consequências e dois gatilhos.
4. Se residência ou exportação não estiver comprovada, bloqueie a alternativa.

**Evidência esperada**

O ADR inclui matriz preenchida, estimativa de custo operacional, plano de exportação, domínio de falha e dois gatilhos mensuráveis. A saída nomeia alternativas bloqueadas e a evidência ausente que permitiria reavaliá-las.

**Entrega esperada**

Um ADR com alternativas, decisão, consequências, riscos, custo e sinais de revisão em `<raiz-do-clone>/entregas/modulo-6/avaliar-plataforma.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação contextual | 25% | Evidência: requisito por opção; insuficiente: provedor escolhido por fama. |
| Responsabilidade e dados | 20% | Evidência: responsabilidade declarada; insuficiente: dado delegado sem controle. |
| Custo e lock-in | 20% | Evidência: custo e saída; insuficiente: serviço assumido neutro. |
| Resiliência e operação | 20% | Evidência: falha e operação; insuficiente: réplica tratada como garantia. |
| Gatilhos mensuráveis | 15% | Evidência: limiar definido; insuficiente: revisão sem medida. |

<!-- Compatibilidade editorial: **Insumos disponíveis** e **Como conduzir** foram substituídos pelos campos auto-contidos acima. -->

## Criar

### Desenhar evolução resiliente de elegibilidade

**Objetivo**

Projetar evolução com estado, recuperação e limites verificáveis.

**Situação**

A API terá armazenamento e notificação assíncrona; a equipe quer atualização gradual, região inicial e expansão futura sem prometer recuperação não testada.

**Seu papel**

Você cria uma proposta arquitetural e operacional.

**Artefato que você irá usar**

Use `<raiz-do-clone>/docs/modulo-6-nuvem/exemplo-arquitetural.md`, `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/k8s/deployment.yaml`, `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/k8s/service.yaml` e `<raiz-do-clone>/laboratorios/plataforma-hospitalar/infra/kind/cluster.yaml`, com requisitos de retenção, SLO proposto e carga sintética. Crie o pacote em `<raiz-do-clone>/entregas/modulo-6/criar-evolucao-resiliente.md`.

**Antes de executar**

O estado inicial não tem dados reais ou backup restaurado. Use kind local, não dependência externa; declare o que rollback não desfaz.

**O que fazer**

1. Desenhe componentes, owner, região/zona e falhas.
2. Escreva pseudomanifests com fatores, requests/limits e probes.
3. Defina rollout, rollback, backup/restore e saídas.
4. Meça elasticidade/custo com carga sintética.
5. Teste falha só em `kind-hospital-local` e registre aceite/rejeição.
6. Se backup/restore não for localmente testável, mantenha risco aberto.

**Evidência esperada**

O pacote contém diagrama acessível, ADR, pseudomanifests, saída esperada de rollout e rollback, medição de custo/elasticidade e resultado ou limitação explícita do backup/restore. A evidência precisa mostrar a contingência quando o teste não puder ser executado.

**Entrega esperada**

Um pacote com diagrama, ADR, manifests ou pseudomanifests, plano de evidências e registro de riscos em `<raiz-do-clone>/entregas/modulo-6/criar-evolucao-resiliente.md`.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Fronteiras e estado explícitos | 25% | Evidência: recurso e responsabilidade; insuficiente: estado sem dono. |
| Resiliência e recuperação testáveis | 25% | Evidência: falha e recuperação; insuficiente: resiliência só declarada. |
| Operação, custo e segurança | 25% | Evidência: trade-off registrado; insuficiente: operação omitida. |
| Clareza de evidências e limites | 25% | Evidência: limites e prova; insuficiente: conclusão sem contexto. |

<!-- Compatibilidade editorial: **Insumos disponíveis** e **Como conduzir** foram substituídos pelos campos auto-contidos acima. -->
