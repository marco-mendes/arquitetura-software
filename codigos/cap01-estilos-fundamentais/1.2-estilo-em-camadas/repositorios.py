"""
Camada de Dados — Implementações em Memória
Implementa as interfaces de RepositorioConsulta, RepositorioPaciente e RepositorioMedico
usando dicionários em memória. Em produção, seria substituído por implementações
que acessam PostgreSQL, MongoDB, etc. — sem alterar a camada de negócios (OCP).
"""

from datetime import datetime
from typing import Optional

from dominio import (
    Consulta,
    CPF,
    Medico,
    Paciente,
    RepositorioConsulta,
    RepositorioMedico,
    RepositorioPaciente,
)


class InMemoriaRepositorioConsulta(RepositorioConsulta):
    def __init__(self):
        self._consultas: dict[int, Consulta] = {}

    def salvar(self, consulta: Consulta) -> None:
        self._consultas[consulta.id] = consulta

    def buscar_por_id(self, id: int) -> Optional[Consulta]:
        return self._consultas.get(id)

    def listar_por_medico(self, medico_id: int, data: datetime) -> list[Consulta]:
        return [
            c for c in self._consultas.values()
            if c.medico.id == medico_id
            and c.horario.inicio.date() == data.date()
            and c.status == "agendada"
        ]

    def listar_por_paciente(self, paciente_id: int) -> list[Consulta]:
        return [
            c for c in self._consultas.values()
            if c.paciente.id == paciente_id
        ]


class InMemoriaRepositorioPaciente(RepositorioPaciente):
    def __init__(self):
        self._pacientes: dict[int, Paciente] = {}

    def salvar(self, paciente: Paciente) -> None:
        self._pacientes[paciente.id] = paciente

    def buscar_por_id(self, id: int) -> Optional[Paciente]:
        return self._pacientes.get(id)

    def buscar_por_cpf(self, cpf: CPF) -> Optional[Paciente]:
        return next(
            (p for p in self._pacientes.values() if p.cpf == cpf), None
        )

    def listar(self) -> list[Paciente]:
        return list(self._pacientes.values())


class InMemoriaRepositorioMedico(RepositorioMedico):
    def __init__(self):
        self._medicos: dict[int, Medico] = {}

    def salvar(self, medico: Medico) -> None:
        self._medicos[medico.id] = medico

    def buscar_por_id(self, id: int) -> Optional[Medico]:
        return self._medicos.get(id)

    def listar(self) -> list[Medico]:
        return list(self._medicos.values())
