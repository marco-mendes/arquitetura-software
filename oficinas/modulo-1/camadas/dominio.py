"""Camada de domínio: as regras do negócio, sem saber que HTTP existe."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Horario:
    inicio: str
    fim: str

    def conflita_com(self, outro: "Horario") -> bool:
        return self.inicio < outro.fim and outro.inicio < self.fim

    def __str__(self) -> str:
        return f"{self.inicio}–{self.fim}"


@dataclass
class Consulta:
    id: int
    medico: str
    paciente: str
    horario: Horario
    status: str = "agendada"

    def realizar(self) -> None:
        self.status = "realizada"

    def cancelar(self) -> None:
        self.status = "cancelada"


class ConflitoDeAgenda(Exception):
    """Regra de domínio violada. Quem traduz isto para HTTP é a apresentação."""
