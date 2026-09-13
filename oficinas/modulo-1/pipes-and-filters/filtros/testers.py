"""Testadores: decidem se o item continua no fluxo.

Cada um sai do fluxo por um motivo diferente, e nenhum conhece o critério
do vizinho.
"""

from dominio import Curriculo, Vaga
from framework import Filtro


class ValidadorDeCurriculo(Filtro):
    """Descarta por dado ausente, antes de qualquer regra de negócio."""

    def processar(self, item: Curriculo) -> Curriculo | None:
        if not item.nome:
            print(f"  [DESCARTADO] Currículo id={item.id}: nome ausente")
            return None
        return item


class FiltroPorExperienciaMinima(Filtro):
    def __init__(self, vaga: Vaga) -> None:
        self._vaga = vaga

    def processar(self, item: Curriculo) -> Curriculo | None:
        if item.anos_experiencia < self._vaga.anos_minimos:
            print(
                f"  [REPROVADO] {item.nome}: {item.anos_experiencia} ano(s) "
                f"< mínimo {self._vaga.anos_minimos}"
            )
            return None
        return item


class FiltroPorPretensaoSalarial(Filtro):
    def __init__(self, vaga: Vaga) -> None:
        self._vaga = vaga

    def processar(self, item: Curriculo) -> Curriculo | None:
        if item.pretensao > self._vaga.teto_salarial:
            print(
                f"  [REPROVADO] {item.nome}: pretensão R${item.pretensao:,} "
                f"> máximo R${self._vaga.teto_salarial:,}"
            )
            return None
        return item
