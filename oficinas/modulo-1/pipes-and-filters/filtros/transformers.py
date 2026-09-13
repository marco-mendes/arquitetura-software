"""Transformadores: mudam o item e o devolvem ao fluxo, sem descartar."""

from dominio import Curriculo, Vaga
from framework import Filtro


class NormalizadorDeCampos(Filtro):
    def processar(self, item: Curriculo) -> Curriculo | None:
        item.nome = item.nome.strip().title()
        item.habilidades = [h.strip().lower() for h in item.habilidades]
        return item


class CalculadorDeScore(Filtro):
    def __init__(self, vaga: Vaga) -> None:
        self._esperadas = [h.lower() for h in vaga.habilidades]

    def processar(self, item: Curriculo) -> Curriculo | None:
        item.compativeis = [h for h in item.habilidades if h in self._esperadas]
        item.score = round(100 * len(item.compativeis) / len(self._esperadas))
        return item
