# Oficina de ferramentas: política declarada, trace verificável

Esta oficina responde a uma pergunta que o livro-texto levanta: **como provar que uma política de governança está de fato valendo?** Uma decisão registrada em ata não governa nada; o que governa é a política aplicada em execução, deixando evidência que alguém consegue consultar depois.

Você vai colocar um *gateway* na frente do serviço de Elegibilidade, declarar três políticas num arquivo de configuração e então verificar cada uma pelo seu efeito observável: um cabeçalho de correlação que aparece na resposta, um `429` quando o limite de chamadas é excedido, e um rastro da requisição consultável numa ferramenta de observabilidade.

### O que você vai observar, e por que importa

| O que a oficina mostra | O conceito do módulo |
| --- | --- |
| A rota, o limite e a correlação vivem num arquivo de configuração, não no código do serviço | [Gateway como borda técnica](padroes-e-decisoes.md#gateway-como-borda-tecnica): política de infraestrutura fora do domínio |
| Um identificador acompanha a requisição do gateway até o serviço | [Correlação e rastreamento distribuído](padroes-e-decisoes.md#correlacao-rastreabilidade-e-rastreamento-distribuido) |
| Cada política declarada tem um efeito que se consegue medir | [Política como hipótese executável](conceitos.md#politica-como-hipotese-executavel) |
| O gateway limita tráfego, e não decide elegibilidade | O [limite deliberado](index.md#limite-deliberado) entre borda técnica e regra de negócio |

### Onde cada arquivo mora

Todos os comandos rodam a partir de `laboratorios/plataforma-hospitalar`.

```text
plataforma-hospitalar/
├── infra/
│   ├── compose.governanca.yml           ← os cinco contêineres da pilha
│   ├── kong/kong.yml                    ← as três políticas de borda
│   └── observabilidade/
│       └── otel-collector.yml           encaminhamento da telemetria
├── src/hospital/servicos/
│   └── elegibilidade.py                 o serviço por trás do gateway
└── tests/
    └── test_gateway_policy.py           verificação automatizada das políticas
```

| Arquivo | O que ele faz |
| --- | --- |
| [`infra/compose.governanca.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/compose.governanca.yml) | Declara os cinco contêineres: o banco, o serviço, o gateway, o coletor de telemetria e a ferramenta de consulta de rastros. |
| [`infra/kong/kong.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/kong/kong.yml) | O arquivo mais importante da oficina: declara a rota pública e as três políticas, em vinte linhas de YAML. |
| [`infra/observabilidade/otel-collector.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/infra/observabilidade/otel-collector.yml) | Diz ao coletor de onde receber telemetria e para onde encaminhá-la. |
| [`tests/test_gateway_policy.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/laboratorios/plataforma-hospitalar/tests/test_gateway_policy.py) | Verifica as políticas por código, sem depender de inspeção manual. |

## Ferramenta

Cinco peças compõem a pilha, e três delas são novas em relação aos módulos anteriores.

| Ferramenta | O que é | Para que serve aqui |
| --- | --- | --- |
| **Docker Engine e Compose** | Já usados no Módulo 3: executam e orquestram contêineres. | Subir os cinco componentes de uma vez. |
| **Kong Gateway 3.8** | Um *gateway* de API: um servidor que fica na frente de um ou mais serviços e aplica políticas comuns antes de encaminhar a requisição. | Aplicar rota, correlação e limite de tráfego sem tocar no código de Elegibilidade. |
| **OpenTelemetry** | Um padrão aberto para emitir telemetria — rastros, métricas e registros. Por ser padrão, o serviço emite sem saber qual ferramenta vai consumir. | Instrumentar gateway e serviço com o mesmo vocabulário. |
| **OpenTelemetry Collector** | Um intermediário que recebe telemetria e a encaminha ao destino final. | Desacoplar quem emite de quem armazena: trocar a ferramenta de consulta não exige mexer nos serviços. |
| **Jaeger** | Uma ferramenta de rastreamento distribuído, que armazena e permite consultar o caminho de uma requisição por vários serviços. | Recuperar o rastro completo de uma chamada a partir do seu identificador. |

Três termos precisam de tradução antes de aparecerem nos comandos. Um **rastro** (*trace*) é o registro do caminho completo de uma requisição, atravessando todos os componentes que a atenderam. Cada etapa desse caminho é um **intervalo** (*span*), com início, duração e o nome de quem a executou. E um **identificador de correlação** é um valor único atribuído à requisição na entrada, repassado a todos os componentes, para que os registros de cada um possam ser reunidos depois.

Duas ressalvas sobre o alcance do laboratório. O limite de três chamadas por segundo é contado localmente, dentro de uma única instância do gateway; em produção, com várias réplicas, o limite exigiria um armazenamento compartilhado, senão cada réplica contaria em separado.

Além disso, das quatro famílias de sinais que o módulo discute, esta oficina exercita apenas rastros e registros. Métricas são um sinal conceitual aqui: elas aparecem no desenho e na conversa sobre SLO, e esta oficina não coleta nem consulta métricas. As evidências que você vai guardar são cabeçalhos HTTP, o `429`, o identificador de correlação em registro seguro e o rastro consultado no Jaeger.

## Pré-requisitos

**Objetivo**

Preparar um ambiente isolado e confirmar ferramentas antes de iniciar contêineres.

**Pré-requisito**

Tenha o repositório local, Docker com Compose v2 e Python 3.11 ou superior. Execute os comandos a partir de `laboratorios/plataforma-hospitalar`. Escolha portas livres; os valores abaixo evitam colisão com o Compose do módulo anterior.

**Execute**

Confira as versões de Docker, Compose e Python. `docker version` mostra Client e Server quando o daemon responde.

**Observe**

A validação do arquivo pode funcionar com daemon indisponível, mas não demonstra contêiner ativo. Uma resposta HTTP e um trace são evidências diferentes.

**Compare**

Compare uma política em `kong.yml` com uma alteração dentro de contêiner. Apenas a primeira é revisável e repetível.

**Questões exploratórias**

- Que parte verifica a intenção da política e qual parte verifica comportamento?
- Por que uma resposta do gateway não demonstra que o trace chegou ao destino?

## Instalação

### Windows

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/windows-install/) e Python pela [documentação oficial](https://docs.python.org/3/using/windows.html). Em novo PowerShell:

```powershell
docker version
docker compose version
py --version
cd laboratorios\plataforma-hospitalar
py -m pip install -e ".[dev]"
New-Item -ItemType Directory -Force evidencias\modulo-4
```

**Resultado esperado**

Docker informa Client e Server, Compose informa versão e a pasta de evidências existe.

**Contingência**

Se o servidor Docker não responder, abra Docker Desktop e aguarde o mecanismo. Preserve a mensagem de erro; não altere permissões amplas nem remova recursos desconhecidos.

### macOS

Instale Docker Desktop pelas [instruções oficiais](https://docs.docker.com/desktop/setup/install/mac-install/) e Python por [Homebrew](https://brew.sh/) ou instalador oficial.

```bash
docker version
docker compose version
python3 --version
cd laboratorios/plataforma-hospitalar
python3 -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-4
```

**Resultado esperado**

As versões são exibidas e o pacote local é instalado. As imagens possuem variantes usuais para Apple Silicon e Intel.

**Contingência**

Se a instalação global falhar, use `python3 -m venv .venv`, ative com `source .venv/bin/activate` e repita.

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
mkdir -p evidencias/modulo-4
```

**Resultado esperado**

O daemon responde e o ambiente Python contém as dependências.

**Contingência**

Se o socket recusar conexão, siga o procedimento pós-instalação da documentação. Não use limpeza global do Docker para uma porta ocupada.

## As políticas declaradas no `kong.yml`

Vale ler este arquivo antes de subir a pilha, porque ele é o objeto de estudo do módulo: **a governança inteira desta oficina cabe em vinte linhas de configuração**, e nenhuma delas está no código do serviço.

A primeira parte declara para onde encaminhar as requisições:

```yaml
services:
  - name: elegibilidade
    url: http://elegibilidade:8000        # o destino interno
    routes:
      - name: elegibilidades-publicas
        paths:
          - /hospital                     # o caminho público
        strip_path: true                  # remove /hospital antes de encaminhar
        methods:
          - GET                           # só GET é aceito nesta rota
```

Uma chamada a `/hospital/elegibilidades/{beneficiario_id}` chega ao gateway, que retira o prefixo `/hospital` e repassa `/elegibilidades/{beneficiario_id}` ao serviço. O consumidor nunca conhece o endereço interno, e a linha `methods: [GET]` já é uma política: um `POST` nesse caminho é recusado pelo gateway, sem sequer alcançar o serviço.

Depois vêm as três políticas propriamente ditas:

```yaml
plugins:
  - name: correlation-id
    config:
      header_name: X-Correlation-ID
      generator: uuid                     # gera um identificador se não vier um
      echo_downstream: true               # devolve o valor ao consumidor

  - name: rate-limiting
    config:
      second: 3                           # três chamadas por segundo
      policy: local                       # contadas nesta instância apenas
      limit_by: ip                        # o limite é por origem
      fault_tolerant: false               # se o contador falhar, recusa
      hide_client_headers: false          # informa o limite ao consumidor

  - name: opentelemetry
    config:
      traces_endpoint: http://otel-collector:4318/v1/traces
      sampling_rate: 1                    # registra 100% das requisições
      propagation:
        default_format: w3c               # padrão de propagação entre serviços
```

Cada uma dessas configurações merece uma leitura, porque são decisões de arquitetura disfarçadas de parâmetro.

O `generator: uuid` resolve um problema concreto: se o consumidor não enviar um identificador de correlação, o gateway cria um. Assim nenhuma requisição fica sem rastro, mesmo vinda de um cliente que não coopera. E `echo_downstream: true` devolve esse identificador na resposta, permitindo que o consumidor cite o valor ao relatar um problema.

O `fault_tolerant: false` é a decisão menos óbvia e a mais reveladora. Ele diz o que fazer quando o próprio mecanismo de contagem falha: recusar a requisição, em vez de deixá-la passar. É a escolha entre falhar fechado e falhar aberto, e ela declara que, aqui, exceder o limite é pior que negar serviço.

O `sampling_rate: 1` significa registrar todas as requisições. Em produção, com volume alto, esse valor costuma cair — e aí a decisão passa a ser qual fração do tráfego se aceita não conseguir investigar depois.

Repare no que nenhuma dessas linhas faz: decidir elegibilidade. O gateway sabe rotear, contar chamadas e propagar identificadores, sem saber o que torna um beneficiário elegível. Se essa regra migrasse para cá, ficaria fora do domínio a que pertence, longe de quem responde por ela e sem os testes que a cercam. É a fronteira que o módulo defende, visível na diferença entre este arquivo e o `elegibilidade.py`.

## Preparação do laboratório

**Objetivo**

Validar a configuração declarativa antes de criar recursos e fixar endereços para este terminal.

**Pré-requisito**

Permaneça em `laboratorios/plataforma-hospitalar` e assegure portas livres.

**Execute**

No macOS ou Linux:

```bash
export ELEGIBILIDADE_PORT=18001
export GATEWAY_PORT=18000
export JAEGER_PORT=16686
export BENEFICIARIO_ID="<identificador-sintetico-da-base-local>"
docker compose -f infra/compose.governanca.yml config --quiet
docker compose -f infra/compose.governanca.yml config --services
```

No PowerShell:

```powershell
$env:ELEGIBILIDADE_PORT = 18001
$env:GATEWAY_PORT = 18000
$env:JAEGER_PORT = 16686
$env:BENEFICIARIO_ID = "<identificador-sintetico-da-base-local>"
docker compose -f infra/compose.governanca.yml config --quiet
docker compose -f infra/compose.governanca.yml config --services
```

**Observe**

O primeiro comando não imprime conteúdo e termina sem erro. O segundo lista banco, Elegibilidade, Kong, Collector e Jaeger. `kong.yml` declara rota, correlation ID, rate limiting e OTLP; `otel-collector.yml` encaminha ao Jaeger. PostgreSQL e API administrativa do Kong não publicam portas.

Defina `BENEFICIARIO_ID` com o identificador sintético provisionado pela base local. Esse valor só entra na chamada HTTP: não o copie para nome de evidência, log, atributo de trace ou texto de entrega.

**Compare**

`config --quiet` demonstra que o documento é interpretável. Ele não confirma prontidão, resposta HTTP ou trace.

**Questões exploratórias**

- Qual rede impede Kong de chegar ao banco de Elegibilidade?
- Por que a variável OTLP é recebida pelo serviço e não pelo banco?

**Objetivo**

Ler a política antes de executá-la e atribuir ownership a cada decisão.

**Pré-requisito**

Abra `infra/kong/kong.yml` e `infra/observabilidade/otel-collector.yml`.

**Execute**

Percorra os dois arquivos separando o que acontece na borda do que acontece na telemetria, e localize no texto a linha exata que sustenta cada afirmação.

**Observe**

Gateway aplica limite e correlação; Elegibilidade mantém consulta e banco. Collector transporta telemetria; regra clínica não passa por ele.

**Compare**

Classifique cada linha como política de borda, de serviço, transporte ou evidência.

**Questões exploratórias**

- Em que arquivo ficaria uma exceção para plano hospitalar?
- Que mudança de limite exigiria avisar consumidores?

**Objetivo**

Planejar uma mudança reversível de limite.

**Pré-requisito**

Leia `rate-limiting` em `kong.yml`.

**Execute**

Escreva hipótese, responsável, efeito sobre consumidor, métrica e condição de retorno.

**Observe**

Uma alteração numérica é mudança de política, ainda que pareça um detalhe menor.

**Compare**

Compare decisão registrada com alteração feita apenas no terminal.

**Questões exploratórias**

- O que muda ao limitar por aplicação cliente?
- Qual sinal indica falsa recusa de tráfego legítimo?

## Execução

**Objetivo**

Iniciar componentes, distinguir acesso direto de acesso governado e coletar evidência de correlação, limite e trace.

**Pré-requisito**

Mantenha as variáveis de porta da preparação no mesmo terminal.

**Execute**

```bash
docker compose -f infra/compose.governanca.yml up -d --build --wait
docker compose -f infra/compose.governanca.yml ps
```

**Resultado esperado**

Os cinco serviços ficam saudáveis. O acesso direto usa `http://localhost:${ELEGIBILIDADE_PORT}/elegibilidades/${BENEFICIARIO_ID}`; o caminho público usa `http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/${BENEFICIARIO_ID}`.

**Contingência**

Se a construção não baixar imagem, guarde o log e repita quando houver conectividade. Se uma porta estiver ocupada, escolha variável nova e rode `config --quiet`; não pare processo desconhecido.

Em macOS ou Linux, consulte diretamente e depois pelo gateway:

```bash
curl -i "http://localhost:${ELEGIBILIDADE_PORT}/elegibilidades/${BENEFICIARIO_ID}"
export CORRELATION_ID="aula-$(uuidgen | tr '[:upper:]' '[:lower:]')"
curl -i "http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/${BENEFICIARIO_ID}" -H "X-Correlation-ID: ${CORRELATION_ID}"
```

No PowerShell:

```powershell
$env:CORRELATION_ID = "aula-" + [guid]::NewGuid().ToString()
curl.exe -i "http://localhost:$env:ELEGIBILIDADE_PORT/elegibilidades/$env:BENEFICIARIO_ID"
curl.exe -i "http://localhost:$env:GATEWAY_PORT/hospital/elegibilidades/$env:BENEFICIARIO_ID" -H "X-Correlation-ID: $env:CORRELATION_ID"
```

**Observe**

As duas chamadas devolvem `200 OK` e o mesmo corpo sintético, mas os cabeçalhos são bem diferentes. A resposta pelo gateway traz isto:

```text
HTTP/1.1 200 OK
Content-Type: application/json

X-RateLimit-Remaining-Second: 2      ← quantas chamadas ainda restam neste segundo
X-RateLimit-Limit-Second: 3          ← o limite declarado no kong.yml
RateLimit-Reset: 1                   ← em quantos segundos o contador zera

x-correlation-id: b8f3e694-ca24-4dce-8eb8-d6ac1620faea

X-Kong-Upstream-Latency: 7           ← tempo que o serviço levou (ms)
X-Kong-Proxy-Latency: 31             ← tempo que o próprio gateway consumiu (ms)
Via: 1.1 kong/3.8.0
```

Cada bloco é uma política se anunciando. Os três cabeçalhos `RateLimit` existem porque `hide_client_headers: false` foi declarado: o consumidor sabe quanto lhe resta antes de ser recusado, o que lhe permite se autorregular em vez de descobrir o limite batendo nele.

O `x-correlation-id` é o identificador que acompanhará esta requisição pelos registros e pelo rastro. Como a chamada não enviou um, o gateway gerou.

Os dois cabeçalhos de latência separam o tempo do serviço do tempo do gateway, e essa distinção é o que permite responder "quem está lento?" sem abrir nenhuma ferramenta. Aqui a mediação custou 31 ms contra 7 ms do serviço, número típico da primeira chamada, quando o gateway ainda está aquecendo conexões.

Já a chamada direta ao serviço, sem passar pelo gateway, não traz nenhum desses cabeçalhos. Ela serve para diagnosticar se o serviço e o banco estão de pé, e nada mais: sem gateway não há limite de tráfego nem correlação. **É essa diferença que mostra onde a política mora.**

**Compare**

Compare `200` direto com `200` governado. O segundo acrescenta política de borda, sem assumir regra clínica.

**Questões exploratórias**

- Qual caminho um consumidor externo deve usar?
- Por que o cabeçalho não prova autorização de domínio?

**Objetivo**

Exceder deliberadamente o limite declarado e interpretar a recusa.

**Pré-requisito**

Entre em uma janela nova de um segundo. A preparação abaixo não toca o gateway; assim, as quatro chamadas seguintes são a única carga contada para esta prova.

**Execute**

No macOS ou Linux, espere até o começo da próxima janela e envie quatro chamadas imediatamente em sequência:

```bash
python -c 'import time; time.sleep(max(0, int(time.time()) + 1.15 - time.time()))'
for n in 1 2 3 4; do curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/${BENEFICIARIO_ID}"; done
python -c 'import time; time.sleep(max(0, int(time.time()) + 1.15 - time.time()))'
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/${BENEFICIARIO_ID}"
```

No PowerShell:

```powershell
$ateProximaJanela = 1100 - ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() % 1000)
Start-Sleep -Milliseconds $ateProximaJanela
1..4 | ForEach-Object { curl.exe -s -o NUL -w "%{http_code}`n" "http://localhost:$env:GATEWAY_PORT/hospital/elegibilidades/$env:BENEFICIARIO_ID" }
$ateProximaJanela = 1100 - ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() % 1000)
Start-Sleep -Milliseconds $ateProximaJanela
curl.exe -s -o NUL -w "%{http_code}`n" "http://localhost:$env:GATEWAY_PORT/hospital/elegibilidades/$env:BENEFICIARIO_ID"
```

**Resultado esperado**

A sequência de códigos é exatamente esta:

```text
1: 200
2: 200
3: 200
4: 429
5: 429
```

Três passam, a quarta é recusada. O número não é acidente: é o `second: 3` do `kong.yml` produzindo efeito observável. **A política declarada em configuração acabou de ser verificada por experimento**, e é isso que o módulo quer dizer com política como hipótese executável.

A resposta `429` traz um cabeçalho que a de sucesso não tinha:

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 1                       ← quando tentar de novo, em segundos
X-RateLimit-Remaining-Second: 0
X-RateLimit-Limit-Second: 3
X-Correlation-ID: a0acc7f5-be3c-470b-970c-d023bd6cfac9
```

O `Retry-After` transforma a recusa em instrução acionável: o consumidor não precisa adivinhar quanto esperar. E o identificador de correlação continua presente, porque a requisição recusada também precisa ser rastreável — investigar por que um cliente legítimo está sendo bloqueado exige encontrar essas chamadas depois.

Passado um segundo, a contagem zera e as chamadas voltam a `200`. Elegibilidade nunca ficou indisponível: quem recusou foi o gateway, na borda, antes de a requisição alcançar o serviço.

**Observe**

O limite é por origem e local ao processo Kong. Paralelismo, outra origem ou mais réplicas mudam a interpretação.

**Compare**

Compare `429` com `503`: o primeiro pede redução de ritmo; o segundo comunica indisponibilidade de capacidade.

**Questões exploratórias**

- Que cliente deveria usar espera progressiva ao receber `429`?
- Qual política adicional protegeria uma rota de escrita idempotente?

**Objetivo**

Consultar um trace pelo identificador que conecta a requisição a seus spans.

**Pré-requisito**

Use trace ID hexadecimal de 32 caracteres e envie `traceparent` válido.

**Execute**

No macOS ou Linux:

```bash
export TRACE_ID=$(python -c 'from uuid import uuid4; print(uuid4().hex)')
export SPAN_ID=$(python -c 'from uuid import uuid4; print(uuid4().hex[:16])')
curl -i "http://localhost:${GATEWAY_PORT}/hospital/elegibilidades/${BENEFICIARIO_ID}" -H "X-Correlation-ID: ${CORRELATION_ID}" -H "traceparent: 00-${TRACE_ID}-${SPAN_ID}-01"
curl -s "http://localhost:${JAEGER_PORT}/api/traces/${TRACE_ID}"
```

No PowerShell:

```powershell
$env:TRACE_ID = [guid]::NewGuid().ToString("N")
$env:SPAN_ID = ([guid]::NewGuid().ToString("N")).Substring(0,16)
curl.exe -i "http://localhost:$env:GATEWAY_PORT/hospital/elegibilidades/$env:BENEFICIARIO_ID" -H "X-Correlation-ID: $env:CORRELATION_ID" -H "traceparent: 00-$env:TRACE_ID-$env:SPAN_ID-01"
curl.exe -s "http://localhost:$env:JAEGER_PORT/api/traces/$env:TRACE_ID"
```

**Resultado esperado**

O JSON contém processos `kong-gateway` e `elegibilidade`. Procure o correlation ID nos atributos. Se Collector ainda estiver exportando, repita a consulta por até vinte segundos, sem criar chamadas novas.

**Observe**

O trace ID confirma propagação de contexto; dois processos confirmam que a operação não termina no proxy. Correlation ID facilita busca entre logs e resposta, mas não substitui relação pai-filho.

**Compare**

Compare resposta HTTP, log estruturado do serviço e JSON da API. Cada um responde pergunta operacional diferente.

Para registrar o log seguro, em qualquer sistema execute:

```bash
docker compose -f infra/compose.governanca.yml logs --no-color elegibilidade > evidencias/modulo-4/log-elegibilidade.jsonl
```

O arquivo deve conter o `correlation_id` gerado e a rota-modelo `/elegibilidades/{beneficiario_id}`; ele não pode conter o valor de `BENEFICIARIO_ID`. O serviço desativa o access log do Uvicorn e o Kong desativa o access log de proxy para que a URI concreta não vá para saída padrão. Antes de exportar spans para Jaeger, o Collector também remove atributos de URL e caminho que Kong possa emitir; a evidência de trace conserva a rota-modelo e nunca a URI concreta.

**Questões exploratórias**

- Que atributo de trace não deve conter identificador de paciente?
- Como detectar perda de spans sem tornar Collector dependência da consulta?

## Resultado esperado

Há evidência de cinco serviços saudáveis, consulta direta `200`, consulta governada com `X-Correlation-ID`, recusa `429` e trace com `kong-gateway` e `elegibilidade`. Resultados diferentes devem incluir comando, horário e saída.

## Interpretação

Kong governa borda pública; Elegibilidade governa modelo e dado. Collector transporta telemetria; Jaeger guarda evidência de estudo. A cadeia une design-time — arquivos versionados, dono e decisão — a runtime — cabeçalho, código HTTP, log e trace. Métricas permanecem apenas como conceito de desenho e SLO nesta oficina, sem coleta nem consulta. Ela não demonstra alta disponibilidade, retenção, autorização corporativa ou limite distribuído.

## Limpeza e contingência

**Execute**

```bash
docker compose -f infra/compose.governanca.yml down -v
docker compose -f infra/compose.governanca.yml ps -a
```

Para mudar a política local, edite `infra/kong/kong.yml`, revise o diff, valide e reconstrua somente Kong. O arquivo é copiado para a imagem didática durante o build, o que evita estado manual e torna a versão aplicada explícita:

```bash
docker compose -f infra/compose.governanca.yml config --quiet
docker compose -f infra/compose.governanca.yml up -d --build kong
```

**Resultado esperado**

O primeiro comando remove somente contêineres, rede e volume didático. A reconstrução cria Kong com o `kong.yml` revisado; repita chamada e limite para confirmar a mudança e restaure valor de aula.

**Contingência**

Se o daemon não respondeu, execute `docker compose -f infra/compose.governanca.yml config --quiet` e `python -m unittest tests.test_module_four -v`, registrando que contêineres não foram executados. Se Jaeger não encontrar trace, leia `docker compose -f infra/compose.governanca.yml logs otel-collector kong elegibilidade`, confirme endpoint OTLP e `traceparent`, corrija arquivo versionado e reinicie o componente. Não crie estado manual em painel.

## Evidência a entregar

Guarde em `evidencias/modulo-4`:

- `versoes.txt` com versões;
- `compose-ps.txt` com estados saudáveis;
- `direto.txt` e `gateway-correlacao.txt`;
- `limite-429.txt` com sequência controlada;
- `trace.json` com `api/traces/${TRACE_ID}`;
- `log-elegibilidade.jsonl` com correlation ID e rota-modelo, sem identificador de beneficiário;
- `testes-integracao.txt` com `python -m pytest tests/test_gateway_policy.py -q`;
- `limpeza.txt` com remoção ou contingência explícita.

Relacione cada arquivo a rota, correlação, limite, propagação ou limpeza. Identifiquem uma afirmação ainda não demonstrada e a política necessária.

Proponha um SLO para Elegibilidade: indicador, objetivo, janela, fonte, dono e comportamento quando orçamento de erro for consumido. Não adicione dado clínico a logs ou traces.
