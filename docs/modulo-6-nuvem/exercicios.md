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

Defina IaaS, PaaS, SaaS, responsabilidade compartilhada, região, zona, contêiner, imagem, orquestração, readiness, liveness, elasticidade, resiliência e rollback. Para cada termo, relacione uma decisão ou arquivo do caso.

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

Descreva o que acontece quando readiness falha, quando liveness falha e quando a dependência compartilhada está indisponível. Diferencie processo vivo, pronto para tráfego e resposta de negócio correta. Explique por que reiniciar todas as réplicas pode piorar o incidente.

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

**Situação**

Outro grupo precisa demonstrar a API hospitalar sem acesso a provedor remoto. Ele possui Docker, kind, kubectl e os arquivos do laboratório.

**Seu papel**

Você produz o roteiro operacional mínimo.

**Insumos disponíveis**

`Dockerfile`, manifests, `cluster.yaml` e os endpoints de saúde.

**Como conduzir**

1. Liste as verificações de versão e o contexto esperado.
2. Construa `hospital-api:1.0.0`, crie `hospital-local` e carregue a imagem.
3. Execute dry-run, apply, rollout status e chamada a `127.0.0.1:18080`.
4. Mostre uma evidência de duas réplicas e uma de endpoints prontos.
5. Inclua limpeza do cluster e o caminho estático caso kind não funcione.

**Entrega esperada**

Um roteiro por plataforma, saída esperada e checklist de evidências.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Reprodutibilidade e contexto seguro | 25% | Evidência: versões e dados sintéticos; insuficiente: passo depende de máquina oculta. |
| Sequência de imagem, cluster e apply | 25% | Evidência: ordem registrada; insuficiente: recursos aplicados sem namespace. |
| Evidência observável | 25% | Evidência: saída ou status; insuficiente: implantação sem prova. |
| Limpeza e contingência | 25% | Evidência: remoção limitada; insuficiente: comando global perigoso. |

## Analisar

### Investigar uma atualização que não termina

**Situação**

Após mudança de imagem, o Deployment mostra progresso incompleto. Existem eventos `ImagePullBackOff`, duas réplicas antigas prontas, revisão anterior e resposta local de readiness. Não há alteração de banco nessa versão.

**Seu papel**

Você conduz a análise sem assumir que cada erro é “Kubernetes”.

**Insumos disponíveis**

Saídas de `kubectl get pods`, `kubectl describe deployment`, histórico do rollout e manifest versionado.

**Como conduzir**

1. Separe fatos, inferências e hipóteses.
2. Compare tag inexistente, falta de credencial de registry e readiness que falha após iniciar.
3. Explique por que `maxUnavailable: 0` limita impacto, mas não corrige a causa.
4. Declare quando `kubectl rollout undo` é seguro no cenário e o que você verificaria depois.
5. Proponha barreira de pipeline que reduza recorrência.

**Entrega esperada**

Uma linha do tempo, tabela de hipóteses/evidências e plano de contenção.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Separação entre fato e hipótese | 25% | Evidência: hipótese rotulada; insuficiente: suposição como incidente confirmado. |
| Diagnóstico diferencial | 25% | Evidência: causas comparadas; insuficiente: primeiro sintoma define causa. |
| Uso correto de rollout e rollback | 25% | Evidência: estado e retorno; insuficiente: rollback usado sem falha observada. |
| Prevenção verificável | 25% | Evidência: controle testável; insuficiente: recomendação sem teste. |

## Avaliar

### Escolher uma plataforma para uma nova capacidade

**Situação**

O hospital criará um portal de confirmação de consultas. Há poucas APIs próprias, uma equipe pequena, exigência de residência de dados, picos semanais previsíveis e integração possível com um SaaS de mensagens. A operação de cluster ainda não é competência consolidada.

**Seu papel**

Você recomenda IaaS, PaaS, Kubernetes gerenciado ou integração prioritária com SaaS, com condições de revisão.

**Insumos disponíveis**

Estimativa de picos, requisitos de disponibilidade, contrato de dados, capacidade da equipe e custo mensal por alternativa.

**Como conduzir**

Compare responsabilidade compartilhada, elasticidade, recuperação, custo direto/operacional e lock-in. Separe requisito confirmado de hipótese. Inclua região, zonas e exportação de dados. Defina dois gatilhos mensuráveis que fariam a equipe reavaliar a escolha.

**Entrega esperada**

Um ADR com alternativas, decisão, consequências, riscos, custo e sinais de revisão.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Comparação contextual | 25% | Evidência: requisito por opção; insuficiente: provedor escolhido por fama. |
| Responsabilidade e dados | 20% | Evidência: responsabilidade declarada; insuficiente: dado delegado sem controle. |
| Custo e lock-in | 20% | Evidência: custo e saída; insuficiente: serviço assumido neutro. |
| Resiliência e operação | 20% | Evidência: falha e operação; insuficiente: réplica tratada como garantia. |
| Gatilhos mensuráveis | 15% | Evidência: limiar definido; insuficiente: revisão sem medida. |

## Criar

### Desenhar evolução resiliente de elegibilidade

**Situação**

A API terá armazenamento durável e uma integração assíncrona para notificar agenda. A equipe quer manter atualização gradual, uma região inicial e possibilidade de expansão futura, sem prometer recuperação regional que ainda não testou.

**Seu papel**

Você cria uma proposta arquitetural e operacional.

**Insumos disponíveis**

O caso do módulo, requisitos de retenção, SLO proposto, dados de carga sintética e o laboratório Kubernetes.

**Como conduzir**

Desenhe componentes stateful e stateless, declare ownership de dados, região/zona e domínios de falha. Inclua configuração segundo os doze fatores, requests/limits iniciais, probes, estratégia de rollout, procedimento de rollback e plano de backup/restore. Descreva como medir elasticidade e custo. Termine com teste de falha seguro e condição para aceitar ou rejeitar a proposta.

**Entrega esperada**

Um pacote com diagrama, ADR, manifests ou pseudomanifests, plano de evidências e registro de riscos.

**Critérios de avaliação**

| Critério | Percentual | Evidência e insuficiência |
| --- | ---: | --- |
| Fronteiras e estado explícitos | 25% | Evidência: recurso e responsabilidade; insuficiente: estado sem dono. |
| Resiliência e recuperação testáveis | 25% | Evidência: falha e recuperação; insuficiente: resiliência só declarada. |
| Operação, custo e segurança | 25% | Evidência: trade-off registrado; insuficiente: operação omitida. |
| Clareza de evidências e limites | 25% | Evidência: limites e prova; insuficiente: conclusão sem contexto. |
