# Oficina de ferramentas

A oficina leva cerca de noventa minutos e usa apenas dados sintéticos, sem chamar nenhum sistema externo. O objetivo é observar um contrato de API sob quatro ângulos, conforme a lista abaixo.

- O documento que descreve o contrato.
- A aplicação que implementa o contrato.
- Um cliente que consome a API.
- Os testes que verificam a concordância entre os três ângulos anteriores.

A prática consiste em executar uma API na própria máquina e ler a documentação que ela gera automaticamente. Em seguida, a API é consumida por um programa cliente, o contrato é submetido a um verificador automático e a suíte de testes é executada. Cada ferramenta citada é apresentada antes do uso, na seção **Ferramenta**. Ao final há uma extensão opcional em .NET que posiciona um *gateway* de API diante de dois serviços.

![Contrato de API observado como documento, implementação, consumo e verificação](../assets/images/m02-oficina-contrato-quatro-angulos.png)

*Figura 10 — O mesmo contrato sob os ângulos de documento, implementação, consumo e verificação. Fonte: curso.*

**Leitura textual da figura:** no centro está o contrato, com a operação `POST /elegibilidades`, a resposta `202 Accepted` e o cabeçalho `Location`. Quatro ângulos apontam para o contrato. Acima aparece o arquivo `contratos/openapi.yaml` como documento e à direita aparecem `main.py` e `models.py` como implementação em FastAPI. À esquerda aparecem o cliente HTTP e a página `/docs` como consumo. Abaixo aparecem o Spectral e sete testes como verificação, alimentados por um caso de entrada inválida em que o CPF `12345678901` é submetido como `123`.

## O que existe antes de você abrir o terminal

A oficina começa numa pasta vazia, na qual são escritos os nove arquivos que compõem a **API de elegibilidades da plataforma hospitalar**, uma aplicação didática local. A aplicação não consulta uma operadora real, não acessa prontuários e não envia dados para fora do computador do aluno. O objetivo é tornar observável um contrato HTTP pequeno, sem simular uma plataforma hospitalar completa.

Cada arquivo aparece completo nesta página, pronto para ser copiado. O título de cada bloco é um link para o mesmo arquivo no repositório do curso, idêntico byte a byte ao conteúdo da página, para quem preferir baixá-lo.

O arquivo `src/hospital/api/main.py` inicia a aplicação FastAPI e expõe apenas as duas operações públicas descritas na tabela abaixo.

| Operação | O que faz nesta oficina | Resultado observável |
| --- | --- | --- |
| `POST /elegibilidades` | recebe CPF sintético, código de operadora e matrícula, valida o contrato e aceita o pedido | `202 Accepted`, corpo com `protocolo` e cabeçalho `Location` |
| `GET /elegibilidades/{protocolo}` | recupera o pedido aceito usando o protocolo retornado no `POST` | `200 OK` com a representação ou `404` se o protocolo não existir |

Os dados aceitos ficam somente na memória do processo, de modo que parar ou reiniciar o servidor remove os protocolos criados. O limite é deliberado, pois a prática compara contrato, consumo e implementação sem afirmar persistência ou idempotência distribuída. A oficina também não trata de autenticação nem da integração da API com a operadora do plano de saúde.

### Onde cada arquivo mora

A árvore abaixo mostra a estrutura a ser montada. Os comandos seguintes são executados a partir da pasta `oficina-contrato` e cada caminho mencionado no texto é relativo a ela.

```text
oficina-contrato/                      ← execute os comandos a partir daqui
├── pyproject.toml                     declara as bibliotecas a instalar
├── .spectral.yaml                     aponta para a configuração de dentro de contratos/
├── contratos/
│   ├── openapi.yaml                   o contrato escrito à mão
│   └── .spectral.yaml                 as regras que o contrato deve cumprir
├── src/hospital/
│   ├── __init__.py                    vazio, torna hospital um pacote
│   └── api/
│       ├── __init__.py                vazio, torna api um pacote
│       ├── models.py                  os formatos de dados e suas validações
│       └── main.py                    a aplicação e as duas rotas
├── tests/
│   └── test_api_contract.py           os sete testes de contrato
└── evidencias/                        você criará esta pasta na preparação
```

A tabela abaixo descreve o papel de cada arquivo, cujo conteúdo aparece na seção seguinte.

| Arquivo | O que ele faz | Onde isso aparece na teoria |
| --- | --- | --- |
| [`contratos/openapi.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/contratos/openapi.yaml) | O contrato escrito à mão, com as duas operações, os formatos de dados e os exemplos que a API promete a quem consome. | É o **contrato** de [interface, contrato e implementação](conceitos.md), publicado num documento que existe independente do código. |
| [`src/hospital/api/models.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/api/models.py) | Os modelos de dados escritos com **Pydantic**, a biblioteca que o FastAPI usa para validar. O tipo declarado em cada campo é a própria regra de validação. | Onde o contrato deixa de ser documento e passa a ser código executável. |
| [`src/hospital/api/main.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/api/main.py) | A aplicação FastAPI, com as duas rotas, o `202` com `Location` e os erros estruturados. | A **implementação**, que pode mudar internamente sem quebrar quem consome, desde que o contrato seja mantido. |
| [`tests/test_api_contract.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/tests/test_api_contract.py) | Sete testes, dos quais cinco exercitam a API por chamadas HTTP e dois comparam o contrato publicado com o que o FastAPI gera. | A verificação de que a promessa publicada e o comportamento real não divergiram. |
| [`.spectral.yaml` e `contratos/.spectral.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/contratos/.spectral.yaml) | As regras que o verificador de contrato aplica ao `openapi.yaml`. | A política de contrato que uma equipe acorda e automatiza. |

O percurso de uma requisição pela aplicação explica a função de cada um desses arquivos.

```mermaid
flowchart TB
    CL[Cliente envia POST /elegibilidades<br/>com CPF, operadora e matrícula] --> V{models.py<br/>o corpo cumpre o contrato?}
    V -->|sim| OK[main.py cria protocolo<br/>202 Accepted + cabeçalho Location]
    V -->|não| ERR[main.py devolve corpo estruturado<br/>422 Unprocessable Entity]
    OK --> G[Cliente segue o Location<br/>GET /elegibilidades/protocolo]
    G --> R[200 OK com a representação<br/>ou 404 se o protocolo não existir]
```

**Texto alternativo:** o cliente envia a requisição e uma decisão verifica se o corpo cumpre o contrato. A decisão leva à aceitação com 202 e cabeçalho Location ou à recusa com 422 estruturado. Depois da aceitação, o fluxo segue para a consulta da elegibilidade pelo protocolo devolvido no cabeçalho Location.

*Figura 11 — Os dois desfechos de uma requisição e o que cada arquivo decide. Fonte: curso.*

**Leitura textual:** o cliente envia `POST /elegibilidades` com CPF, código de operadora e matrícula. A validação declarada em `models.py` decide o desfecho antes da execução de qualquer código de negócio. Quando o corpo cumpre o contrato, `main.py` cria o protocolo e responde `202 Accepted` com o cabeçalho `Location`. Quando o corpo não cumpre o contrato, a mesma aplicação devolve `422 Unprocessable Entity` com um corpo estruturado que lista campo, mensagem e tipo do erro. No desfecho de aceitação, o cliente usa o endereço do `Location` para chamar `GET /elegibilidades/{protocolo}`. Essa rota responde `200 OK` com a representação ou `404` quando o protocolo não existe no processo atual.

### Conteúdo dos nove arquivos

Crie a pasta e a estrutura antes de escrever os arquivos. No macOS e no Linux, use os comandos abaixo.

```bash
mkdir -p oficina-contrato/contratos oficina-contrato/src/hospital/api oficina-contrato/tests
cd oficina-contrato
```

No PowerShell:

```powershell
mkdir oficina-contrato\contratos, oficina-contrato\src\hospital\api, oficina-contrato\tests
cd oficina-contrato
```

O `pyproject.toml` declara as bibliotecas e torna o pacote instalável. Esse arquivo permite o `pip install -e` usado mais adiante, razão pela qual nenhum comando precisa informar o caminho do código.

[`pyproject.toml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "api-elegibilidades"
version = "0.1.0"
description = "API de elegibilidades da plataforma hospitalar, oficina do módulo 2"
requires-python = ">=3.11"
dependencies = [
  "fastapi",
  "uvicorn",
  "pydantic",
  "httpx",
]

[project.optional-dependencies]
dev = [
  "pytest",
  "pyyaml",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

Os dois arquivos `__init__.py` ficam vazios de propósito. A presença deles torna `hospital` e `hospital.api` pacotes Python importáveis, condição para que o Python localize `hospital.api.main:app`.

[`src/hospital/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/__init__.py)

```python

```

[`src/hospital/api/__init__.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/api/__init__.py)

```python

```

O `models.py` declara os formatos de dados com **Pydantic**. O tipo e as restrições de cada campo são a própria regra de validação, que o FastAPI aplica antes de chamar a função da rota.

[`src/hospital/api/models.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/api/models.py)

```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PedidoElegibilidade(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "cpf": "12345678901",
                    "codigo_operadora": "OPS-001",
                    "matricula_plano": "MAT-2026-001",
                }
            ]
        }
    )

    cpf: str = Field(pattern=r"^\d{11}$")
    codigo_operadora: str = Field(min_length=1, max_length=40)
    matricula_plano: str = Field(min_length=1, max_length=60)


class ElegibilidadeAceita(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocolo: str
    situacao: str = Field(pattern=r"^recebida$")
    criado_em: datetime


class DetalheErro(BaseModel):
    model_config = ConfigDict(extra="forbid")

    campo: str
    mensagem: str
    tipo: str


class ErroAPI(BaseModel):
    model_config = ConfigDict(extra="forbid")

    codigo: str
    mensagem: str
    detalhes: list[DetalheErro]
```

O `main.py` monta a aplicação e as duas rotas. O tratador de erro de validação faz com que uma requisição fora do contrato receba um corpo estruturado no formato da API, diferente do formato padrão do FastAPI.

[`src/hospital/api/main.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/src/hospital/api/main.py)

```python
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from hospital.api.models import (
    ElegibilidadeAceita,
    ErroAPI,
    PedidoElegibilidade,
)


app = FastAPI(
    title="API de elegibilidades da plataforma hospitalar",
    version="1.0.0",
)

_elegibilidades: dict[str, ElegibilidadeAceita] = {}


def limpar_elegibilidades() -> None:
    """Reinicia o armazenamento efêmero usado nos testes e na oficina."""

    _elegibilidades.clear()


@app.get("/health/live", include_in_schema=False)
def live() -> dict[str, str]:
    """Indica que o processo atende, sem consultar dependências externas."""

    return {"status": "live"}


@app.get("/health/ready", include_in_schema=False)
def ready() -> dict[str, str]:
    """Indica que esta instância pode receber tráfego do Service."""

    return {"status": "ready"}


@app.exception_handler(RequestValidationError)
async def tratar_erro_de_validacao(
    _request, error: RequestValidationError
) -> JSONResponse:
    detalhes = [
        {
            "campo": ".".join(str(part) for part in item["loc"]),
            "mensagem": item["msg"],
            "tipo": item["type"],
        }
        for item in error.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "codigo": "dados_invalidos",
            "mensagem": "A requisição não atende ao contrato.",
            "detalhes": detalhes,
        },
    )


@app.post(
    "/elegibilidades",
    response_model=ElegibilidadeAceita,
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Pedido aceito para processamento.",
    responses={
        202: {
            "headers": {
                "Location": {
                    "description": "Caminho do recurso aceito.",
                    "required": True,
                    "schema": {"type": "string"},
                    "example": (
                        "/elegibilidades/"
                        "550e8400-e29b-41d4-a716-446655440000"
                    ),
                }
            }
        },
        422: {"model": ErroAPI},
    },
    operation_id="criarElegibilidade",
    summary="Aceita uma consulta de elegibilidade",
)
def criar_elegibilidade(
    _pedido: PedidoElegibilidade, response: Response
) -> ElegibilidadeAceita:
    aceita = ElegibilidadeAceita(
        protocolo=str(uuid4()),
        situacao="recebida",
        criado_em=datetime.now(timezone.utc),
    )
    _elegibilidades[aceita.protocolo] = aceita
    response.headers["Location"] = f"/elegibilidades/{aceita.protocolo}"
    return aceita


@app.get(
    "/elegibilidades/{protocolo}",
    response_model=ElegibilidadeAceita,
    responses={404: {"model": ErroAPI}},
    operation_id="consultarElegibilidade",
    summary="Consulta uma elegibilidade aceita",
)
def consultar_elegibilidade(protocolo: str):
    encontrada = _elegibilidades.get(protocolo)
    if encontrada is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "codigo": "elegibilidade_nao_encontrada",
                "mensagem": "Protocolo de elegibilidade não encontrado.",
                "detalhes": [],
            },
        )
    return encontrada
```

O `contratos/openapi.yaml` é o contrato escrito à mão, independente do código. O arquivo é longo porque descreve cada promessa da API, incluindo os exemplos.

[`contratos/openapi.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/contratos/openapi.yaml)

```yaml
openapi: 3.1.0
info:
  title: API de elegibilidades da plataforma hospitalar
  version: 1.0.0
  contact:
    name: Disciplina de Arquitetura de Software
  description: >-
    Contrato didático para aceitar e recuperar consultas administrativas de
    elegibilidade. O laboratório mantém dados somente em memória.
tags:
  - name: Elegibilidades
    description: Operações administrativas de elegibilidade.
servers:
  - url: http://127.0.0.1:8000
    description: Servidor local da oficina.
paths:
  /elegibilidades:
    post:
      tags: [Elegibilidades]
      operationId: criarElegibilidade
      summary: Aceita uma consulta de elegibilidade
      description: >-
        Valida o pedido, cria um protocolo efêmero e informa onde consultar o
        recurso aceito.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PedidoElegibilidade'
            examples:
              pedidoValido:
                summary: Pedido sintético válido
                value:
                  cpf: '12345678901'
                  codigo_operadora: OPS-001
                  matricula_plano: MAT-2026-001
      responses:
        '202':
          description: Pedido aceito para processamento.
          headers:
            Location:
              description: Caminho do recurso aceito.
              required: true
              schema:
                type: string
              example: /elegibilidades/550e8400-e29b-41d4-a716-446655440000
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ElegibilidadeAceita'
              examples:
                aceita:
                  summary: Protocolo criado
                  value:
                    protocolo: 550e8400-e29b-41d4-a716-446655440000
                    situacao: recebida
                    criado_em: '2026-07-17T13:30:00Z'
        '422':
          description: Corpo ausente ou incompatível com o contrato.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErroAPI'
              examples:
                cpfAusente:
                  summary: CPF obrigatório ausente
                  value:
                    codigo: dados_invalidos
                    mensagem: A requisição não atende ao contrato.
                    detalhes:
                      - campo: body.cpf
                        mensagem: Field required
                        tipo: missing
  /elegibilidades/{protocolo}:
    get:
      tags: [Elegibilidades]
      operationId: consultarElegibilidade
      summary: Consulta uma elegibilidade aceita
      description: Recupera o estado efêmero associado ao protocolo informado.
      parameters:
        - name: protocolo
          in: path
          required: true
          description: Identificador retornado na aceitação do pedido.
          schema:
            type: string
      responses:
        '200':
          description: Elegibilidade localizada.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ElegibilidadeAceita'
              examples:
                localizada:
                  summary: Estado atual
                  value:
                    protocolo: 550e8400-e29b-41d4-a716-446655440000
                    situacao: recebida
                    criado_em: '2026-07-17T13:30:00Z'
        '404':
          description: Protocolo não localizado no processo atual.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErroAPI'
              examples:
                ausente:
                  summary: Protocolo desconhecido
                  value:
                    codigo: elegibilidade_nao_encontrada
                    mensagem: Protocolo de elegibilidade não encontrado.
                    detalhes: []
components:
  schemas:
    PedidoElegibilidade:
      type: object
      additionalProperties: false
      required: [cpf, codigo_operadora, matricula_plano]
      properties:
        cpf:
          type: string
          pattern: '^\d{11}$'
          description: Identificador sintético com onze dígitos usado no laboratório.
        codigo_operadora:
          type: string
          minLength: 1
          maxLength: 40
          description: Código da operadora no contexto da plataforma.
        matricula_plano:
          type: string
          minLength: 1
          maxLength: 60
          description: Matrícula administrativa no plano.
      examples:
        - cpf: '12345678901'
          codigo_operadora: OPS-001
          matricula_plano: MAT-2026-001
    ElegibilidadeAceita:
      type: object
      additionalProperties: false
      required: [protocolo, situacao, criado_em]
      properties:
        protocolo:
          type: string
          description: Identificador da consulta aceita.
        situacao:
          type: string
          const: recebida
          description: Estado inicial do pedido.
        criado_em:
          type: string
          format: date-time
          description: Instante UTC em que o pedido foi aceito.
    DetalheErro:
      type: object
      additionalProperties: false
      required: [campo, mensagem, tipo]
      properties:
        campo:
          type: string
        mensagem:
          type: string
        tipo:
          type: string
    ErroAPI:
      type: object
      additionalProperties: false
      required: [codigo, mensagem, detalhes]
      properties:
        codigo:
          type: string
          description: Código estável para tratamento pelo consumidor.
        mensagem:
          type: string
          description: Explicação legível do problema.
        detalhes:
          type: array
          items:
            $ref: '#/components/schemas/DetalheErro'
```

Os dois arquivos do Spectral declaram as regras que o contrato precisa cumprir. O arquivo da raiz apenas aponta para o arquivo de `contratos`, o que permite executar o verificador a partir de qualquer uma das duas pastas.

[`.spectral.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/.spectral.yaml)

```yaml
# CLI verificada: @stoplight/spectral-cli@6.16.1
extends:
  - ./contratos/.spectral.yaml
```

[`contratos/.spectral.yaml`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/contratos/.spectral.yaml)

```yaml
# CLI verificada: @stoplight/spectral-cli@6.16.1
extends: spectral:oas

rules:
  operation-operationId: error
  operation-description: error
  operation-tags: error
```

O `tests/test_api_contract.py` contém a verificação. Cinco testes exercitam a API por chamadas HTTP e dois comparam o contrato publicado com o que o FastAPI gera automaticamente.

[`tests/test_api_contract.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/tests/test_api_contract.py)

```python
"""Testes de contrato da API de elegibilidades.

Este arquivo responde a uma pergunta: **a aplicação faz o que o contrato promete?**

Há dois contratos em jogo, e a diferença entre eles é o assunto do módulo:

- o **contrato explícito**, escrito à mão em `contratos/openapi.yaml`, é a promessa
  publicada para quem consome a API;
- o **contrato gerado**, que o FastAPI monta sozinho a partir do código e serve em
  `/openapi.json`, descreve o que a aplicação realmente faz hoje.

Os cinco primeiros testes exercitam a aplicação pela porta da frente. Os dois
últimos comparam os dois contratos entre si, que é onde uma divergência costuma
aparecer sem ninguém notar.

Para rodar apenas este arquivo:

    python -m pytest tests/test_api_contract.py -q
"""

from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
import yaml

from hospital.api.main import app, limpar_elegibilidades
from hospital.api.models import ElegibilidadeAceita, ErroAPI, PedidoElegibilidade


# Caminho do contrato escrito à mão, relativo à raiz do laboratório.
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contratos" / "openapi.yaml"

# Corpo válido reaproveitado por vários testes. CPF e matrícula são sintéticos.
PEDIDO_VALIDO = {
    "cpf": "12345678901",
    "codigo_operadora": "OPS-001",
    "matricula_plano": "MAT-2026-001",
}


def setup_function():
    """Roda antes de cada teste.

    A aplicação guarda os pedidos em memória, então um teste enxergaria os
    protocolos criados pelo anterior. Limpar aqui deixa cada teste independente
    da ordem de execução.
    """
    limpar_elegibilidades()


def carregar_contrato_explicito() -> dict:
    """Lê `contratos/openapi.yaml` como dicionário Python."""
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


def exemplos_da_resposta(contrato: dict, caminho: str, metodo: str, status: str) -> list:
    """Devolve os exemplos JSON declarados para uma resposta do contrato.

    Existe para evitar a indexação encadeada longa que essa navegação exigiria
    dentro do teste. A estrutura percorrida é a do OpenAPI:
    paths → caminho → método → responses → status → content → mídia → examples.
    """
    resposta = contrato["paths"][caminho][metodo]["responses"][status]
    exemplos = resposta["content"]["application/json"]["examples"]
    return [item["value"] for item in exemplos.values()]


def test_post_aceita_pedido_e_get_recupera_pelo_location():
    """O caminho feliz: `POST` aceita e `GET` recupera pelo endereço devolvido.

    O `202 Accepted` significa "recebi e ainda vou processar", e não "pronto".
    Por isso a resposta traz um `protocolo` e o cabeçalho `Location` com o
    endereço onde consultar o andamento — o consumidor não precisa montar essa
    URL por conta própria.
    """
    client = TestClient(app)

    criado = client.post("/elegibilidades", json=PEDIDO_VALIDO)

    assert criado.status_code == 202
    corpo = criado.json()
    assert corpo["situacao"] == "recebida"
    assert corpo["protocolo"]

    # Não compara a data com um valor fixo: só exige que seja ISO 8601 válida.
    datetime.fromisoformat(corpo["criado_em"].replace("Z", "+00:00"))

    assert criado.headers["location"] == f"/elegibilidades/{corpo['protocolo']}"

    # Seguir o Location é exatamente o que um consumidor bem-comportado faz.
    recuperado = client.get(criado.headers["location"])

    assert recuperado.status_code == 200
    assert recuperado.json() == corpo


def test_pedido_sem_cpf_recebe_erro_422_estruturado():
    """Campo obrigatório ausente vira `422` com corpo previsível.

    O erro faz parte do contrato: quem consome precisa conseguir tratar a falha
    programaticamente, e para isso o corpo traz `codigo`, `mensagem` e a lista
    `detalhes` apontando o campo problemático.
    """
    client = TestClient(app)
    pedido_incompleto = {
        "codigo_operadora": "OPS-001",
        "matricula_plano": "MAT-2026-001",
    }

    resposta = client.post("/elegibilidades", json=pedido_incompleto)

    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "dados_invalidos"
    assert corpo["mensagem"]
    assert any(detalhe["campo"] == "body.cpf" for detalhe in corpo["detalhes"])


def test_pedido_com_campo_fora_do_contrato_e_recusado():
    """Campo a mais também é violação de contrato, não cortesia.

    Aceitar um campo desconhecido em silêncio faz o consumidor acreditar que ele
    foi processado. O modelo recusa, e o campo extra aparece em `detalhes`.
    """
    client = TestClient(app)
    pedido_com_extra = PEDIDO_VALIDO | {"campo_nao_contratado": "valor"}

    resposta = client.post("/elegibilidades", json=pedido_com_extra)

    assert resposta.status_code == 422
    detalhes = resposta.json()["detalhes"]
    assert any(detalhe["campo"] == "body.campo_nao_contratado" for detalhe in detalhes)


def test_protocolo_inexistente_recebe_erro_404_estruturado():
    """Consultar protocolo que não existe devolve `404` no mesmo formato de erro.

    O corpo segue o mesmo esquema `ErroAPI` do `422`: um formato de erro por API,
    não um por operação.
    """
    client = TestClient(app)

    resposta = client.get("/elegibilidades/protocolo-inexistente")

    assert resposta.status_code == 404
    assert resposta.json() == {
        "codigo": "elegibilidade_nao_encontrada",
        "mensagem": "Protocolo de elegibilidade não encontrado.",
        "detalhes": [],
    }


def test_health_separa_processo_vivo_de_pronto_para_receber_trafego():
    """`/health/live` e `/health/ready` respondem perguntas diferentes.

    Vivo significa que o processo não travou. Pronto significa que ele pode
    receber tráfego. Um orquestrador reinicia com base no primeiro e tira do
    balanceamento com base no segundo.
    """
    client = TestClient(app)

    assert client.get("/health/live").json() == {"status": "live"}
    assert client.get("/health/ready").json() == {"status": "ready"}


def test_contrato_explicito_declara_operacoes_schemas_e_exemplos_validos():
    """O `openapi.yaml` está bem formado e seus exemplos são de verdade.

    Um exemplo desatualizado no contrato é pior que exemplo nenhum, porque quem
    consome copia e não funciona. Aqui cada exemplo declarado é validado contra o
    modelo correspondente, e o exemplo de requisição é enviado à aplicação real.
    """
    contrato = carregar_contrato_explicito()

    assert contrato["openapi"] == "3.1.0"
    assert set(contrato["paths"]) == {
        "/elegibilidades",
        "/elegibilidades/{protocolo}",
    }

    schemas = contrato["components"]["schemas"]
    for nome in ("PedidoElegibilidade", "ElegibilidadeAceita", "ErroAPI"):
        assert nome in schemas

    schema_pedido = schemas["PedidoElegibilidade"]
    assert set(schema_pedido["required"]) == set(PEDIDO_VALIDO)

    # O exemplo publicado precisa ser aceito pela aplicação de verdade.
    exemplo_pedido = schema_pedido["examples"][0]
    PedidoElegibilidade.model_validate(exemplo_pedido)
    assert TestClient(app).post("/elegibilidades", json=exemplo_pedido).status_code == 202

    # Cada exemplo de resposta precisa bater com o modelo daquela resposta.
    respostas_documentadas = (
        ("/elegibilidades", "post", "202", ElegibilidadeAceita),
        ("/elegibilidades", "post", "422", ErroAPI),
        ("/elegibilidades/{protocolo}", "get", "200", ElegibilidadeAceita),
        ("/elegibilidades/{protocolo}", "get", "404", ErroAPI),
    )
    for caminho, metodo, status, modelo in respostas_documentadas:
        for exemplo in exemplos_da_resposta(contrato, caminho, metodo, status):
            modelo.model_validate(exemplo)


def test_contrato_explicito_e_contrato_gerado_nao_divergem():
    """O contrato publicado e o que a aplicação gera dizem a mesma coisa.

    Este é o teste que pega o erro mais caro do módulo: alguém altera o código,
    o contrato gerado acompanha, e o `openapi.yaml` publicado continua prometendo
    o formato antigo para quem consome. A comparação é pontual de propósito —
    operações, campos obrigatórios e a resposta `202` —, porque comparar os dois
    documentos inteiros quebraria a cada detalhe de formatação.
    """
    explicito = carregar_contrato_explicito()
    gerado = app.openapi()

    for caminho, metodo in (
        ("/elegibilidades", "post"),
        ("/elegibilidades/{protocolo}", "get"),
    ):
        assert metodo in explicito["paths"][caminho]
        assert metodo in gerado["paths"][caminho]

    campos_obrigatorios_explicito = set(
        explicito["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    campos_obrigatorios_gerado = set(
        gerado["components"]["schemas"]["PedidoElegibilidade"]["required"]
    )
    assert campos_obrigatorios_gerado == campos_obrigatorios_explicito

    aceito_explicito = explicito["paths"]["/elegibilidades"]["post"]["responses"]["202"]
    aceito_gerado = gerado["paths"]["/elegibilidades"]["post"]["responses"]["202"]
    assert aceito_gerado["description"] == aceito_explicito["description"]
    assert aceito_gerado["headers"]["Location"] == aceito_explicito["headers"]["Location"]
```

A oficina trabalha com dois contratos, cuja distinção é o assunto central do módulo.

```mermaid
flowchart TB
    H[contratos/openapi.yaml<br/>contrato explícito, escrito à mão<br/>a promessa publicada] --> SP[Spectral<br/>o documento cumpre as regras?]
    CD[models.py e main.py<br/>o código] --> GER[/openapi.json<br/>contrato gerado pelo FastAPI<br/>o que a aplicação faz hoje]
    H --> T[test_api_contract.py<br/>dois testes comparam os dois]
    GER --> T
    T --> D[divergência aparece aqui<br/>antes de aparecer no consumidor]
```

**Texto alternativo:** o contrato escrito à mão alimenta o verificador Spectral e a comparação feita pelos testes. O código gera o contrato que o FastAPI publica e a comparação entre os dois contratos revela divergências.

*Figura 12 — Contrato explícito, contrato gerado e onde a divergência é detectada. Fonte: curso.*

**Leitura textual:** à esquerda, o contrato explícito é o arquivo escrito à mão que representa a promessa publicada aos consumidores. Esse contrato alimenta os testes e o Spectral, que verifica se o documento cumpre as regras acordadas. Do outro lado, o código dos dois arquivos Python produz o contrato gerado e servido pelo FastAPI, que descreve o comportamento atual da aplicação. Os dois contratos chegam ao arquivo de testes, no qual dois dos sete testes os comparam. A figura registra que a divergência é detectada nessa etapa, antes de chegar ao consumidor, o que justifica a existência do teste.

### Leitura do contrato `openapi.yaml`

O `openapi.yaml` é o arquivo mais citado da oficina e deve ser lido antes da execução de qualquer comando. **OpenAPI** é um formato padronizado para descrever em texto as operações de uma API, o conteúdo enviado, o conteúdo devolvido e os erros possíveis. Como o formato é legível por máquinas, ferramentas geram documentação, clientes e testes a partir dele. O arquivo é escrito em **YAML**, notação em que a hierarquia se expressa por indentação, sem chaves nem colchetes.

O documento tem quatro blocos de primeiro nível e começa pelo bloco de identificação mostrado abaixo.

```yaml
openapi: 3.1.0                    # versão da especificação OpenAPI usada
info:
  title: API de elegibilidades da plataforma hospitalar
  version: 1.0.0                  # versão desta API, não da especificação
tags:
  - name: Elegibilidades          # agrupa operações na documentação
servers:
  - url: http://127.0.0.1:8000    # onde a API atende
```

O bloco contém duas versões diferentes. O campo `openapi: 3.1.0` indica a gramática que o documento segue, enquanto o campo `version: 1.0.0` dentro de `info` é a versão da própria API, que muda quando o contrato evolui.

O bloco seguinte é `paths`, que descreve cada operação. O trecho abaixo mostra o `POST` com comentários.

```yaml
paths:
  /elegibilidades:                          # o caminho
    post:                                   # o método HTTP nesse caminho
      operationId: criarElegibilidade       # nome único, usado por geradores de cliente
      summary: Aceita uma consulta de elegibilidade
      requestBody:
        required: true                      # não dá para chamar sem corpo
        content:
          application/json:                 # o formato aceito
            schema:
              $ref: '#/components/schemas/PedidoElegibilidade'
            examples:
              pedidoValido:
                value:
                  cpf: '12345678901'        # ← este exemplo será quebrado de propósito
                  codigo_operadora: OPS-001
                  matricula_plano: MAT-2026-001
```

O `$ref` é uma referência interna que evita repetir a descrição dos campos, pois aponta para `components/schemas/PedidoElegibilidade`, definido mais abaixo no documento. O mecanismo aplica ao contrato o princípio de não duplicar código.

Ainda dentro do `POST`, cada resposta possível é declarada, como mostra o trecho abaixo.

```yaml
      responses:
        '202':
          description: Pedido aceito para processamento.
          headers:
            Location:                       # o cabeçalho faz parte do contrato
              required: true
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ElegibilidadeAceita'
        '422':
          description: Corpo ausente ou incompatível com o contrato.
```

A declaração do `422` ao lado do `202` torna o erro parte da promessa. O consumidor que lê o documento sabe, antes de escrever a primeira linha de código, que precisa tratar essas duas respostas.

Por fim, o bloco `components/schemas` define os formatos de dados reaproveitados pelas operações, conforme o trecho abaixo.

```yaml
components:
  schemas:
    PedidoElegibilidade:
      type: object
      additionalProperties: false           # campo não previsto é recusado
      required: [cpf, codigo_operadora, matricula_plano]
      properties:
        cpf:
          type: string
          pattern: '^\d{11}$'               # exatamente onze dígitos
        codigo_operadora:
          type: string
          minLength: 1
          maxLength: 40
```

O trecho combina os mecanismos de validação `required`, `pattern` e `additionalProperties` do JSON Schema. A lista `required` define os campos obrigatórios e produz o `422` quando o consumidor omite o `cpf`. O `pattern` é uma expressão regular cujo valor `^\d{11}$` exige exatamente onze dígitos entre o início e o fim da cadeia de caracteres. A declaração `additionalProperties: false` recusa campos não previstos, que de outro modo seriam ignorados pela API sem nenhum aviso ao consumidor.

O `models.py` do laboratório escreve as mesmas regras em Python por meio de `Field(pattern=r"^\d{11}$")`, da lista de campos sem valor padrão e de `ConfigDict(extra="forbid")`. Os dois arquivos expressam o mesmo contrato em duas linguagens diferentes. A concordância entre eles é verificada pelos dois últimos testes da suíte, que comparam o YAML publicado com o contrato gerado pelo FastAPI.

### Os códigos de status HTTP usados aqui

Cada resposta HTTP começa por um número de três dígitos que informa, antes de qualquer conteúdo, como a requisição terminou. O primeiro dígito define a família do código, conforme a tabela abaixo.

| Família | Significado | Quem errou |
| --- | --- | --- |
| `2xx` | Deu certo | ninguém |
| `4xx` | A requisição está errada | quem chamou |
| `5xx` | O servidor falhou ao processar | quem atende |

A divisão em famílias atribui responsabilidade pelo erro. A resposta `500` para um pedido malformado transfere ao provedor a culpa por um erro do consumidor, enquanto a resposta `400` para um defeito interno transfere ao consumidor a culpa pelo erro do provedor.

A tabela abaixo apresenta os quatro códigos usados pela API e o motivo de cada escolha.

| Código | Nome | Por que este contrato o escolheu |
| --- | --- | --- |
| `200` | OK | Resposta padrão de sucesso. Aqui, o `GET` devolve `200` porque o recurso existe e está sendo entregue na hora. |
| `202` | Accepted | Indica que o pedido foi recebido e ainda será processado. O `POST` usa `202` no lugar de `200` ou `201` porque a decisão de elegibilidade depende da operadora e não sai na mesma chamada. O corpo traz um protocolo para consulta posterior. |
| `404` | Not Found | O protocolo informado não existe. É `4xx` porque quem chamou pediu algo inexistente. |
| `422` | Unprocessable Content | O corpo é JSON bem formado e viola uma regra do contrato, como a ausência do `cpf` ou um `cpf` sem onze dígitos. Difere do `400`, usado quando a requisição não pôde ser interpretada. |

A diferença entre `202` e `201` costuma gerar confusão. O código `201 Created` afirma que o recurso já existe em definitivo, enquanto `202 Accepted` afirma apenas que o pedido entrou na fila e não promete nenhum resultado.

### Leitura detalhada das duas rotas

O trecho abaixo mostra o `POST` completo, como está em `src/hospital/api/main.py`.

```python
@app.post(
    "/elegibilidades",
    response_model=ElegibilidadeAceita,          # formato da resposta de sucesso
    status_code=status.HTTP_202_ACCEPTED,        # 202, e não 200: ainda vai processar
    responses={
        202: {"headers": {"Location": {...}}},   # declara o cabeçalho no contrato
        422: {"model": ErroAPI},                 # declara o formato do erro
    },
    operation_id="criarElegibilidade",           # nome usado por geradores de cliente
    summary="Aceita uma consulta de elegibilidade",
)
def criar_elegibilidade(
    _pedido: PedidoElegibilidade, response: Response
) -> ElegibilidadeAceita:
    aceita = ElegibilidadeAceita(
        protocolo=str(uuid4()),                  # identificador único do pedido
        situacao="recebida",
        criado_em=datetime.now(timezone.utc),
    )
    _elegibilidades[aceita.protocolo] = aceita   # guarda em memória
    response.headers["Location"] = f"/elegibilidades/{aceita.protocolo}"
    return aceita
```

O trecho registra quatro decisões de implementação, descritas na lista abaixo.

- A anotação `_pedido: PedidoElegibilidade` faz o FastAPI validar o corpo recebido **antes** da execução da função. Se o CPF não tiver onze dígitos, a função não é executada.
- O `status_code` fixa o código `202` para cada resposta bem-sucedida.
- O cabeçalho `Location` é escrito à mão, com o endereço de consulta montado a partir do protocolo recém-gerado.
- O bloco `responses` existe apenas para documentação. Ele não altera o comportamento e faz o cabeçalho e o formato de erro aparecerem no contrato gerado.

O trecho abaixo mostra o `GET`.

```python
@app.get(
    "/elegibilidades/{protocolo}",               # {protocolo} vira parâmetro da função
    response_model=ElegibilidadeAceita,
    responses={404: {"model": ErroAPI}},
    operation_id="consultarElegibilidade",
)
def consultar_elegibilidade(protocolo: str):
    encontrada = _elegibilidades.get(protocolo)
    if encontrada is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "codigo": "elegibilidade_nao_encontrada",
                "mensagem": "Protocolo de elegibilidade não encontrado.",
                "detalhes": [],
            },
        )
    return encontrada
```

O trecho `{protocolo}` no caminho é um parâmetro cujo valor na URL chega à função no argumento de mesmo nome. Quando o protocolo não existe, a função monta um `404` no **mesmo formato** de erro do `422` com `codigo`, `mensagem` e `detalhes`. O formato único de erro por API permite ao consumidor escrever um único tratador para as falhas das rotas `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`.

### O erro `422` é montado num lugar só

Nenhuma das duas rotas trata erros de validação, tarefa atribuída ao interceptador registrado à parte e mostrado abaixo.

```python
@app.exception_handler(RequestValidationError)
async def tratar_erro_de_validacao(_request, error) -> JSONResponse:
    detalhes = [
        {
            "campo": ".".join(str(part) for part in item["loc"]),  # ex.: body.cpf
            "mensagem": item["msg"],
            "tipo": item["type"],
        }
        for item in error.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "codigo": "dados_invalidos",
            "mensagem": "A requisição não atende ao contrato.",
            "detalhes": detalhes,
        },
    )
```

Quando a validação do Pydantic falha em qualquer rota, o FastAPI desvia a execução para essa função. A função percorre os erros encontrados e monta a lista `detalhes`, com a localização interna do campo convertida no texto `body.cpf` exibido na resposta. A centralização garante o mesmo formato para cada falha de validação da API, sem depender da implementação de cada rota.

A preparação termina quando as condições da lista abaixo valem ao mesmo tempo. Somente depois disso a página `/docs` ou o Bruno devem ser abertos.

- Existe uma pasta `.venv` e o interpretador dela responde com a versão do Python.
- O comando `python -m pytest tests/test_api_contract.py -q` termina com os testes aprovados.
- O servidor, ao iniciar, informa que está atendendo em `http://127.0.0.1:8000`.

## Ferramenta

A tabela abaixo descreve as ferramentas usadas na oficina antes da instalação de cada uma.

| Ferramenta | O que é | Para que serve aqui |
| --- | --- | --- |
| **Python 3.11+** | A linguagem em que a API e os testes estão escritos. | Executar a aplicação e a suíte de testes. |
| **FastAPI** | Uma biblioteca Python para construir APIs. Ela lê as anotações de tipo do código e, a partir delas, valida as requisições e gera a documentação. | Implementar as duas rotas e produzir o contrato gerado em `/openapi.json`. |
| **Uvicorn** | O servidor que atende as requisições HTTP. O FastAPI define o que responder e o Uvicorn abre a porta e recebe as conexões. | Colocar a API no ar em `http://127.0.0.1:8000`. |
| **Bruno** | Um cliente HTTP com interface gráfica, parecido com Postman ou Insomnia. Permite montar e enviar requisições sem escrever código. | Agir como um consumidor externo da API. |
| **Node.js e `npx`** | Node.js é o ambiente que executa JavaScript fora do navegador. O `npx` é um utilitário distribuído com ele que baixa e executa uma ferramenta sem instalá-la permanentemente. | Executar o Spectral, que é escrito em JavaScript. |
| **Spectral CLI 6.16.1** | Um verificador de contratos OpenAPI, operado por linha de comando. Faz para o contrato o que um verificador de estilo faz para o código. | Conferir se o `openapi.yaml` cumpre as regras acordadas. |

A versão do Spectral está fixada em `6.16.1` de propósito, porque versões diferentes trazem regras diferentes e a versão fixa garante a mesma saída para a turma inteira.

As ferramentas examinam aspectos diferentes do contrato, sem que uma substitua as outras. O Bruno mostra uma execução real da API sem proteger o contrato contra regressões futuras. O Spectral analisa o documento OpenAPI sem provar que o servidor obedece a ele. O `TestClient` usado nos testes verifica o comportamento da aplicação apenas nos casos escritos pela equipe. A fidelidade do contrato à intenção do negócio continua a cargo de uma pessoa, que revisa o significado de cada campo e de cada erro descrito no OpenAPI.

## Pré-requisitos

**Objetivo**

Preparar um ambiente local descartável com Python, Bruno e Node.js. Reserve uma janela com acesso à internet para instalar dependências e para a primeira execução do `npx`, que baixa o Spectral.

**Pré-requisito**

A oficina exige um terminal, um editor de texto e a pasta `oficina-contrato` já criada com os nove arquivos da seção anterior. Os comandos são executados a partir dessa pasta.

### O que é o ambiente virtual que você vai criar

Os comandos adiante criam uma pasta `.venv`. Um **ambiente virtual** é uma instalação de Python isolada, contida numa pasta do próprio projeto. Sem ambiente virtual, cada biblioteca instalada iria para o Python do sistema e misturaria as dependências do laboratório com as de outros projetos da máquina. Nessa situação, a versão exigida por um projeto poderia impedir o funcionamento de outro.

Com o ambiente virtual, as instalações da oficina ficam dentro de `.venv` e a remoção dessa pasta desfaz a instalação por completo. Por isso a limpeza ao fim da oficina consiste em remover o diretório `.venv`.

Por consequência, os comandos chamam o interpretador de dentro da pasta, que é `.venv\Scripts\python.exe` no Windows e `python` após a ativação no macOS e no Linux. A chamada do `python` do sistema por engano executaria o laboratório sem as bibliotecas instaladas e produziria o erro `ModuleNotFoundError`.

O conteúdo da instalação está declarado em `pyproject.toml`, o arquivo que descreve o pacote do laboratório, mostrado abaixo.

```toml
dependencies = [          # necessárias para a aplicação rodar
  "fastapi",
  "uvicorn",
  "pydantic",
  ...
]

[project.optional-dependencies]
dev = [                   # necessárias apenas para desenvolver e testar
  "pytest",
  "pytest-asyncio",
  "pyyaml",
]
```

O comando de instalação usa o argumento `.[dev]`, cujas partes têm significados distintos. O caractere `.` designa o pacote que está na pasta atual e o `[dev]` acrescenta o grupo opcional com as ferramentas de teste. A opção `-e` vem de *editable* e instala o pacote como um atalho para o código-fonte, de modo que a alteração de um arquivo em `src/` vale imediatamente sem reinstalação.

## Instalação

### Windows

Abra o PowerShell e instale Python, Node.js LTS e Bruno quando ainda não estiverem disponíveis, com os comandos abaixo.

```powershell
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Bruno.Bruno
```

**Resultado esperado**

Cada instalador termina com confirmação. Feche e reabra o PowerShell para atualizar o `PATH`.

**Contingência**

Se `winget` não existir, siga as [instruções oficiais de instalação do Python](https://docs.python.org/3/using/index.html) e os instaladores indicados nas [referências](sintese-e-referencias.md#ferramentas). Se um pacote já estiver instalado, continue.

Crie o ambiente e instale o laboratório com os comandos abaixo. A ativação é opcional, porque os passos seguintes usam o interpretador explícito da `.venv`.

```powershell
cd oficina-contrato
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe --version
node --version
npx --version
```

Use exatamente `.venv\Scripts\python.exe -m pip install -e ".[dev]"` para garantir que o pacote entre no ambiente criado.

**Resultado esperado**

O Python informa a versão 3.11 ou superior, Node e npx informam suas versões e a instalação editável termina sem erro.

**Contingência**

Se `py` não encontrar o Python, reabra o terminal e tente o caminho de instalação informado pelo instalador do Windows. Se a criação parcial da `.venv` falhar, remova apenas essa pasta e repita o comando de criação do ambiente virtual. A política de execução do PowerShell não deve ser alterada de forma permanente para este laboratório.

### macOS

Instale primeiro o [Homebrew pelo site oficial](https://brew.sh/) quando ele ainda não existir e depois execute os comandos abaixo.

```bash
brew install python@3.12 node
brew install bruno
cd oficina-contrato
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
node --version
npx --version
```

**Resultado esperado**

O terminal mostra `(.venv)`, Python 3.11 ou superior e versões de Node e npx.

**Contingência**

Se o Homebrew expuser `python3` em vez de `python3.12`, use `python3 -m venv .venv`. Se Bruno já existir, apenas abra o aplicativo.

### Linux

Os comandos abaixo valem para Debian ou Ubuntu. Em outras distribuições, instale os pacotes equivalentes.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.usebruno.Bruno
flatpak info com.usebruno.Bruno
cd oficina-contrato
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python --version
node --version
npx --version
```

**Resultado esperado**

As versões aparecem no terminal e o comando `flatpak info` mostra nome, versão e origem do Bruno.

**Contingência**

Se `remote-add` falhar, execute `flatpak remotes` e confirme se `flathub` já existe, pois uma origem existente permite continuar a instalação. Se a distribuição fornecer uma versão antiga do Node, instale uma versão LTS pelas instruções oficiais do Node.js. Como alternativa ao Flatpak, o Bruno também pode ser instalado pelos [pacotes oficiais](https://www.usebruno.com/downloads) publicados no site do projeto para Linux.

## Preparação do laboratório

**Execute**

Confirme que o terminal está na pasta `oficina-contrato`, crie uma pasta para evidências e execute a suíte de testes atual.

No PowerShell:

```powershell
New-Item -ItemType Directory -Force evidencias
.venv\Scripts\python.exe -m pytest tests -q
```

Em macOS ou Linux:

```bash
mkdir -p evidencias
python -m pytest tests -q
```

**Resultado esperado**

A última linha da saída traz a contagem de testes, como no exemplo abaixo.

```text
.......                                                                  [100%]
=============================== warnings summary ===============================
.venv/lib/python3.13/site-packages/fastapi/testclient.py:1
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
7 passed, 1 warning in 0.73s
```

Cada `.` na primeira linha representa um dos sete testes aprovados. O aviso sobre `httpx` vem de dentro do FastAPI e não indica problema no laboratório. O número total pode crescer em módulos posteriores, porém neste encontro a referência são os sete testes de `test_api_contract.py`.

**Contingência**

Se `hospital.api` não for encontrado, repita a instalação editável com o interpretador da `.venv`.

**Observe**

O mesmo contrato aparece em quatro formas nesta pasta, cada uma com sua maneira de expressar a mesma regra.

Em `src/hospital/api/models.py`, as regras de validação são declaradas no tipo de cada campo da classe Pydantic. O campo `cpf` é declarado como `Field(pattern=r"^\d{11}$")`, o que exige onze dígitos sem código adicional que interprete a declaração. Os campos `codigo_operadora` e `matricula_plano` declaram limites de tamanho da mesma maneira. A configuração `model_config = ConfigDict(extra="forbid")` faz com que um campo não previsto seja recusado pela API, sem ser ignorado silenciosamente.

Em `src/hospital/api/main.py`, a rota `POST` declara `status_code=status.HTTP_202_ACCEPTED` e escreve à mão o cabeçalho `Location` com o endereço do protocolo recém-criado. O `404` da rota `GET` também aparece ali, montado no mesmo formato de erro do `422`.

Em `contratos/openapi.yaml`, as mesmas decisões estão escritas para quem consome, sem exigir a leitura de Python. O schema `PedidoElegibilidade` descreve o corpo enviado, o `ElegibilidadeAceita` descreve o corpo devolvido no `202` e o `ErroAPI` é o formato único de erro da API inteira.

Em `tests/test_api_contract.py`, cada uma dessas promessas corresponde a uma verificação executável.

**Compare**

Nenhuma das quatro formas torna as outras dispensáveis, embora seja comum tratá-las como intercambiáveis. O `openapi.yaml` é a única forma legível pelo consumidor sem acesso ao código, porém não executa nada e pode prometer um comportamento que a aplicação abandonou meses atrás. Os testes executam o contrato apenas nas amostras que a equipe escreveu. O código atende qualquer caso recebido sem registrar o motivo do limite de onze dígitos do campo `cpf`.

## O que os testes estão verificando

A suíte de testes costuma ser executada sem ser lida. Recomenda-se abrir [`tests/test_api_contract.py`](https://github.com/marco-mendes/arquitetura-software/blob/main/oficinas/modulo-2/tests/test_api_contract.py) antes de executar o pytest, porque o arquivo é a descrição executável do contrato lido em YAML na seção anterior.

Os três elementos do topo do arquivo, descritos na lista abaixo, explicam o restante.

- O `TestClient` chama a aplicação FastAPI diretamente em memória, sem abrir porta nem iniciar o Uvicorn. Por isso os testes funcionam mesmo com a porta 8000 ocupada. Um erro de conexão nos testes indica que outro cliente foi executado por engano.
- O `setup_function` é executado antes de cada teste e limpa os pedidos guardados. Como a aplicação mantém os dados em memória, sem essa limpeza um teste enxergaria os protocolos criados pelo anterior e passaria a depender da ordem de execução.
- O `PEDIDO_VALIDO` é o corpo sintético reaproveitado pelos testes, com CPF e matrícula que não existem fora deste laboratório.

Os sete testes se dividem nos dois grupos da tabela abaixo, cuja diferença é o assunto do módulo.

| Grupo | Testes | O que provam |
| --- | --- | --- |
| Comportamento da API | os cinco primeiros | Que a aplicação responde o que promete, com `202` e `Location`, recuperação pelo `GET`, `422` com corpo estruturado para campo ausente e para campo a mais, `404` no mesmo formato de erro e a distinção entre processo vivo e pronto para receber tráfego. |
| Acordo entre os dois contratos | os dois últimos | Que o `openapi.yaml` publicado e o contrato que o FastAPI gera a partir do código dizem a mesma coisa e que os exemplos declarados no YAML são aceitos pela aplicação real. |

O segundo grupo detecta o erro mais caro do módulo, que ocorre quando alguém altera o código e o contrato gerado acompanha a mudança automaticamente. Nessa situação, o documento publicado continua prometendo o formato antigo aos consumidores. Cada teste do arquivo começa com um texto que explica o que ele comprova e o motivo da verificação.

Os testes também têm limites de cobertura. Eles comparam operações, campos obrigatórios e a resposta `202` e não comparam os dois documentos inteiros, porque uma comparação total falharia a cada diferença de formatação. Descrições divergentes em outras respostas, exemplos ausentes e mudanças de significado num campo que manteve o mesmo tipo passariam sem detecção.

## As regras que o Spectral aplica

O **Spectral** é um verificador de contratos que lê um documento OpenAPI e aponta o que estiver fora das regras. Ele cumpre para o contrato o papel que um verificador de estilo cumpre para o código. As regras são definidas num arquivo de configuração, que no laboratório está dividido em dois arquivos.

O `.spectral.yaml` da raiz tem apenas duas linhas úteis, que apontam para o arquivo dentro de `contratos/`. A indireção permite executar os comandos a partir da raiz do laboratório e manter a configuração ao lado do contrato que ela governa.

O `contratos/.spectral.yaml`, mostrado abaixo, contém as decisões de regra.

```yaml
extends: spectral:oas

rules:
  operation-operationId: error
  operation-description: error
  operation-tags: error
```

A primeira linha herda o conjunto de regras que o próprio Spectral distribui para OpenAPI, chamado `spectral:oas`. O conjunto reúne dezenas de verificações prontas, entre elas a regra `oas3-valid-media-example`, que aparecerá mais adiante quando um exemplo for quebrado de propósito.

O bloco `rules` acrescenta três exigências e as marca com a severidade `error`. Essa severidade faz o comando terminar com código diferente de zero, o que reprova uma esteira de integração contínua, enquanto um aviso apenas imprime texto e não interrompe a esteira.

Cada uma das três exigências atende a um interessado concreto. O `operationId` é um identificador único da operação que os geradores de cliente usam para nomear o método criado, que sem ele recebe um nome automático e ilegível. A descrição atende quem lê a documentação para decidir se a operação serve à sua necessidade. As *tags* agrupam operações, o que faz diferença quando a API cresce e a página de documentação precisa de navegação.

O Spectral **não** julga significado. Ele verifica a existência de uma descrição sem avaliar se ela descreve a operação corretamente, de modo que um `POST /elegibilidades` descrito como "remove um beneficiário" passa na verificação. A conferência da fidelidade do contrato à intenção continua a cargo de uma pessoa revisora, razão pela qual a revisão de contrato não é automatizável por completo.

## Execução

Os blocos a seguir iniciam a API e observam o contrato pela documentação que o próprio FastAPI gera, por um cliente HTTP externo e pelos testes automatizados. Cada um desses três ângulos revela um aspecto que os outros dois não revelam.

**Execute**

Inicie a API em um terminal dedicado. No PowerShell, use o comando abaixo.

```powershell
.venv\Scripts\python.exe -m uvicorn hospital.api.main:app --reload
```

Em macOS ou Linux:

```bash
python -m uvicorn hospital.api.main:app --reload
```

**Resultado esperado**

O terminal fica ocupado pelo servidor e mostra a saída abaixo.

```text
INFO:     Will watch for changes in these directories: ['.../oficina-contrato']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [41287] using StatReload
INFO:     Started server process [41289]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

A linha `Application startup complete` confirma que a API está em execução. O terminal não volta ao *prompt* porque continua atendendo requisições, comportamento esperado do servidor. Deixe essa janela aberta e use outra para os comandos seguintes, pois cada chamada feita à API aparecerá nesta janela como uma linha de *log*.

**Contingência**

Se a porta 8000 estiver ocupada, encerre o processo antigo que a ocupa antes de iniciar o servidor do laboratório. O uso de outra porta exige também a alteração da URL base configurada no Bruno. Um conflito local de porta não justifica nenhuma edição no arquivo OpenAPI do contrato principal.

Abra `http://127.0.0.1:8000/docs`. Expanda `POST /elegibilidades`, use **Try it out**, mantenha o exemplo e execute.

**Resultado esperado**

A documentação mostra o status `202`, o corpo com protocolo e o cabeçalho `location`. Copie o protocolo para a evidência.

**Observe**

A página `/docs` não foi escrita manualmente. O FastAPI a monta em tempo de execução a partir dos modelos Pydantic e das assinaturas das rotas, razão pela qual ela acompanha o código. Essa página exibe o **contrato gerado**, que descreve o comportamento atual da aplicação. O contrato gerado coexiste com o `openapi.yaml` escrito à mão, que é a promessa publicada. Os dois contratos podem divergir e os dois últimos testes da suíte existem para detectar essa divergência.

**Contingência**

Se `/docs` não abrir, acesse `http://127.0.0.1:8000/openapi.json` no navegador para verificar se a aplicação responde. Quando o JSON abre, basta recarregar a página `/docs` no navegador. Quando o JSON também não abre, a aplicação não está atendendo na porta 8000 e precisa ser iniciada de novo pelo Uvicorn.

Abra o Bruno e escolha a opção de importar uma coleção a partir de um documento OpenAPI. Selecione o arquivo `contratos/openapi.yaml`, escolha uma pasta dentro de `evidencias/bruno` e confirme a importação da coleção. Quando o importador não definir a URL base da coleção, defina esse valor manualmente como `http://127.0.0.1:8000` nas configurações do Bruno.

**Resultado esperado**

Bruno cria requisições para `POST /elegibilidades` e `GET /elegibilidades/{protocolo}`.

**Observe**

A importação mostra por que o contrato existe em formato legível por máquina. O Bruno não tinha acesso ao código da API e montou as duas requisições com os campos corretos apenas a partir do `openapi.yaml`. Um consumidor real usa o mesmo documento para gerar clientes em outra linguagem de programação. Uma documentação escrita apenas como texto para leitura humana não permite essa geração automática pelo Bruno ou por outras ferramentas.

**Contingência**

Se a interface não localizar o importador, consulte a opção **Import Collection** e escolha **OpenAPI**.

No Bruno, envie o `POST` com:

```json
{
  "cpf": "12345678901",
  "codigo_operadora": "OPS-001",
  "matricula_plano": "MAT-2026-001"
}
```

**Resultado esperado**

A resposta completa, com cabeçalhos e corpo:

```text
HTTP/1.1 202 Accepted
server: uvicorn
content-type: application/json
location: /elegibilidades/3d1bbeb6-92a7-4aab-a7ec-62df7296a580

{"protocolo":"3d1bbeb6-92a7-4aab-a7ec-62df7296a580","situacao":"recebida","criado_em":"2026-09-01T00:26:22.639666Z"}
```

O identificador será diferente no seu computador, porque a API gera um protocolo novo a cada pedido. O valor depois de `location:` é o mesmo `protocolo` do corpo, montado como caminho. Copie o protocolo para o parâmetro do `GET` e envie a consulta, que devolve `200 OK` com exatamente o mesmo corpo da resposta ao `POST`.

**Observe**

O `202` comunica apenas que o pedido foi recebido e ainda será processado. Por isso a resposta não traz o resultado da elegibilidade, somente um protocolo e o endereço de consulta. O cabeçalho `Location` entrega esse endereço pronto, o que dispensa o consumidor de montar a URL por convenção e permite ao provedor mudar o formato da URL sem afetar os consumidores.

**Compare**

Compare com o que aconteceria num `200` que devolvesse a decisão na hora. O `202` permite ao provedor processar o pedido depois e exige do consumidor uma segunda chamada. É a mesma escolha de [interface, contrato e implementação](conceitos.md) sendo exercida no nível do código de status.

**Contingência**

Se o `GET` retornar `404`, confirme que a consulta usa a mesma instância do servidor e que o protocolo não contém aspas ou espaços. A reinicialização do Uvicorn apaga a memória do processo, situação em que é preciso criar um novo pedido com `POST /elegibilidades`.

Remova `cpf` do corpo e envie outro `POST`.

**Resultado esperado**

A resposta é `422 Unprocessable Entity`, com o corpo abaixo, que detalha o motivo da recusa.

```json
{
  "codigo": "dados_invalidos",
  "mensagem": "A requisição não atende ao contrato.",
  "detalhes": [
    {
      "campo": "body.cpf",
      "mensagem": "Field required",
      "tipo": "missing"
    }
  ]
}
```

O campo `detalhes` aponta exatamente onde está o problema: `body.cpf`, ausente. Um cliente consegue tratar isso programaticamente, destacando o campo no formulário do usuário.

**Observe**

O corpo do erro tem formato previsível com os campos `codigo` e `mensagem` e a lista `detalhes`, que aponta o campo problemático. O consumidor trata a falha por programa a partir desses campos, sem exibir texto solto ao usuário final. Por isso o formato do erro faz parte do contrato da API, com a mesma importância das respostas `202` e `200`.

**Compare**

A comparação entre o `422` e o `500` mostra a diferença de responsabilidade entre as duas respostas. O `422` informa que o pedido do consumidor está errado e indica o campo com problema. O `500` informa uma falha interna do servidor da API. A troca de um pelo outro atribui ao consumidor um defeito do provedor, ou atribui ao provedor um erro do consumidor.

**Contingência**

Se receber `202`, confirme que o campo foi removido do corpo efetivamente enviado e não apenas de um exemplo exibido.

Valide o contrato. No PowerShell:

```powershell
npx @stoplight/spectral-cli@6.16.1 lint contratos/openapi.yaml 2>&1 | Tee-Object -FilePath evidencias\spectral-valido.txt
$spectralExit = $LASTEXITCODE
if ($spectralExit -ne 0) { exit $spectralExit }
```

Em macOS ou Linux:

```bash
set -o pipefail
npx @stoplight/spectral-cli@6.16.1 lint contratos/openapi.yaml 2>&1 | tee evidencias/spectral-valido.txt
```

**Resultado esperado**

A saída esperada é uma única linha:

```text
No results with a severity of 'error' found!
```

O comando também termina com código de saída zero, que é o que uma esteira de integração contínua verifica. Na primeira execução o `npx` baixa a versão `6.16.1` e demora mais.

**Contingência**

Se o comando `npx` não for reconhecido no terminal, retorne à instalação do Node.js descrita na seção de instalação. Se houver erro de rede, repita o comando quando a conexão com a internet estiver disponível. A ausência de execução do Spectral não deve ser interpretada como sinal de que o contrato OpenAPI é válido.

Execute somente os testes de contrato e capture o resultado. No PowerShell:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_api_contract.py -q 2>&1 | Tee-Object -FilePath evidencias\testes-contrato.txt
$pytestExit = $LASTEXITCODE
if ($pytestExit -ne 0) { exit $pytestExit }
```

Em macOS ou Linux:

```bash
set -o pipefail
python -m pytest tests/test_api_contract.py -q 2>&1 | tee evidencias/testes-contrato.txt
```

**Resultado esperado**

O resumo mostra `7 passed`.

**Observe**

Os sete testes têm finalidades diferentes. Cinco deles chamam a API pelos endereços públicos e conferem status, corpo e cabeçalho da resposta. Os dois últimos comparam o `openapi.yaml` publicado com o contrato que o FastAPI gera a partir do código. A comparação detecta o caso em que o código muda e o contrato gerado acompanha a mudança enquanto o documento publicado continua a prometer o formato antigo.

**Compare**

Cada ferramenta desta oficina examina uma parte limitada do contrato da API de elegibilidades. O Spectral examina o documento OpenAPI sem verificar se a aplicação o obedece durante a execução. O Bruno mostra uma execução real da API sem proteger o contrato contra regressões em versões futuras. Os testes verificam o comportamento da aplicação apenas nos casos que a equipe escreveu na suíte. A revisão humana da semântica do contrato continua necessária com qualquer combinação das três ferramentas.

**Contingência**

Leia primeiro a mensagem do teste que falhou antes das demais falhas da suíte. Um erro de conexão indica que outro cliente HTTP foi executado no lugar do `TestClient`, que não depende do Uvicorn em execução. Um erro de exemplo indica uma possível divergência entre o YAML do contrato e o comportamento da aplicação FastAPI.

## Uma falha deliberada no contrato

Até aqui tudo passou. Um contrato só se mostra útil quando alguém quebra e o mecanismo acusa, então este bloco introduz um erro de propósito e observa quem o detecta.

**Execute**

Copie o contrato antes de mexer nele, para preservar intacta a versão de referência. No PowerShell:

```powershell
Copy-Item contratos\openapi.yaml evidencias\openapi-experimento.yaml
```

Em macOS ou Linux:

```bash
cp contratos/openapi.yaml evidencias/openapi-experimento.yaml
```

**Resultado esperado**

O arquivo de experimento aparece em `evidencias`.

**Contingência**

Se o destino não existir, volte à preparação e crie a pasta `evidencias`.

No arquivo copiado, altere somente o valor do campo `cpf` de `12345678901` para `123` no exemplo de mídia da requisição de criação. O caminho YAML completo desse valor dentro do documento é `paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf`. A anotação `examples` do schema em `components` não deve ser alterada nesta etapa do experimento com o Spectral.

Valide a cópia no PowerShell e confirme que a falha realmente ocorreu:

```powershell
npx @stoplight/spectral-cli@6.16.1 lint evidencias\openapi-experimento.yaml
$spectralExit = $LASTEXITCODE
if ($spectralExit -eq 0) { throw "O exemplo inválido não foi detectado." }
$spectralExit
```

Em macOS ou Linux:

```bash
set +e
npx @stoplight/spectral-cli@6.16.1 lint evidencias/openapi-experimento.yaml
spectral_exit=$?
set -e
test "$spectral_exit" -ne 0
printf 'Código esperado: %s\n' "$spectral_exit"
```

**Resultado esperado**

Desta vez o Spectral acusa o erro e a saída aponta o lugar exato:

```text
/caminho/para/evidencias/openapi-experimento.yaml
 35:24  error  oas3-valid-media-example  "cpf" property must match pattern "^\d{11}$"  paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf

✖ 1 problem (1 error, 0 warnings, 0 infos, 0 hints)
```

A saída do Spectral pode ser lida em partes, da esquerda para a direita de cada linha impressa. O par `35:24` indica a linha e a coluna do erro dentro do arquivo YAML do contrato. O identificador `oas3-valid-media-example` é o nome da regra violada, herdada do conjunto `spectral:oas`. A mensagem descreve a restrição violada, enquanto o caminho no final localiza o campo dentro da estrutura do documento. O comando termina com código de saída `1`, valor que reprovaria uma esteira de integração contínua. Essa falha deliberada é a evidência que deve ser guardada na pasta `evidencias`.

**Contingência**

Se o Spectral não apontar nenhuma falha, confirme que a alteração foi feita no caminho `paths./elegibilidades.post.requestBody.content.application/json.examples.pedidoValido.value.cpf`. Preserve as aspas em `'123'` e verifique se o arquivo `.spectral.yaml` está na raiz do laboratório. Alterar `components.schemas.PedidoElegibilidade.examples` não exercita a regra de exemplo de mídia. No servidor, um `cpf` igual a `123` também deve produzir a resposta `422` com o corpo de erro padronizado da API.

**Observe**

O erro foi detectado sem que a API fosse chamada. O Spectral leu apenas o documento e percebeu que o exemplo publicado viola o padrão declarado pelo próprio contrato. Um exemplo desatualizado é pior que exemplo nenhum, porque quem consome copia e não funciona.

**Compare**

O `cpf` inválido pode ser recusado em dois momentos diferentes do ciclo de desenvolvimento da API. O Spectral recusa o valor na leitura do documento OpenAPI, antes de qualquer execução do servidor. O servidor FastAPI recusa o mesmo valor durante a chamada, com a resposta `422`. As duas verificações atuam em camadas diferentes, sendo a primeira mais barata porque acontece antes da execução do código.

Mantenha a cópia como evidência da falha deliberada e não substitua `contratos/openapi.yaml`.

## Extensão com gateway de API Ocelot em .NET

Esta extensão é independente das etapas anteriores e não altera a API de elegibilidades. Ela demonstra o padrão de **gateway de API** com o [Ocelot](https://ocelot.readthedocs.io/), um gateway leve para .NET configurado por um arquivo JSON declarativo. Um processo na porta 4000 passa a ser a única entrada para duas APIs internas nas portas 5001 e 5002 e reescreve os caminhos públicos `/api/...` para os serviços de destino.

**Objetivo**

O objetivo é observar um gateway que roteia requisições por configuração declarativa, sem lógica de negócio própria. O consumidor enxerga uma única origem, de modo que a topologia interna pode mudar sem afetar os consumidores da API.

**Pré-requisito**

O laboratório exige o SDK do .NET 8 ou superior, verificado com `dotnet --version`. A instalação usa `winget install Microsoft.DotNet.SDK.8` no Windows, `brew install --cask dotnet-sdk` no macOS ou os [pacotes oficiais do .NET](https://dotnet.microsoft.com/download) no Linux. Reserve três terminais e as portas 4000, 5001 e 5002 do computador. Crie os projetos numa pasta de trabalho fora do clone da disciplina, separada do laboratório da API de elegibilidades.

**Execute**

Crie os três projetos e adicione o pacote do Ocelot ao gateway. Os comandos do `dotnet` são idênticos no PowerShell, no macOS e no Linux e devem ser executados na pasta de trabalho.

```bash
dotnet new web -n ClienteService
dotnet new web -n ProdutoService
dotnet new web -n OcelotGateway
dotnet add OcelotGateway package Ocelot
```

Substitua o `Program.cs` do `ClienteService`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/clientes", () => new[] {
    new { Id = 1, Nome = "João Silva" },
    new { Id = 2, Nome = "Maria Oliveira" }
});

app.Run();
```

Substitua o `Program.cs` do `ProdutoService`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/produtos", () => new[] {
    new { Id = 1, Nome = "Produto A" },
    new { Id = 2, Nome = "Produto B" }
});

app.Run();
```

No `OcelotGateway`, substitua o `Program.cs` e crie um arquivo `ocelot.json` na raiz do projeto:

```csharp
using Ocelot.DependencyInjection;
using Ocelot.Middleware;

var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("ocelot.json", optional: false, reloadOnChange: true);
builder.Services.AddOcelot(builder.Configuration);

var app = builder.Build();

await app.UseOcelot();

app.Run();
```

```json
{
  "Routes": [
    {
      "DownstreamPathTemplate": "/clientes",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "localhost", "Port": 5001 }],
      "UpstreamPathTemplate": "/api/clientes"
    },
    {
      "DownstreamPathTemplate": "/produtos",
      "DownstreamScheme": "http",
      "DownstreamHostAndPorts": [{ "Host": "localhost", "Port": 5002 }],
      "UpstreamPathTemplate": "/api/produtos"
    }
  ],
  "GlobalConfiguration": {
    "BaseUrl": "http://localhost:4000"
  }
}
```

Dois termos do Ocelot precisam de definição antes da leitura do arquivo. **Upstream** é o lado de quem chega, isto é, o caminho público que o consumidor enxerga. **Downstream** é o lado de quem atende, isto é, o serviço interno para onde a requisição será encaminhada. Os dois termos vêm do inglês e significam rio acima e rio abaixo, em referência ao sentido em que a requisição percorre o gateway até o serviço.

Cada rota declara um par de endereços. O `UpstreamPathTemplate` é o endereço público `/api/clientes`, enquanto o `DownstreamPathTemplate` com o host e a porta forma o destino interno `localhost:5001/clientes`. O consumidor conhece apenas a porta 4000 do gateway e nunca a porta 5001. Por isso o serviço pode ser movido para outra máquina com a alteração exclusiva do arquivo `ocelot.json`.

O bloco `GlobalConfiguration` define o endereço do próprio gateway. Para repassar subcaminhos inteiros, o Ocelot aceita o coringa `{everything}` nos dois modelos, como em `/api/clientes/{everything}` para `/clientes/{everything}`.

Inicie cada processo no próprio terminal, sempre a partir da pasta de trabalho:

```bash
dotnet run --project ClienteService --urls=http://localhost:5001
dotnet run --project ProdutoService --urls=http://localhost:5002
dotnet run --project OcelotGateway --urls=http://localhost:4000
```

Com os três processos ativos, consulte os serviços pelo gateway. No PowerShell:

```powershell
Invoke-RestMethod http://localhost:4000/api/clientes
Invoke-RestMethod http://localhost:4000/api/produtos
```

Em macOS ou Linux:

```bash
curl -s http://localhost:4000/api/clientes
curl -s http://localhost:4000/api/produtos
```

**Resultado esperado**

O gateway responde `200 OK` com o JSON dos serviços internos, que traz os clientes João Silva e Maria Oliveira e os produtos Produto A e Produto B, sem que o consumidor conheça as portas 5001 e 5002. A consulta direta a `http://localhost:5001/clientes` devolve o mesmo corpo, porque o gateway apenas roteou a requisição sem transformar a resposta.

**Contingência**

Se o comando `dotnet` não for reconhecido, reabra o terminal após instalar o SDK do .NET. Se uma porta estiver ocupada, encerre o processo antigo ou ajuste a porta no `--urls` e no `ocelot.json` ao mesmo tempo. Se o gateway responder `404`, confirme que `ocelot.json` está na raiz do projeto `OcelotGateway` e que o caminho requisitado coincide com `UpstreamPathTemplate`. Se a restauração de pacotes falhar por erro de rede, repita o comando `dotnet add OcelotGateway package Ocelot` quando a conexão com a internet estiver disponível.

**Observe**

O gateway não tem lógica de negócio, porque as rotas existem apenas como dados de configuração. O versionamento do `ocelot.json` documenta a topologia da borda da mesma forma que o `openapi.yaml` documenta o contrato de cada serviço.

**Compare**

A extensão mostra na prática a restrição REST de sistema em camadas, em que o consumidor não sabe se fala com o serviço final ou com um intermediário. O contrato OpenAPI protege a fronteira de um serviço, enquanto o gateway organiza a fronteira do conjunto de serviços. Ao terminar a extensão, encerre os três processos do .NET com `Ctrl+C` em cada um dos três terminais abertos.

## Resultado esperado

Ao final da oficina, as respostas e os resultados listados abaixo terão sido observados no laboratório.

- `202` com `Location` na criação da elegibilidade e recuperação do recurso por `GET`.
- Erro `422` com o corpo de erro padronizado.
- Lint aprovado e lint deliberadamente reprovado pelo Spectral.
- Sete testes de contrato aprovados.

A oficina também permite identificar qual ferramenta examina o documento, qual examina a implementação e qual examina a experiência do consumidor. Quem fez a extensão terá visto ainda um gateway de API que roteia duas APIs por configuração declarativa no Ocelot.

## Interpretação

O experimento demonstra que exemplos de contrato podem ser executáveis, que erros fazem parte do contrato e que a semântica HTTP comunica estado temporal. Ele não demonstra persistência, segurança, escalabilidade ou integração com sistemas externos como a operadora do plano de saúde. A reinicialização do servidor Uvicorn comprova o limite do armazenamento em memória, porque apaga todos os protocolos criados até aquele momento.

## Limpeza e contingência

**Execute**

No terminal do Uvicorn, pressione `Ctrl+C` para encerrar o servidor e depois feche o Bruno. Os artefatos descartáveis podem ser removidos da pasta de trabalho, desde que não façam parte das evidências exigidas na seção Evidência a entregar.

No PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
```

Em macOS ou Linux:

```bash
rm -rf .venv
```

**Resultado esperado**

O servidor para e o ambiente local é removido. `contratos`, `src` e `tests` permanecem.

**Contingência**

Se algum arquivo estiver em uso no Windows, feche terminais e editor ligados à `.venv` antes de repetir. Nunca remova a pasta do laboratório inteira para limpar o ambiente.

## Evidência a entregar

A entrega reúne os itens listados abaixo.

- Os arquivos `spectral-valido.txt` e `testes-contrato.txt`.
- A coleção Bruno importada.
- As respostas de `POST`, `GET` e `422`.
- Uma nota curta que compare o contrato explícito, o contrato gerado e a execução.

Inclua a falha deliberada sem apresentá-la como defeito pendente. Se fizer a extensão do Ocelot, acrescente a saída das duas consultas feitas pelo gateway e o arquivo `ocelot.json` usado na configuração.

## Questões exploratórias

1. O que `202` permite ao provedor mudar sem quebrar o consumidor?
2. Por que `Location` é melhor que pedir ao consumidor para montar uma URL por convenção?
3. Qual divergência entre OpenAPI e aplicação os testes atuais ainda não detectam?
4. Quando uma chave de idempotência passaria a ser necessária?
5. Que parte do experimento deixaria de funcionar com duas instâncias e memória separada?
