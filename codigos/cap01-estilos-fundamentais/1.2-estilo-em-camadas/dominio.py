"""
Camada de Domínio — Sistema de Agendamento de Clínica
Contém: Value Objects (CPF, Horario), Entidades (Medico, Paciente, Consulta),
        Interfaces de Repositório (ABC)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# --- Value Objects ---

@dataclass(frozen=True)
class CPF:
    valor: str

    def __post_init__(self):
        digitos = "".join(c for c in self.valor if c.isdigit())
        if len(digitos) != 11:
            raise ValueError(f"CPF inválido: {self.valor!r}")

    def __str__(self) -> str:
        d = "".join(c for c in self.valor if c.isdigit())
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"


@dataclass(frozen=True)
class Horario:
    inicio: datetime
    fim: datetime

    def __post_init__(self):
        if self.fim <= self.inicio:
            raise ValueError("Horário de fim deve ser posterior ao de início.")

    def conflita_com(self, outro: Horario) -> bool:
        """Retorna True se os dois horários se sobrepõem."""
        return self.inicio < outro.fim and self.fim > outro.inicio

    def __str__(self) -> str:
        return f"{self.inicio.strftime('%H:%M')}–{self.fim.strftime('%H:%M')}"


# --- Entidades ---

@dataclass
class Medico:
    id: int
    nome: str
    crm: str
    especialidade: str


@dataclass
class Paciente:
    id: int
    nome: str
    cpf: CPF
    telefone: str


@dataclass
class Consulta:
    id: int
    medico: Medico
    paciente: Paciente
    horario: Horario
    status: str = "agendada"   # agendada | realizada | cancelada
    observacoes: str = ""

    def cancelar(self) -> None:
        if self.status != "agendada":
            raise ValueError(
                f"Impossível cancelar consulta com status '{self.status}'."
            )
        self.status = "cancelada"

    def realizar(self, observacoes: str = "") -> None:
        if self.status != "agendada":
            raise ValueError(
                f"Impossível realizar consulta com status '{self.status}'."
            )
        self.status = "realizada"
        self.observacoes = observacoes


# --- Interfaces de Repositório (contrato da camada de dados) ---

class RepositorioConsulta(ABC):
    @abstractmethod
    def salvar(self, consulta: Consulta) -> None: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Consulta]: ...

    @abstractmethod
    def listar_por_medico(self, medico_id: int, data: datetime) -> list[Consulta]: ...

    @abstractmethod
    def listar_por_paciente(self, paciente_id: int) -> list[Consulta]: ...


class RepositorioPaciente(ABC):
    @abstractmethod
    def salvar(self, paciente: Paciente) -> None: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Paciente]: ...

    @abstractmethod
    def buscar_por_cpf(self, cpf: CPF) -> Optional[Paciente]: ...

    @abstractmethod
    def listar(self) -> list[Paciente]: ...


class RepositorioMedico(ABC):
    @abstractmethod
    def salvar(self, medico: Medico) -> None: ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Medico]: ...

    @abstractmethod
    def listar(self) -> list[Medico]: ...
