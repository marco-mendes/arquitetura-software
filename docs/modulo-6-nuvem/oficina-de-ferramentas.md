# Oficina de ferramentas: Docker, kind e Kubernetes locais

Esta oficina cria e remove um cluster local descartável. Ela usa a imagem da API de elegibilidade, mas não envia dados, credenciais ou imagens a serviço remoto. Todos os nomes e portas são fixos: cluster `hospital-local`, namespace `hospital`, Deployment e Service `hospital-api`, porta do contêiner `8000` e acesso local `http://127.0.0.1:18080`. Não use estes comandos contra um contexto compartilhado.

## Leia antes de executar comandos

O `Dockerfile` descreve como produzir a imagem imutável: parte de Python 3.12, instala a aplicação, cria um usuário sem privilégios e expõe a porta 8000. A construção local materializa esse pacote. A tag `hospital-api:1.0.0` é a revisão usada pelo Deployment, sem relação com um endereço de registry de produção. Um contêiner só aparece quando essa imagem é executada.

O arquivo `infra/kind/cluster.yaml` instrui o **kind** a criar o cluster Kubernetes `hospital-local` em contêineres Docker, com um nó de controle e a porta 30080 limitada a `127.0.0.1:18080`. Ele cria um **cluster local descartável** para a oficina. Ele não deve ser usado em um cluster compartilhado, nem os comandos desta página devem ser apontados para qualquer contexto compartilhado.

Os manifestos expressam o estado inicial, antes de serem aplicados ao cluster: `namespace.yaml` cria a fronteira `hospital`. `configmap.yaml` fornece somente `APP_ENV=local-kind`. `deployment.yaml` pede duas réplicas da imagem, recursos e atualização gradual. `service.yaml` seleciona os Pods por `app: hospital-api`. `hpa.yaml` declara a faixa de duas a cinco réplicas, dependente de métricas disponíveis. Nada disso cria dados clínicos ou tolerância a falhas de zona.

As probes deixam a condição observável. `readiness` consulta `/health/ready` e mantém um Pod fora dos endpoints enquanto ele não pode receber tráfego. `liveness` consulta `/health/live` para permitir reinício de um processo travado. Ela não deve depender de banco ou de uma API remota. O estado inicial esperado é: nenhum recurso do namespace `hospital` aplicado, nenhuma imagem no nó kind e nenhum contexto `kind-hospital-local` até que o cluster seja criado e a imagem seja carregada.

### O que você vai observar, e por que importa

| O que a oficina mostra | O conceito do módulo |
| --- | --- |
| A imagem é imutável e a revisão fica registrada | [Contêiner, imagem e orquestração](conceitos.md#conteiner-imagem-e-orquestracao) |
| Duas réplicas atendendo, nenhuma guardando estado próprio | [Stateless, stateful e os doze fatores](padroes-e-decisoes.md#stateless-stateful-e-os-doze-fatores) |
| A faixa de réplicas é declarada uma vez e ajustada pelo cluster | [Elasticidade e escalabilidade](padroes-e-decisoes.md#elasticidade-e-escalabilidade) |
| A atualização troca Pods sem derrubar o serviço | [Resiliência, rollout e rollback](padroes-e-decisoes.md#resiliencia-rollout-e-rollback) |
| Duas verificações de saúde com finalidades distintas | [Região, zona e fronteiras de falha](conceitos.md#regiao-zona-e-fronteiras-de-falha) |

![Percurso da imagem Docker ao serviço local e ciclo de reconciliação do Kubernetes](../assets/images/m06-oficina-kind-reconciliacao.png)

*Figura 10 — Da imagem imutável ao estado declarado que o cluster mantém sozinho. Fonte: curso.*

**Leitura textual da figura:** a faixa superior numera sete etapas em sequência, do `Dockerfile` à imagem `hospital-api:1.0.0`, dela ao `kind load`, ao cluster `hospital-local`, ao namespace `hospital`, ao Deployment com duas réplicas, ao Service e finalmente ao acesso local em `127.0.0.1:18080`. Sob as etapas aparecem os comandos que produzem evidência de cada uma: `docker image inspect`, `kind get clusters` e `kubectl`. Ao centro, o ciclo de reconciliação parte do estado desejado de duas réplicas, passa pelo Pod apagado, pelo novo Pod criado e retorna ao estado desejado. À direita, readiness consulta `/health/ready` e retira o Pod dos endpoints, enquanto liveness consulta `/health/live` e reinicia o processo.

### Onde cada arquivo mora

Todos os comandos rodam a partir de `laboratorios/plataforma-hospitalar`.

```text
plataforma-hospitalar/
├── Dockerfile                    ← receita da imagem imutável
└── infra/
    ├── kind/cluster.yaml         ← define o cluster local descartável
    └── k8s/
        ├── namespace.yaml        a fronteira lógica "hospital"
        ├── configmap.yaml        configuração externa ao código
        ├── deployment.yaml       ← o manifesto central: réplicas, recursos e probes
        ├── service.yaml          o endereço estável na frente dos Pods
        └── hpa.yaml              a faixa de réplicas para escala automática
```

| Arquivo | O que ele faz |
| --- | --- |
| [`Dockerfile`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/Dockerfile) | Descreve como produzir a imagem: parte de Python 3.12, instala a aplicação e cria um usuário sem privilégios. |
| [`infra/kind/cluster.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/kind/cluster.yaml) | Declara o cluster local com um nó de controle e o mapeamento de porta para a sua máquina. |
| [`infra/k8s/deployment.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/k8s/deployment.yaml) | Pede duas réplicas, declara pedido e teto de recursos, e define as duas verificações de saúde. |
| [`infra/k8s/service.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/k8s/service.yaml) | Dá um endereço estável a um conjunto de Pods que nascem e morrem. |
| [`infra/k8s/hpa.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/k8s/hpa.yaml) | Declara a faixa de duas a cinco réplicas, conforme a carga. |

## Ferramentas e evidências

| Ferramenta | O que é | Para que serve aqui |
| --- | --- | --- |
| **Docker Engine** | Executa contêineres, já usado nos módulos 3 e 4. | Construir a imagem da aplicação. |
| **Kubernetes** | Um orquestrador de contêineres: recebe uma descrição do estado desejado e trabalha continuamente para que a realidade corresponda a ela. | Manter duas réplicas no ar, substituir as que falham e trocar versões sem derrubar o serviço. |
| **kind** | Sigla de *Kubernetes in Docker*: cria um cluster Kubernetes completo dentro de contêineres, na sua máquina. | Ter um cluster descartável sem nuvem nem custo. |
| **kubectl** | O programa de linha de comando que conversa com o Kubernetes. | Aplicar os manifestos e observar o que o cluster fez com eles. |

Três termos aparecem em cada comando adiante. Um **Pod** é a menor unidade que o Kubernetes executa, envolvendo um ou mais contêineres que compartilham rede e armazenamento. Um **Deployment** declara quantas réplicas de um Pod devem existir e como substituí-las ao trocar de versão. E um **manifesto** é o arquivo YAML que descreve o estado desejado de um desses objetos.

Cada ferramenta deixa uma evidência própria, e vale saber de antemão qual comando comprova o quê: `docker image inspect hospital-api:1.0.0` confirma que a imagem existe localmente, `kind get clusters` lista os clusters criados, e `kubectl` mostra o estado que o cluster alcançou depois de receber os manifestos.

A diferença que dá sentido à oficina inteira: você não vai mandar o Kubernetes criar dois Pods. Você vai **declarar que devem existir dois**, e ele passa a garantir isso. Apagar um Pod à mão faz o orquestrador criar outro, e é esse comportamento que se chama reconciliação.

O Service usa uma porta fixa mapeada pelo kind apenas em `127.0.0.1:18080`. A escala automática pode exibir `<unknown>` na coluna de métricas quando o cluster não tem coletor instalado. A lição sobre pedidos de recurso, tetos e configuração declarativa continua valendo.

## O `deployment.yaml` linha a linha

Este é o manifesto onde estão quase todas as decisões da oficina. Vale lê-lo antes de aplicá-lo, porque cada bloco corresponde a um conceito do módulo.

O primeiro bloco declara quantas cópias devem existir e como trocá-las de versão:

```yaml
spec:
  replicas: 2                    # o estado desejado: sempre duas
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0          # nunca fique com menos de 2 atendendo
      maxSurge: 1                # pode subir 1 a mais durante a troca
```

A combinação `maxUnavailable: 0` com `maxSurge: 1` é uma decisão de disponibilidade, escrita como configuração. Ela diz: durante uma atualização, crie primeiro o Pod novo, espere que ele fique pronto, e só então remova o antigo. O cluster chega a ter três Pods por instantes, e nunca menos que dois atendendo. Trocar `maxUnavailable` para `1` tornaria a atualização mais rápida e aceitaria uma janela de capacidade reduzida.

O segundo bloco declara o que cada réplica precisa de recursos:

```yaml
          resources:
            requests:            # o que o Pod precisa para ser agendado
              cpu: 100m
              memory: 128Mi
            limits:              # o teto que ele não pode ultrapassar
              cpu: 250m
              memory: 256Mi
```

A distinção entre pedido e teto costuma confundir, e as consequências são bem diferentes. O **pedido** é usado para decidir em qual nó o Pod cabe: o Kubernetes só o agenda onde houver 100 milicores livres. O **teto** é o que o Pod não pode ultrapassar em execução. Exceder o teto de memória faz o contêiner ser encerrado.

Declarar os dois é o que permite ao orquestrador distribuir carga sem que um serviço consuma a máquina inteira, e é a base sobre a qual a escala automática decide acrescentar réplicas.

O terceiro bloco declara duas verificações de saúde que parecem iguais e respondem perguntas opostas:

```yaml
          readinessProbe:              # "posso receber tráfego?"
            httpGet:
              path: /health/ready
            periodSeconds: 3

          livenessProbe:               # "ainda estou vivo?"
            httpGet:
              path: /health/live
            periodSeconds: 5
```

Reprovar na verificação de **prontidão** tira o Pod da lista de destinos do Service, sem reiniciá-lo: ele continua vivo, apenas deixa de receber requisições até se recuperar. Reprovar na de **vitalidade** faz o Kubernetes reiniciar o contêiner, por concluir que ele travou.

Confundir as duas produz um defeito clássico. Se a verificação de vitalidade consultasse o banco de dados, uma lentidão no banco reiniciaria todos os Pods em cadeia, transformando um problema de dependência numa queda geral. É por isso que `/health/live` responde sem consultar nada externo, enquanto `/health/ready` pode ser mais exigente.

O Service, por sua vez, resolve outro problema:

```yaml
spec:
  type: NodePort
  selector:
    app: hospital-api            # encontra Pods por rótulo, não por endereço
  ports:
    - port: 8000
      nodePort: 30080
```

Pods são efêmeros: nascem, morrem e trocam de endereço a cada substituição. O `selector` por rótulo é o que dá estabilidade ao conjunto. Qualquer Pod marcado como `app: hospital-api` entra automaticamente no balanceamento, e quem chama nunca precisa saber quantos são nem onde estão.

## Pré-requisitos

**Objetivo**

Confirmar um ambiente local antes de criar recursos.

**Pré-requisito**

Tenha Docker iniciado, `kubectl`, `kind` e Python instalados. Trabalhe na pasta `laboratorios/plataforma-hospitalar` deste repositório, onde estão imagem e manifests.

**Execute**

Verifique versões e contexto. No macOS/Linux use `docker version`, `kind version`, `kubectl version --client` e `python3 --version`. No PowerShell use `docker version`, `kind version`, `kubectl version --client` e `py --version`.

**Observe**

Docker deve mostrar Client e Server. `kubectl config current-context` pode mostrar outro contexto antes do cluster. Não aplique manifest até o contexto `kind-hospital-local` existir.

**Compare**

Ter o cliente `kubectl` não confirma um cluster. Ter um cluster não confirma que a imagem local está nele.

**Questões exploratórias**

- Que risco existe em executar `kubectl apply` no contexto errado?
- Por que o laboratório fixa o acesso em `127.0.0.1`?

## Instalação

### Windows

Instale [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/). Em PowerShell, após iniciar Docker Desktop, execute `docker version`, `kind version`, `kubectl version --client` e `py --version`. Depois, entre em `laboratorios\plataforma-hospitalar`.

**Resultado esperado**

As versões aparecem, e Docker mostra servidor em execução.

**Contingência**

Se Docker não responder, inicie Docker Desktop e aguarde. Se a porta 18080 estiver ocupada, pare aqui: não altere o manifest durante a aula, libere a porta local ou execute somente validação estática.

### macOS

Instale [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/). Execute `docker version`, `kind version`, `kubectl version --client`, `python3 --version` e entre em `laboratorios/plataforma-hospitalar`.

**Resultado esperado**

Docker responde e os três executáveis estão no `PATH`.

**Contingência**

Em Mac com recurso insuficiente, feche cargas locais e tente novamente. Não remova imagens ou clusters de colegas. Se kind não puder criar o nó, faça a validação estática descrita na limpeza e registre a limitação.

### Linux

Instale [Docker Engine](https://docs.docker.com/engine/install/), [kubectl](https://kubernetes.io/docs/tasks/tools/) e [kind](https://kind.sigs.k8s.io/docs/user/quick-start/), seguindo a política da distribuição para acesso ao socket Docker. Execute `docker version`, `kind version`, `kubectl version --client`, `python3 --version` e entre em `laboratorios/plataforma-hospitalar`.

**Resultado esperado**

O daemon Docker responde sem precisar usar um cluster remoto.

**Contingência**

Se o socket recusar acesso, aplique a orientação oficial da distribuição. Não use `sudo` para apontar kubectl a outro contexto nem remova recursos não relacionados.

## Preparação do laboratório

**Objetivo**

Validar manifests, criar o cluster e disponibilizar a imagem dentro dele.

**Pré-requisito**

Esteja em `laboratorios/plataforma-hospitalar`, com Docker respondendo. Confirme que não há cluster local de mesmo nome com `kind get clusters`.

**Execute**

No macOS/Linux:

    kubectl apply --dry-run=client -f infra/k8s/namespace.yaml
    kubectl apply --dry-run=client -f infra/k8s/configmap.yaml -f infra/k8s/deployment.yaml -f infra/k8s/service.yaml -f infra/k8s/hpa.yaml
    docker build -t hospital-api:1.0.0 .
    kind create cluster --name hospital-local --config infra/kind/cluster.yaml
    kind load docker-image hospital-api:1.0.0 --name hospital-local
    kubectl config current-context

No PowerShell, os mesmos comandos são seguros:

    kubectl apply --dry-run=client -f infra/k8s/namespace.yaml
    kubectl apply --dry-run=client -f infra/k8s/configmap.yaml -f infra/k8s/deployment.yaml -f infra/k8s/service.yaml -f infra/k8s/hpa.yaml
    docker build -t hospital-api:1.0.0 .
    kind create cluster --name hospital-local --config infra/kind/cluster.yaml
    kind load docker-image hospital-api:1.0.0 --name hospital-local
    kubectl config current-context

**Observe**

O dry-run confirma sintaxe aceita pelo cliente. Ele não executa Pods. A sequência valida primeiro o namespace e, depois, os recursos que pertencem a `hospital`. O contexto final precisa ser `kind-hospital-local`. O carregamento explícito é necessário porque a imagem existe inicialmente apenas no Docker local.

**Compare**

`docker build` produz uma imagem. `kind load` a torna disponível no nó. Nenhum dos dois cria o Deployment.

**Questões exploratórias**

- Por que `IfNotPresent` faz sentido para a imagem carregada no kind?
- Que evidência adicional uma CI produziria para uma imagem de produção?

**Objetivo**

Ler o estado desejado antes de aplicá-lo.

**Pré-requisito**

Abra `infra/k8s/deployment.yaml`, `service.yaml`, `hpa.yaml` e `infra/kind/cluster.yaml`.

**Execute**

Localize nos manifestos os rótulos e o seletor que ligam o Service aos Pods. Depois localize a porta, os recursos, as duas verificações de saúde, a estratégia `RollingUpdate` e a faixa de réplicas, formulando uma hipótese para cada valor escolhido.

**Observe**

O Service só enxerga Pods com `app: hospital-api`. Readiness usa `/health/ready`. Liveness usa `/health/live`.

**Compare**

Compare um Pod existente com um Pod pronto: somente o pronto deve receber tráfego pelo Service.

**Questões exploratórias**

- Qual falha seria detectada por readiness mas não deveria reiniciar um processo?
- Por que duas réplicas no kind não equivalem a duas zonas?

## Execução

**Objetivo**

Aplicar a API, comprovar rollout e coletar um sinal de tráfego local.

**Pré-requisito**

O contexto deve ser `kind-hospital-local` e a imagem `hospital-api:1.0.0` deve ter sido carregada.

**Execute**

No macOS/Linux:

    kubectl apply -f infra/k8s/namespace.yaml
    kubectl apply -f infra/k8s/configmap.yaml -f infra/k8s/deployment.yaml -f infra/k8s/service.yaml -f infra/k8s/hpa.yaml
    kubectl rollout status deployment/hospital-api -n hospital
    kubectl get deployment,pods,service,hpa -n hospital -o wide
    curl --fail --silent http://127.0.0.1:18080/health/ready
    kubectl get endpointslice -n hospital -l kubernetes.io/service-name=hospital-api

No PowerShell:

    kubectl apply -f infra/k8s/namespace.yaml
    kubectl apply -f infra/k8s/configmap.yaml -f infra/k8s/deployment.yaml -f infra/k8s/service.yaml -f infra/k8s/hpa.yaml
    kubectl rollout status deployment/hospital-api -n hospital
    kubectl get deployment,pods,service,hpa -n hospital -o wide
    curl.exe --fail --silent http://127.0.0.1:18080/health/ready
    kubectl get endpointslice -n hospital -l kubernetes.io/service-name=hospital-api

**Observe**

O rollout informa que duas réplicas estão disponíveis, e o endpoint devolve `{"status":"ready"}`. `EndpointSlice` contém os endereços prontos. O HPA pode não ter métrica atual no kind básico. Registre esse fato em vez de inventar escalonamento.

**Compare**

Compare `kubectl get pods` com `curl`. O primeiro descreve estado do cluster. O segundo prova que o caminho local até readiness respondeu.

**Questões exploratórias**

- Que sinal complementar mostraria que o endpoint ainda atende com uma réplica fora?
- Como requests de CPU participam do cálculo de utilização do HPA?

**Objetivo**

Observar uma atualização bloqueada e restaurar a revisão saudável sem tocar em dados.

**Pré-requisito**

O rollout inicial está concluído. A única alteração abaixo é uma tag de imagem propositalmente ausente. Não use uma tag de ambiente real.

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

Os Pods novos apresentam `ErrImagePull` ou `ImagePullBackOff`, e o rollout esgota o timeout. A revisão anterior permanece disponível por `maxUnavailable: 0`. Após o undo, a tag volta a `hospital-api:1.0.0` e liveness responde.

**Compare**

Compare falha de imagem (nem inicia) com falha de readiness (inicia, mas não entra no Service). Ambas bloqueiam uma atualização, mas a evidência e a correção são distintas.

**Questões exploratórias**

- Que parte de uma migração de banco `rollout undo` não desfaria?
- Qual política de CI evitaria chegar a uma tag inexistente?

**Objetivo**

Avaliar elasticidade sem confundir configuração com capacidade comprovada.

**Pré-requisito**

O cluster está saudável e você não modificará a quantidade de réplicas manualmente como prova de HPA.

**Execute**

Execute `kubectl describe hpa hospital-api -n hospital` e registre se há métrica de CPU. Investigue em documentação do kind/Kubernetes o que seria necessário para Metrics Server. Não instale add-ons durante a aula sem acordo de escopo.

**Observe**

Sem servidor de métricas, o alvo pode aparecer desconhecido. O manifesto ainda explicita mínimo, máximo e alvo de utilização.

**Compare**

Compare uma política declarada com uma evidência de aumento automático ocorrido sob carga.

**Questões exploratórias**

- Que carga sintética respeitaria a capacidade da máquina do grupo?
- Que métrica além de CPU indicaria uma fila crescente?

## Resultado esperado

Ao fim, o namespace `hospital` foi criado antes de ConfigMap, Deployment, Service e HPA. O Deployment `hospital-api` tem duas réplicas prontas, e o Service é acessível somente em `127.0.0.1:18080`. Há uma revisão saudável, uma tentativa bloqueada por imagem ausente, eventos descritos e rollback confirmado. O resultado não afirma tolerância a falha de zona, autoscaling ativo sem métrica ou prontidão de produção.

## Interpretação

O Deployment mostrou reconciliação e atualização gradual. O Service mostrou descoberta por labels. As probes mostraram a separação entre receber tráfego e manter o processo vivo. A tag ausente confirmou que Kubernetes não conserta uma imagem inválida por conta própria. Rollback é procedimento de contenção quando a revisão anterior é compatível. Para produção, some autenticação, políticas de rede, secrets, registro de imagem, backup e exercícios de falha ao desenho.

## Limpeza e contingência

Colete a evidência antes de apagar. Depois, no macOS/Linux ou PowerShell, execute `kind delete cluster --name hospital-local`. O comando remove somente o cluster criado pela oficina. A imagem `hospital-api:1.0.0` pode permanecer no Docker para próxima aula. Remova-a apenas se você a construiu e não precisa dela, com `docker image rm hospital-api:1.0.0`. Se kind não puder rodar nesta máquina, valide primeiro `namespace.yaml` com `kubectl apply --dry-run=client -f infra/k8s/namespace.yaml`, depois os quatro manifests namespaced com os quatro `-f` explícitos acima, e execute `python -m pytest tests/test_k8s_manifests.py -q` dentro do laboratório. Registre que a validação foi estática. Não tente usar um cluster remoto como substituto.

## Evidência a entregar

Entregue texto ou capturas sem dados pessoais contendo:

- versões de Docker, kind e kubectl.
- saída do dry-run.
- contexto `kind-hospital-local`.
- imagem carregada.
- rollout inicial.
- lista de Pods e do Service.
- resposta de readiness.
- trecho de `describe` com `ImagePullBackOff`.
- comando e status do rollback.
- resposta de liveness.
- confirmação da remoção do cluster.

Acrescente duas conclusões: uma garantia obtida e um limite que o laboratório não prova.

## Rotas complementares, fora da entrega

As três sequências abaixo não fazem parte da evidência a entregar. Elas existem porque a prática do módulo usa um caminho só, kind mais kubectl, e convém conhecer o que existe antes e ao lado dele. Execute-as depois da entrega, se quiser, e nunca contra um cluster compartilhado.

### Imagens e contêineres sem orquestrador

Antes de qualquer cluster, o Docker sozinho já mostra a diferença entre imagem e contêiner. A imagem é o pacote imutável com sistema de arquivos, dependências, configuração e binários. O contêiner é uma execução dessa imagem, efêmera, que se inicia, para e remove em segundos.

Confirme a instalação e liste o que já existe na máquina.

```sh
docker --version
docker images
```

Baixe uma imagem que ainda não esteja local. O Docker verifica se ela existe na máquina, busca no Docker Hub quando não existe e a guarda para execuções futuras.

```sh
docker pull mysql:latest
```

Execute um contêiner a partir dela. O comando cria o contêiner `mysql-container`, define a senha do usuário administrador e mapeia a porta 3306 do contêiner para a máquina.

```sh
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=admin -d -p 3306:3306 mysql:latest
```

A saída é o identificador do contêiner criado. Confirme que ele está em execução e consulte o banco por dentro.

```sh
docker ps
docker exec -it mysql-container mysql -uroot -padmin -e "SHOW DATABASES;"
```

A segunda chamada deve listar `information_schema`, `mysql`, `performance_schema` e `sys`. Remover o contêiner ao final é `docker rm -f mysql-container`.

### Docker Swarm, a orquestração nativa

O Swarm transforma um host Docker em nó gerenciador e permite criar um cluster sem instalar nada além do próprio Docker. A figura do Swarm em [Padrões e decisões](padroes-e-decisoes.md) descreve a repartição entre gerenciadores e trabalhadores.

```sh
docker swarm init
docker info | grep Swarm
```

A saída do segundo comando deve conter `Swarm: active`. O primeiro comando devolve um token de adesão, usado no nó que vai entrar no cluster.

```sh
docker swarm join --token <TOKEN> <IP_DO_MANAGER>:2377
docker node ls
```

Com o cluster de pé, um serviço replicado distribui réplicas entre os nós disponíveis.

```sh
docker service create --name webserver -p 8080:80 --replicas 3 nginx
docker service ls
docker service ps webserver
curl http://localhost:8080
```

`docker service ls` mostra a proporção de réplicas ativas, no formato `3/3`. `docker service ps` mostra em qual nó cada réplica está, que é a evidência de distribuição. Para desfazer, execute `docker swarm leave --force` no nó que sai.

### Minikube, um Kubernetes local alternativo

O Minikube resolve o mesmo problema que o kind e usa uma máquina virtual ou um contêiner como nó. A sequência abaixo repete, com outros comandos, o que a oficina fez com kind.

```sh
minikube start
kubectl cluster-info
kubectl create deployment webserver --image=nginx
kubectl get deployments
kubectl get pods -o wide
```

Pods não são alcançáveis de fora por padrão, então um Service precisa expor o Deployment. Anote a porta atribuída na coluna `PORT(S)`.

```sh
kubectl expose deployment webserver --type=NodePort --port=80
kubectl get services
```

O Minikube atribui um endereço próprio ao nó, e a chamada abaixo monta o endereço completo a partir dele e da porta exposta.

```sh
minikube ip
curl http://$(minikube ip):$(kubectl get service webserver -o=jsonpath='{.spec.ports[0].nodePort}')
kubectl port-forward svc/webserver 8080:80 &
```

Escalar para três réplicas e observar os ReplicaSets fecha a comparação com a reconciliação vista na oficina.

```sh
kubectl scale deployment webserver --replicas=3
kubectl get pods -o wide
kubectl get rs
minikube delete
```

O último comando remove o cluster inteiro, com seus Deployments e Services.
