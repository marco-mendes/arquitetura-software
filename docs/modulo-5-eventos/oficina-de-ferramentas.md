# Oficina de ferramentas: RabbitMQ e consumidor idempotente

Oficina local: RabbitMQ, publicação repetida de `ResultadoLaboratorialDisponibilizado.v1`, efeito SQLite e dead-letter queue. Kafka é extensão comparativa. Use dados sintéticos.

## Ferramenta

| Ferramenta | Papel local | Evidência observável |
| --- | --- | --- |
| Docker Engine e Compose v2 | executar RabbitMQ isolado | healthcheck e configuração válida |
| RabbitMQ 4 com management plugin | exchange, fila, confirmações e DLQ | filas no endpoint local |
| Python 3.11 ou superior | publicar e consumir modelo Pydantic | saída de tentativas |
| `aio-pika` e SQLite | AMQP assíncrono e store durável local | uma linha de efeito |

AMQP usa `RABBITMQ_PORT` e management usa `RABBITMQ_MANAGEMENT_PORT`; os padrões são 15672 e 15673. A conta e o volume pertencem apenas a este ambiente descartável.

## Pré-requisitos

### Essencial em aula

**Objetivo**

Confirmar que Docker, Compose e Python estão disponíveis e que a execução ocorrerá com dados sintéticos.

**Pré-requisito**

Tenha o repositório local e Docker iniciado. Execute a partir de `laboratorios/plataforma-hospitalar`; o pacote já declara `aio-pika`, Pydantic e a dependência de desenvolvimento.

**Execute**

Verifique versões, instale o pacote local e crie uma pasta descartável para a evidência.

**Observe**

`docker version` precisa mostrar Client e Server; `docker compose version` e a versão Python confirmam o caminho escolhido.

**Compare**

Configuração válida não é a mesma evidência que broker pronto. A primeira lê YAML; a segunda depende do healthcheck.

**Questões exploratórias**

- Que dado seria excessivo no payload de um resultado?
- Qual é a diferença entre `exam_id` e `event_id` na repetição?

## Instalação

### Windows

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/windows-install/) e Python pelas [instruções oficiais](https://docs.python.org/3/using/windows.html). Em PowerShell:

```powershell
docker version
docker compose version
py --version
cd laboratorios\plataforma-hospitalar
py -m pip install -e ".[dev]"
New-Item -ItemType Directory -Force evidencias\modulo-5
```

**Resultado esperado**

As versões são exibidas e o pacote pode ser importado pelo Python usado no terminal.

**Contingência**

Se o Docker não responder, abra Docker Desktop e aguarde o mecanismo. Se a instalação Python afetar outro projeto, crie um ambiente virtual local e repita os comandos dentro dele.

### macOS

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/mac-install/) e use Python do sistema, Homebrew ou instalador oficial.

```bash
docker version
docker compose version
python3 --version
cd laboratorios/plataforma-hospitalar
python3 -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-5
```

**Resultado esperado**

O daemon Docker responde e o ambiente contém as bibliotecas do laboratório.

**Contingência**

Se `pip` não puder alterar o ambiente global, use `python3 -m venv .venv`, ative com `source .venv/bin/activate` e execute a instalação novamente.

### Linux

Instale Docker Engine e o plugin Compose pelas [instruções oficiais](https://docs.docker.com/engine/install/) e Python pelo mecanismo da distribuição.

```bash
docker version
docker compose version
python3 --version
cd laboratorios/plataforma-hospitalar
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-5
```

**Resultado esperado**

Docker responde e o ambiente virtual contém o pacote local.

**Contingência**

Se o socket do Docker recusar conexão, siga a orientação pós-instalação da distribuição. Não remova contêineres ou volumes alheios para liberar uma porta.

## Preparação do laboratório

### Essencial em aula

**Objetivo**

Escolher portas, validar o Compose e iniciar um broker isolado.

**Pré-requisito**

Permaneça em `laboratorios/plataforma-hospitalar`. Escolha portas livres; se as sugestões estiverem ocupadas, altere apenas os valores do terminal.

**Execute**

No macOS ou Linux:

```bash
export RABBITMQ_PORT=15672
export RABBITMQ_MANAGEMENT_PORT=15673
export RABBITMQ_URL="amqp://guest:guest@localhost:${RABBITMQ_PORT}/"
docker compose -f infra/compose.eventos.yml config --quiet
docker compose -f infra/compose.eventos.yml up -d --build --wait
docker compose -f infra/compose.eventos.yml ps
```

No PowerShell:

```powershell
$env:RABBITMQ_PORT = 15672
$env:RABBITMQ_MANAGEMENT_PORT = 15673
$env:RABBITMQ_URL = "amqp://guest:guest@localhost:$env:RABBITMQ_PORT/"
docker compose -f infra/compose.eventos.yml config --quiet
docker compose -f infra/compose.eventos.yml up -d --build --wait
docker compose -f infra/compose.eventos.yml ps
```

**Observe**

`config --quiet` termina sem texto de erro. O serviço `rabbitmq` fica saudável antes de `--wait` retornar. A saída de `ps` é a primeira evidência de runtime; ela ainda não demonstra routing nem idempotência.

**Compare**

Compare a porta AMQP 15672 com a porta web 15673. A primeira é usada por `aio-pika`; a segunda existe apenas para inspeção local do management plugin.

**Questões exploratórias**

- Por que alterar variável de porta é mais seguro que editar um arquivo compartilhado?
- O que o healthcheck confirma e o que ele não confirma?

### Exploração em dupla

**Objetivo**

Ler a topologia antes de enviar mensagens.

**Pré-requisito**

Abra `src/hospital/eventos/publicador.py`, `src/hospital/eventos/consumidor.py` e `infra/compose.eventos.yml`.

**Execute**

Uma pessoa identifica publicação, exchange e routing key; a outra identifica fila, DLX, DLQ e momento da confirmação. Troquem as explicações.

**Observe**

`hospital.events` é a exchange topic; `billing.resultados.v1` é a fila de trabalho; `hospital.events.dlx` encaminha rejeições a `billing.resultados.v1.dlq`.

**Compare**

Compare o que a infraestrutura roteia com o que `ProcessedEventStore` decide. O broker não sabe se já houve lançamento administrativo; o consumidor não decide se uma mensagem inválida deve parecer sucesso.

**Questões exploratórias**

- Qual mudança exigiria uma nova versão do evento?
- Por que o store pertence ao consumidor, não à exchange?

### Extensão

**Objetivo**

Planejar uma futura avaliação de Kafka sem mudar a oficina principal.

**Pré-requisito**

Considere a necessidade de reprocessar eventos de resultados por vários grupos independentes por um período definido.

**Execute**

Escreva uma hipótese de tópico, chave de partição por `exam_id`, prazo de retenção, grupos de consumidores e regra de proteção de referências. Não suba Kafka nesta etapa.

**Observe**

Replay depende de retenção e offsets; ele não remove a necessidade de `event_id`, idempotência ou versão de contrato.

**Compare**

Compare uma fila de Faturamento, que distribui trabalho pendente, com um log Kafka, que permite posições independentes de leitura.

**Questões exploratórias**

- Que requisito mensurável justificaria a extensão?
- Qual efeito externo ainda exigiria chave de idempotência?

## Execução

### Essencial em aula

**Objetivo**

Declarar a fila, publicar o mesmo fato duas vezes e registrar um único lançamento administrativo sintético.

**Pré-requisito**

O broker está saudável e `RABBITMQ_URL` aponta para o terminal atual. Use um UUID sintético fixo nesta sequência para que as duas mensagens tenham o mesmo `event_id`.

**Execute**

Primeiro execute o consumidor uma vez para declarar a fila; como ela está vazia, ele não produz efeito. Depois publique e consuma, repita a publicação com o mesmo ID e consuma de novo. No macOS ou Linux:

```bash
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m hospital.eventos.publicador --event-id 3fa85f64-5717-4562-b3fc-2c963f66afa6
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
python -m pytest tests/test_event_idempotency.py -q
```

No PowerShell, troque `python` por `py` se esse for o iniciador instalado; os argumentos são idênticos.

**Observe**

A primeira entrega válida imprime `processed=True attempts=1`. A segunda imprime `processed=False attempts=2`. O teste `test_event_idempotency.py` confirma uma linha de efeito e duas tentativas em banco temporário; a sequência manual preserva a mesma observação no arquivo de evidência.

**Compare**

Compare “duas mensagens recebidas” com “duas cobranças”. O primeiro é comportamento permitido pela entrega pelo menos uma vez; o segundo seria falha de idempotência.

**Questões exploratórias**

- Em qual etapa uma queda poderia gerar redelivery?
- Por que confirmar antes do SQLite seria inseguro?

### Exploração em dupla

**Objetivo**

Inspecionar o estado persistido sem revelar dados clínicos.

**Pré-requisito**

A sequência essencial já criou `evidencias/modulo-5/processed-events.sqlite3` com valores sintéticos.

**Execute**

Consulte apenas contagens e a identidade sintética da ocorrência:

```bash
python -c "import sqlite3; c=sqlite3.connect('evidencias/modulo-5/processed-events.sqlite3'); print(c.execute('select event_id, attempts from processed_events').fetchall()); print(c.execute('select count(*) from billing_effects').fetchone())"
```

**Observe**

Há uma ocorrência com duas tentativas e a contagem de `billing_effects` é um. Registre a saída em um arquivo local de evidência se a turma precisar comparar resultados.

**Compare**

Compare a tabela de tentativas com a de efeitos: a primeira mede entrega vista; a segunda representa a consequência de negócio idempotente.

**Questões exploratórias**

- Como a tabela mudaria se o `event_id` fosse novo?
- Que restrição única seria necessária em um banco compartilhado?

### Extensão

**Objetivo**

Observar uma mensagem inválida na dead-letter queue.

**Pré-requisito**

A fila já foi declarada pelo consumidor. Mantenha o mesmo ambiente local e não use payloads reais.

**Execute**

Publique deliberadamente uma mensagem sem `result_reference`, consuma uma vez e consulte a contagem da DLQ no management endpoint local:

```bash
python -m hospital.eventos.publicador --event-id 65e95d82-4f8c-4e93-9bb3-3e0e92deaf1d --invalid
python -m hospital.eventos.consumidor --once --store evidencias/modulo-5/processed-events.sqlite3
curl -u guest:guest "http://localhost:${RABBITMQ_MANAGEMENT_PORT}/api/queues/%2F/billing.resultados.v1.dlq"
```

**Verificação no PowerShell**

Use `curl.exe`: `curl` pode ser um alias. `%2F` codifica o vhost padrão.

```powershell
if (-not $env:RABBITMQ_MANAGEMENT_PORT) {
  $env:RABBITMQ_MANAGEMENT_PORT = 15673
}
$dlqUrl = "http://localhost:$env:RABBITMQ_MANAGEMENT_PORT/api/queues/%2F/billing.resultados.v1.dlq"
$response = curl.exe --fail --silent --user guest:guest $dlqUrl | ConvertFrom-Json
if ($response.messages -lt 1) {
  throw "A DLQ ainda não contém a mensagem; aguarde um instante e execute a consulta novamente."
}
$response.messages

# Ao terminar este terminal, remova os overrides para voltar aos padrões do Compose.
Remove-Item Env:RABBITMQ_PORT -ErrorAction SilentlyContinue
Remove-Item Env:RABBITMQ_MANAGEMENT_PORT -ErrorAction SilentlyContinue
Remove-Item Env:RABBITMQ_URL -ErrorAction SilentlyContinue
```

**Resultado esperado no PowerShell**

O valor é `1` ou maior e o JSON contém `messages`. Os padrões são AMQP 15672 e management 15673; se ocupados, defina portas livres antes da subida. Os `Remove-Item` removem apenas overrides do terminal.

**Evidência automatizada**

Com Compose ativo, o teste opt-in percorre publicação, validação, rejeição, DLX e DLQ:

```bash
COMPOSE_LIVE=1 RABBITMQ_URL="amqp://guest:guest@localhost:${RABBITMQ_PORT}" RABBITMQ_MANAGEMENT_PORT="${RABBITMQ_MANAGEMENT_PORT}" python -m pytest tests/test_event_idempotency.py -q
```

`3 passed` confirma a mensagem inválida na `billing.resultados.v1.dlq`.

**Observe**

O consumidor rejeita a mensagem ao validar Pydantic; ele não imprime sucesso de processamento. A resposta JSON do endpoint mostra `messages` maior que zero na fila `billing.resultados.v1.dlq`.

**Compare**

Compare uma mensagem inválida em DLQ com uma mensagem temporariamente indisponível. A primeira pede correção de contrato ou decisão de recuperação; a segunda pode pedir retry com atraso e limite.

**Questões exploratórias**

- Por que republicar o corpo inválido sem correção produz um ciclo?
- Qual sinal operacional avisaria que uma DLQ deixou de ser excepcional?

## Resultado esperado

O ambiente termina com RabbitMQ saudável, `hospital.events`, `billing.resultados.v1`, DLQ e SQLite com duas tentativas e um efeito. A mensagem inválida segue para dead-letter. A extensão conceitual trata retenção, offsets, particionamento e transações Kafka.

## Interpretação

O experimento demonstra entrega pelo menos uma vez, não exactly-once. SQLite evita duplicação entre execuções; em sistemas distribuídos, trate-a com banco e efeitos externos. O Compose não é produção: não inclui cluster, TLS, credenciais, backup ou retenção. Use evidência para discutir semântica.

## Limpeza e contingência

### Essencial em aula

**Objetivo**

Remover os recursos locais criados pela oficina sem afetar outros projetos.

**Pré-requisito**

A evidência desejada foi copiada para local apropriado e o terminal ainda está em `laboratorios/plataforma-hospitalar`.

**Execute**

```bash
docker compose -f infra/compose.eventos.yml down -v
rm -rf evidencias/modulo-5
```

No PowerShell, use `Remove-Item -Recurse -Force evidencias\modulo-5` para remover a pasta opcional de evidências.

**Observe**

`down -v` remove apenas serviços e volume nomeados por este arquivo Compose. Uma nova subida inicia sem filas e sem SQLite anterior.

**Compare**

Compare esta limpeza limitada com comandos globais do Docker: somente a primeira preserva recursos de outros estudos.

**Questões exploratórias**

- O que seria perdido se a DLQ fosse removida antes de ser analisada?
- Qual evidência deve ser guardada sem registrar dado sensível?

## Evidência a entregar

Entregue uma nota com: configuração validada; saídas `processed=True attempts=1` e `processed=False attempts=2`; consulta de um efeito; mensagem na DLQ; e a explicação de por que há entrega pelo menos uma vez com idempotência, não exactly-once. Use IDs sintéticos. Indique quando Kafka seria extensão, não substituição automática.
