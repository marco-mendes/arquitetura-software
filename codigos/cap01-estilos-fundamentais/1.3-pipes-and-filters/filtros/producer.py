"""Producer — ponto de entrada do pipeline."""

from typing import Any
from framework import Filtro
from dominio import Curriculo


class LeitorDeCurriculos(Filtro):
    """
    Producer: recebe dicionários brutos e converte em objetos Curriculo.
    Ponto de entrada do pipeline — ignora o dado de entrada.
    """

    def __init__(self, dados_brutos: list[dict]):
        self._dados = dados_brutos

    def processar(self, _: Any) -> list[Curriculo]:
        return [Curriculo(**d) for d in self._dados]
