# Padrões e decisões: capacidade sem ilusões

## Stateless, stateful e os doze fatores

Uma aplicação **stateless** não mantém, no processo de uma réplica, o único estado necessário para atender a próxima requisição. Sessão, arquivo temporário relevante e fila local precisam ter destino explícito: token assinado, cache compartilhado, banco ou armazenamento de objeto. Isso permite substituir um Pod sem perder a conversa por acidente. Stateless não significa “sem dados”. O estado durável fica fora da instância descartável e tem owner, política de consistência e recuperação.

Uma aplicação **stateful** conserva identidade ou estado ligado à réplica: banco, nó de fila, volume ou processo com sequência. Ela pode rodar em Kubernetes, mas exige decisões adicionais sobre volume, ordem, quorum, backup, restore e atualização. Forçar banco relacional a parecer stateless só desloca o risco para um volume sem estratégia. Para a API de elegibilidade, o armazenamento em memória é deliberadamente didático: no laboratório a API é tratada como stateless e os dados não sobrevivem à troca de Pod. Produção exigiria um store externo e teste de recuperação.

Os **doze fatores** são heurísticas para aplicações entregues como serviço: uma base de código, dependências declaradas, configuração no ambiente, backing services tratados como recursos anexados, build/release/run separados, processos sem estado, portas exportadas, concorrência por processos, inicialização e desligamento rápidos, paridade entre ambientes, logs como fluxo e tarefas administrativas descartáveis. Eles não substituem análise de domínio. A regra de configuração, por exemplo, não autoriza pôr segredo em ConfigMap. Para isso há mecanismo próprio e controle de acesso.

## Elasticidade e escalabilidade

**Escalabilidade** é a capacidade de crescer mantendo comportamento aceitável. **Elasticidade** é ajustar capacidade em resposta a demanda. Escalar horizontalmente aumenta réplicas. Escalar verticalmente muda recursos da mesma réplica. O HPA do laboratório declara mínimo de duas e máximo de cinco réplicas, com alvo de CPU. Isso é uma política, não uma prova: a métrica deve existir, o request de CPU deve ser definido e a equipe precisa observar latência, fila, erro e saturação para confirmar que CPU é um sinal útil.

Cada réplica tem request de `100m` de CPU e `128Mi` de memória: são insumos para agendamento. Os limits de `250m` e `256Mi` estabelecem teto. CPU pode sofrer throttling, e memória excedida pode resultar em término. Escolher números por hábito é pior que não declarar hipótese. Comece com uma carga sintética, registre consumo e latência, ajuste e repita. A capacidade de banco, conexão e dependências também limita a escala. Aumentar somente a API pode amplificar uma falha posterior.

**Texto alternativo:** uma métrica disponível alimenta o HPA, que altera réplicas no Deployment. Essas réplicas ainda dependem de serviços que podem se tornar o próximo gargalo.

*Figura 8 — Escala da API limitada por suas dependências. Fonte: curso.*

```mermaid
flowchart LR
    M[Métrica disponível] --> H[HPA]
    H -->|aumenta ou reduz| D[Deployment]
    D --> P[Pods]
    P --> X[Dependências: banco, API, fila]
    X -. limite pode migrar .-> P
```

**Leitura textual da figura:** uma métrica alimenta o HPA, que ajusta Pods pelo Deployment. Novas réplicas ainda dependem de banco, APIs e filas. Se uma delas saturar, a elasticidade da camada web pode apenas deslocar o gargalo.

## Resiliência, rollout e rollback

Resiliência é continuar ou recuperar serviço dentro de um objetivo explícito diante de falhas. Réplicas reduzem impacto de queda de um Pod. Readiness impede que uma instância ainda não pronta receba tráfego. O rollout com `maxUnavailable: 0` preserva capacidade desejada durante atualização. Isso não garante ausência de erro: uma versão logicamente inválida pode responder saúde e ainda produzir decisão errada. Por isso, health check, teste de contrato, telemetria e revisão de mudança são complementares.

Um **rollback** retorna o Deployment à revisão anterior. Ele é útil se existe uma versão anterior saudável, mas não desfaz efeitos irreversíveis em banco, mensagens ou integrações. A migração de dados deve ter compatibilidade de ida e volta ou procedimento separado. Na oficina, a falha é segura: muda-se somente a imagem para uma tag propositalmente ausente. Os novos Pods ficam indisponíveis, e `kubectl rollout undo` restaura a imagem local conhecida. Não se altera dado hospitalar.

## Orquestradores: Swarm e Kubernetes

Orquestrar contêineres é automatizar cinco responsabilidades que, feitas à mão, não sobrevivem à escala. Gerenciar muitos contêineres distribuídos entre máquinas. Aumentar ou reduzir instâncias conforme a demanda. Distribuir carga entre os serviços. Monitorar e reiniciar o que falhou. Repartir recursos entre os nós de um cluster. Um orquestrador é a peça que transforma essas cinco em configuração declarada.

Duas opções aparecem com frequência, e elas não têm o mesmo peso operacional.

O **Docker Swarm** é a orquestração nativa do Docker e usa o mesmo vocabulário de quem já constrói imagens.

![Cluster Docker Swarm com três nós gerenciadores num grupo de consenso Raft sobre um repositório de estado distribuído, e sete nós trabalhadores numa rede gossip.](https://github.com/user-attachments/assets/8cc1d428-9e49-4755-8765-ff5c1dc0f869)

*Figura 13 — Como o Swarm reparte decisão e execução entre nós. Fonte: Docker.*

**Leitura textual da figura:** na parte de cima, uma área tracejada rotulada como grupo de consenso Raft contém três nós gerenciadores, ligados entre si, e um repositório interno de estado distribuído que os três compartilham. Na parte de baixo, outra área tracejada rotulada como rede gossip contém sete nós trabalhadores. Setas de mão dupla ligam cada trabalhador a gerenciadores diferentes, sem que um trabalhador dependa de um gerenciador específico. A decisão sobre o estado desejado vive no grupo de consenso, e a execução vive nos trabalhadores.

Na prática, `docker swarm init` transforma um host em nó gerenciador e devolve um token de adesão. `docker swarm join` liga trabalhadores ao cluster, e `docker node ls` lista os nós com seu papel. Um serviço replicado nasce com `docker service create --name webserver -p 8080:80 --replicas 3 nginx`, e `docker service ps webserver` mostra em qual nó cada réplica está. Sair do cluster é `docker swarm leave --force`.

O **Kubernetes** paga um custo operacional maior e entrega um modelo de extensão bem mais amplo.

![Cluster Kubernetes com o plano de controle contendo servidor de API, etcd, escalonador e gerenciadores de controladores, e três nós de trabalho com kubelet e kube-proxy.](https://github.com/user-attachments/assets/39f5105e-6892-4248-8ef6-106af52f6e71)

*Figura 14 — Os componentes que sustentam a reconciliação em um cluster Kubernetes. Fonte: Kubernetes.*

**Leitura textual da figura:** uma área tracejada à esquerda delimita o plano de controle e contém o servidor de API ao centro, o etcd como repositório de persistência, o escalonador, o gerenciador de controladores e o gerenciador de controladores de nuvem, este último ligado por uma seta à API do provedor de nuvem. À direita, três nós de trabalho aparecem lado a lado, cada um com um kubelet e um kube-proxy. Setas partem dos nós em direção ao servidor de API, que concentra as leituras e escritas do estado. Nenhum componente conversa com o etcd diretamente, exceto o servidor de API.

A escolha entre os dois segue o mesmo critério das demais decisões deste módulo. Para poucas cargas e uma equipe pequena, o Swarm entrega replicação e balanceamento com um custo de aprendizado baixo. Para muitas cargas que precisam de políticas comuns, extensões e controle fino de rollout, o Kubernetes justifica a operação. A oficina deste módulo usa kind, que é Kubernetes local e descartável, justamente para tornar a reconciliação observável sem contratar um cluster gerenciado.

## Custo e lock-in

Custo inclui recursos ociosos, armazenamento, tráfego, observabilidade, suporte, licenças, operação e teste de continuidade. “Pague pelo uso” não significa custo baixo quando um recurso nunca reduz, logs crescem sem retenção ou uma saída de dados é frequente. Etiquetas de custo, orçamento, limite de ambiente e decisão de desligamento são arquitetura. Um SLO mais exigente pode justificar redundância. A justificativa deve mostrar valor e custo marginal.

**Lock-in** é a dificuldade de trocar ou negociar uma dependência, técnica ou organizacional. Serviços gerenciados podem ser escolhas excelentes quando reduzem risco operacional, mas ficam explícitos no ADR: API proprietária, formato de dados, identidade, observabilidade, egress e habilidades da equipe. Abstrair tudo prematuramente cria uma plataforma paralela. Prefira contratos de domínio, exportação testada, infraestrutura declarativa e uma condição mensurável de saída. Aceite lock-in quando o benefício específico é conhecido e revisável.
