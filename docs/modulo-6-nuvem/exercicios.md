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

Demonstrar uma implantação descartável, delimitada à máquina do grupo e baseada em evidências.

**Situação**

Outro grupo precisa demonstrar a API hospitalar sem acesso a provedor remoto. Ele possui Docker, kind, kubectl e os arquivos do laboratório.

**Seu papel**

Você produz o roteiro operacional mínimo.

**Artefato que você irá usar**

`Dockerfile`, manifests, `cluster.yaml` e os endpoints de saúde.

**Antes de executar**

Confirme que o contexto ativo será `kind-hospital-local` antes de aplicar recursos. O kind cria um cluster local descartável; não use um cluster compartilhado como substituto.

**O que fazer**

1. Liste as verificações de versão e o contexto esperado.
2. Construa `hospital-api:1.0.0`, crie `hospital-local` e carregue a imagem.
3. Execute dry-run, apply, rollout status e chamada a `127.0.0.1:18080`.
4. Mostre uma evidência de duas réplicas e uma de endpoints prontos.
5. Inclua limpeza do cluster e o caminho estático caso kind não funcione.

**Evidência esperada**

Versões, contexto local, imagem carregada, duas réplicas prontas, resposta de readiness e confirmação de limpeza.

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

Separar sinal, hipótese e contenção de uma atualização bloqueada sem tocar em dados ou em ambiente compartilhado.

**Situação**

Após mudança de imagem, o Deployment mostra progresso incompleto. Existem eventos `ImagePullBackOff`, duas réplicas antigas prontas, revisão anterior e resposta local de readiness. Não há alteração de banco nessa versão.

**Seu papel**

Você conduz a análise sem assumir que cada erro é “Kubernetes”.

**Artefato que você irá usar**

Saídas de `kubectl get pods`, `kubectl describe deployment`, histórico do rollout e manifest versionado.

**Antes de executar**

Use somente as saídas sintéticas fornecidas e uma imagem propositalmente ausente no cluster kind local; não altere uma imagem ou Deployment compartilhado.

**O que fazer**

1. Separe fatos, inferências e hipóteses.
2. Compare tag inexistente, falta de credencial de registry e readiness que falha após iniciar.
3. Explique por que `maxUnavailable: 0` limita impacto, mas não corrige a causa.
4. Declare quando `kubectl rollout undo` é seguro no cenário e o que você verificaria depois.
5. Proponha barreira de pipeline que reduza recorrência.

**Evidência esperada**

Linha do tempo, eventos de `ImagePullBackOff`, revisão anterior identificada, justificativa do rollback e barreira de pipeline verificável.

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

Justificar um modelo de serviço por responsabilidade, dados, custo e capacidade de operação, e não pela fama de um fornecedor.

**Situação**

O hospital criará um portal de confirmação de consultas. Há poucas APIs próprias, uma equipe pequena, exigência de residência de dados, picos semanais previsíveis e integração possível com um SaaS de mensagens. A operação de cluster ainda não é competência consolidada.

**Seu papel**

Você recomenda IaaS, PaaS, Kubernetes gerenciado ou integração prioritária com SaaS, com condições de revisão.

**Artefato que você irá usar**

Estimativa de picos, requisitos de disponibilidade, contrato de dados, capacidade da equipe e custo mensal por alternativa.

**Antes de executar**

Trate AWS, iFood e Taco Bell somente como contextos comparáveis; não assuma que a plataforma ou a escala deles transfere-se ao hospital.

**O que fazer**

Compare responsabilidade compartilhada, elasticidade, recuperação, custo direto/operacional e lock-in. Separe requisito confirmado de hipótese. Inclua região, zonas e exportação de dados. Defina dois gatilhos mensuráveis que fariam a equipe reavaliar a escolha.

**Evidência esperada**

Matriz de responsabilidades, estimativa de custo operacional, plano de exportação, domínio de falha e dois gatilhos mensuráveis.

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

Projetar uma evolução que declare estado, recuperação e limites antes de prometer resiliência.

**Situação**

A API terá armazenamento durável e uma integração assíncrona para notificar agenda. A equipe quer manter atualização gradual, uma região inicial e possibilidade de expansão futura, sem prometer recuperação regional que ainda não testou.

**Seu papel**

Você cria uma proposta arquitetural e operacional.

**Artefato que você irá usar**

O caso do módulo, requisitos de retenção, SLO proposto, dados de carga sintética e o laboratório Kubernetes.

**Antes de executar**

Use dados sintéticos e mantenha a demonstração no kind local. Declare toda dependência que o rollback não consegue desfazer antes de propor o teste de falha.

**O que fazer**

Desenhe componentes stateful e stateless, declare ownership de dados, região/zona e domínios de falha. Inclua configuração segundo os doze fatores, requests/limits iniciais, probes, estratégia de rollout, procedimento de rollback e plano de backup/restore. Descreva como medir elasticidade e custo. Termine com teste de falha seguro e condição para aceitar ou rejeitar a proposta.

**Evidência esperada**

Diagrama acessível, ADR, manifestos ou pseudomanifests, sinal de rollout, procedimento de rollback e teste de backup/restore planejado.

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
