"""Camada de apresentação: traduz chamadas e erros em códigos HTTP.

Ela não decide nenhuma regra. O 409 nasce aqui, mas o motivo dele nasce no
domínio, e é essa separação que o estilo em camadas existe para manter.
"""

from dominio import ConflitoDeAgenda, Consulta
from servicos import ServicoDeAgenda


class ApresentacaoHTTP:
    def __init__(self, servico: ServicoDeAgenda) -> None:
        self._servico = servico

    def post_consultas(self, medico: str, paciente: str, inicio: str, fim: str) -> None:
        try:
            consulta = self._servico.agendar(medico, paciente, inicio, fim)
        except ConflitoDeAgenda as erro:
            print(f"HTTP 409 CONFLICT → {{'erro': '{erro}'}}")
            return
        print(f"HTTP 201 CREATED → {self._como_dicionario(consulta)}")

    def post_realizacao(self, consulta_id: int) -> None:
        self._responder(self._servico.realizar(consulta_id), consulta_id)

    def delete_consulta(self, consulta_id: int) -> None:
        self._responder(self._servico.cancelar(consulta_id), consulta_id)

    def get_agenda(self) -> None:
        for consulta in self._servico.agenda():
            print(f"  {self._como_dicionario(consulta)}")

    def _responder(self, consulta: Consulta | None, consulta_id: int) -> None:
        if consulta is None:
            print(f"HTTP 404 NOT FOUND → {{'erro': 'consulta {consulta_id} inexistente'}}")
            return
        print(f"HTTP 200 OK → {self._como_dicionario(consulta)}")

    @staticmethod
    def _como_dicionario(consulta: Consulta) -> dict:
        return {
            "id": consulta.id,
            "medico": consulta.medico,
            "paciente": consulta.paciente,
            "horario": str(consulta.horario),
            "status": consulta.status,
        }
