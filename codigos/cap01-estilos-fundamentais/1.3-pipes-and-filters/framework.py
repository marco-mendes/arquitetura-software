"""
Framework de Pipeline — Pipes and Filters
Contém a abstração Filtro e a classe Pipeline que encadeia filtros.
Sem dependências externas — apenas abc e typing.
"""

from abc import ABC, abstractmethod
from typing import Any


class Filtro(ABC):
    """
    Contrato base para todos os filtros.
    Cada filtro recebe dados, transforma e devolve — sem estado compartilhado.
    """

    @abstractmethod
    def processar(self, dados: Any) -> Any: ...

    @property
    def nome(self) -> str:
        return self.__class__.__name__


class Pipeline:
    """
    Encadeia filtros e executa a transformação em sequência.
    Cada filtro recebe o output do anterior como input.
    """

    def __init__(self):
        self._filtros: list[Filtro] = []

    def adicionar(self, filtro: Filtro) -> "Pipeline":
        self._filtros.append(filtro)
        return self

    def executar(self, dados: Any) -> Any:
        resultado = dados
        for filtro in self._filtros:
            resultado = filtro.processar(resultado)
        return resultado

    def __repr__(self) -> str:
        nomes = " → ".join(f.nome for f in self._filtros)
        return f"Pipeline({nomes})"
