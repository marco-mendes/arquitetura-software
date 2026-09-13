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
