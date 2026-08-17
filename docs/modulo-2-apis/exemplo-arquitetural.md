# Exemplo arquitetural: aceitar uma elegibilidade

## O que este exemplo mostra

A equipe administrativa precisa consultar a elegibilidade de um paciente no plano de saúde. A operadora externa é lenta e nem sempre está disponível. Neste incremento a API ainda **não** fala com a operadora: ela só **recebe** o pedido, guarda um protocolo e deixa consultar o estado depois. É o menor passo possível que já exercita um contrato HTTP.

## A sequência completa

```mermaid
sequenceDiagram
    actor Consumidor
    participant API as API de elegibilidades
    participant Memoria as Armazenamento em memória
    Consumidor->>API: POST /elegibilidades + PedidoElegibilidade
    API->>API: valida corpo contra o schema
    API->>Memoria: guarda protocolo e estado recebida
    Memoria-->>API: registro efêmero confirmado
    API-->>Consumidor: 202 + Location + ElegibilidadeAceita
    Consumidor->>API: GET /elegibilidades/{protocolo}
    API->>Memoria: procura protocolo
    Memoria-->>API: estado recebida
    API-->>Consumidor: 200 + ElegibilidadeAceita
```

**Texto alternativo:** o consumidor envia `POST`; a API valida, guarda protocolo `recebida` em memória e responde `202` com `Location`. Um `GET` devolve `200` com a representação aceita.

*Figura 5 — Sequência de aceitação e consulta de uma elegibilidade armazenada em memória. Fonte: curso.*

**Leitura textual:** o consumidor envia pedido; a API valida, guarda estado efêmero e responde `202` com endereço de consulta. O uso do endereço devolve `200` e a representação aceita.

`recebida` não quer dizer "aprovada": significa apenas que a plataforma aceitou o pedido.

O código a seguir está dividido em quatro passos, escrito em **FastAPI** (um framework Python para construir APIs HTTP) com **Pydantic** (uma biblioteca que usa o tipo declarado em cada campo para validar os dados automaticamente). Os trechos abaixo são esqueletos, só para mostrar a forma; o código completo está no laboratório, em `src/hospital/api/`.

## Passo 1 — O contrato vira classes

O consumidor envia três campos:

```json
{
  "cpf": "12345678901",
  "codigo_operadora": "OPS-001",
  "matricula_plano": "MAT-2026-001"
}
```

Em `models.py`, esse contrato vira classes Pydantic. O tipo de cada campo já funciona como regra de validação: se o corpo da requisição não bater com o tipo esperado, o FastAPI recusa o pedido antes mesmo de a sua lógica rodar.

```python
# models.py
from datetime import datetime
from pydantic import BaseModel, Field

class PedidoElegibilidade(BaseModel):         # o que o consumidor envia
    cpf: str = Field(pattern=r"^\d{11}$")     # 11 dígitos, sintético
    codigo_operadora: str
    matricula_plano: str

class ElegibilidadeAceita(BaseModel):         # o que a API devolve
    protocolo: str
    situacao: str                             # neste incremento, sempre "recebida"
    criado_em: datetime
```

O `cpf` aqui é só um identificador sintético de onze dígitos — nenhuma validação cadastral real é afirmada. O contrato não expõe XML, tabela nem código interno da operadora: `codigo_operadora` e `matricula_plano` já estão na linguagem da plataforma.

## Passo 2 — A rota que aceita e guarda

A rota `POST /elegibilidades` recebe o pedido já validado (pelo tipo `PedidoElegibilidade`), cria um protocolo, guarda em memória e responde `202 Accepted` com o cabeçalho `Location` apontando onde consultar.

```python
# main.py
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import FastAPI, Response, status

app = FastAPI(title="API de elegibilidades da plataforma hospitalar")
_elegibilidades: dict[str, ElegibilidadeAceita] = {}   # memória: some ao reiniciar

@app.post("/elegibilidades", status_code=status.HTTP_202_ACCEPTED)
def criar_elegibilidade(pedido: PedidoElegibilidade, response: Response) -> ElegibilidadeAceita:
    aceita = ElegibilidadeAceita(
        protocolo=str(uuid4()),
        situacao="recebida",
        criado_em=datetime.now(timezone.utc),
    )
    _elegibilidades[aceita.protocolo] = aceita
    response.headers["Location"] = f"/elegibilidades/{aceita.protocolo}"
    return aceita
```

É isto que o consumidor observa:

```http
HTTP/1.1 202 Accepted
Location: /elegibilidades/550e8400-e29b-41d4-a716-446655440000
```

```json
{
  "protocolo": "550e8400-e29b-41d4-a716-446655440000",
  "situacao": "recebida",
  "criado_em": "2026-07-17T13:30:00Z"
}
```

O código usa `202` — não `200` nem `201` — porque a API só aceitou o pedido; ela ainda não decidiu nada. Guardar os dados num dicionário em memória é uma decisão simples de implementação: funciona enquanto o processo está rodando, mas tudo se perde se ele reiniciar. Esse limite precisa ficar declarado para quem consome a API.

## Passo 3 — A rota que recupera

`GET /elegibilidades/{protocolo}` devolve a mesma representação enquanto o processo está de pé. Protocolo desconhecido vira `404`.

```python
from fastapi.responses import JSONResponse

@app.get("/elegibilidades/{protocolo}")
def consultar_elegibilidade(protocolo: str):
    encontrada = _elegibilidades.get(protocolo)
    if encontrada is None:                                  # protocolo inexistente
        return JSONResponse(status_code=404, content={
            "codigo": "elegibilidade_nao_encontrada",
            "mensagem": "Protocolo de elegibilidade não encontrado.",
            "detalhes": [],
        })
    return encontrada
```

## Passo 4 — O caminho de erro

Quando falta `cpf`, o Pydantic detecta a violação antes de a rota rodar. Um tratador transforma o erro técnico na representação pública `ErroAPI` — `codigo` para automação, `mensagem` e `detalhes` para pessoas.

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def tratar_erro_de_validacao(_request, error) -> JSONResponse:
    detalhes = [
        {"campo": ".".join(map(str, e["loc"])), "mensagem": e["msg"], "tipo": e["type"]}
        for e in error.errors()
    ]
    return JSONResponse(status_code=422, content={
        "codigo": "dados_invalidos",
        "mensagem": "A requisição não atende ao contrato.",
        "detalhes": detalhes,
    })
```

O corpo do erro que o consumidor recebe:

```json
{
  "codigo": "dados_invalidos",
  "mensagem": "A requisição não atende ao contrato.",
  "detalhes": [
    { "campo": "body.cpf", "mensagem": "Field required", "tipo": "missing" }
  ]
}
```

`422 Unprocessable Entity` é o status para um corpo que chegou, mas não cumpre o contrato.

## O contrato explícito e o contrato gerado

Existem duas descrições da mesma API. O arquivo `contratos/openapi.yaml` é o contrato **explícito**: alguém escreveu esse arquivo à mão. O FastAPI também **gera** sozinho um `/openapi.json`, a partir do código. Os testes comparam os dois — operações, campos, exemplos — e conseguem pegar divergências pontuais, mas não garantem que os dois documentos sejam idênticos em tudo.

Esses testes usam `TestClient(app)`, uma ferramenta que simula requisições HTTP dentro do próprio processo de teste, sem precisar ligar um servidor separado. Assim dá para checar status, cabeçalho e formato da resposta rapidamente.

## Gateway e adaptador de operadora

O laboratório roda apenas uma FastAPI, em `http://127.0.0.1:8000`, sem gateway. Mas quando a plataforma cresce e ganha várias capacidades, a porta de entrada (borda pública) e a integração com sistemas externos passam a ter responsabilidades diferentes:

```mermaid
flowchart LR
    A[Sistema administrativo] --> G[Gateway de borda\nrota, autenticação técnica, limite, correlação]
    G --> E[API de elegibilidade\ncontrato da plataforma]
    E --> T[Adaptador de operadora\ntradução de vocabulário e protocolo]
    T --> O[Operadora externa]
    E --> M[(estado do pedido)]
```

**Texto alternativo:** o sistema administrativo chama o gateway, que encaminha à API; ela mantém o estado e usa adaptador para chamar a operadora.

*Figura 6 — Uma evolução possível: políticas técnicas na borda, tradução no adaptador e estado na plataforma. Fonte: curso.*

**Leitura textual:** gateway aplica políticas; adaptador traduz vocabulário e protocolo da operadora; o estado pertence à API — uma hipótese de evolução, sem componente correspondente no laboratório.

O gateway pode autenticar, limitar tráfego e rotear as chamadas. O que ele **não** deve fazer é traduzir `beneficiaryKey` da operadora para `matricula_plano`, nem decidir que um estado desconhecido significa `negada`. Essas traduções são responsabilidade do **adaptador**, onde podem ser testadas e observadas de forma isolada. Assim, o formato SOAP/XML da operadora e suas regras específicas não vazam para o resto da plataforma.

## Equivalências em Java e .NET

Em **Spring Boot**, `@RestController`, `ResponseEntity.accepted()`, Springdoc e MockMvc cumprem os mesmos papéis. Em **ASP.NET Core**, `MapPost`/`MapGet`, `Results.Accepted()`, OpenAPI e `WebApplicationFactory` fazem o mesmo. Python, Java e C# variam no *como*; a decisão preserva recurso, HTTP, schema, erro e evidência.
