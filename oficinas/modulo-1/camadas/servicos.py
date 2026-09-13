"""Camada de serviço: coordena o caso de uso.

Ela chama o domínio para decidir e o repositório para guardar. Não conhece
HTTP e não sabe se o armazenamento é memória, arquivo ou banco.
"""

from dominio import ConflitoDeAgenda, Consulta, Horario
from repositorios import RepositorioDeConsultas


class ServicoDeAgenda:
    def __init__(self, repositorio: RepositorioDeConsultas) -> None:
        self._repositorio = repositorio

    def agendar(self, medico: str, paciente: str, inicio: str, fim: str) -> Consulta:
        horario = Horario(inicio, fim)
        for ocupada in self._repositorio.agendadas_do_medico(medico):
            if ocupada.horario.conflita_com(horario):
                raise ConflitoDeAgenda(
                    f"Dr(a). {medico} já tem consulta das {ocupada.horario.inicio} "
                    f"às {ocupada.horario.fim}."
                )
        return self._repositorio.salvar(medico, paciente, horario)

    def realizar(self, consulta_id: int) -> Consulta | None:
        consulta = self._repositorio.por_id(consulta_id)
        if consulta:
            consulta.realizar()
        return consulta

    def cancelar(self, consulta_id: int) -> Consulta | None:
        consulta = self._repositorio.por_id(consulta_id)
        if consulta:
            consulta.cancelar()
        return consulta

    def agenda(self) -> list[Consulta]:
        return self._repositorio.todas()
