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

| Critério | Peso |
| --- | ---: |
| Definições precisas | 50% |
| Relação com o caso | 30% |
| Limites explicitados | 20% |

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

| Critério | Peso |
| --- | ---: |
| Semântica correta de probes | 40% |
| Cenário de falha coerente | 35% |
| Limites reconhecidos | 25% |

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

| Critério | Peso |
| --- | ---: |
| Reprodutibilidade e contexto seguro | 25% |
| Sequência de imagem, cluster e apply | 25% |
| Evidência observável | 25% |
| Limpeza e contingência | 25% |

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

| Critério | Peso |
| --- | ---: |
| Separação entre fato e hipótese | 25% |
| Diagnóstico diferencial | 25% |
| Uso correto de rollout e rollback | 25% |
| Prevenção verificável | 25% |

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

| Critério | Peso |
| --- | ---: |
| Comparação contextual | 25% |
| Responsabilidade e dados | 20% |
| Custo e lock-in | 20% |
| Resiliência e operação | 20% |
| Gatilhos mensuráveis | 15% |

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

| Critério | Peso |
| --- | ---: |
| Fronteiras e estado explícitos | 25% |
| Resiliência e recuperação testáveis | 25% |
| Operação, custo e segurança | 25% |
| Clareza de evidências e limites | 25% |
