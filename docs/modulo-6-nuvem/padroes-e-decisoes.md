# Padrões e decisões: capacidade sem ilusões

## Stateless, stateful e os doze fatores

Uma aplicação **stateless** não mantém, no processo de uma réplica, o único estado necessário para atender a próxima requisição. Sessão, arquivo temporário relevante e fila local precisam ter destino explícito: token assinado, cache compartilhado, banco ou armazenamento de objeto. Isso permite substituir um Pod sem perder a conversa por acidente. Stateless não significa “sem dados”. O estado durável fica fora da instância descartável e tem owner, política de consistência e recuperação.

Uma aplicação **stateful** conserva identidade ou estado ligado à réplica: banco, nó de fila, volume ou processo com sequência. Ela pode rodar em Kubernetes, mas exige decisões adicionais sobre volume, ordem, quorum, backup, restore e atualização. Forçar banco relacional a parecer stateless só desloca o risco para um volume sem estratégia. Para a API de elegibilidade, o armazenamento em memória é deliberadamente didático: no laboratório a API é tratada como stateless e os dados não sobrevivem à troca de Pod. Produção exigiria um store externo e teste de recuperação.

### Os doze fatores

Os **doze fatores** são um conjunto de heurísticas para aplicações entregues como serviço, publicado por Adam Wiggins em 2011 a partir da operação da plataforma Heroku. O texto de referência está em [12factor.net](https://12factor.net/pt_br/), com tradução para português, e cada fator tem sua própria página. A lista abaixo traz o nome do fator, o que ele exige e a consequência prática de ignorá-lo num ambiente de nuvem.

| Fator | O que exige | Consequência de ignorar |
| --- | --- | --- |
| [1. Base de código](https://12factor.net/pt_br/codebase) | uma base de código versionada, com muitos deploys | não se sabe qual código está em produção |
| [2. Dependências](https://12factor.net/pt_br/dependencies) | declarar e isolar dependências explicitamente | a aplicação funciona numa máquina e falha em outra |
| [3. Configurações](https://12factor.net/pt_br/config) | guardar configuração no ambiente, fora do código | promover uma versão entre ambientes exige recompilar |
| [4. Serviços de apoio](https://12factor.net/pt_br/backing-services) | tratar banco, fila e cache como recursos anexados | trocar uma dependência vira mudança de código |
| [5. Build, release, run](https://12factor.net/pt_br/build-release-run) | separar estritamente as três etapas | não há artefato para retornar num rollback |
| [6. Processos](https://12factor.net/pt_br/processes) | executar a aplicação como processos sem estado | substituir uma réplica perde a sessão do usuário |
| [7. Vínculo de portas](https://12factor.net/pt_br/port-binding) | exportar o serviço por vínculo de porta | a aplicação depende de um servidor externo já instalado |
| [8. Concorrência](https://12factor.net/pt_br/concurrency) | escalar horizontalmente pelo modelo de processos | crescer exige máquina maior em vez de mais réplicas |
| [9. Descartabilidade](https://12factor.net/pt_br/disposability) | iniciar rápido e desligar de forma limpa | cada implantação derruba requisições em andamento |
| [10. Paridade dev/prod](https://12factor.net/pt_br/dev-prod-parity) | manter ambientes o mais parecidos possível | o erro só aparece em produção |
| [11. Logs](https://12factor.net/pt_br/logs) | tratar logs como fluxo de eventos | o diagnóstico morre junto com o contêiner |
| [12. Processos administrativos](https://12factor.net/pt_br/admin-processes) | rodar tarefas administrativas como processos efêmeros | a migração de schema roda de dentro de uma réplica viva |

Quatro fatores explicam boa parte do que este módulo pratica. O sexto, processos sem estado, é o que torna a substituição de réplica segura. O terceiro, configuração no ambiente, é o que permite promover a mesma imagem entre ambientes. O quinto, separação entre build, release e run, é o que dá ao rollback uma revisão anterior para onde voltar. O nono, descartabilidade, é o que faz a atualização gradual não derrubar requisições em andamento.

Eles não substituem análise de domínio nem decisão de segurança. A regra de configuração, por exemplo, não autoriza pôr segredo em ConfigMap. Para isso há mecanismo próprio e controle de acesso.

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

## Os seis Rs da modernização

As decisões acima valem para uma aplicação que já se decidiu levar para a nuvem. Antes disso vem outra pergunta, e ela se aplica a cada aplicação do portfólio separadamente: o que fazer com esta aqui? O vocabulário mais usado para responder é o dos **seis Rs**, na formulação da [Microsoft App Modernization Guidance](https://learn.microsoft.com/pt-br/azure/app-modernization-guidance/plan/the-6-rs-of-application-modernization), que por sua vez estende os [cinco Rs de racionalização](https://learn.microsoft.com/pt-br/azure/cloud-adoption-framework/digital-estate/5-rs-of-rationalization) usados em migração.

| R | O que significa | Esforço | Sinal de que é este |
| --- | --- | --- | --- |
| **Rehost** | mover sem alterar código, também chamado de *lift and shift* | baixo | prazo curto, aplicação estável, ganho esperado é sair do data center |
| **Replatform** | mover para uma plataforma de execução nova com alterações mínimas de código, o *lift, tinker and shift* | baixo a médio | trocar o banco por um gerenciado ou o servidor de aplicação por um runtime operado já resolve |
| **Refactor** | alterar o código existente sem mudar de forma relevante o comportamento externo | alto | o monolito atende ao negócio, mas não escala nem integra |
| **Rebuild** | recomeçar a aplicação | muito alto | o custo de replatform ou refactor supera o benefício, e há função nova a incorporar |
| **Retire** | desativar e desligar | baixo | o uso caiu, ou outra aplicação já faz o mesmo |
| **Retain** | manter como está, por ora | nenhum | custo, dependência ou risco impedem mexer agora |

Três leituras ajudam a não escolher no chute.

**Rehost e replatform** são os movimentos de entrada. Eles cabem quando a organização quer começar a usar PaaS, precisa de adoção rápida com mudança mínima em aplicações legadas críticas, tem uma aplicação pouco complexa que não exige ganho expressivo de desempenho, ou precisa preservar os arranjos existentes de identidade, segurança e conformidade sem ruptura. A recompensa é a troca de despesa de capital por despesa operacional, pagando pelo recurso que se usa.

**Refactor** é descrito pela Microsoft como atividade de alto impacto e alto esforço. Ele cabe quando é preciso melhorar desempenho, escala e integração de um monolito sem redesenhá-lo por completo, quando há recursos para uma evolução significativa de funcionalidade, ou quando segurança e governança precisam de aprimoramento. A aplicação alvo costuma ter complexidade moderada e se beneficiar de otimização de código.

**Rebuild** é para quem já tem maturidade e quer decompor monolitos em microsserviços, redesenhar a arquitetura para crescimento futuro sobre contêineres ou serverless, ou implantar controles avançados de segurança e conformidade. É o movimento mais caro e o que mais depende de agilidade organizacional.

Os dois Rs restantes costumam ser esquecidos, e são os mais baratos. **Retire** remove custo e superfície de ataque de uma vez. **Retain** é uma decisão legítima, desde que registrada com a razão e com a data de reavaliação. Manter por omissão, sem registrar, é o que transforma dívida em surpresa.

O R não é um rótulo a colar na aplicação. Ele é o resumo de uma decisão que precisa citar o atributo que se quer melhorar, a restrição que limita a escolha e a evidência que confirmará o acerto.
