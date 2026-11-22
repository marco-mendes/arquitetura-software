# Oficina de ferramentas

A oficina executa dois serviços separados com bancos de dados próprios e provoca a falha de um deles enquanto o outro continua em execução. A atividade torna observáveis três decisões discutidas nas páginas de teoria do módulo, que são a propriedade dos dados, a fronteira física e a falha parcial.

O caso é a plataforma da rede hospitalar fictícia usada nas páginas anteriores do módulo, que atende pacientes de planos de saúde. **Elegibilidade** decide se o paciente tem cobertura do plano naquele momento. **Exames** registra o pedido de exame feito pelo médico depois de consultar a decisão de Elegibilidade, de modo que a recepção só confirma o pedido ao paciente quando Elegibilidade responde. As duas capacidades têm dados e ciclos de mudança próprios, o que permite usá-las para demonstrar uma fronteira entre serviços.

### Objetivo da oficina {#o-que-a-oficina-demonstra}

| Observação na oficina | Conceito do módulo |
| --- | --- |
| Cada serviço só alcança o próprio banco, por construção da rede | [Propriedade dos dados](conceitos.md#propriedade-dos-dados) e banco por serviço |
| Exames responde `200` na verificação de saúde e `503` na operação | [Falha parcial](conceitos.md#chamadas-sincronas-e-falhas-parciais), em que o sistema degrada em partes e continua parcialmente disponível |
| A chamada entre serviços tem prazo de espera e traduz o erro do vizinho | O custo da [fronteira física](conceitos.md#fronteira-logica-e-fronteira-fisica), que a chamada local não tinha |

![Serviços e bancos isolados com degradação durante uma falha parcial](../assets/images/m03-oficina-falha-parcial.png)

*Figura 5 — Fronteira de dados definida pela rede e degradação de um serviço durante a falha da dependência. Fonte: curso.*

**Leitura textual da figura:** três faixas horizontais representam redes distintas. Na rede de serviços, a API de Exames chama a API de Elegibilidade pela biblioteca httpx com prazo de espera declarado. Na rede de banco de dados, cada serviço tem o próprio PostgreSQL privado, sem caminho de rede entre os dois bancos. A parte inferior mostra o resultado observável durante a falha, com `GET /health` respondendo 200 enquanto a operação responde 503, porque Elegibilidade está fora do ar.

### Topologia da oficina {#a-topologia-que-voce-vai-montar}

O diagrama abaixo representa a topologia declarada no arquivo de composição, que convém entender antes de escrever os arquivos da oficina.

```mermaid
flowchart TB
    CL[Você, pelo terminal<br/>portas 18001 e 18002] --> AN[rede application-net]
    AN --> EL[serviço elegibilidade]
    AN --> EX[serviço exames]
    EX -->|httpx com prazo de 2s| EL
    EL --> RE[rede elegibilidade-db-net<br/>internal: true]
    EX --> RX[rede exames-db-net<br/>internal: true]
    RE --> DE[(Postgres elegibilidade)]
    RX --> DX[(Postgres exames)]
```

**Texto alternativo:** o terminal alcança os dois serviços por uma rede de aplicação, em que Exames chama Elegibilidade por HTTP com prazo de espera. Cada serviço tem uma rede interna própria que leva ao seu banco, sem ligação entre as duas redes de banco.

*Figura 11 — Redes da oficina e isolamento entre um serviço e o banco do outro. Fonte: curso.*

**Leitura textual da figura:** o terminal alcança as portas publicadas dos dois serviços, que estão na rede de aplicação. Nessa rede, o serviço de Exames chama o serviço de Elegibilidade por HTTP com prazo de espera de dois segundos. Cada serviço pertence também a uma segunda rede, marcada como interna, que leva ao próprio PostgreSQL. As duas redes de banco não têm ligação entre si nem saída externa, por isso o serviço de Exames não consegue resolver o nome do banco de Elegibilidade. A fronteira de dados é garantida pela construção da rede e não depende da disciplina de quem escreve o código.

### Arquivos da oficina {#onde-cada-arquivo-mora}

A oficina começa por uma pasta vazia chamada `oficina-servicos`, na qual são escritos os nove arquivos abaixo. Todos os comandos rodam a partir dessa pasta.

```text
oficina-servicos/                   ← execute os comandos a partir daqui
├── pyproject.toml                  declara as bibliotecas e torna o pacote instalável
├── Dockerfile                      a imagem compartilhada pelos dois serviços
├── infra/
│   ├── compose.servicos.yml        define os quatro contêineres e as três redes
│   └── postgres/
│       ├── Dockerfile              imagem do banco, com o script de carga
│       └── init.sql                cria papéis restritos, tabelas e dados sintéticos
├── src/hospital/
│   ├── __init__.py                 vazio, torna hospital um pacote
│   └── servicos/
│       ├── __init__.py             vazio, torna servicos um pacote
│       ├── elegibilidade.py        o serviço que decide
│       └── exames.py               o serviço que depende do primeiro
├── tests/
│   └── test_service_boundaries.py  os quatro testes de fronteira
└── evidencias/modulo-3/            você criará esta pasta na preparação
```

Cada arquivo aparece completo nesta página. O título de cada bloco é um link para o mesmo arquivo no repositório do curso, com conteúdo idêntico ao da página.

No macOS e no Linux, os comandos abaixo criam a estrutura de pastas antes da escrita dos arquivos.

```bash
mkdir -p oficina-servicos/infra/postgres oficina-servicos/src/hospital/servicos oficina-servicos/tests
cd oficina-servicos
```

No PowerShell, a mesma estrutura é criada com os comandos abaixo.

```powershell
mkdir oficina-servicos\infra\postgres, oficina-servicos\src\hospital\servicos, oficina-servicos\tests
cd oficina-servicos
```

O `pyproject.toml` declara as bibliotecas e torna o pacote instalável, o que permite importar `hospital.servicos.exames` dentro do contêiner e nos testes.

[`pyproject.toml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "servicos-hospitalares"
version = "0.1.0"
description = "Dois serviços com bancos próprios, oficina do módulo 3"
requires-python = ">=3.11"
dependencies = [
  "fastapi",
  "uvicorn",
  "httpx",
  "psycopg[binary]",
  "pydantic",
]

[project.optional-dependencies]
dev = [
  "pytest",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

O `Dockerfile` produz a imagem compartilhada pelos dois serviços, que diferem apenas no comando que o arquivo de composição passa a cada um.

[`Dockerfile`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/Dockerfile)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN python -m pip install --no-cache-dir .

RUN useradd --create-home --uid 10001 app
USER app

EXPOSE 8000
```

Os dois arquivos `__init__.py` ficam vazios e transformam as pastas em pacotes Python importáveis pelos serviços e pelos testes.

[`src/hospital/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/src/hospital/__init__.py)

```python

```

[`src/hospital/servicos/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/src/hospital/servicos/__init__.py)

```python

```

O `elegibilidade.py` implementa o serviço que decide a elegibilidade. Ele consulta somente a própria base e não conhece o serviço de Exames.

[`src/hospital/servicos/elegibilidade.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/src/hospital/servicos/elegibilidade.py)

```python
import os

from fastapi import FastAPI, HTTPException, status
import psycopg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://elegibilidade:elegibilidade@localhost:5433/elegibilidade",
)

app = FastAPI(title="Serviço de elegibilidade", version="1.0.0")


def abrir_conexao():
    return psycopg.connect(DATABASE_URL)


@app.get("/health")
def health():
    try:
        with abrir_conexao() as connection:
            connection.execute("SELECT 1")
    except psycopg.Error as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "banco_indisponivel"},
        ) from error
    return {"status": "ok", "servico": "elegibilidade"}


@app.get("/elegibilidades/{beneficiario_id}")
def consultar_elegibilidade(beneficiario_id: str):
    with abrir_conexao() as connection:
        row = connection.execute(
            "SELECT elegivel FROM elegibilidade.beneficiarios WHERE id = %s",
            (beneficiario_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"codigo": "beneficiario_nao_encontrado"},
        )
    return {"beneficiario_id": beneficiario_id, "elegivel": row[0]}
```

O `exames.py` implementa o serviço que depende de Elegibilidade e contém o tratamento da falha parcial. Cada situação de Elegibilidade gera um código de resposta diferente em Exames. A indisponibilidade gera `503`, o beneficiário desconhecido gera `422` e a resposta fora do contrato gera `502`.

[`src/hospital/servicos/exames.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/src/hospital/servicos/exames.py)

```python
import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
import httpx
from pydantic import BaseModel, Field
import psycopg


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://exames:exames@localhost:5434/exames"
)
ELIGIBILIDADE_URL = os.getenv("ELIGIBILIDADE_URL", "http://localhost:8001")

app = FastAPI(title="Serviço de exames", version="1.0.0")


class PedidoExame(BaseModel):
    beneficiario_id: str = Field(min_length=1)
    codigo_exame: str = Field(min_length=1)


class ExameSolicitado(PedidoExame):
    solicitacao_id: int
    situacao: str


def abrir_conexao():
    return psycopg.connect(DATABASE_URL)


def obter_cliente_elegibilidade():
    with httpx.Client(base_url=ELIGIBILIDADE_URL, timeout=2.0) as client:
        yield client


def registrar_solicitacao(beneficiario_id: str, codigo_exame: str) -> int:
    with abrir_conexao() as connection:
        row = connection.execute(
            """
            INSERT INTO exames.solicitacoes (beneficiario_id, codigo_exame)
            VALUES (%s, %s)
            RETURNING id
            """,
            (beneficiario_id, codigo_exame),
        ).fetchone()
    assert row is not None
    return row[0]


@app.get("/health")
def health():
    try:
        with abrir_conexao() as connection:
            connection.execute("SELECT 1")
    except psycopg.Error as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "banco_indisponivel"},
        ) from error
    return {"status": "ok", "servico": "exames"}


@app.post(
    "/exames",
    response_model=ExameSolicitado,
    status_code=status.HTTP_201_CREATED,
)
def solicitar_exame(
    pedido: PedidoExame,
    cliente: Annotated[httpx.Client, Depends(obter_cliente_elegibilidade)],
):
    try:
        response = cliente.get(f"/elegibilidades/{pedido.beneficiario_id}")
    except httpx.HTTPError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "dependencia_indisponivel"},
        ) from error
    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "dependencia_indisponivel"},
        )
    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"codigo": "beneficiario_desconhecido"},
        )
    try:
        response.raise_for_status()
        elegibilidade = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"codigo": "contrato_invalido"},
        ) from error
    if elegibilidade.get("beneficiario_id") != pedido.beneficiario_id or not isinstance(
        elegibilidade.get("elegivel"), bool
    ):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"codigo": "contrato_invalido"},
        )
    if not elegibilidade["elegivel"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"codigo": "beneficiario_inelegivel"},
        )
    try:
        solicitacao_id = registrar_solicitacao(
            pedido.beneficiario_id, pedido.codigo_exame
        )
    except psycopg.Error as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"codigo": "banco_indisponivel"},
        ) from error
    return ExameSolicitado(
        solicitacao_id=solicitacao_id,
        beneficiario_id=pedido.beneficiario_id,
        codigo_exame=pedido.codigo_exame,
        situacao="solicitado",
    )
```

O `infra/postgres/init.sql` roda na primeira inicialização de cada banco. O mesmo arquivo atende aos dois bancos porque o bloco condicional do início decide o que criar conforme o nome do banco. Os papéis de acesso são criados sem privilégio de superusuário e sem permissão para criar banco, papel ou replicação.

[`infra/postgres/init.sql`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/infra/postgres/init.sql)

```sql
SELECT current_database() = 'elegibilidade' AS is_elegibilidade \gset
SELECT current_database() = 'exames' AS is_exames \gset

\if :is_elegibilidade
CREATE ROLE elegibilidade LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD 'elegibilidade';
CREATE SCHEMA AUTHORIZATION elegibilidade;
SET ROLE elegibilidade;
CREATE TABLE elegibilidade.beneficiarios (
    id text PRIMARY KEY,
    elegivel boolean NOT NULL
);
INSERT INTO elegibilidade.beneficiarios (id, elegivel)
VALUES ('paciente-001', true), ('paciente-002', false);
RESET ROLE;
\elif :is_exames
CREATE ROLE exames LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD 'exames';
CREATE SCHEMA AUTHORIZATION exames;
SET ROLE exames;
CREATE TABLE exames.solicitacoes (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    beneficiario_id text NOT NULL,
    codigo_exame text NOT NULL,
    criado_em timestamptz NOT NULL DEFAULT now()
);
RESET ROLE;
\else
\echo 'O banco deve se chamar elegibilidade ou exames'
\quit
\endif
```

O `infra/postgres/Dockerfile` copia esse script para o diretório em que a imagem oficial do PostgreSQL o executa automaticamente.

[`infra/postgres/Dockerfile`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/infra/postgres/Dockerfile)

```dockerfile
FROM postgres:16-alpine

COPY infra/postgres/init.sql /docker-entrypoint-initdb.d/init.sql
```

O `infra/compose.servicos.yml` é o arquivo central da oficina. Ele declara as três redes, entre as quais as duas redes de banco marcadas com `internal: true`, marcação que produz o isolamento mostrado na Figura 11.

[`infra/compose.servicos.yml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/infra/compose.servicos.yml)

```yaml
services:
  db_elegibilidade:
    build:
      context: ..
      dockerfile: infra/postgres/Dockerfile
    environment:
      POSTGRES_DB: elegibilidade
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: local-elegibilidade-admin
    volumes:
      - elegibilidade_data:/var/lib/postgresql/data
    networks:
      elegibilidade-db-net:
        aliases:
          - elegibilidade-db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d elegibilidade"]
      interval: 2s
      timeout: 3s
      retries: 15

  db_exames:
    build:
      context: ..
      dockerfile: infra/postgres/Dockerfile
    environment:
      POSTGRES_DB: exames
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: local-exames-admin
    volumes:
      - exames_data:/var/lib/postgresql/data
    networks:
      exames-db-net:
        aliases:
          - exames-db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d exames"]
      interval: 2s
      timeout: 3s
      retries: 15

  elegibilidade:
    build:
      context: ..
      dockerfile: Dockerfile
    command: ["python", "-m", "uvicorn", "hospital.servicos.elegibilidade:app", "--host", "0.0.0.0", "--port", "8000"]
    environment:
      DATABASE_URL: postgresql://elegibilidade:elegibilidade@db_elegibilidade:5432/elegibilidade
    ports:
      - "${ELEGIBILIDADE_PORT:-8001}:8000"
    depends_on:
      db_elegibilidade:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 2s
      timeout: 3s
      retries: 15
    networks:
      - application-net
      - elegibilidade-db-net

  exames:
    build:
      context: ..
      dockerfile: Dockerfile
    command: ["python", "-m", "uvicorn", "hospital.servicos.exames:app", "--host", "0.0.0.0", "--port", "8000"]
    environment:
      DATABASE_URL: postgresql://exames:exames@db_exames:5432/exames
      ELIGIBILIDADE_URL: http://elegibilidade:8000
    ports:
      - "${EXAMES_PORT:-8002}:8000"
    depends_on:
      db_exames:
        condition: service_healthy
      elegibilidade:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 2s
      timeout: 3s
      retries: 15
    networks:
      - application-net
      - exames-db-net

volumes:
  elegibilidade_data:
  exames_data:

networks:
  application-net:
  elegibilidade-db-net:
    internal: true
  exames-db-net:
    internal: true
```

O `tests/test_service_boundaries.py` verifica as fronteiras por código, sem depender de inspeção manual.

[`tests/test_service_boundaries.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-3/tests/test_service_boundaries.py)

```python
from pathlib import Path

import httpx
import psycopg
from fastapi.testclient import TestClient

from hospital.servicos import exames


ROOT = Path(__file__).resolve().parents[1]
EXAMES_SOURCE = ROOT / "src" / "hospital" / "servicos" / "exames.py"


def _client_for_eligibility(response: httpx.Response) -> TestClient:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/elegibilidades/paciente-001"
        return response

    dependency_client = httpx.Client(
        transport=httpx.MockTransport(handler), base_url="http://contrato.local"
    )
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: dependency_client
    )
    return TestClient(exames.app)


def teardown_function():
    exames.app.dependency_overrides.clear()


def test_exames_consumes_eligibility_only_through_http_contract(monkeypatch):
    monkeypatch.setattr(exames, "registrar_solicitacao", lambda *_: 41)
    eligibility_response = httpx.Response(
        200,
        json={"beneficiario_id": "paciente-001", "elegivel": True},
    )

    response = _client_for_eligibility(eligibility_response).post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "solicitacao_id": 41,
        "beneficiario_id": "paciente-001",
        "codigo_exame": "HEM-001",
        "situacao": "solicitado",
    }


def test_exames_makes_partial_failure_observable_when_dependency_is_down():
    def unavailable(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("serviço interrompido")

    dependency_client = httpx.Client(
        transport=httpx.MockTransport(unavailable), base_url="http://contrato.local"
    )
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: dependency_client
    )

    response = TestClient(exames.app).post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 503
    assert response.json()["detail"]["codigo"] == "dependencia_indisponivel"


def test_exames_makes_its_own_database_failure_observable(monkeypatch):
    eligibility_response = httpx.Response(
        200,
        json={"beneficiario_id": "paciente-001", "elegivel": True},
    )
    client = _client_for_eligibility(eligibility_response)

    def database_unavailable(*_args):
        raise psycopg.OperationalError("banco de Exames indisponível")

    monkeypatch.setattr(exames, "registrar_solicitacao", database_unavailable)

    response = client.post(
        "/exames",
        json={"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"},
    )

    assert response.status_code == 503
    assert response.json()["detail"]["codigo"] == "banco_indisponivel"


def test_exames_source_cannot_access_eligibility_table_directly():
    source = EXAMES_SOURCE.read_text(encoding="utf-8").casefold()

    assert "elegibilidade.beneficiarios" not in source
    assert "from elegibilidade" not in source
    assert "join elegibilidade" not in source
    assert "db_elegibilidade" not in source
```

As senhas valem somente para esta demonstração local com dados inventados. Ao final, o comando `down -v` remove contêineres, redes e volumes.

## Ferramenta

| Ferramenta | O que é | Para que serve aqui |
| --- | --- | --- |
| **Docker Engine** | O programa que executa contêineres, que são processos isolados com seu próprio sistema de arquivos e sua própria rede. | Rodar quatro processos isolados na sua máquina como se fossem quatro servidores. |
| **Docker Compose** | Um utilitário que sobe vários contêineres de uma vez, a partir de um arquivo YAML que descreve o conjunto. | Declarar os dois serviços, os dois bancos e as redes entre eles num arquivo só. |
| **PostgreSQL 16** | Um banco de dados relacional. | Dar a cada serviço um armazenamento próprio e separado. |
| **FastAPI e Uvicorn** | A biblioteca que implementa as rotas e o servidor que as atende, já usados no Módulo 2. | Servir as duas APIs. |
| **httpx** | Uma biblioteca Python para fazer chamadas HTTP. | É por ela que Exames chama Elegibilidade, com prazo de espera configurado. |

Um **contêiner** é um processo empacotado com as dependências de que precisa para rodar e isolado do restante da máquina. Uma **verificação de saúde**, em inglês *health check*, é um comando que o Docker executa periodicamente para decidir se o contêiner está saudável. A diferença entre um contêiner em execução e um contêiner saudável é o assunto central da etapa de falha parcial desta oficina.

**Objetivo**

Observar uma fronteira de dados e uma falha parcial em uma demonstração local.

**Pré-requisito**

Docker em execução e Python 3.11 ou superior.

## Pré-requisitos

Verifique `docker version`, `docker compose version` e `python --version` antes de continuar.

## Instalação

### Windows

Instale o Docker Desktop e o Python. Use o comando `py` quando o comando `python` não estiver no PATH do sistema.

### macOS

Instale Docker Desktop e Python 3 pelo instalador oficial ou gerenciador de pacotes.

### Linux

Instale Docker Engine, o plugin Compose e Python 3 pelo método da sua distribuição.

## Preparação do laboratório

Os comandos abaixo entram na pasta da oficina e criam o diretório de evidências. No Windows, o comando `py` substitui `python` quando necessário.

```bash
cd oficina-servicos
python -m pip install -e ".[dev]"
mkdir -p evidencias/modulo-3
```

No PowerShell, o equivalente para o diretório é `New-Item -ItemType Directory -Force evidencias\modulo-3`.

## Fronteira declarada no Compose {#a-fronteira-declarada-no-compose}

A fronteira entre os dois serviços está escrita no arquivo de composição, fora do código Python. Por esse motivo, a leitura desse arquivo vem antes da execução dos serviços.

O bloco de redes fica no fim do arquivo de composição.

```yaml
networks:
  application-net:              # por onde os dois serviços conversam
  elegibilidade-db-net:
    internal: true              # sem saída para fora: só quem está nela se alcança
  exames-db-net:
    internal: true
```

O arquivo declara três redes e liga cada serviço a exatamente duas delas.

```yaml
  elegibilidade:
    networks:
      - application-net         # fala com o outro serviço
      - elegibilidade-db-net    # fala com o próprio banco

  exames:
    networks:
      - application-net
      - exames-db-net           # o banco de Exames, e nenhum outro
```

Com essa declaração, o serviço de Exames não tem rota de rede até `db_elegibilidade`. Uma consulta ao banco de Elegibilidade escrita no código de Exames falharia por falta de caminho de rede. A propriedade dos dados passa a ser garantida pela infraestrutura e deixa de depender da disciplina da equipe.

O módulo trata o banco por serviço como uma decisão de autoridade sobre os dados, independente da tecnologia escolhida. Os dois bancos da oficina rodam o mesmo PostgreSQL na mesma versão e se distinguem apenas pelos serviços que têm permissão de alcançá-los.

O bloco de dependências declara a ordem de inicialização dos serviços.

```yaml
  exames:
    depends_on:
      db_exames:
        condition: service_healthy      # espera o banco ficar saudável
      elegibilidade:
        condition: service_healthy      # espera o outro serviço também
```

Cada serviço também declara o comando que verifica a sua saúde.

```yaml
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 2s        # verifica a cada 2 segundos
      timeout: 3s         # desiste se demorar mais que 3
      retries: 15         # marca como não saudável após 15 falhas
```

O comando de saúde chama a operação `/health` do próprio serviço e não verifica se as dependências estão disponíveis. Esse detalhe explica o resultado da etapa de falha parcial.

## Execução

A execução começa pela subida dos quatro contêineres e pela observação do estado nominal. Em seguida, uma solicitação elegível é criada, Elegibilidade é interrompida para provocar a falha parcial e o ambiente é recuperado.

**Execute**

As etapas seguem a ordem da tabela abaixo, com estado de entrada, evidência esperada e contingência para o caso de divergência.

**Observe**

Em cada etapa, a observação compara a saúde dos contêineres informada pelo `docker compose ps` com a resposta da API a uma requisição real. A falha parcial aparece no momento em que essas duas leituras divergem.

**Compare**

O estado nominal tem os quatro contêineres saudáveis. No estado degradado, Exames continua saudável para o Docker e não consegue concluir a operação que depende de Elegibilidade. A diferença entre um processo em execução e uma capacidade disponível distingue a falha parcial da queda do sistema.

**Questões exploratórias**

Qual dependência permanece saudável e qual capacidade deixa de ser concluída?

### Roteiro de transição do ambiente

| Etapa | Estado de entrada | Ação e evidência esperada | Contingência |
| --- | --- | --- | --- |
| Validar configuração | Os quatro serviços estão parados. | Execute os dois comandos `config`. O `--quiet` termina sem texto e `--services` lista `elegibilidade`, `exames`, `db_elegibilidade` e `db_exames`. | Se o Docker não responder, guarde a saída e faça só a validação estática. |
| Iniciar e inspecionar | Compose válido e serviços parados. | Suba a demonstração. O `ps` mostra quatro serviços `healthy` e os dois `/health` retornam `200`. | Se uma porta estiver ocupada, escolha outras portas. Nenhum recurso fora deste projeto deve ser removido. |
| Demonstrar falha parcial | As duas aplicações e bases estão saudáveis. | Pare `elegibilidade`. Exames permanece saudável e `POST /exames` retorna `503 dependencia_indisponivel`. | Se o resultado divergir, guarde `ps` e logs antes de reiniciar. |
| Recuperar e verificar | Elegibilidade está parada e Exames continua saudável. | Execute `up -d --wait`. Os dois `/health` voltam a `200` e o teste de fronteiras é executado. | Se o daemon não responder, execute somente os testes Python e registre a limitação. |
| Limpar | A demonstração pode estar em qualquer estado anterior. | `down -v` remove contêineres, redes e volumes. O `ps -a` não lista recursos ativos. | Se houver resíduo, repita apenas esse `down -v`. |

### Escolher portas e validar a configuração

As variáveis abaixo definem portas livres para evitar conflito com as portas padrão 8001 e 8002 em *shells* POSIX.

```bash
export ELEGIBILIDADE_PORT=18001
export EXAMES_PORT=18002
```

No PowerShell, as mesmas variáveis são definidas com os comandos abaixo.

```powershell
$env:ELEGIBILIDADE_PORT = 18001
$env:EXAMES_PORT = 18002
```

```bash
docker compose -f infra/compose.servicos.yml config --quiet
```

A ausência de texto com código de saída zero indica que a configuração é sintaticamente válida. Essa validação não demonstra que o Docker está em execução nem que os serviços estão saudáveis.

```bash
docker compose -f infra/compose.servicos.yml config --services
```

A saída deve listar os quatro nomes de serviço, o que evita iniciar por engano um arquivo de composição diferente.

## Iniciar e observar a demonstração

```bash
docker compose -f infra/compose.servicos.yml up -d --build --wait
```

## Resultado esperado

A opção `--wait` faz o comando terminar quando as quatro verificações de saúde ficam saudáveis. Se uma imagem não puder ser baixada ou uma porta estiver ocupada, a saída deve ser guardada e outra porta deve ser escolhida, sem remover recursos do Docker que não pertencem a este projeto.

```bash
docker compose -f infra/compose.servicos.yml ps
```

A saída esperada mostra os quatro serviços saudáveis.

```text
SERVICE            STATUS                    PORTS
db_elegibilidade   Up 17 seconds (healthy)   5432/tcp
db_exames          Up 17 seconds (healthy)   5432/tcp
elegibilidade      Up 15 seconds (healthy)   0.0.0.0:18001->8000/tcp
exames             Up 12 seconds (healthy)   0.0.0.0:18002->8000/tcp
```

Os dois bancos mostram apenas `5432/tcp`, sem o prefixo `0.0.0.0:`, porque não têm porta publicada para a máquina local e só podem ser alcançados a partir da rede interna de cada um. As aplicações mostram `0.0.0.0:18001->8000`, que indica o encaminhamento da porta 18001 da máquina local para a porta 8000 dentro do contêiner.

Os comandos abaixo verificam a saúde dos dois serviços a partir da máquina local.

```bash
curl -i "http://localhost:${ELEGIBILIDADE_PORT}/health"
curl -i "http://localhost:${EXAMES_PORT}/health"
```

No PowerShell, o comando `curl.exe` evita o alias `curl`, que aponta para `Invoke-WebRequest`.

```powershell
curl.exe -i "http://localhost:$env:ELEGIBILIDADE_PORT/health"
curl.exe -i "http://localhost:$env:EXAMES_PORT/health"
```

Cada resposta deve ter o status `200`. Em seguida, o comando abaixo cria uma solicitação para um beneficiário elegível.

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

No PowerShell, o comando abaixo cria a mesma solicitação e deve retornar `201`.

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

A resposta completa da solicitação é a seguinte.

```text
HTTP/1.1 201 Created
server: uvicorn
content-type: application/json

{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001","solicitacao_id":1,"situacao":"solicitado"}
```

O status `202` usado no Módulo 2 indicava somente que o pedido tinha sido aceito para processamento posterior. O status `201 Created` desta oficina indica que o recurso passou a existir, porque a solicitação já está gravada no banco de Exames quando a resposta chega ao consumidor.

Antes de responder `201`, o serviço de Exames chamou Elegibilidade por HTTP e gravou a solicitação na própria base depois de receber a aprovação. O `solicitacao_id` vem dessa gravação e volta a começar em 1 depois do comando `down -v`, que remove o volume do banco.

## Interpretação

### Tornar a falha parcial observável

```bash
docker compose -f infra/compose.servicos.yml stop elegibilidade
```

```bash
docker compose -f infra/compose.servicos.yml ps
```

O diagrama abaixo representa o estado do serviço de Exames depois da interrupção de Elegibilidade.

```mermaid
flowchart TB
    H[GET /health em Exames] --> BD{Exames alcança<br/>o próprio banco?}
    BD -->|sim| OK[200 OK<br/>o processo está saudável]
    OP[POST /exames] --> DEP{Elegibilidade responde?}
    DEP -->|não, prazo esgotado| ERR[503 Service Unavailable<br/>dependencia_indisponivel]
    OK -.->|mesma instância, ao mesmo tempo| ERR
```

**Texto alternativo:** a verificação de saúde de Exames consulta apenas o próprio banco e responde 200, enquanto a operação de negócio depende de Elegibilidade e responde 503. Uma seta tracejada indica que as duas respostas vêm da mesma instância ao mesmo tempo.

*Figura 12 — Respostas 200 e 503 da mesma instância de Exames. Fonte: curso.*

**Leitura textual da figura:** dois caminhos partem do mesmo processo de Exames. O primeiro é a verificação de saúde, que consulta apenas o banco de Exames e responde 200. O segundo é a operação de negócio, que consulta Elegibilidade sobre o beneficiário, não recebe resposta dentro do prazo e devolve 503 com o código de dependência indisponível. Uma seta tracejada liga as duas respostas para indicar que elas saem da mesma instância no mesmo instante. Esse comportamento caracteriza uma degradação parcial, diferente da queda do sistema inteiro. Uma verificação de saúde que também consultasse Elegibilidade eliminaria essa distinção e levaria o orquestrador a reiniciar um processo que está funcionando.

Com Elegibilidade parada, a chamada abaixo deve retornar `503 Service Unavailable` com o código `dependencia_indisponivel`, enquanto o `GET /health` de Exames continua retornando `200`.

```bash
curl -i -X POST "http://localhost:${EXAMES_PORT}/exames" \
  -H 'Content-Type: application/json' \
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

No PowerShell, o comando abaixo repete a chamada e deve retornar `503`.

```powershell
curl.exe -i -X POST "http://localhost:$env:EXAMES_PORT/exames" `
  -H "Content-Type: application/json" `
  -d '{"beneficiario_id":"paciente-001","codigo_exame":"HEM-001"}'
```

A saída da chamada mostra o status e o código da falha.

```text
HTTP/1.1 503 Service Unavailable
server: uvicorn
content-type: application/json

{"detail":{"codigo":"dependencia_indisponivel"}}
```

No mesmo momento, a verificação de saúde de Exames continua respondendo com sucesso.

```text
HTTP/1.1 200 OK

{"status":"ok","servico":"exames"}
```

A emissão de duas respostas contraditórias pelo mesmo serviço no mesmo instante caracteriza a falha parcial.

O serviço de Exames está saudável segundo a própria verificação, porque o processo responde e a base própria está acessível. O serviço não consegue concluir a operação que depende de Elegibilidade. Numa arquitetura de serviços, um processo em execução pode estar incapaz de atender a uma capacidade. Por esse motivo, um monitoramento que verifica apenas se os processos estão em execução indica saúde mesmo quando uma capacidade está indisponível.

O sistema não ficou indisponível por inteiro. As consultas a Elegibilidade feitas antes da parada não foram desfeitas e a base de Exames continua íntegra. As operações de Exames que não dependem de Elegibilidade continuariam funcionando, porque a falha ficou restrita ao caminho que atravessa a fronteira entre os serviços.

### Escolha do status 503 {#por-que-o-erro-e-503-e-nao-500}

O trecho abaixo mostra o tratamento da chamada a Elegibilidade em `exames.py`.

```python
try:
    response = cliente.get(f"/elegibilidades/{pedido.beneficiario_id}")
except httpx.HTTPError as error:                    # a rede falhou
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={"codigo": "dependencia_indisponivel"},
    ) from error
```

O status `503` comunica que o defeito é temporário e não foi causado pelo consumidor. Um `500` indicaria um erro interno de Exames, enquanto um `400` atribuiria ao consumidor a responsabilidade por um pedido correto. O `503` indica que a chamada pode ser repetida mais tarde e permite ao consumidor decidir quando fazer a nova tentativa.

O mesmo arquivo traduz cada resposta possível de Elegibilidade num status próprio de Exames, conforme a tabela.

| Situação em Elegibilidade | Resposta de Exames | Justificativa |
| --- | --- | --- |
| Não responde ou a rede falha | `503 dependencia_indisponivel` | Problema transitório de infraestrutura. |
| Responde `5xx` | `503 dependencia_indisponivel` | Para o consumidor de Exames, o erro do provedor equivale a uma indisponibilidade. |
| Responde `404` para beneficiário desconhecido | `422 beneficiario_desconhecido` | O pedido identifica um beneficiário inexistente, de modo que o problema está no pedido do consumidor. |
| Responde fora do contrato esperado | `502 contrato_invalido` | Exames recebeu uma resposta ilegível de um serviço do qual depende. |
| Responde que o beneficiário não é elegível | `422 beneficiario_inelegivel` | A resposta é uma decisão de negócio negativa, sem falha técnica. |

Exames não repassa o código de status recebido de Elegibilidade. Um `404` de Elegibilidade não se torna `404` de Exames, porque a rota `/exames` existe e o recurso inexistente é o beneficiário. O repasse do status de um serviço interno acoplaria o consumidor à topologia interna do sistema.

A tabela também separa falha técnica de decisão de negócio. O beneficiário inelegível é a resposta correta a uma pergunta legítima e recebe o status `422` com código próprio, enquanto o `503` fica reservado para a indisponibilidade técnica.

O prazo de espera é declarado na criação do cliente HTTP, como mostra o trecho abaixo.

```python
with httpx.Client(base_url=ELIGIBILIDADE_URL, timeout=2.0) as client:
```

Sem esse prazo de espera, uma chamada a um serviço que não responde ficaria aguardando indefinidamente e ocuparia o processo de Exames. A indisponibilidade de Elegibilidade passaria a ser também uma indisponibilidade de Exames. Esse risco é um custo da fronteira física, que não existe numa chamada de função dentro do mesmo processo.

```bash
docker compose -f infra/compose.servicos.yml up -d --wait
```

## Verificar as fronteiras sem depender do Compose

Com os serviços saudáveis, o comando abaixo executa os testes de fronteira.

```bash
python -m pytest tests/test_service_boundaries.py -q
```

A saída esperada é `4 passed`, com o teste `test_exames_makes_its_own_database_failure_observable` entre os aprovados. Os testes verificam o contrato HTTP e a falha parcial, além da falha da base própria e da ausência de SQL contra a tabela de Elegibilidade. No Windows sem ambiente virtual ativado, o comando é `py -m pytest tests/test_service_boundaries.py -q`.

## Limpeza e contingência

### Limpar a demonstração

```bash
docker compose -f infra/compose.servicos.yml down -v
```

```bash
docker compose -f infra/compose.servicos.yml ps -a
```

## Evidência a entregar

A pasta `oficina-servicos/evidencias/modulo-3/` deve guardar as saídas dos comandos de versão e das verificações de saúde. Também deve guardar as respostas `201` e `503` e a saída dos testes. Se o daemon do Docker nunca respondeu, a evidência consiste na saída de `config --quiet` e dos testes Python, com o registro “Compose validado estaticamente. Execução de contêineres não realizada porque o daemon não respondeu”. Verificações de saúde só podem constar da evidência quando foram observadas numa execução real dos contêineres.
