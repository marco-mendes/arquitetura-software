import os

from fastapi import FastAPI, HTTPException, status
import psycopg

from hospital.telemetria import instrumentar_app


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://elegibilidade:elegibilidade@localhost:5433/elegibilidade",
)

app = FastAPI(title="Serviço de elegibilidade", version="1.0.0")
instrumentar_app(app, "elegibilidade")


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
