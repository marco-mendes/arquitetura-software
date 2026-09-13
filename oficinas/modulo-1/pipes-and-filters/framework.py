"""O orquestrador do fluxo.

Ele não conhece nenhum critério de triagem. Sabe apenas que cada filtro
recebe um item, devolve um item ou devolve None para tirá-lo do fluxo.
"""

from dominio import Curriculo


class Filtro:
    """Contrato único que todos os filtros cumprem."""

    def processar(self, item: Curriculo) -> Curriculo | None:
        raise NotImplementedError


class Pipeline:
    def __init__(self) -> None:
        self._filtros: list[Filtro] = []

    def adicionar(self, filtro: Filtro) -> "Pipeline":
        self._filtros.append(filtro)
        return self

    def executar(self, itens: list[Curriculo]) -> list[Curriculo]:
        """Cada filtro processa a corrente inteira antes de passá-la adiante."""
        corrente = list(itens)
        for filtro in self._filtros:
            corrente = [
                saida
                for saida in (filtro.processar(item) for item in corrente)
                if saida is not None
            ]
        return corrente

    def __str__(self) -> str:
        nomes = " → ".join(type(f).__name__ for f in self._filtros)
        return f"Pipeline({nomes})"
