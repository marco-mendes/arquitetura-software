"""
Camada de Negócios — Serviços de Agendamento
Contém as regras de negócio: conflito de agenda, validação de entidades,
relatórios. Depende apenas das interfaces de repositório (nunca das implementações).
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from dominio import (
    Consulta,
    Horario,
    RepositorioConsulta,
    RepositorioMedico,
    RepositorioPaciente,
)


# --- Exceções de domínio ---

class ConflitodeAgendaError(Exception):
    pass


class EntidadeNaoEncontradaError(Exception):
    pass


# --- DTO de entrada ---

@dataclass
class SolicitacaoAgendamento:
    paciente_id: int
    medico_id: int
    inicio: datetime
    fim: datetime


# --- Serviço de agendamento ---

class AgendamentoServico:
    """
    Gerencia o ciclo de vida das consultas.
    Invariante central: um médico não pode ter dois horários sobrepostos.
    """

    def __init__(
        self,
        repo_consulta: RepositorioConsulta,
        repo_paciente: RepositorioPaciente,
        repo_medico: RepositorioMedico,
    ):
        self._repo_consulta = repo_consulta
        self._repo_paciente = repo_paciente
        self._repo_medico = repo_medico
        self._proximo_id = 1

    def agendar(self, solicitacao: SolicitacaoAgendamento) -> Consulta:
        paciente = self._repo_paciente.buscar_por_id(solicitacao.paciente_id)
        if not paciente:
            raise EntidadeNaoEncontradaError(
                f"Paciente {solicitacao.paciente_id} não encontrado."
            )

        medico = self._repo_medico.buscar_por_id(solicitacao.medico_id)
        if not medico:
            raise EntidadeNaoEncontradaError(
                f"Médico {solicitacao.medico_id} não encontrado."
            )

        horario = Horario(inicio=solicitacao.inicio, fim=solicitacao.fim)

        # Verifica conflito de agenda — invariante de negócio
        consultas_existentes = self._repo_consulta.listar_por_medico(
            solicitacao.medico_id, solicitacao.inicio
        )
        for existente in consultas_existentes:
            if horario.conflita_com(existente.horario):
                raise ConflitodeAgendaError(
                    f"Dr(a). {medico.nome} já tem consulta das "
                    f"{existente.horario.inicio.strftime('%H:%M')} às "
                    f"{existente.horario.fim.strftime('%H:%M')}."
                )

        consulta = Consulta(
            id=self._proximo_id,
            medico=medico,
            paciente=paciente,
            horario=horario,
        )
        self._proximo_id += 1
        self._repo_consulta.salvar(consulta)
        return consulta

    def cancelar(self, consulta_id: int) -> Consulta:
        consulta = self._repo_consulta.buscar_por_id(consulta_id)
        if not consulta:
            raise EntidadeNaoEncontradaError(f"Consulta {consulta_id} não encontrada.")
        consulta.cancelar()
        self._repo_consulta.salvar(consulta)
        return consulta

    def realizar(self, consulta_id: int, observacoes: str = "") -> Consulta:
        consulta = self._repo_consulta.buscar_por_id(consulta_id)
        if not consulta:
            raise EntidadeNaoEncontradaError(f"Consulta {consulta_id} não encontrada.")
        consulta.realizar(observacoes)
        self._repo_consulta.salvar(consulta)
        return consulta


# --- Serviço de relatórios ---

class RelatorioServico:
    def __init__(self, repo_consulta: RepositorioConsulta):
        self._repo_consulta = repo_consulta

    def agenda_diaria(self, medico_id: int, data: datetime) -> list[Consulta]:
        consultas = self._repo_consulta.listar_por_medico(medico_id, data)
        return sorted(consultas, key=lambda c: c.horario.inicio)

    def historico_paciente(self, paciente_id: int) -> list[Consulta]:
        return sorted(
            self._repo_consulta.listar_por_paciente(paciente_id),
            key=lambda c: c.horario.inicio,
        )
