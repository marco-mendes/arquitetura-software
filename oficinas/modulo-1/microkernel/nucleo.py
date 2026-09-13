"""O núcleo: conhece categorias e ordem, e nada sobre impostos.

Não existe nenhuma menção a ICMS, ISS ou São Paulo neste arquivo. Quem sabe
calcular imposto paulista é o plugin, que se anuncia ao núcleo em tempo de
execução.
"""

from dominio import Fatura

ORDEM_CATEGORIAS = ("impostos", "frete", "notificacao")


class Plugin:
    """O contrato de extensão. Mudá-lo obriga todos os plugins a mudar."""

    nome: str = ""
    categoria: str = ""

    def aplica_se(self, fatura: Fatura) -> bool:
        return True

    def executar(self, fatura: Fatura) -> None:
        raise NotImplementedError


class Registro:
    def __init__(self) -> None:
        self._por_categoria: dict[str, list[Plugin]] = {}

    def registrar(self, plugin: Plugin) -> None:
        self._por_categoria.setdefault(plugin.categoria, []).append(plugin)
        print(f"  [Registry] Plugin '{plugin.nome}' registrado em '{plugin.categoria}'")

    def ativos(self) -> dict[str, list[str]]:
        return {
            categoria: [p.nome for p in plugins]
            for categoria, plugins in self._por_categoria.items()
        }

    def da_categoria(self, categoria: str) -> list[Plugin]:
        return self._por_categoria.get(categoria, [])


class Nucleo:
    def __init__(self, registro: Registro) -> None:
        self._registro = registro

    def processar(self, fatura: Fatura) -> None:
        for categoria in ORDEM_CATEGORIAS:
            for plugin in self._registro.da_categoria(categoria):
                if plugin.aplica_se(fatura):
                    plugin.executar(fatura)
