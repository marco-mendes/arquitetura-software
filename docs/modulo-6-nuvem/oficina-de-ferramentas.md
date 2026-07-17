# Oficina de ferramentas: Docker, kind e Kubernetes locais

Esta oficina cria e remove um cluster local descartável. Ela usa a imagem da API de elegibilidade, mas não envia dados, credenciais ou imagens a serviço remoto. Todos os nomes e portas são fixos: cluster `hospital-local`, namespace `hospital`, Deployment e Service `hospital-api`, porta do contêiner `8000` e acesso local `http://127.0.0.1:18080`. Não use estes comandos contra um contexto compartilhado.

## Ferramenta

| Ferramenta | Papel | Evidência observável |
| --- | --- | --- |
| Docker Engine/Desktop | construir a imagem local | `docker image inspect hospital-api:1.0.0` |
| kind | criar Kubernetes em contêineres | `kind get clusters` |
| kubectl | aplicar e observar estado declarado | rollout, Pods, eventos e Service |
| Kubernetes | reconciliar Deployment, Service e HPA | duas réplicas prontas e revisão registrada |

O repositório contém `infra/kind/cluster.yaml` e os cinco manifests em `infra/k8s`. O Service NodePort 30080 é mapeado pelo kind somente em `127.0.0.1:18080`. O HPA pode exibir `<unknown>` sem Metrics Server; isso não impede a lição sobre requests, limits e configuração declarativa.

## Pré-requisitos

### Essencial em aula

**Objetivo**

Confirmar um ambiente local antes de criar recursos.

**Pré-requisito**

Tenha Docker iniciado, `kubectl`, `kind` e Python instalados. Trabalhe na pasta `laboratorios/plataforma-hospitalar` deste repositório, onde estão imagem e manifests.

**Execute**

Verifique versões e contexto. No macOS/Linux use `docker version`, `kind version`, `kubectl version --client` e `python3 --version`. No PowerShell use `docker version`, `kind version`, `kubectl version --client` e `py --version`.

**Observe**

Docker deve mostrar Client e Server. `kubectl config current-context` pode mostrar outro contexto antes do cluster; não aplique manifest até o contexto `kind-hospital-local` existir.

**Compare**

Ter o cliente `kubectl` não confirma um cluster; ter um cluster não confirma que a imagem local está nele.

**Questões exploratórias**

- Que risco existe em executar `kubectl apply` no contexto errado?
- Por que o laboratório fixa o acesso em `127.0.0.1`?

## Instalação

### Windows

Instale [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/). Em PowerShell, após iniciar Docker Desktop, execute `docker version`, `kind version`, `kubectl version --client` e `py --version`; depois, entre em `laboratorios\plataforma-hospitalar`.

**Resultado esperado**

As versões aparecem; Docker mostra servidor em execução.

**Contingência**

Se Docker não responder, inicie Docker Desktop e aguarde. Se a porta 18080 estiver ocupada, pare aqui: não altere o manifest durante a aula, libere a porta local ou execute somente validação estática.

### macOS

Instale [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/). Execute `docker version`, `kind version`, `kubectl version --client`, `python3 --version` e entre em `laboratorios/plataforma-hospitalar`.

**Resultado esperado**

Docker responde e os três executáveis estão no `PATH`.

**Contingência**

Em Mac com recurso insuficiente, feche cargas locais e tente novamente; não remova imagens ou clusters de colegas. Se kind não puder criar o nó, faça a validação estática descrita na limpeza e registre a limitação.

### Linux

Instale [Docker Engine](https://docs.docker.com/engine/install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/), seguindo a política da distribuição para acesso ao socket Docker. Execute `docker version`, `kind version`, `kubectl version --client`, `python3 --version` e entre em `laboratorios/plataforma-hospitalar`.

**Resultado esperado**

O daemon Docker responde sem precisar usar um cluster remoto.

**Contingência**

Se o socket recusar acesso, aplique a orientação oficial da distribuição. Não use `sudo` para apontar kubectl a outro contexto nem remova recursos não relacionados.

## Preparação do laboratório

### Essencial em aula

**Objetivo**

Validar manifests, criar o cluster e disponibilizar a imagem dentro dele.

**Pré-requisito**

Esteja em `laboratorios/plataforma-hospitalar`; Docker deve responder. Confirme que não há cluster local de mesmo nome com `kind get clusters`.

**Execute**

No macOS/Linux:

    kubectl apply --dry-run=client -f infra/k8s
    docker build -t hospital-api:1.0.0 .
    kind create cluster --name hospital-local --config infra/kind/cluster.yaml
    kind load docker-image hospital-api:1.0.0 --name hospital-local
    kubectl config current-context

No PowerShell, os mesmos comandos são seguros:

    kubectl apply --dry-run=client -f infra/k8s
    docker build -t hospital-api:1.0.0 .
    kind create cluster --name hospital-local --config infra/kind/cluster.yaml
    kind load docker-image hospital-api:1.0.0 --name hospital-local
    kubectl config current-context

**Observe**

O dry-run confirma sintaxe aceita pelo cliente; ele não executa Pods. O contexto final precisa ser `kind-hospital-local`. O carregamento explícito é necessário porque a imagem existe inicialmente apenas no Docker local.

**Compare**

`docker build` produz uma imagem; `kind load` a torna disponível no nó. Nenhum dos dois cria o Deployment.

**Questões exploratórias**

- Por que `IfNotPresent` faz sentido para a imagem carregada no kind?
- Que evidência adicional uma CI produziria para uma imagem de produção?

### Exploração em dupla

**Objetivo**

Ler o estado desejado antes de aplicá-lo.

**Pré-requisito**

Abra `infra/k8s/deployment.yaml`, `service.yaml`, `hpa.yaml` e `infra/kind/cluster.yaml`.

**Execute**

Uma pessoa localiza labels e selector; a outra localiza porta, resources, readiness, liveness, `RollingUpdate` e faixa do HPA. Troquem as explicações e formulem uma hipótese para cada valor.

**Observe**

O Service só enxerga Pods com `app: hospital-api`. Readiness usa `/health/ready`; liveness usa `/health/live`.

**Compare**

Compare um Pod existente com um Pod pronto: somente o pronto deve receber tráfego pelo Service.

**Questões exploratórias**

- Qual falha seria detectada por readiness mas não deveria reiniciar um processo?
- Por que duas réplicas no kind não equivalem a duas zonas?

## Execução

### Essencial em aula

**Objetivo**

Aplicar a API, comprovar rollout e coletar um sinal de tráfego local.

**Pré-requisito**

O contexto deve ser `kind-hospital-local` e a imagem `hospital-api:1.0.0` deve ter sido carregada.

**Execute**

No macOS/Linux:

    kubectl apply -f infra/k8s
    kubectl rollout status deployment/hospital-api -n hospital
    kubectl get deployment,pods,service,hpa -n hospital -o wide
    curl --fail --silent http://127.0.0.1:18080/health/ready
    kubectl get endpointslice -n hospital -l kubernetes.io/service-name=hospital-api

No PowerShell:

    kubectl apply -f infra/k8s
    kubectl rollout status deployment/hospital-api -n hospital
    kubectl get deployment,pods,service,hpa -n hospital -o wide
    curl.exe --fail --silent http://127.0.0.1:18080/health/ready
    kubectl get endpointslice -n hospital -l kubernetes.io/service-name=hospital-api

**Observe**

O rollout informa que duas réplicas estão disponíveis; o endpoint devolve `{"status":"ready"}`. `EndpointSlice` contém os endereços prontos. O HPA pode não ter métrica atual no kind básico; registre esse fato em vez de inventar escalonamento.

**Compare**

Compare `kubectl get pods` com `curl`: o primeiro descreve estado do cluster; o segundo prova que o caminho local até readiness respondeu.

**Questões exploratórias**

- Que sinal complementar mostraria que o endpoint ainda atende com uma réplica fora?
- Como requests de CPU participam do cálculo de utilização do HPA?

### Exploração em dupla

**Objetivo**

Observar uma atualização bloqueada e restaurar a revisão saudável sem tocar em dados.

**Pré-requisito**

O rollout inicial está concluído. A única alteração abaixo é uma tag de imagem propositalmente ausente; não use uma tag de ambiente real.

**Execute**

No macOS/Linux, permita que o status não concluído seja observado sem encerrar o terminal:

    kubectl set image deployment/hospital-api hospital-api=hospital-api:imagem-propositalmente-ausente -n hospital
    kubectl rollout status deployment/hospital-api -n hospital --timeout=20s || true
    kubectl get pods -n hospital
    kubectl describe deployment/hospital-api -n hospital
    kubectl rollout undo deployment/hospital-api -n hospital
    kubectl rollout status deployment/hospital-api -n hospital
    curl --fail --silent http://127.0.0.1:18080/health/live

No PowerShell, a falha do status aparece em `$LASTEXITCODE`, mas os comandos seguintes continuam por padrão:

    kubectl set image deployment/hospital-api hospital-api=hospital-api:imagem-propositalmente-ausente -n hospital
    kubectl rollout status deployment/hospital-api -n hospital --timeout=20s
    kubectl get pods -n hospital
    kubectl describe deployment/hospital-api -n hospital
    kubectl rollout undo deployment/hospital-api -n hospital
    kubectl rollout status deployment/hospital-api -n hospital
    curl.exe --fail --silent http://127.0.0.1:18080/health/live

**Observe**

Os Pods novos apresentam `ErrImagePull` ou `ImagePullBackOff`, e o rollout esgota o timeout. A revisão anterior permanece disponível por `maxUnavailable: 0`; após undo, a tag volta a `hospital-api:1.0.0` e liveness responde.

**Compare**

Compare falha de imagem (nem inicia) com falha de readiness (inicia, mas não entra no Service). Ambas bloqueiam uma atualização, mas a evidência e a correção são distintas.

**Questões exploratórias**

- Que parte de uma migração de banco `rollout undo` não desfaria?
- Qual política de CI evitaria chegar a uma tag inexistente?

### Extensão

**Objetivo**

Avaliar elasticidade sem confundir configuração com capacidade comprovada.

**Pré-requisito**

O cluster está saudável e você não modificará a quantidade de réplicas manualmente como prova de HPA.

**Execute**

Execute `kubectl describe hpa hospital-api -n hospital` e registre se há métrica de CPU. Investigue em documentação do kind/Kubernetes o que seria necessário para Metrics Server; não instale add-ons durante a aula sem acordo de escopo.

**Observe**

Sem servidor de métricas, o alvo pode aparecer desconhecido. O manifesto ainda explicita mínimo, máximo e alvo de utilização.

**Compare**

Compare uma política declarada com uma evidência de aumento automático ocorrido sob carga.

**Questões exploratórias**

- Que carga sintética respeitaria a capacidade da máquina do grupo?
- Que métrica além de CPU indicaria uma fila crescente?

## Resultado esperado

Ao fim, existem namespace `hospital`, Deployment `hospital-api` com duas réplicas prontas, Service acessível somente em `127.0.0.1:18080`, ConfigMap e HPA. Há uma revisão saudável, uma tentativa bloqueada por imagem ausente, eventos descritos e rollback confirmado. O resultado não afirma tolerância a falha de zona, autoscaling ativo sem métrica ou prontidão de produção.

## Interpretação

O Deployment demonstrou reconciliação e atualização gradual; o Service demonstrou descoberta por labels; probes demonstraram separação de receber tráfego e manter processo. A tag ausente demonstrou que Kubernetes não conserta uma imagem inválida. Rollback é procedimento de contenção quando a revisão anterior é compatível. Para produção, some autenticação, políticas de rede, secrets, registro de imagem, backup e exercícios de falha ao desenho.

## Limpeza e contingência

Colete a evidência antes de apagar. Depois, no macOS/Linux ou PowerShell, execute `kind delete cluster --name hospital-local`. O comando remove somente o cluster criado pela oficina. A imagem `hospital-api:1.0.0` pode permanecer no Docker para próxima aula; remova-a apenas se você a construiu e não precisa dela: `docker image rm hospital-api:1.0.0`. Se kind não puder rodar nesta máquina, ainda execute `kubectl apply --dry-run=client -f infra/k8s`, `python -m pytest tests/test_k8s_manifests.py -q` dentro do laboratório e registre que a validação foi estática; não tente usar um cluster remoto como substituto.

## Evidência a entregar

Entregue texto ou capturas sem dados pessoais contendo: versões de Docker/kind/kubectl; saída do dry-run; contexto `kind-hospital-local`; imagem carregada; rollout inicial; lista de Pods/Service; resposta de readiness; trecho de `describe` com `ImagePullBackOff`; comando e status do rollback; resposta de liveness; e confirmação da remoção do cluster. Acrescente duas conclusões: uma garantia obtida e um limite que o laboratório não prova.
