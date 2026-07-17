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
