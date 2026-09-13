"""Camada de repositório: guarda e recupera consultas.

Trocar a lista em memória por um banco de dados muda somente este arquivo.
"""

from dataclasses import dataclass, field

from dominio import Consulta, Horario


@dataclass
class RepositorioDeConsultas:
    _consultas: list[Consulta] = field(default_factory=list)
    _proximo_id: int = 1

    def salvar(self, medico: str, paciente: str, horario: Horario) -> Consulta:
        consulta = Consulta(self._proximo_id, medico, paciente, horario)
        self._consultas.append(consulta)
        self._proximo_id += 1
        return consulta

    def agendadas_do_medico(self, medico: str) -> list[Consulta]:
        return [
            c for c in self._consultas if c.medico == medico and c.status == "agendada"
        ]

    def por_id(self, consulta_id: int) -> Consulta | None:
        return next((c for c in self._consultas if c.id == consulta_id), None)

    def todas(self) -> list[Consulta]:
        return list(self._consultas)
