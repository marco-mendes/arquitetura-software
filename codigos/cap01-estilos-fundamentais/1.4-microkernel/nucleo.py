"""
Núcleo — CoreFaturamento e PluginRegistry
O núcleo não conhece as implementações dos plugins — apenas o contrato (Protocol).
"""

from __future__ import annotations
from typing import Protocol, runtime_checkable

from dominio import Fatura, ResultadoEmissao


@runtime_checkable
class PluginFaturamento(Protocol):
    """
    Contrato que todo plugin deve respeitar.
    Estável por design: mudanças aqui quebram todos os plugins existentes.
    """

    @property
    def nome(self) -> str: ...

    def processar(self, fatura: Fatura, resultado: ResultadoEmissao) -> ResultadoEmissao: ...


class PluginRegistry:
    """
    Registro de plugins por categoria.
    Permite descoberta e carregamento dinâmico de plugins sem alterar o núcleo.
    """

    def __init__(self):
        self._plugins: dict[str, list] = {}

    def registrar(self, categoria: str, plugin: PluginFaturamento) -> None:
        if not isinstance(plugin, PluginFaturamento):
            raise TypeError(
                f"'{type(plugin).__name__}' não implementa o contrato PluginFaturamento."
            )
        self._plugins.setdefault(categoria, []).append(plugin)
        print(f"  [Registry] Plugin '{plugin.nome}' registrado em '{categoria}'")

    def obter(self, categoria: str) -> list:
        return self._plugins.get(categoria, [])

    def status(self) -> dict[str, list[str]]:
        return {cat: [p.nome for p in plugins]
                for cat, plugins in self._plugins.items()}


class CoreFaturamento:
    """
    Núcleo do sistema de faturamento.
    Não contém lógica fiscal, de frete ou notificação — isso é responsabilidade
    dos plugins. O núcleo apenas orquestra a execução.
    """

    # Ordem de execução garante consistência (impostos antes de frete, etc.)
    ORDEM_CATEGORIAS = ["impostos", "frete", "notificacao"]

    def __init__(self):
        self._registry = PluginRegistry()

    def registrar_plugin(self, categoria: str, plugin: PluginFaturamento) -> None:
        self._registry.registrar(categoria, plugin)

    def emitir(self, fatura: Fatura) -> ResultadoEmissao:
        resultado = ResultadoEmissao(
            fatura_id=fatura.id,
            valor_bruto=fatura.valor_bruto,
        )
        for categoria in self.ORDEM_CATEGORIAS:
            for plugin in self._registry.obter(categoria):
                resultado = plugin.processar(fatura, resultado)
        return resultado

    def status_plugins(self) -> dict[str, list[str]]:
        return self._registry.status()
