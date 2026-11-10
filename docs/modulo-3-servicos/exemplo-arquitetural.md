# Exemplo arquitetural: elegibilidade e exames

O laboratório concretiza dois bounded contexts em processos FastAPI independentes. Cada processo possui um PostgreSQL e uma credencial própria. O objetivo é expor um limite verificável, sem simular a plataforma hospitalar inteira: Exames conhece o contrato HTTP de Elegibilidade e não conhece sua tabela.

## Onde está o bounded context

Como [conceitos](conceitos.md) define, um bounded context delimita onde um modelo e sua linguagem têm significado consistente. Ele é uma fronteira semântica e não exige processo separado. Neste laboratório, cada bounded context também se tornou um processo (um microsserviço) por uma escolha de implantação feita para tornar a fronteira observável, e essa escolha não constitui regra geral.

Dentro de cada contexto existe um vocabulário próprio que o outro lado não precisa conhecer. Em Elegibilidade, `elegivel` resume vínculo, vigência e regra da operadora — um cálculo que pode mudar por completo sem que nada além do campo booleano seja exposto. Em Exames, `situacao` descreve uma etapa do fluxo clínico da solicitação, sem relação com o vocabulário de Elegibilidade. A única tradução entre os dois modelos acontece no contrato HTTP; nenhum dos dois enxerga o schema, a tabela ou o código interno do outro.

```mermaid
flowchart LR
    subgraph Elegibilidade[Bounded context: Elegibilidade]
      AE[elegibilidade.py\nGET /elegibilidades/id]
      DE[(PostgreSQL elegibilidade)]
      AE --> DE
    end
    subgraph Exames[Bounded context: Exames]
      AX[exames.py\nPOST /exames]
      DX[(PostgreSQL exames)]
      AX --> DX
    end
    AX -->|único contrato entre os dois| AE
```

**Texto alternativo:** dois bounded contexts lado a lado, Elegibilidade e Exames, cada um com seu próprio código-fonte e seu próprio PostgreSQL; a única ligação entre eles é a chamada HTTP do contrato.

*Figura 1 — Os dois bounded contexts do laboratório e o código de cada um. Fonte: curso.*

**Leitura textual da figura:** o bounded context Elegibilidade contém `elegibilidade.py` e seu próprio PostgreSQL; o bounded context Exames contém `exames.py` e seu próprio PostgreSQL; a única seta entre os dois contextos é a chamada HTTP do contrato, sem acesso direto a banco ou código interno.

As seções a seguir mostram o código de cada lado desta figura: primeiro os componentes, depois o fluxo entre eles.

## Componentes

O serviço **Elegibilidade** oferece `GET /elegibilidades/{beneficiario_id}`. Seu schema contém beneficiários sintéticos e a decisão booleana. Cada processo é uma aplicação FastAPI própria, com sua própria conexão PostgreSQL, e os dois códigos se comunicam apenas por HTTP, sem import nem chamada de função entre eles.

```python
# hospital/servicos/elegibilidade.py
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

O serviço **Exames** oferece `POST /exames`, consulta o primeiro serviço por HTTP e, se a resposta for positiva, registra uma solicitação no próprio schema. O contrato de entrada e saída é declarado em Pydantic, como no exemplo do módulo 2:

```python
# hospital/servicos/exames.py
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

def abrir_conexao():
    return psycopg.connect(DATABASE_URL)

class PedidoExame(BaseModel):
    beneficiario_id: str = Field(min_length=1)
    codigo_exame: str = Field(min_length=1)

class ExameSolicitado(PedidoExame):
    solicitacao_id: int
    situacao: str

def obter_cliente_elegibilidade():
    with httpx.Client(base_url=ELIGIBILIDADE_URL, timeout=2.0) as client:
        yield client
```

`ELIGIBILIDADE_URL` é a única informação que Exames recebe sobre o outro serviço: um endereço HTTP, injetado por variável de ambiente. Nenhuma URL de banco alheio é passada a Exames, e essa ausência de configuração impede o acesso direto sem depender de uma regra no código.

Ambos oferecem `GET /health`. O health check comprova conexão com seu banco local; ele não declara nenhuma dependência remota saudável. Essa escolha permite ver uma falha parcial: Exames continua com processo e banco ativos, embora uma operação que depende de Elegibilidade retorne `503`.

```python
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
```

```mermaid
flowchart LR
    U[Consumidor] -->|POST /exames| X[Serviço Exames]
    X -->|GET /elegibilidades/id| E[Serviço Elegibilidade]
    E -->|SELECT próprio| DE[(PostgreSQL elegibilidade)]
    X -->|INSERT próprio| DX[(PostgreSQL exames)]
    X -. proibido .-> DE
```

**Texto alternativo:** o consumidor solicita exames; Exames consulta Elegibilidade por HTTP e cada serviço acessa exclusivamente seu próprio banco PostgreSQL.

*Figura 2 — Contrato entre serviços e propriedade de dados. Fonte: curso.*

**Leitura textual da figura:** o consumidor chama Exames; Exames consulta Elegibilidade por HTTP; cada serviço acessa apenas seu PostgreSQL, e o caminho direto entre Exames e o banco de Elegibilidade é explicitamente proibido.

## Fluxo nominal

O consumidor envia:

```json
{
  "beneficiario_id": "paciente-001",
  "codigo_exame": "HEM-001"
}
```

O Pydantic valida a forma do pedido antes de a rota rodar (o mesmo mecanismo do módulo 2). Dentro da rota, Exames chama `GET /elegibilidades/paciente-001` pelo cliente HTTP injetado, sem conhecer nenhum detalhe interno de Elegibilidade além do contrato:

```python
# hospital/servicos/exames.py
@app.post("/exames", response_model=ExameSolicitado, status_code=status.HTTP_201_CREATED)
def solicitar_exame(
    pedido: PedidoExame,
    cliente: Annotated[httpx.Client, Depends(obter_cliente_elegibilidade)],
):
    response = cliente.get(f"/elegibilidades/{pedido.beneficiario_id}")
    # ... validação da resposta (ver "Fluxos alternativos") ...
    elegibilidade = response.json()
    if not elegibilidade["elegivel"]:
        raise HTTPException(status_code=422, detail={"codigo": "beneficiario_inelegivel"})
    solicitacao_id = registrar_solicitacao(pedido.beneficiario_id, pedido.codigo_exame)
    return ExameSolicitado(
        solicitacao_id=solicitacao_id,
        beneficiario_id=pedido.beneficiario_id,
        codigo_exame=pedido.codigo_exame,
        situacao="solicitado",
    )
```

`registrar_solicitacao` é a única função de Exames que toca seu próprio banco — e só o seu:

```python
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
```

Do lado de Elegibilidade, a mesma chamada executa uma consulta parametrizada em `elegibilidade.beneficiarios` e responde:

```json
{
  "beneficiario_id": "paciente-001",
  "elegivel": true
}
```

Exames aceita a decisão, chama `registrar_solicitacao` (mostrado acima) e retorna `201 Created`:

```json
{
  "solicitacao_id": 1,
  "beneficiario_id": "paciente-001",
  "codigo_exame": "HEM-001",
  "situacao": "solicitado"
}
```

O identificador pode aumentar em nova execução. Depois de `down -v`, o volume é removido e a primeira solicitação da próxima execução volta a usar o identificador `1`.

## Fluxos alternativos

Cada linha do parágrafo anterior sobre falhas é, no código, uma verificação explícita antes do caminho feliz. É a mesma rota `solicitar_exame`, agora com os trechos que a versão resumida do fluxo nominal ocultou:

```python
# hospital/servicos/exames.py
@app.post("/exames", response_model=ExameSolicitado, status_code=status.HTTP_201_CREATED)
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
    if not isinstance(elegibilidade.get("elegivel"), bool):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"codigo": "contrato_invalido"},
        )
    if not elegibilidade["elegivel"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"codigo": "beneficiario_inelegivel"},
        )
    solicitacao_id = registrar_solicitacao(pedido.beneficiario_id, pedido.codigo_exame)
    return ExameSolicitado(
        solicitacao_id=solicitacao_id,
        beneficiario_id=pedido.beneficiario_id,
        codigo_exame=pedido.codigo_exame,
        situacao="solicitado",
    )
```

Cada `raise` corresponde a um dos casos do parágrafo anterior: `paciente-002` cai no último bloco (`200` com `elegivel: false` → `422 beneficiario_inelegivel`); um identificador inexistente cai no bloco de `404` (`422 beneficiario_desconhecido`); uma estrutura incompatível na resposta cai no bloco de `contrato_invalido`; e uma conexão que falha (`httpx.HTTPError`, por exemplo um timeout) ou um erro `5xx` do próprio provedor caem nos dois blocos de `dependencia_indisponivel`, produzindo:

```json
{
  "detail": {
    "codigo": "dependencia_indisponivel"
  }
}
```

Essa resposta não afirma que o processo de Exames parou. Ela comunica que a capacidade solicitada não pode ser concluída enquanto uma dependência necessária está indisponível — o teste `test_exames_makes_partial_failure_observable_when_dependency_is_down` simula exatamente essa queda de conexão e verifica o `503` com esse código.

### Execução de ponta a ponta dos dois serviços

Os blocos desta página formam dois arquivos que rodam na mesma pasta. O arquivo `elegibilidade.py` recebe o primeiro bloco da seção Componentes. O arquivo `exames.py` recebe, nesta ordem, o bloco de `PedidoExame`, o bloco de `/health`, o bloco de `registrar_solicitacao` e a rota completa desta seção, e a versão resumida do fluxo nominal fica fora dele porque declara a mesma rota. Os pacotes necessários são os do laboratório (`fastapi`, `httpx`, `pydantic` e `psycopg`), e a instalação é feita com `pip install fastapi httpx pydantic "psycopg[binary]"`.

O programa abaixo, salvo como `demo_servicos.py` na mesma pasta e executado com `python3 demo_servicos.py`, substitui o PostgreSQL de cada serviço por um banco SQLite em memória próprio e entrega as chamadas HTTP de Exames a um `TestClient` de Elegibilidade, para que o exemplo rode sem contêiner e sem rede com a ligação entre os serviços restrita ao contrato HTTP. No laboratório, cada serviço usa o PostgreSQL real e a chamada atravessa a rede do Compose.

```python
# demo_servicos.py
import json
import sqlite3

import httpx
from fastapi.testclient import TestClient

import elegibilidade
import exames


class ConexaoSQLite:
    """Substituto didático de psycopg.connect: um banco SQLite em memória por serviço."""

    def __init__(self, schema: str, script: str):
        sqlite3.register_converter("boolean", lambda valor: valor == b"1")
        self._banco = sqlite3.connect(
            ":memory:", check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self._banco.execute(f"ATTACH DATABASE ':memory:' AS {schema}")
        self._banco.executescript(script)

    def __enter__(self):
        return self

    def __exit__(self, *_erro):
        self._banco.commit()  # o banco em memória continua aberto entre requisições

    def execute(self, sql: str, parametros=()):
        # psycopg usa %s como marcador de parâmetro, e o SQLite usa ?
        return self._banco.execute(sql.replace("%s", "?"), parametros)


banco_elegibilidade = ConexaoSQLite(
    "elegibilidade",
    """
    CREATE TABLE elegibilidade.beneficiarios (id text PRIMARY KEY, elegivel boolean NOT NULL);
    INSERT INTO elegibilidade.beneficiarios (id, elegivel)
    VALUES ('paciente-001', 1), ('paciente-002', 0);
    """,
)
banco_exames = ConexaoSQLite(
    "exames",
    """
    CREATE TABLE exames.solicitacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        beneficiario_id text NOT NULL,
        codigo_exame text NOT NULL
    );
    """,
)


def exibir(metodo: str, rota: str, resposta: httpx.Response) -> None:
    corpo = json.dumps(resposta.json(), ensure_ascii=False)
    print(f"{metodo} {rota} -> {resposta.status_code} {corpo}")


def recusar_conexao(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("conexão recusada pelo serviço Elegibilidade", request=request)


def main() -> None:
    # Cada serviço abre somente o próprio banco substituto.
    elegibilidade.abrir_conexao = lambda: banco_elegibilidade
    exames.abrir_conexao = lambda: banco_exames

    cliente_elegibilidade = TestClient(elegibilidade.app)
    cliente_exames = TestClient(exames.app)

    # Exames recebe um cliente HTTP que entrega as chamadas ao app de Elegibilidade.
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: cliente_elegibilidade
    )

    print("1. Health check de cada serviço")
    exibir("GET", "/health (Elegibilidade)", cliente_elegibilidade.get("/health"))
    exibir("GET", "/health (Exames)", cliente_exames.get("/health"))

    print("\n2. Beneficiário elegível: a solicitação é registrada")
    pedido = {"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001"}
    exibir("POST", "/exames", cliente_exames.post("/exames", json=pedido))

    print("\n3. Beneficiário inelegível: a solicitação é recusada")
    pedido = {"beneficiario_id": "paciente-002", "codigo_exame": "HEM-001"}
    exibir("POST", "/exames", cliente_exames.post("/exames", json=pedido))

    print("\n4. Beneficiário inexistente em Elegibilidade")
    pedido = {"beneficiario_id": "paciente-999", "codigo_exame": "HEM-001"}
    exibir("POST", "/exames", cliente_exames.post("/exames", json=pedido))

    print("\n5. Elegibilidade indisponível: a conexão HTTP é recusada")
    cliente_indisponivel = httpx.Client(
        base_url=exames.ELIGIBILIDADE_URL, transport=httpx.MockTransport(recusar_conexao)
    )
    exames.app.dependency_overrides[exames.obter_cliente_elegibilidade] = (
        lambda: cliente_indisponivel
    )
    pedido = {"beneficiario_id": "paciente-001", "codigo_exame": "HEM-002"}
    exibir("POST", "/exames", cliente_exames.post("/exames", json=pedido))
    exibir("GET", "/health (Exames)", cliente_exames.get("/health"))

    print("\n6. Linhas gravadas no banco de Exames")
    with exames.abrir_conexao() as connection:
        linhas = connection.execute("SELECT * FROM exames.solicitacoes").fetchall()
    print(linhas)


if __name__ == "__main__":
    main()
```

A execução imprime:

```text
1. Health check de cada serviço
GET /health (Elegibilidade) -> 200 {"status": "ok", "servico": "elegibilidade"}
GET /health (Exames) -> 200 {"status": "ok", "servico": "exames"}

2. Beneficiário elegível: a solicitação é registrada
POST /exames -> 201 {"beneficiario_id": "paciente-001", "codigo_exame": "HEM-001", "solicitacao_id": 1, "situacao": "solicitado"}

3. Beneficiário inelegível: a solicitação é recusada
POST /exames -> 422 {"detail": {"codigo": "beneficiario_inelegivel"}}

4. Beneficiário inexistente em Elegibilidade
POST /exames -> 422 {"detail": {"codigo": "beneficiario_desconhecido"}}

5. Elegibilidade indisponível: a conexão HTTP é recusada
POST /exames -> 503 {"detail": {"codigo": "dependencia_indisponivel"}}
GET /health (Exames) -> 200 {"status": "ok", "servico": "exames"}

6. Linhas gravadas no banco de Exames
[(1, 'paciente-001', 'HEM-001')]
```

O caso 5 reproduz a falha parcial descrita acima: a solicitação recebe `503 dependencia_indisponivel`, o `/health` de Exames continua com `200` e o banco de Exames guarda apenas a solicitação aprovada no caso 2.

## Fronteira de dados executável

O arquivo Compose cria dois servidores PostgreSQL. No primeiro existe somente o schema `elegibilidade`; no segundo, somente `exames`. O script de inicialização cria uma credencial própria para cada schema e a usa para criá-lo, de modo que cada aplicação só enxerga sua própria autoridade sobre os dados:

```sql
-- infra/postgres/init.sql (executado uma vez, contra o banco "elegibilidade")
CREATE ROLE elegibilidade LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS PASSWORD 'elegibilidade';
CREATE SCHEMA AUTHORIZATION elegibilidade;
SET ROLE elegibilidade;
CREATE TABLE elegibilidade.beneficiarios (
    id text PRIMARY KEY,
    elegivel boolean NOT NULL
);
INSERT INTO elegibilidade.beneficiarios (id, elegivel)
VALUES ('paciente-001', true), ('paciente-002', false);
```

O mesmo script, contra o banco `exames`, cria a role `exames` e a tabela `exames.solicitacoes`, sem nenhuma referência ao schema `elegibilidade`. Cada banco usa rede interna e alias próprio; cada aplicação recebe apenas sua URL e só participa da rede do banco que possui. A rede de aplicação é separada e serve ao HTTP entre serviços. Não há porta de banco publicada para a máquina durante a oficina, reduzindo caminhos acidentais.

O teste `test_exames_source_cannot_access_eligibility_table_directly` funciona como uma guarda simples: ele lê o próprio arquivo-fonte de Exames como texto e procura referências que não deveriam existir.

```python
# tests/test_service_boundaries.py
from pathlib import Path

import httpx
from fastapi.testclient import TestClient

import exames  # no laboratório: from hospital.servicos import exames

EXAMES_SOURCE = Path(__file__).with_name("exames.py")

def test_exames_source_cannot_access_eligibility_table_directly():
    source = EXAMES_SOURCE.read_text(encoding="utf-8").casefold()

    assert "elegibilidade.beneficiarios" not in source
    assert "from elegibilidade" not in source
    assert "join elegibilidade" not in source
    assert "db_elegibilidade" not in source
```

Guardas textuais não substituem permissões: a separação física e as credenciais oferecem a proteção efetiva; este teste só documenta a intenção e detecta regressões óbvias, como alguém colar um `SELECT` direto na tabela alheia.

O teste de contrato usa um transporte HTTP controlado (`httpx.MockTransport`) para responder como Elegibilidade, mas importa somente `hospital.servicos.exames` — nunca o código do provedor:

```python
# tests/test_service_boundaries.py
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
    assert response.json()["solicitacao_id"] == 41
```

`_client_for_eligibility` troca, via `dependency_overrides`, o cliente HTTP real por um que responde com o payload controlado acima — Exames nunca percebe a diferença, porque só enxerga o contrato. Assim o teste avalia o que o consumidor espera do contrato, sem chamar função interna nem instanciar repositório do provedor. Se a implementação de Elegibilidade mudar mantendo status e corpo, o teste do consumidor permanece válido.

O bloco abaixo completa o arquivo de testes com `_client_for_eligibility` e um `main`. Para executar, salve os dois blocos de teste anteriores seguidos deste bloco em `test_fronteira.py`, na mesma pasta de `exames.py`, e rode `python3 test_fronteira.py`. O `main` chama as funções de teste diretamente, usa `pytest.MonkeyPatch` (o pacote `pytest` faz parte das dependências de desenvolvimento do laboratório e é instalado com `pip install pytest`) e, ao final, aponta a guarda para um arquivo com `SELECT` na tabela de Elegibilidade para mostrar a reprovação.

```python
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


if __name__ == "__main__":
    import tempfile

    import pytest

    test_exames_source_cannot_access_eligibility_table_directly()
    print("Guarda textual sobre exames.py: aprovado")

    with pytest.MonkeyPatch.context() as monkeypatch:
        test_exames_consumes_eligibility_only_through_http_contract(monkeypatch)
    exames.app.dependency_overrides.clear()
    print("Contrato HTTP consumido por Exames: aprovado")

    # A guarda precisa reprovar um arquivo de Exames que lê a tabela de Elegibilidade.
    with tempfile.TemporaryDirectory() as pasta:
        EXAMES_SOURCE = Path(pasta) / "exames.py"
        EXAMES_SOURCE.write_text(
            'SQL = "SELECT elegivel FROM elegibilidade.beneficiarios"\n',
            encoding="utf-8",
        )
        try:
            test_exames_source_cannot_access_eligibility_table_directly()
        except AssertionError:
            print("Guarda textual sobre um exames.py com SELECT na tabela alheia: reprovado")
```

A execução imprime:

```text
Guarda textual sobre exames.py: aprovado
Contrato HTTP consumido por Exames: aprovado
Guarda textual sobre um exames.py com SELECT na tabela alheia: reprovado
```

## O que o exemplo deliberadamente não inclui

Não há autenticação, dados pessoais reais, descoberta dinâmica, TLS, migrações versionadas ou telemetria distribuída. Também não há SAGA, CQRS ou mensageria. O fluxo faz uma consulta síncrona antes de uma única transação local; adicionar padrões avançados esconderia a lição principal.

Em produção, a equipe precisaria definir SLOs, propagação de correlação, limites de recursos, política de logs, proteção de dados e restauração. O código também adotaria migrações em vez de um script de inicialização descartável. O Compose serve como ambiente didático reproduzível e não foi preparado para produção.

## Alternativa: monólito modular

Os mesmos limites poderiam existir em uma aplicação: `Elegibilidade` exporia uma interface interna e seria o único módulo autorizado a acessar suas tabelas; `Exames` dependeria dessa interface. A chamada não sofreria falha de rede e uma implantação seria suficiente. Se as equipes e os requisitos de escala fossem iguais, essa alternativa provavelmente teria menor custo.

A versão distribuída é escolhida aqui para observar propriedades que só aparecem com rede e processos independentes. Não transforma a alternativa modular em desenho inferior.

Qualquer que seja a forma escolhida, a regra central permanece: a configuração de Exames recebe a URL HTTP de Elegibilidade e a URL de seu próprio banco e não recebe a URL do banco alheio.
