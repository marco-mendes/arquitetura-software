# Oficina de ferramentas: dois serviços, dois bancos e uma falha parcial

Nesta oficina, a demonstração local descartável é definida por `laboratorios/plataforma-hospitalar/infra/compose.servicos.yml`. Ela reúne os arquivos de aplicação em `laboratorios/plataforma-hospitalar/src/hospital/servicos/`, dois serviços FastAPI (`elegibilidade` e `exames`) e duas bases PostgreSQL (`db_elegibilidade` e `db_exames`). Elegibilidade decide se um beneficiário pode prosseguir; Exames consulta esse contrato e grava somente em sua própria base. Ao iniciar, nada está em execução; ao encerrar com `down -v`, contêineres, redes e dados didáticos são removidos.

As senhas são exclusivas dessa demonstração local. Dados são sintéticos. O health check de cada aplicação confirma seu processo e banco próprio, não todas as dependências remotas.

## Ferramenta

| Ferramenta | Uso | Verificação |
| --- | --- | --- |
| Docker Engine e Docker Compose v2 | contêineres, redes e health checks | `docker version` e `docker compose version` |
| Python 3.11+ | testes de fronteira | `python --version` |
| FastAPI, httpx e PostgreSQL 16 | HTTP e persistência isolada | respostas de saúde e dois bancos |

**Objetivo**

Observar uma fronteira de dados e uma falha parcial em uma demonstração local.

**Pré-requisito**

Docker em execução e Python 3.11 ou superior.

## Pré-requisitos

Verifique `docker version`, `docker compose version` e `python --version` antes de continuar.

## Instalação

### Windows

Instale Docker Desktop e Python; use `py` quando `python` não estiver no PATH.

### macOS

Instale Docker Desktop e Python 3 pelo instalador oficial ou gerenciador de pacotes.

### Linux

Instale Docker Engine, o plugin Compose e Python 3 pelo método da sua distribuição.

## Preparação do laboratório

Na raiz do clone, entre na pasta do laboratório e prepare um local para evidências. Em Windows use `py` no lugar de `python`, se necessário.

```bash
cd laboratorios/plataforma-hospitalar
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-3
```

No PowerShell, o equivalente para o diretório é `New-Item -ItemType Directory -Force evidencias\modulo-3`.

## Execução

**Execute**

As etapas na ordem.

**Observe**

A saída de cada uma.

**Compare**

O estado nominal com a falha parcial.

**Questões exploratórias**

Qual dependência permanece saudável e qual capacidade deixa de ser concluída?

Modalidades: **Essencial em aula**, **Exploração em dupla** e **Extensão** usam o mesmo roteiro com profundidades diferentes.

### Roteiro de transição do ambiente

| Etapa | Estado de entrada | Ação e evidência esperada | Contingência |
| --- | --- | --- | --- |
| Validar configuração | Os quatro serviços estão parados. | Execute os dois comandos `config`; `--quiet` termina sem texto e `--services` lista `elegibilidade`, `exames`, `db_elegibilidade` e `db_exames`. | Se o Docker não responder, guarde a saída e faça só a validação estática. |
| Iniciar e inspecionar | Compose válido e serviços parados. | Suba a demonstração; `ps` mostra quatro serviços `healthy` e os dois `/health` retornam `200`. | Se uma porta estiver ocupada, escolha outras portas; não remova recursos fora deste projeto. |
| Demonstrar falha parcial | As duas aplicações e bases estão saudáveis. | Pare `elegibilidade`; Exames permanece saudável, mas `POST /exames` retorna `503 dependencia_indisponivel`. | Se o resultado divergir, guarde `ps` e logs antes de reiniciar. |
| Recuperar e verificar | Elegibilidade está parada e Exames continua saudável. | Execute `up -d --wait`; os dois `/health` voltam a `200`, então rode o teste de fronteiras. | Se o daemon não responder, execute somente os testes Python e registre a limitação. |
| Limpar | A demonstração pode estar em qualquer estado anterior. | `down -v` remove contêineres, redes e volumes; `ps -a` não lista recursos ativos. | Se houver resíduo, repita apenas esse `down -v`. |

### Escolher portas e validar a configuração

Defina portas livres para não disputar os padrões 8001 e 8002. Em shells POSIX:

```bash
export ELEGIBILIDADE_PORT=18001
export EXAMES_PORT=18002
```

No PowerShell:

```powershell
$env:ELEGIBILIDADE_PORT = 18001
$env:EXAMES_PORT = 18002
```

```bash
docker compose -f infra/compose.servicos.yml config --quiet
```

Resultado: nenhum texto e código zero significam que a configuração é sintaticamente válida. Essa validação não demonstra que Docker está em execução nem que os serviços estão saudáveis.

```bash
docker compose -f infra/compose.servicos.yml config --services
```

Confirme os quatro nomes apresentados. O comando ajuda a evitar iniciar um arquivo Compose diferente por engano.

## Iniciar e observar a demonstração

```bash
docker compose -f infra/compose.servicos.yml up -d --build --wait
```

## Resultado esperado

O `--wait` termina quando os quatro health checks ficam saudáveis. Se uma imagem não puder ser baixada ou uma porta estiver ocupada, guarde a saída e escolha outra porta; não remova recursos Docker fora deste projeto.

```bash
docker compose -f infra/compose.servicos.yml ps
```

A saída equivalente de `docker compose ps` deve listar `db_elegibilidade`, `db_exames`, `elegibilidade` e `exames` como `healthy`. Com as portas escolhidas, as aplicações aparecem como `0.0.0.0:18001->8000` e `0.0.0.0:18002->8000`.

Confirme a saúde a partir da sua máquina:

```bash
curl -i "http://localhost:${ELEGIBILIDADE_PORT}/health"
curl -i "http://localhost:${EXAMES_PORT}/health"
```

No PowerShell, `curl.exe` evita o alias `curl` para `Invoke-WebRequest`:

```powershell
curl.exe -i "http://localhost:$env:ELEGIBILIDADE_PORT/health"
curl.exe -i "http://localhost:$env:EXAMES_PORT/health"
```

Cada resposta deve ser `200`. Agora crie uma solicitação elegível:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

PowerShell (201):

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

Espere `201 Created`, com `situacao: "solicitado"`. O identificador pode variar entre execuções; depois de `down -v`, volta ao primeiro valor da nova base.

## Interpretação

### Tornar a falha parcial observável

```bash
docker compose -f infra/compose.servicos.yml stop elegibilidade
```

```bash
docker compose -f infra/compose.servicos.yml ps
```

Repita a chamada abaixo. Ela deve retornar `503 Service Unavailable` e o código `dependencia_indisponivel`, enquanto `GET /health` de Exames ainda retorna `200`:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

PowerShell (503):

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

Essa é a falha parcial: a capacidade de criar exame depende temporalmente de Elegibilidade, mas o processo e a base de Exames não pararam.

```bash
docker compose -f infra/compose.servicos.yml up -d --wait
```

## Verificar as fronteiras sem depender do Compose

Com os serviços saudáveis, execute:

```bash
python -m pytest tests/test_service_boundaries.py -q
```

Espere `4 passed`, incluindo `test_exames_makes_its_own_database_failure_observable`. Os testes verificam o contrato HTTP, a falha parcial, a falha da base própria e a ausência de SQL contra a tabela de Elegibilidade. Em Windows sem ambiente ativado, use `py -m pytest tests/test_service_boundaries.py -q`.

## Limpeza e contingência

### Limpar a demonstração

```bash
docker compose -f infra/compose.servicos.yml down -v
```

```bash
docker compose -f infra/compose.servicos.yml ps -a
```

## Evidência a entregar

Guarde em `laboratorios/plataforma-hospitalar/evidencias/modulo-3/` as saídas de versões, health checks, `201`, `503` e testes. Se o daemon nunca respondeu, faça somente `config --quiet` e os testes Python e registre: “Compose validado estaticamente; execução de contêineres não realizada porque o daemon não respondeu”. Não afirme que observou health checks sem uma execução real.
