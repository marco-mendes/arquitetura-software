# Oficina de ferramentas: política declarada, trace verificável

Esta oficina acrescenta governança à plataforma hospitalar sem alterar a fronteira de dados do módulo anterior. Você subirá PostgreSQL, Elegibilidade, Kong, OpenTelemetry Collector e Jaeger a partir de `infra/compose.governanca.yml`. Chamará o serviço diretamente e pelo gateway, confirmará correlation ID, produzirá um `429` controlado e consultará um trace pela API do Jaeger. Todos os recursos são locais, descartáveis e de código aberto; não há estado configurado por painel.

## Ferramenta

| Ferramenta | Papel local | Evidência observável |
| --- | --- | --- |
| Docker Engine e Compose v2 | criar rede e contêineres | `docker version` e `docker compose version` |
| Kong Gateway 3.8 | rota e políticas declaradas | resposta com cabeçalho e `429` |
| OpenTelemetry Collector 0.111 | receber e encaminhar OTLP | trace no destino |
| Jaeger all-in-one 1.62 | consultar trace local | `GET /api/traces/{id}` |
| Python 3.11 ou superior | executar integração | `test_gateway_policy.py` |

O Docker Compose é uma reprodução de estudo, não uma topologia de produção. O limite de três chamadas por segundo usa armazenamento local do Kong; múltiplas réplicas exigiriam uma decisão de armazenamento compartilhado. O Jaeger local não é retenção de dados clínicos e não deve receber dados sensíveis. Métricas são um sinal conceitual nesta oficina: ela não coleta nem consulta métricas. As evidências runtime deste roteiro são cabeçalhos, `429`, log JSON seguro e traces no Jaeger.

## Pré-requisitos

### Essencial em aula

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

## Preparação do laboratório

### Essencial em aula

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

### Exploração em dupla

**Objetivo**

Ler a política antes de executá-la e atribuir ownership a cada decisão.

**Pré-requisito**

Abra `infra/kong/kong.yml` e `infra/observabilidade/otel-collector.yml`.

**Execute**

Uma pessoa descreve o que ocorre na borda; a outra descreve os spans. Troquem descrições e localizem cada afirmação no arquivo.

**Observe**

Gateway aplica limite e correlação; Elegibilidade mantém consulta e banco. Collector transporta telemetria, não regra clínica.

**Compare**

Classifique cada linha como política de borda, de serviço, transporte ou evidência.

**Questões exploratórias**

- Em que arquivo ficaria uma exceção para plano hospitalar?
- Que mudança de limite exigiria avisar consumidores?

### Extensão

**Objetivo**

Planejar uma mudança reversível de limite.

**Pré-requisito**

Leia `rate-limiting` em `kong.yml`.

**Execute**

Escreva hipótese, responsável, efeito sobre consumidor, métrica e condição de retorno.

**Observe**

Uma alteração numérica é mudança de política, não mero detalhe.

**Compare**

Compare decisão registrada com alteração feita apenas no terminal.

**Questões exploratórias**

- O que muda ao limitar por aplicação cliente?
- Qual sinal indica falsa recusa de tráfego legítimo?

## Execução

### Essencial em aula

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

As duas chamadas devolvem `200 OK` e o mesmo corpo sintético. A chamada governada ecoa `X-Correlation-ID`; se omitido, Kong cria UUID. O acesso direto diagnostica serviço e banco; não demonstra rate limiting.

**Compare**

Compare `200` direto com `200` governado. O segundo acrescenta política de borda, sem assumir regra clínica.

**Questões exploratórias**

- Qual caminho um consumidor externo deve usar?
- Por que o cabeçalho não prova autorização de domínio?

### Exploração em dupla

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

As quatro primeiras linhas são exatamente `200`, `200`, `200` e `429 Too Many Requests`. A quinta linha, depois da janela nova, volta a `200`. O `429` é proteção de tráfego, não indisponibilidade de Elegibilidade.

**Observe**

O limite é por origem e local ao processo Kong. Paralelismo, outra origem ou mais réplicas mudam a interpretação.

**Compare**

Compare `429` com `503`: o primeiro pede redução de ritmo; o segundo comunica indisponibilidade de capacidade.

**Questões exploratórias**

- Que cliente deveria usar espera progressiva ao receber `429`?
- Qual política adicional protegeria uma rota de escrita idempotente?

### Extensão

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

### Exploração em dupla

Relacione cada arquivo a rota, correlação, limite, propagação ou limpeza. Identifiquem uma afirmação ainda não demonstrada e a política necessária.

### Extensão

Proponha um SLO para Elegibilidade: indicador, objetivo, janela, fonte, dono e comportamento quando orçamento de erro for consumido. Não adicione dado clínico a logs ou traces.
