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
