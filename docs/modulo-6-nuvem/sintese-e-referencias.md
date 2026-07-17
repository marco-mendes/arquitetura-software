# Síntese e referências

## Síntese para revisão

Nuvem é uma escolha de obtenção e operação de capacidade. IaaS entrega infraestrutura virtualizada; PaaS entrega uma plataforma operada; SaaS entrega software configurável. A responsabilidade compartilhada não deixa lacuna: identidade, classificação de dados, configuração, disponibilidade desejada e continuidade precisam de owner. Região e zona ajudam a modelar localização e domínio de falha, mas uma réplica extra no mesmo nó não prova tolerância a falha regional.

Contêiner empacota uma execução; Docker constrói e executa imagens; Kubernetes orquestra estado desejado, rede e réplicas. Stateless facilita substituir réplicas porque o estado relevante vive em recurso externo com política explícita. Stateful exige identidade, persistência, ordem, backup e recuperação próprios. Os doze fatores orientam configuração, processos, dependências, logs e ciclo de entrega; não substituem segurança ou decisões de domínio.

Elasticidade só existe quando métrica, capacidade e limites suportam ajuste. Requests e limits tornam pressupostos de recurso auditáveis; HPA é política que depende de métricas e não uma garantia de desempenho. Resiliência combina isolamento de falha, probes, rollout, observação e recuperação. Readiness retira instância do tráfego; liveness detecta processo travado. Rollback restaura uma revisão, mas não apaga efeitos irreversíveis nem substitui migração compatível.

Custo inclui recursos, tráfego, retenção, observabilidade e operação. Lock-in deve ser assumido de modo informado: serviços gerenciados podem reduzir risco com grande valor, desde que contratos, exportação, habilidades e custo de saída sejam conhecidos. A pergunta útil permanece: que atributo queremos melhorar, que decisão o materializa e qual evidência poderá refutá-la?

## Equivalências em Java e .NET

| Ideia do módulo | Java | .NET |
| --- | --- | --- |
| Imagem de aplicação | [Jib](https://github.com/GoogleContainerTools/jib) ou Dockerfile para Spring Boot | Dockerfile para ASP.NET Core ou `dotnet publish` em contêiner |
| Health endpoints | Spring Boot Actuator liveness/readiness | ASP.NET Core Health Checks |
| Configuração por ambiente | Spring externalized configuration | `IConfiguration` e variáveis de ambiente |
| Kubernetes client e manifests | Fabric8 Kubernetes Client ou manifests | KubernetesClient ou manifests |
| Limites e rollout | `Deployment`, `Service`, `HPA` iguais | `Deployment`, `Service`, `HPA` iguais |

O runtime muda, mas as responsabilidades não. Em Java, um endpoint de Actuator ainda precisa de semântica correta; em .NET, Health Checks não escolhem dependências sem uma decisão da equipe. A portabilidade mais importante é preservar contrato, evidência e procedimento de recuperação em qualquer linguagem.

## Fontes públicas para aprofundar

- [NIST: The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final) define características e modelos de serviço de nuvem.
- [Kubernetes: Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) explica atualizações, revisões e rollback.
- [Kubernetes: probes de liveness, readiness e startup](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/) descreve a semântica e as consequências das probes.
- [Kubernetes: Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) documenta métricas, requests e comportamento do HPA.
- [kind: quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) descreve clusters Kubernetes locais e carregamento de imagens.
- [Docker: imagens](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/) explica a distinção entre imagem e contêiner.
- [The Twelve-Factor App](https://12factor.net/) apresenta as doze práticas para aplicações entregues como serviço.

## Perguntas de saída

Que modelo de serviço reduz risco para esta capacidade e qual responsabilidade permanece? Que estado pode desaparecer com um Pod e que estado exige recuperação? Em qual região e zona a falha realmente está isolada? O que readiness e liveness significam neste runtime? Há capacidade de retorno sem dano de dados? Como o custo cresce com tráfego, logs e redundância? Qual dependência aceita lock-in e como seria exportada? Se uma resposta não vier acompanhada de manifest, teste, métrica, contrato ou procedimento, ela ainda é uma hipótese.
