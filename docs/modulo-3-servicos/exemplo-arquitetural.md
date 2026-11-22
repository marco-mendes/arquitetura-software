# Exemplo arquitetural

O exemplo usa o caso do módulo, a plataforma de uma rede hospitalar fictícia que atende pacientes de planos de saúde. Quando um médico pede um exame, a recepção registra o pedido no serviço de Exames, que antes de gravar consulta o serviço de Elegibilidade para saber se o paciente tem cobertura do plano.

O laboratório implementa os *bounded contexts* de Elegibilidade e de Exames em dois processos FastAPI independentes, cada um com o próprio PostgreSQL e a própria credencial de acesso. O exemplo expõe um limite verificável entre os dois serviços sem simular a plataforma hospitalar inteira. Exames conhece o contrato HTTP de Elegibilidade e não conhece a tabela em que Elegibilidade guarda os dados.

## Bounded contexts do exemplo {#onde-esta-o-bounded-context}

Um *bounded context* delimita a parte do sistema em que um modelo e a sua linguagem têm significado consistente, como define a página de [Conceitos](conceitos.md). Ele é uma fronteira semântica e não exige processo separado. Neste laboratório, cada *bounded context* também foi implantado como processo próprio, decisão tomada para tornar a fronteira observável e que não constitui regra geral.

Cada contexto tem um vocabulário próprio que o outro contexto não precisa conhecer. Em Elegibilidade, o campo `elegivel` resume vínculo, vigência e regra da operadora num cálculo que pode mudar por completo sem alterar o campo booleano exposto. Em Exames, o campo `situacao` descreve uma etapa do fluxo clínico da solicitação e não tem relação com o vocabulário de Elegibilidade. A tradução entre os dois modelos ocorre somente no contrato HTTP, sem acesso de um contexto ao *schema*, às tabelas ou ao código interno do outro.

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

**Texto alternativo:** os *bounded contexts* Elegibilidade e Exames lado a lado, cada um com o próprio código-fonte e o próprio PostgreSQL, ligados apenas pela chamada HTTP do contrato.

*Figura 1 — Bounded contexts do laboratório e código de cada um. Fonte: curso.*

**Leitura textual da figura:** o *bounded context* Elegibilidade contém `elegibilidade.py` e o próprio PostgreSQL, enquanto o *bounded context* Exames contém `exames.py` e outro PostgreSQL. A única seta entre os dois contextos representa a chamada HTTP do contrato, sem acesso direto a banco ou a código interno.

As seções seguintes mostram primeiro o código dos componentes de cada lado da figura e depois o fluxo de uma solicitação entre eles.

## Componentes

O serviço **Elegibilidade** oferece a operação `GET /elegibilidades/{beneficiario_id}`. O *schema* do serviço contém beneficiários sintéticos com a decisão booleana de elegibilidade de cada um. Cada serviço é uma aplicação FastAPI com a própria conexão ao PostgreSQL, enquanto os códigos dos dois serviços se comunicam apenas por HTTP, sem `import` ou chamada de função entre eles.

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

O serviço **Exames** oferece a operação `POST /exames`, que consulta Elegibilidade por HTTP e registra a solicitação no próprio *schema* quando a resposta é positiva. O contrato de entrada e de saída é declarado com Pydantic, como no exemplo do Módulo 2.

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

A variável de ambiente `ELIGIBILIDADE_URL` contém um endereço HTTP e é a única informação que Exames recebe sobre o outro serviço. Exames não recebe a URL do banco de Elegibilidade, de modo que a própria configuração impede o acesso direto sem depender de uma regra no código.

Os dois serviços oferecem a operação `GET /health`, que verifica apenas a conexão com o banco local e não declara a saúde de nenhuma dependência remota. Essa escolha torna a falha parcial visível, porque Exames continua com processo e banco ativos enquanto a operação que depende de Elegibilidade retorna `503`.

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

**Texto alternativo:** o consumidor solicita exames, Exames consulta Elegibilidade por HTTP e cada serviço acessa somente o próprio banco PostgreSQL.

*Figura 2 — Contrato entre serviços e propriedade de dados. Fonte: curso.*

**Leitura textual da figura:** o consumidor chama Exames, que consulta Elegibilidade por HTTP antes de gravar a solicitação no próprio PostgreSQL. O caminho direto entre Exames e o banco de Elegibilidade aparece marcado como proibido na figura.

## Fluxo nominal

O consumidor envia o pedido abaixo para a operação `POST /exames` de Exames.

```json
{
  "beneficiario_id": "paciente-001",
  "codigo_exame": "HEM-001"
}
```

O Pydantic valida a forma do pedido antes da execução da rota, com o mesmo mecanismo usado no Módulo 2. Dentro da rota, Exames chama `GET /elegibilidades/paciente-001` pelo cliente HTTP injetado e não usa nenhum detalhe de Elegibilidade além do contrato.

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

A função `registrar_solicitacao` é a única função de Exames que acessa banco de dados, sempre o banco do próprio Exames.

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

Em Elegibilidade, a mesma chamada executa uma consulta parametrizada na tabela `elegibilidade.beneficiarios` e devolve a resposta abaixo.

```json
{
  "beneficiario_id": "paciente-001",
  "elegivel": true
}
```

Exames aceita a decisão de elegibilidade, chama a função `registrar_solicitacao` e retorna `201 Created` com o corpo abaixo.

```json
{
  "solicitacao_id": 1,
  "beneficiario_id": "paciente-001",
  "codigo_exame": "HEM-001",
  "situacao": "solicitado"
}
```

O identificador da solicitação aumenta a cada nova execução enquanto o volume do banco existir. Depois do comando `down -v`, o volume é removido e a primeira solicitação da execução seguinte volta a receber o identificador `1`.

## Fluxos alternativos

A rota `solicitar_exame` completa contém uma verificação explícita para cada resposta de Elegibilidade que impede o registro da solicitação. O trecho abaixo mostra a rota com as verificações que a versão resumida do fluxo nominal omitiu.

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

Cada `raise` da rota corresponde a uma das situações da tabela.

| Situação | Resposta de Elegibilidade | Resposta de Exames |
| --- | --- | --- |
| Beneficiário `paciente-002` | `200` com `elegivel: false` | `422 beneficiario_inelegivel` |
| Identificador inexistente | `404` | `422 beneficiario_desconhecido` |
| Estrutura incompatível com o contrato | `200` com corpo inválido | `502 contrato_invalido` |
| Falha de conexão ou estouro do prazo de espera | exceção `httpx.HTTPError` | `503 dependencia_indisponivel` |
| Erro do provedor | `5xx` | `503 dependencia_indisponivel` |

A falha de conexão e o erro do provedor produzem a resposta abaixo.

```json
{
  "detail": {
    "codigo": "dependencia_indisponivel"
  }
}
```

A resposta informa que a capacidade solicitada não pode ser concluída enquanto uma dependência necessária está indisponível, sem indicar que o processo de Exames parou. O teste `test_exames_makes_partial_failure_observable_when_dependency_is_down` simula essa queda de conexão e verifica o status `503` com o código `dependencia_indisponivel`.

### Execução de ponta a ponta dos dois serviços

Os blocos de código desta página formam dois arquivos que rodam na mesma pasta. O arquivo `elegibilidade.py` recebe o primeiro bloco da seção Componentes. O arquivo `exames.py` recebe os blocos de `PedidoExame` e de `/health`, seguidos do bloco de `registrar_solicitacao` e da rota completa desta seção. A versão resumida do fluxo nominal fica fora de `exames.py`, porque declara a mesma rota. O comando `pip install fastapi httpx pydantic "psycopg[binary]"` instala os quatro pacotes do laboratório usados pelos dois arquivos e pelo programa de demonstração.

O programa abaixo deve ser salvo como `demo_servicos.py` na mesma pasta e executado com `python3 demo_servicos.py`. Ele substitui o PostgreSQL de cada serviço por um banco SQLite em memória e entrega as chamadas HTTP de Exames a um `TestClient` de Elegibilidade. Com essa substituição, o exemplo roda sem contêiner e sem rede e mantém a ligação entre os serviços restrita ao contrato HTTP. No laboratório, cada serviço usa o PostgreSQL real e a chamada atravessa a rede do Compose.

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

A execução do programa imprime a saída abaixo.

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

O caso 5 reproduz a falha parcial descrita na seção anterior, com a solicitação recusada com `503 dependencia_indisponivel` enquanto o `/health` de Exames continua com `200`. O banco de Exames guarda apenas a solicitação aprovada no caso 2.

## Fronteira de dados executável

O arquivo do Compose cria dois servidores PostgreSQL, o primeiro somente com o *schema* `elegibilidade` e o segundo somente com o *schema* `exames`. O script de inicialização cria uma credencial própria para cada *schema* e usa essa credencial para criar o *schema*, de modo que cada aplicação só tem autoridade sobre os próprios dados.

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

No banco `exames`, o mesmo script cria a *role* `exames` e a tabela `exames.solicitacoes` sem nenhuma referência ao *schema* `elegibilidade`. Cada banco usa uma rede interna e um nome de rede próprios. Cada aplicação recebe apenas a URL do próprio banco e participa somente da rede desse banco, enquanto uma rede de aplicação separada atende às chamadas HTTP entre os serviços. A oficina não publica nenhuma porta de banco para a máquina local, o que elimina caminhos de acesso acidentais aos bancos.

O teste `test_exames_source_cannot_access_eligibility_table_directly` é uma verificação textual que lê o arquivo-fonte de Exames e procura referências que não deveriam existir nele.

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

A proteção efetiva vem da separação física e das credenciais, que uma verificação textual não substitui. O teste documenta a intenção da fronteira e detecta regressões evidentes, como um `SELECT` escrito diretamente sobre a tabela de Elegibilidade.

O teste de contrato usa o transporte HTTP controlado `httpx.MockTransport` para responder no lugar de Elegibilidade. O teste importa somente o módulo `hospital.servicos.exames` e não importa o código do provedor.

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

A função `_client_for_eligibility` usa `dependency_overrides` para trocar o cliente HTTP real por um cliente que responde com o conteúdo controlado acima. Exames não distingue os dois clientes, porque depende apenas do contrato. O teste avalia o que o consumidor espera do contrato sem chamar função interna nem instanciar repositório do provedor. Uma mudança na implementação de Elegibilidade que mantenha o status e o corpo da resposta não invalida o teste do consumidor.

O bloco abaixo completa o arquivo de testes com a função `_client_for_eligibility` e uma função `main`. Os dois blocos de teste anteriores e este bloco devem ser salvos em sequência no arquivo `test_fronteira.py` da mesma pasta de `exames.py` e executados com `python3 test_fronteira.py`. A função `main` chama as funções de teste diretamente e usa `pytest.MonkeyPatch`. O pacote `pytest` faz parte das dependências de desenvolvimento do laboratório e é instalado com `pip install pytest`. Ao final, a função aponta a verificação textual para um arquivo com `SELECT` na tabela de Elegibilidade para mostrar a reprovação.

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

A execução do programa imprime a saída abaixo.

```text
Guarda textual sobre exames.py: aprovado
Contrato HTTP consumido por Exames: aprovado
Guarda textual sobre um exames.py com SELECT na tabela alheia: reprovado
```

## Escopo do exemplo {#o-que-o-exemplo-deliberadamente-nao-inclui}

O exemplo não inclui autenticação, dados pessoais reais ou descoberta dinâmica de serviços. Também não inclui TLS e migrações versionadas, nem telemetria distribuída ou mensageria. O fluxo faz uma consulta síncrona antes de uma única transação local, situação em que padrões como SAGA e CQRS acrescentariam componentes sem benefício para o objetivo do exemplo.

Em produção, a equipe precisaria definir os objetivos de nível de serviço e a propagação de identificadores de correlação entre as chamadas. Também precisaria definir limites de recursos, política de logs, proteção de dados e procedimento de restauração. O código adotaria migrações versionadas no lugar do script de inicialização descartável. O Compose da oficina é um ambiente didático reproduzível e não foi preparado para uso em produção.

## Alternativa com monólito modular {#alternativa-monolito-modular}

Os mesmos limites poderiam existir numa única aplicação. Nesse desenho, o módulo `Elegibilidade` exporia uma interface interna e seria o único módulo autorizado a acessar as suas tabelas, enquanto o módulo `Exames` dependeria dessa interface. A chamada entre os módulos não estaria sujeita a falha de rede e uma única implantação atenderia aos dois módulos. Com as mesmas equipes e os mesmos requisitos de escala para os dois módulos, essa alternativa teria provavelmente um custo operacional menor.

O laboratório usa a versão distribuída para tornar observáveis as propriedades que só aparecem com rede e processos independentes, o que não torna a alternativa modular um desenho inferior.

Nas duas formas, a configuração de Exames recebe a URL HTTP de Elegibilidade e a URL do próprio banco, sem receber a URL do banco de Elegibilidade.
