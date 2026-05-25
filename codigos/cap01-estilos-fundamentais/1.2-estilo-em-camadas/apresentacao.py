"""
Camada de Apresentação — Controllers HTTP (simulados)
Traduz requisições HTTP em chamadas à camada de negócios e formata as respostas.
Não contém regras de negócio — apenas coordenação e serialização.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from servicos import (
    AgendamentoServico,
    ConflitodeAgendaError,
    EntidadeNaoEncontradaError,
    RelatorioServico,
    SolicitacaoAgendamento,
)


@dataclass
class Resposta:
    status: int
    corpo: Any

    def __str__(self) -> str:
        rotulos = {200: "OK", 201: "CREATED", 400: "BAD REQUEST",
                   404: "NOT FOUND", 409: "CONFLICT"}
        rotulo = rotulos.get(self.status, "UNKNOWN")
        return f"HTTP {self.status} {rotulo} → {self.corpo}"


class AgendaController:
    """Simula os handlers de uma API REST de agendamento."""

    def __init__(self, agendamento: AgendamentoServico, relatorio: RelatorioServico):
        self._agendamento = agendamento
        self._relatorio = relatorio

    def post_consulta(self, corpo: dict) -> Resposta:
        """POST /consultas"""
        try:
            solicitacao = SolicitacaoAgendamento(
                paciente_id=corpo["paciente_id"],
                medico_id=corpo["medico_id"],
                inicio=datetime.fromisoformat(corpo["inicio"]),
                fim=datetime.fromisoformat(corpo["fim"]),
            )
            c = self._agendamento.agendar(solicitacao)
            return Resposta(201, {
                "id": c.id,
                "medico": c.medico.nome,
                "paciente": c.paciente.nome,
                "horario": str(c.horario),
                "status": c.status,
            })
        except ConflitodeAgendaError as e:
            return Resposta(409, {"erro": str(e)})
        except (EntidadeNaoEncontradaError, KeyError, ValueError) as e:
            return Resposta(400, {"erro": str(e)})

    def delete_consulta(self, consulta_id: int) -> Resposta:
        """DELETE /consultas/{id}"""
        try:
            c = self._agendamento.cancelar(consulta_id)
            return Resposta(200, {"id": c.id, "status": c.status})
        except EntidadeNaoEncontradaError as e:
            return Resposta(404, {"erro": str(e)})
        except ValueError as e:
            return Resposta(400, {"erro": str(e)})

    def patch_consulta_realizar(self, consulta_id: int, observacoes: str = "") -> Resposta:
        """PATCH /consultas/{id}/realizar"""
        try:
            c = self._agendamento.realizar(consulta_id, observacoes)
            return Resposta(200, {"id": c.id, "status": c.status, "observacoes": c.observacoes})
        except (EntidadeNaoEncontradaError, ValueError) as e:
            return Resposta(400, {"erro": str(e)})

    def get_agenda(self, medico_id: int, data: str) -> Resposta:
        """GET /agenda?medico_id=X&data=YYYY-MM-DD"""
        try:
            data_dt = datetime.fromisoformat(data)
            consultas = self._relatorio.agenda_diaria(medico_id, data_dt)
            return Resposta(200, [
                {
                    "id": c.id,
                    "paciente": c.paciente.nome,
                    "horario": str(c.horario),
                    "status": c.status,
                }
                for c in consultas
            ])
        except ValueError as e:
            return Resposta(400, {"erro": str(e)})

    def get_historico_paciente(self, paciente_id: int) -> Resposta:
        """GET /pacientes/{id}/historico"""
        consultas = self._relatorio.historico_paciente(paciente_id)
        return Resposta(200, [
            {
                "id": c.id,
                "medico": c.medico.nome,
                "horario": str(c.horario),
                "status": c.status,
            }
            for c in consultas
        ])
