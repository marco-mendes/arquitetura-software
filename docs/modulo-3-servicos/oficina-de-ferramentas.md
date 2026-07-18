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

Antes deste Compose: a demonstração é `compose.servicos.yml`, com `elegibilidade`, `exames`, `db_elegibilidade` e `db_exames`, todos parados. Ele só valida arquivos; numa execução, espere os dois `/health` em `200` nas portas configuradas. Encerre com `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml config --quiet
```

Resultado: nenhum texto e código zero significam que a configuração é sintaticamente válida. Essa validação não demonstra que Docker está em execução nem que os serviços estão saudáveis.

Antes deste Compose: `infra/compose.servicos.yml` ainda declara Elegibilidade, Exames e suas duas bases paradas. Ele só lista a topologia; não há portas ou health checks ativos. Depois de iniciar, espere 18001/18002 e encerre com `down -v`.

```bash
docker compose -f infra/compose.servicos.yml config --services
```

Confirme os quatro nomes apresentados. O comando ajuda a evitar iniciar um arquivo Compose diferente por engano.

## Iniciar e observar a demonstração

Antes deste Compose: a demonstração **serviços da plataforma hospitalar** usa `infra/compose.servicos.yml` e `src/hospital/servicos/` para iniciar Elegibilidade, Exames e suas duas bases, todas paradas inicialmente. Espere os dois `/health` em `200` nas portas configuradas; encerre com `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml up -d --build --wait
```

## Resultado esperado

O `--wait` termina quando os quatro health checks ficam saudáveis. Se uma imagem não puder ser baixada ou uma porta estiver ocupada, guarde a saída e escolha outra porta; não remova recursos Docker fora deste projeto.

Antes deste Compose: `infra/compose.servicos.yml` mantém Elegibilidade, Exames e as duas bases em execução. Espere aplicações e bases `healthy`, com os dois `/health` nas portas configuradas. Encerre somente esta demonstração com `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml ps
```

A saída equivalente de `docker compose ps` deve listar `db_elegibilidade`, `db_exames`, `elegibilidade` e `exames` como `healthy`. Com as portas escolhidas, as aplicações aparecem como `0.0.0.0:18001->8000` e `0.0.0.0:18002->8000`.

Confirme a saúde a partir da sua máquina:

```bash
curl -i "http://localhost:${ELEGIBILIDADE_PORT}/health"
curl -i "http://localhost:${EXAMES_PORT}/health"
```

Cada resposta deve ser `200`. Agora crie uma solicitação elegível:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

Espere `201 Created`, com `situacao: "solicitado"`. O identificador pode variar entre execuções; depois de `down -v`, volta ao primeiro valor da nova base.

## Interpretação

### Tornar a falha parcial observável

Antes deste Compose: `infra/compose.servicos.yml` tem as duas aplicações e bases saudáveis. Pare só Elegibilidade; Exames e `db_exames` ficam ativos e seu `/health` continua `200`. Encerre todos os recursos depois com `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml stop elegibilidade
```

Antes deste Compose: o mesmo arquivo contém as duas aplicações e bases, mas Elegibilidade está parada; Exames e sua base continuam saudáveis na porta configurada. Encerre tudo com `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml ps
```

Repita a chamada abaixo. Ela deve retornar `503 Service Unavailable` e o código `dependencia_indisponivel`, enquanto `GET /health` de Exames ainda retorna `200`:

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

Essa é a falha parcial: a capacidade de criar exame depende temporalmente de Elegibilidade, mas o processo e a base de Exames não pararam.

Antes deste Compose: `infra/compose.servicos.yml` e seus dois serviços e bancos permanecem definidos, com Elegibilidade parada e Exames saudável. Reinicie e espere ambos os `/health` em `200`; encerre com `docker compose -f infra/compose.servicos.yml down -v`.

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

Antes deste Compose: `infra/compose.servicos.yml` reúne os arquivos em `src/hospital/servicos/`, os dois serviços e suas bases, saudáveis nas portas 18001/18002. O comando remove contêineres, redes e volumes; depois não há portas ou health checks. Ele encerra a demonstração.

```bash
docker compose -f infra/compose.servicos.yml down -v
```

Antes deste Compose: o arquivo ainda descreve os dois serviços e bases, mas todos estão encerrados, sem portas ou health checks. O comando confirma isso; se houver resíduo, repita `docker compose -f infra/compose.servicos.yml down -v`.

```bash
docker compose -f infra/compose.servicos.yml ps -a
```

## Evidência a entregar

Guarde em `laboratorios/plataforma-hospitalar/evidencias/modulo-3/` as saídas de versões, health checks, `201`, `503` e testes. Se o daemon nunca respondeu, faça somente `config --quiet` e os testes Python e registre: “Compose validado estaticamente; execução de contêineres não realizada porque o daemon não respondeu”. Não afirme que observou health checks sem uma execução real.
